#!/usr/bin/env python3
"""Brief MD lint: mechanical check of a client brief (folder or .zip).

This script judges neither the quality nor the substance of the brief. It checks what a program
can check reliably: structure, manifest, labels, empty sections, secrets, personal data and
hidden instructions. Python standard library only.

Usage:
    python3 brief_lint.py PATH [--level express|standard|complete] [--json]

Exit codes: 0 nothing to report, 1 warnings, 2 errors.

Reports never reproduce a secret in clear text (values are masked).
"""
import argparse
import json
import re
import shutil
import sys
import tempfile
import unicodedata
import zipfile
from pathlib import Path

SPEC_PATH = Path(__file__).with_name("spec.json")
SEV_ORDER = {"error": 0, "warning": 1, "info": 2}
SEV_LABEL = {"error": "ERROR", "warning": "WARNING", "info": "INFO"}

TAG_RE = re.compile(r"\[(confirmed|memory|inferred|unknown)\]", re.I)
H2_RE = re.compile(r"^##\s+(.+?)\s*$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
ANNEX_RE = re.compile(r"^A\d+-.+\.md$", re.I)

HIDDEN_RE = re.compile("[​-‏‪-‮⁠-⁤⁦-⁩﻿]")
HTML_COMMENT_RE = re.compile(r"<!--.*?-->", re.S)

SECRET_PATTERNS = [
    ("private key", re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH |DSA |PGP )?PRIVATE KEY")),
    ("AWS key", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("GitHub token", re.compile(r"\bgh[pousr]_[A-Za-z0-9]{30,}\b")),
    ("sk- style API key", re.compile(r"\bsk-[A-Za-z0-9_\-]{20,}")),
    ("Slack token", re.compile(r"\bxox[baprs]-[A-Za-z0-9\-]{10,}")),
    ("Google key", re.compile(r"\bAIza[0-9A-Za-z_\-]{35}\b")),
    ("Stripe key", re.compile(r"\b[sr]k_(?:live|test)_[0-9a-zA-Z]{16,}\b")),
    ("JWT token", re.compile(r"\beyJ[A-Za-z0-9_\-]{10,}\.[A-Za-z0-9_\-]{10,}\.[A-Za-z0-9_\-]{10,}")),
    ("credentials in a URL", re.compile(r"\b[a-z][a-z0-9+.\-]*://[^/\s:@]+:[^/\s:@]+@")),
]
PASSWORD_RE = re.compile(
    r"\b(?:password|passwd|passcode|pwd|mot\s+de\s+passe|mdp)\b\s*(?:is\s+|est\s+|:\s*|=\s*|→\s*)+(\S+)", re.I)
PASSWORD_IGNORE = {
    "to", "a", "an", "the", "no", "none", "unknown", "shared", "sent", "provided", "given", "managed",
    "held", "separately", "yes", "n/a", "na", "-", "will", "be", "via", "by", "in", "through", "not",
    "available", "on", "with", "kept", "stored",
}
EMAIL_RE = re.compile(r"\b[\w.+\-]+@[\w\-]+(?:\.[\w\-]+)+\b")
FREEMAIL = {"gmail.com", "googlemail.com", "outlook.com", "hotmail.com", "hotmail.fr", "live.com", "live.fr",
            "yahoo.com", "yahoo.fr", "icloud.com", "me.com", "aol.com", "gmx.com", "gmx.de", "orange.fr",
            "free.fr", "wanadoo.fr", "laposte.net", "proton.me", "protonmail.com"}
PHONE_PATTERNS = [
    # International format with a leading plus sign, such as +44 20 7946 0958.
    re.compile(r"(?<![\w+])\+\d{1,3}(?:[\s.\-]?\(?\d{1,4}\)?){2,5}(?!\d)"),
    # North American format, such as (415) 555-0132 or 415-555-0132.
    re.compile(r"(?<!\d)\(?\d{3}\)?[\s.\-]\d{3}[\s.\-]\d{4}(?!\d)"),
    # French national format, such as 06 12 34 56 78.
    re.compile(r"(?<![\d+])0[1-9](?:[\s.\-]?\d{2}){4}(?!\d)"),
]
IBAN_RE = re.compile(r"\b[A-Z]{2}\d{2}(?:\s?[A-Z0-9]{4}){3,7}(?:\s?[A-Z0-9]{1,4})?\b")
CARD_RE = re.compile(r"(?<!\d)(?:\d[ \-]?){14,15}\d(?!\d)")
NATIONAL_ID_PATTERNS = [
    # French social security number (NIR).
    re.compile(
        r"(?<!\d)[12]\s?\d{2}\s?(?:0[1-9]|1[0-2]|[2-9]\d)\s?(?:\d{2}|2[AB])\s?\d{3}\s?\d{3}(?:\s?\d{2})?(?!\d)"),
    # US Social Security number.
    re.compile(r"(?<!\d)\d{3}-\d{2}-\d{4}(?!\d)"),
]

INJECTION_PATTERNS = [
    re.compile(r"\b(?:ignore|disregard|forget)\b.{0,40}\b(?:instructions?|rules|guidelines)\b", re.I),
    re.compile(r"\bignor(?:e|ez|er)\b.{0,40}\b(?:instructions?|consignes?)\b", re.I),
    re.compile(r"\b(?:system prompt|prompt syst[èe]me)\b", re.I),
    re.compile(r"\b(?:note|message|instructions?|consignes?)\s+(?:for|to|pour|à)\s+(?:the\s+|l')?(?:assistant|ai|ia|llm|model|mod[èe]le)\b", re.I),
    re.compile(r"\byou\s+(?:must|should)\s+(?:respond|answer|say|declare|conclude|state|rate)\b", re.I),
    re.compile(r"\b(?:tu|vous)\s+(?:dois|devez)\s+(?:r[ée]pondre|d[ée]clarer|affirmer|conclure|indiquer)\b", re.I),
]


def norm(s):
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = re.sub(r"\([^)]*\)", " ", s)
    s = re.sub(r"[^a-zA-Z0-9\s]", " ", s.lower())
    return re.sub(r"\s+", " ", s).strip()


def heading_matches(expected, actual):
    e, a = norm(expected), norm(actual)
    return bool(e) and bool(a) and (a.startswith(e) or e.startswith(a))


def load_spec():
    with open(SPEC_PATH, encoding="utf-8") as f:
        return json.load(f)


class Report:
    def __init__(self):
        self.findings = []

    def add(self, sev, code, file, msg, line=None):
        self.findings.append({"severity": sev, "code": code, "file": file,
                              "line": line, "message": msg})

    def count(self, sev):
        return sum(1 for f in self.findings if f["severity"] == sev)


def mask(value, keep=4):
    return f"{value[:keep]}… ({len(value)} chars)"


def iban_valid(raw):
    s = re.sub(r"\s", "", raw).upper()
    if not 15 <= len(s) <= 34:
        return False
    rearranged = s[4:] + s[:4]
    digits = "".join(str(int(c, 36)) for c in rearranged)
    return int(digits) % 97 == 1


def luhn_valid(digits):
    total, alt = 0, False
    for ch in reversed(digits):
        n = int(ch)
        if alt:
            n *= 2
            if n > 9:
                n -= 9
        total += n
        alt = not alt
    return total % 10 == 0


def line_of(text, pos):
    return text.count("\n", 0, pos) + 1


def scan_text(text, file, rep):
    for label, rx in SECRET_PATTERNS:
        for m in rx.finditer(text):
            rep.add("error", "SECRET", file,
                    f"Probable secret ({label}): {mask(m.group(0))}. Remove it before sending.",
                    line_of(text, m.start()))
    for m in PASSWORD_RE.finditer(text):
        token = m.group(1).strip(".,;:!?)\"'»").lower()
        if token and token not in PASSWORD_IGNORE and not token.startswith(("[", "(")):
            rep.add("error", "SECRET", file,
                    "Password apparently written in clear text (value masked). "
                    "Access is shared through a separate channel, never in a file.",
                    line_of(text, m.start()))
    for m in IBAN_RE.finditer(text):
        if iban_valid(m.group(0)):
            rep.add("error", "BANK_ACCOUNT", file,
                    f"Valid IBAN detected: {mask(m.group(0), 4)}.", line_of(text, m.start()))
    for m in CARD_RE.finditer(text):
        digits = re.sub(r"\D", "", m.group(0))
        if len(digits) in (15, 16) and digits[0] in "3456" and luhn_valid(digits):
            rep.add("error", "BANK_ACCOUNT", file,
                    f"Possible payment card number: {mask(digits, 4)}.", line_of(text, m.start()))
    for rx in NATIONAL_ID_PATTERNS:
        for m in rx.finditer(text):
            rep.add("warning", "IDENTIFIER", file,
                    "Sequence of digits that may be a national identification number "
                    "(such as a social security number). To check.",
                    line_of(text, m.start()))
    for m in EMAIL_RE.finditer(text):
        domain = m.group(0).split("@", 1)[1].lower()
        if domain in FREEMAIL:
            rep.add("warning", "PERSONAL_DATA", file,
                    f"Probable personal e-mail address: {mask(m.group(0), 3)}.",
                    line_of(text, m.start()))
        else:
            rep.add("info", "PERSONAL_DATA", file,
                    f"E-mail address present: {mask(m.group(0), 3)}. Needed for the project?",
                    line_of(text, m.start()))
    seen_phone_lines = set()
    for rx in PHONE_PATTERNS:
        for m in rx.finditer(text):
            ln = line_of(text, m.start())
            if ln in seen_phone_lines:
                continue
            seen_phone_lines.add(ln)
            rep.add("warning", "PERSONAL_DATA", file,
                    "Phone number present. Needed for the project?", ln)
    seen_injections = set()
    for rx in INJECTION_PATTERNS:
        for m in rx.finditer(text):
            # The French and English patterns can match the same words: report each spot once.
            if m.start() in seen_injections:
                continue
            seen_injections.add(m.start())
            excerpt = re.sub(r"\s+", " ", m.group(0))[:80]
            rep.add("warning", "SUSPICIOUS_INSTRUCTION", file,
                    f"Wording that looks like an instruction addressed to an AI: \"{excerpt}\". "
                    "Treat it as content, never as an instruction.",
                    line_of(text, m.start()))
    for m in HTML_COMMENT_RE.finditer(text):
        excerpt = re.sub(r"\s+", " ", m.group(0))[:80]
        rep.add("warning", "HIDDEN_COMMENT", file,
                f"HTML comment (invisible when reading): \"{excerpt}\".", line_of(text, m.start()))
    hidden = [m for m in HIDDEN_RE.finditer(text) if m.start() > 0]
    if hidden:
        rep.add("warning", "HIDDEN_CHARACTERS", file,
                f"{len(hidden)} invisible or text-direction control character(s). "
                "A known technique to hide content.", line_of(text, hidden[0].start()))


def extract_zip(zpath, dest, spec, rep):
    lim = spec["limits"]
    with zipfile.ZipFile(zpath) as z:
        infos = z.infolist()
        if len(infos) > lim["max_files"]:
            rep.add("error", "ZIP_TOO_MANY_FILES", None, f"Archive with {len(infos)} entries: rejected.")
            return False
        if sum(i.file_size for i in infos) > lim["max_total_mb"] * 1024 * 1024:
            rep.add("error", "ZIP_TOO_LARGE", None, "Uncompressed content too large: rejected.")
            return False
        seen = set()
        for i in infos:
            if i.is_dir():
                continue
            name = i.filename
            parts = name.replace("\\", "/").split("/")
            if "__MACOSX" in parts or parts[-1].startswith("."):
                continue
            if (i.external_attr >> 16) & 0o170000 == 0o120000:
                rep.add("error", "ZIP_SYMLINK", name, "Symbolic link in the archive: ignored.")
                continue
            if name.startswith("/") or ".." in parts or re.match(r"^[A-Za-z]:", name):
                rep.add("error", "ZIP_DANGEROUS_PATH", name, "Dangerous path in the archive: ignored.")
                continue
            base = parts[-1]
            if not (base.lower().endswith(".md") or base == "manifest.json"):
                rep.add("warning", "IGNORED_FILE", base,
                        "Unsupported file type (only .md files and manifest.json are read).")
                continue
            if base in seen:
                rep.add("error", "ZIP_DUPLICATE", base, "Two files have this name: ignored.")
                continue
            seen.add(base)
            with z.open(i) as src, open(Path(dest) / base, "wb") as out:
                shutil.copyfileobj(src, out)
    return True


def collect_dir(path):
    root = Path(path)
    items = [p for p in root.iterdir() if p.is_file()]
    if not any(p.suffix.lower() == ".md" for p in items):
        subs = [p for p in root.iterdir() if p.is_dir() and not p.name.startswith(".")]
        if len(subs) == 1:
            root = subs[0]
            items = [p for p in root.iterdir() if p.is_file()]
    return {p.name: p for p in items if p.suffix.lower() == ".md" or p.name == "manifest.json"}


def parse_frontmatter(text):
    if text.startswith("﻿"):
        text = text[1:]
    lines = text.split("\n")
    if not lines or lines[0].strip() != "---":
        return None, text
    for idx in range(1, len(lines)):
        if lines[idx].strip() == "---":
            fm = {}
            for ln in lines[1:idx]:
                if ":" in ln:
                    k, v = ln.split(":", 1)
                    fm[k.strip()] = v.strip()
            return fm, "\n".join(lines[idx + 1:])
    return None, text


def parse_sections(body):
    sections, current, buf = [], None, []
    for ln in body.split("\n"):
        m = H2_RE.match(ln)
        if m:
            if current is not None:
                sections.append((current, "\n".join(buf)))
            current, buf = m.group(1), []
        elif current is not None:
            buf.append(ln)
    if current is not None:
        sections.append((current, "\n".join(buf)))
    return sections


def clean_content(content):
    c = TAG_RE.sub(" ", content)
    c = re.sub(r"[\s\-\*\d\.\)\(:;,!?_`>#|]+", " ", c)
    return c.strip()


def is_empty(content):
    c = clean_content(content)
    return c == "" or norm(c) in {"unknown", "n a", "na", "none", "not provided", "not filled", "tbd"}


def tag_counts(text):
    counts = {"confirmed": 0, "memory": 0, "inferred": 0, "unknown": 0}
    for m in TAG_RE.finditer(text):
        key = m.group(1).lower()
        if key in counts:
            counts[key] += 1
    return counts


def check_manifest(files, spec, rep):
    if "manifest.json" not in files:
        rep.add("warning", "MANIFEST_MISSING", "manifest.json",
                "No manifest: the provenance of the brief is unknown (mode, tool, review). "
                "Standard level applied by default.")
        return None
    try:
        data = json.loads(files["manifest.json"].read_text(encoding="utf-8"))
    except (ValueError, UnicodeDecodeError) as exc:
        rep.add("error", "MANIFEST_INVALID", "manifest.json", f"Unreadable JSON: {exc}")
        return None
    if not isinstance(data, dict):
        rep.add("error", "MANIFEST_INVALID", "manifest.json", "The manifest must be a JSON object.")
        return None
    ms = spec["manifest"]
    for key in ms["required"]:
        if key not in data:
            rep.add("error", "MANIFEST_FIELD", "manifest.json", f"Required field missing: {key}.")
    for key in ("level", "mode", "llm_memory"):
        if key in data and data[key] not in ms[key]:
            rep.add("error", "MANIFEST_VALUE", "manifest.json",
                    f"Unexpected value for {key}: {str(data[key])[:40]!r}. Expected: {', '.join(ms[key])}.")
    if "date" in data and not DATE_RE.match(str(data["date"])):
        rep.add("warning", "MANIFEST_VALUE", "manifest.json", "date: expected format YYYY-MM-DD.")
    if not isinstance(data.get("files", {}), dict):
        rep.add("error", "MANIFEST_VALUE", "manifest.json", "files must be an object.")
        data["files"] = {}
    for name, meta in data.get("files", {}).items():
        if not isinstance(meta, dict):
            rep.add("error", "MANIFEST_VALUE", "manifest.json", f"files.{name} must be an object.")
            continue
        for key in ("client_review", "visibility"):
            if key in meta and meta[key] not in ms[key]:
                rep.add("error", "MANIFEST_VALUE", "manifest.json",
                        f"files.{name}.{key}: unexpected value. Expected: {', '.join(ms[key])}.")
    return data


def lint(path, level_arg=None, spec=None):
    spec = spec or load_spec()
    rep = Report()
    tmp = None
    p = Path(path)
    if not p.exists():
        rep.add("error", "PATH", str(path), "Path not found.")
        return build_result(spec, rep, None, None, "unknown", {}, {})
    if p.is_file() and p.suffix.lower() == ".zip":
        tmp = tempfile.mkdtemp(prefix="brief-md-")
        try:
            ok = extract_zip(p, tmp, spec, rep)
        except zipfile.BadZipFile:
            rep.add("error", "ZIP_INVALID", p.name, "Unreadable archive.")
            ok = False
        if not ok:
            shutil.rmtree(tmp, ignore_errors=True)
            return build_result(spec, rep, None, None, "unknown", {}, {})
        files = collect_dir(tmp)
    elif p.is_dir():
        files = collect_dir(p)
    else:
        rep.add("error", "PATH", p.name, "Provide a folder or a .zip archive.")
        return build_result(spec, rep, None, None, "unknown", {}, {})
    try:
        return analyse(files, spec, rep, level_arg)
    finally:
        if tmp:
            shutil.rmtree(tmp, ignore_errors=True)


def analyse(files, spec, rep, level_arg):
    manifest = check_manifest(files, spec, rep)
    levels = spec["levels"]
    if level_arg:
        level, source = level_arg, "option"
    elif manifest and manifest.get("level") in levels:
        level, source = manifest["level"], "manifest"
    else:
        # Without a manifest we cannot tell whether a missing file is intended, so the most demanding level applies.
        level, source = "standard", "default, no manifest"
    expected_files = levels[level]
    mf = (manifest or {}).get("files", {}) if isinstance((manifest or {}).get("files", {}), dict) else {}

    def visibility(stem):
        meta = mf.get(f"{stem}.md", {})
        return meta.get("visibility", "shared") if isinstance(meta, dict) else "shared"

    report_files = {}
    max_kb = spec["limits"]["max_file_kb"]
    for stem in spec["files"]:
        name = f"{stem}.md"
        present = name in files
        entry = {"expected": stem in expected_files, "present": present, "visibility": visibility(stem)}
        if not present:
            if stem in expected_files and entry["visibility"] != "in_person":
                firm = source in ("manifest", "option") and stem != "00-summary"
                rep.add("error" if firm else "warning", "FILE_MISSING", name,
                        "File expected for this level, missing." if firm else
                        "File missing (target level unknown without a manifest: confirm with the client "
                        "whether this is intended).")
            elif entry["visibility"] == "in_person":
                rep.add("info", "FILE_IN_PERSON", name, "Not sent: to discuss in person (declared visibility).")
            report_files[stem] = entry
            continue
        raw = files[name].read_bytes()
        if b"\x00" in raw[:4096]:
            rep.add("error", "BINARY_FILE", name, "Binary content: file ignored.")
            entry["present"] = False
            report_files[stem] = entry
            continue
        text = raw.decode("utf-8", errors="replace")
        entry["size_kb"] = round(len(raw) / 1024, 1)
        if len(raw) > max_kb * 1024:
            rep.add("warning", "LARGE_FILE", name, f"More than {max_kb} KB: very long for a brief.")
        fm, body = parse_frontmatter(text)
        if fm is None:
            rep.add("warning", "HEADER_MISSING", name, "YAML header missing or not closed.")
        else:
            for key in spec["required_frontmatter"]:
                if key not in fm:
                    rep.add("warning", "HEADER_FIELD", name, f"Header: field {key} missing.")
            if fm.get("file") and fm["file"] != stem:
                rep.add("warning", "HEADER_MISMATCH", name,
                        f"Header: file = {fm['file'][:40]!r}, expected {stem!r}.")
            if fm.get("date") and not DATE_RE.match(fm["date"]):
                rep.add("info", "HEADER_DATE", name, "Header: date expected in YYYY-MM-DD format.")
        sections = parse_sections(body)
        expected = spec["files"][stem]
        optional = set(spec["optional_sections"])
        found, empty, missing = [], [], []
        for exp in expected:
            match = next((c for h, c in sections if heading_matches(exp, h)), None)
            if match is None:
                if exp not in optional:
                    missing.append(exp)
            else:
                found.append(exp)
                if exp not in optional and is_empty(match):
                    empty.append(exp)
        for s in missing:
            rep.add("warning", "SECTION_MISSING", name, f"Expected section missing: \"{s}\".")
        for s in empty:
            rep.add("info", "SECTION_EMPTY", name, f"Section empty or reduced to [unknown]: \"{s}\".")
        q = next((c for h, c in sections if heading_matches("Questions to complete", h)), None)
        if q is not None:
            n_q = sum(1 for ln in q.split("\n") if re.match(r"^\s*(?:[-*]|\d+[.)])\s+\S", ln))
            if n_q > 3:
                rep.add("info", "TOO_MANY_QUESTIONS", name, f"{n_q} end-of-file questions (3 at most requested).")
        tags = tag_counts(body)
        if sum(tags.values()) == 0 and stem != "00-summary":
            rep.add("warning", "TAGS_MISSING", name,
                    "No [confirmed] / [memory] / [inferred] / [unknown] label: "
                    "treat the information as unverified.")
        entry.update({"expected_sections": len([e for e in expected if e not in optional]),
                      "found_sections": len([e for e in found if e not in optional]),
                      "empty_sections": empty, "missing_sections": missing, "tags": tags})
        scan_text(text, name, rep)
        report_files[stem] = entry

    for name in files:
        stem = name[:-3] if name.endswith(".md") else name
        if name == "manifest.json" or stem in spec["files"]:
            continue
        if ANNEX_RE.match(name) and level == "complete":
            scan_text(files[name].read_text(encoding="utf-8", errors="replace"), name, rep)
            continue
        rep.add("warning", "UNEXPECTED_FILE", name, "Unrecognized name: file not analysed.")
    for name in mf:
        meta = mf[name] if isinstance(mf[name], dict) else {}
        if name not in files and meta.get("visibility", "shared") != "in_person" \
                and name[:-3] in spec["files"] and name[:-3] not in expected_files:
            rep.add("info", "MANIFEST_FILE_MISSING", name, "Listed in the manifest but missing from the folder.")

    blocking = {}
    for bf in spec["blocking_fields"]:
        stem = bf["file"]
        entry = report_files.get(stem, {})
        if not entry.get("present"):
            blocking[bf["name"]] = "in person" if entry.get("visibility") == "in_person" else "file missing"
            continue
        text = files[f"{stem}.md"].read_text(encoding="utf-8", errors="replace")
        _, body = parse_frontmatter(text)
        content = next((c for h, c in parse_sections(body) if heading_matches(bf["section"], h)), None)
        if content is None:
            blocking[bf["name"]] = "section missing"
        elif is_empty(content):
            blocking[bf["name"]] = "empty"
        else:
            t = tag_counts(content)
            weak = t["confirmed"] == 0 and (t["inferred"] + t["memory"] > 0 or sum(t.values()) == 0)
            blocking[bf["name"]] = "filled, not confirmed" if weak else "filled"

    provenance = {k: (manifest or {}).get(k) for k in ("mode", "llm", "llm_memory", "date", "status")} if manifest else None
    return build_result(spec, rep, manifest is not None, provenance, level, report_files, blocking, source)


def build_result(spec, rep, manifest_present, provenance, level, files, blocking, source="unknown"):
    findings = sorted(rep.findings, key=lambda f: (SEV_ORDER[f["severity"]], f["file"] or ""))
    return {
        "spec_version": spec["version"], "level": level, "level_source": source,
        "manifest": {"present": bool(manifest_present), "provenance": provenance},
        "files": files, "blocking_fields": blocking, "findings": findings,
        "summary": {"errors": rep.count("error"), "warnings": rep.count("warning"), "infos": rep.count("info")},
    }


def render_text(res):
    out = [f"Brief MD lint (spec {res['spec_version']})",
           f"Level: {res['level']} (source: {res['level_source']})"]
    prov = res["manifest"]["provenance"]
    if prov:
        out.append("Provenance: " + ", ".join(f"{k}={v}" for k, v in prov.items() if v))
    expected = [k for k, v in res["files"].items() if v.get("expected")]
    present = [k for k in expected if res["files"][k].get("present")]
    out.append(f"Expected files present: {len(present)}/{len(expected)}")
    out.append("")
    for f in res["findings"]:
        where = f["file"] or "-"
        ln = f":{f['line']}" if f.get("line") else ""
        out.append(f"[{SEV_LABEL[f['severity']]}] {where}{ln}: {f['message']}")
    if res["blocking_fields"]:
        out.append("")
        out.append("Blocking fields:")
        for k, v in res["blocking_fields"].items():
            out.append(f"  - {k}: {v}")
    r = res["summary"]
    out.append("")
    out.append(f"Summary: {r['errors']} error(s), {r['warnings']} warning(s), {r['infos']} info(s).")
    return "\n".join(out)


def main(argv=None):
    ap = argparse.ArgumentParser(description="Mechanical check of a Brief MD brief.")
    ap.add_argument("path", help="Folder or .zip archive")
    ap.add_argument("--level", choices=["express", "standard", "complete"])
    ap.add_argument("--json", action="store_true", help="JSON output")
    args = ap.parse_args(argv)
    res = lint(args.path, args.level)
    print(json.dumps(res, ensure_ascii=False, indent=2) if args.json else render_text(res))
    r = res["summary"]
    return 2 if r["errors"] else 1 if r["warnings"] else 0


if __name__ == "__main__":
    sys.exit(main())
