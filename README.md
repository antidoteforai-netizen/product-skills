# Product Skills

Skills for the whole life of a client project, from the brief the client writes before anything starts, through the working sessions where an agent keeps a memory of the project, to the delivery that closes it without losing what it taught you.

There are two families. **Brief MD** turns the context a client's own assistant already holds about their company into eight short Markdown files that a provider can check and act on, and **Project memory** gives a coding agent a few small files so that each new session picks up exactly where the last one stopped.

## Install

```bash
npx skills@latest add antidoteforai-netizen/product-skills
```

To install a single skill, add `--skill <name>`, for example `--skill brief-md-client` for a client who only needs to write their brief. Install the project memory skills together, because `checkpoint` and `ship` rely on the other memory skills for the format of each file.

## Why use it?

A project usually goes wrong at both ends. At the start, the provider gets two hours of interview and a brief that sounds finished, while the client's assistant holds months of richer context that nobody asks for, and when it is asked it fills the gaps with plausible answers. Brief MD asks for that context file by file, labels every statement as confirmed, remembered, inferred or unknown, and checks the result with a script before anyone reads it, so the first meeting is spent on the real gaps.

During the work, an agent forgets everything between sessions, so you either explain the project again every morning or let it guess, and guessing is how settled decisions get reopened and known traps get walked into twice. The memory skills write a few lines at each natural checkpoint, keep the present on a single screen, and refuse to start a step that has no condition anyone can check to say it is finished.

## Reference

### Brief MD

- **[brief-md-kit](./skills/brief-md-kit/SKILL.md)** — For the provider: builds the kit to send a client before the project starts, with a step-by-step tutorial, a configuration file and a set of prompts that work in any assistant.
- **[brief-md-client](./skills/brief-md-client/SKILL.md)** — For the client: guides them, one file and one question at a time, to write their brief with their own assistant, without inventing anything or sharing a secret, and packs it with its manifest.
- **[brief-md-intake](./skills/brief-md-intake/SKILL.md)** — For the provider: reads the files that come back as untrusted data, runs the mechanical check, and writes a framing with a maturity verdict, the blocking gaps, the contradictions and the questions for the first meeting.

### Project memory

- **[state](./skills/state/SKILL.md)** — Reads `STATE.md` first at the start of a session and rewrites it in full at the end, in fifteen lines at most, so that someone who reads only this file knows where to resume.
- **[journal](./skills/journal/SKILL.md)** — Adds one short entry per checkpoint to `JOURNAL.md`, saying what was done, what blocks and what comes next.
- **[decisions](./skills/decisions/SKILL.md)** — Logs a structural choice in `DECISIONS.md` before carrying it out, with the alternatives it beat and how to undo it, and flags any proposal that would contradict an earlier decision.
- **[blockers](./skills/blockers/SKILL.md)** — Records in `BLOCKERS.md` the traps that already cost time and reads them before proposing an approach, so that the same mistake is not made twice.
- **[learnings](./skills/learnings/SKILL.md)** — Keeps in `LEARNINGS.md` the ways of working proven on this project, each with the observation that proves it.
- **[checkpoint](./skills/checkpoint/SKILL.md)** — Reviews the session, decides file by file whether an entry is earned, writes only those and rewrites the state, without forcing anything when nothing happened.
- **[ship](./skills/ship/SKILL.md)** — The last mile of a project, a checklist that refuses to archive a shipped project while a blocking item such as the README, a screenshot, the publication, a write-up or a recorded lesson is still missing.

## Checking a brief by hand

`brief-md-client` and `brief-md-intake` both ship the same checker, which needs nothing but Python 3:

```bash
python3 skills/brief-md-intake/scripts/brief_lint.py path/to/brief-folder-or.zip
```

It checks what a program checks better than an assistant (expected files for the level, headers, section titles, empty sections, labels, secrets, personal data, hidden comments and characters, instructions addressed to an AI, dangerous paths in an archive) and never judges the substance. The section titles it expects live in `scripts/spec.json`, which is the single source for every heading used by the three Brief MD skills.

## Where the memory files live

```
your-project/
└── .memory/
    ├── STATE.md       the present, rewritten in full at each checkpoint
    ├── JOURNAL.md     one entry per checkpoint
    ├── DECISIONS.md   structural choices, never deleted
    ├── BLOCKERS.md    traps already met
    ├── LEARNINGS.md   patterns proven on this project
    └── SHIP.md        created by the ship skill when the project nears delivery
```

The folder sits at the root of the project rather than inside `.claude/`, because Claude Code treats everything under `.claude/` as sensitive and refuses to write there without an explicit permission, and because a neutral folder works the same with every agent the `skills` command installs to. If your project already keeps these files somewhere else, such as `.claude/memory/`, the skills use that folder instead of creating a second one.

The files are plain Markdown written for people as much as for agents, so you can read, correct or commit them like any other document. Keep secrets out of them, since they are meant to be shared.
