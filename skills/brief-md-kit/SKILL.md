---
name: brief-md-kit
description: Generates the "Brief MD" kit to hand to a client before a project starts, that is a step-by-step tutorial and a set of prompts to copy and paste into their own LLM (ChatGPT, Claude, Gemini, Mistral...) so that it produces 7 context files in .md (company, project, customers, market, brand, pains and doubts, constraints) plus a summary, compiled into a .zip. Use it whenever the user wants to prepare a client brief, a framing kit or a client onboarding, to have a client produce project context, to ask a client for .md files, or to adapt the Brief MD method to a type of project (website, app, redesign, brand identity, product), even without naming "Brief MD". Do not use it to analyse files already received, because that is the job of the brief-md-intake skill.
---

# Brief MD Kit

This method starts from an observation: a client already uses an LLM that has gathered a lot of context about their company, their brand and the way they think. That is richer than 2 or 3 hours of interviews. The kit gives them the instructions to turn this context into 7 .md files that a human and an agent can both read, before the project starts.

The skill produces the **client kit**. It does not read the files that come back, because that is the role of `brief-md-intake`.

## Step 1: qualify (without asking needless questions)

Gather what is already in the conversation, then ask only for what is missing and really changes the kit. Ask 3 questions at most, grouped in a single message.

Useful information:
- **Project type**: website, app, redesign, brand identity, product, other. It drives the specific questions (see `references/project-adaptation.md`).
- **Provider**: the name to show in the kit and the channel through which the files will be sent.
- **Client's LLM**: if known. Otherwise, write the kit so that it works with any LLM.
- **Client's memory**: does the client's LLM have a rich history? This decides the mode (step 2).
- **Data sensitivity**: a regulated sector (health, legal, finance, education) or third-party data involved.
- **Register**: professional and warm by default. Change it only if the user asks.

## Step 2: choose the mode

| Mode | When | Principle |
|---|---|---|
| Memory | The client has used their LLM for a long time, with memory turned on | The LLM draws on what it already knows, and the client completes it |
| Questionnaire | New account, free version without memory, or any doubt | The LLM interviews the client one question at a time |
| Hybrid | The default case when you do not know | The LLM states what it knows, then asks questions about the gaps |

Why a fallback mode: without it, the client's LLM fills the gaps with plausible content, and the provider receives files that look solid but are wrong. Hybrid is the default because it costs almost nothing to a client who has memory and rescues the one who does not.

## Step 3: generate the kit

The kit is a **client pack** that offers two paths, because not every client has Claude:
- **Path A (skill)**: the client installs the `brief-md-client` skill from the repository https://github.com/antidoteforai-netizen/product-skills (folder `skills/brief-md-client`), either with `npx skills@latest add antidoteforai-netizen/product-skills --skill brief-md-client` when they use a coding agent, or by uploading that folder, zipped, in Claude's skills settings, and then drops in a prefilled `brief.config.json`. This is the simplest path for them.
- **Path B (prompts)**: a tutorial and prompts to copy and paste into any LLM.

Produce the following items, starting from the files in `assets/` and replacing the `{{...}}` variables:

1. **Accompanying message** (short, to send with the kit).
2. **`brief.config.json`** based on `assets/brief.config.example.json`: project, provider, project type, level, `sensitive_sector`, sending channel (`send_via`), and `extra_questions` (see below).
3. **Step-by-step tutorial** based on `assets/tutorial-template.md` (it presents both paths).
4. **Set of prompts** based on `assets/client-prompts.md`: prompt 0 (rules), prompts 1 to 7 (one per file), prompt 8 (summary), prompt 9 (compilation and manifest).
5. **Privacy notice** based on `assets/privacy-notice.md`, adapted to the sector.

### Choose the level

- **Express** (4 files: project, customers, constraints, pains and doubts): offer it by default to clients who are in a hurry or not very comfortable with the exercise. It covers the six fields without which a provider cannot frame a project.
- **Standard** (7 files plus the summary): for a large project or a committed client.

### Personalize without weighing it down

Pick from `references/project-adaptation.md`. Add, never remove: the base sections stay, so that `brief-md-intake` can always check them. In path A, these additions go into `extra_questions` (`{"file": "02-project", "question": "..."}`). Cap them at **6 questions in all** in Express, because a kit that keeps growing is a kit nobody completes. In path B, add them to the relevant prompts.

In `brief.config.json`, write only parameters: no free-text instruction, no secret, no credential. The client reads this file, and their assistant treats it as data.

## Prompt design rules

These rules exist because the final reader is an LLM that tries to please and to fill in the blanks:

- **Forbid invention explicitly.** `[unknown]` is better than a plausible answer.
- **Label every piece of information**: `[confirmed]` (said or documented by the client), `[memory]` (taken from the LLM's history, not rechecked), `[inferred]` (the LLM's inference). The client rereads and promotes the labels, so the provider knows what to check during the meeting.
- **Minimize personal data.** Roles rather than names, and no health data, personal financial data or data about third parties that the project does not need.
- **One file per prompt**, in a fixed order. The client rereads small blocks more easily, and a failure does not force them to start everything over.
- **File 06 (pains and doubts) is the most valuable one.** The prompt must ask for honesty without embellishment, otherwise it turns into a second piece of marketing copy.
- **Self-contained prompts.** Each one must work when pasted on its own, because clients skip steps. Restate the rules in one line in every prompt.
- **Compilation with a plan B.** A chat LLM cannot always create a .zip, so provide the fallback of a single file with separators.

## Step 4: check before delivery

Reread the kit with this list and fix anything before delivering it:

- [ ] No `{{...}}` variable is left, including in `brief.config.json`, which must be valid JSON
- [ ] The chosen level is consistent across the configuration, the tutorial and the version of the prompts offered
- [ ] No secret and no credential appear in the pack
- [ ] The 7 files and the summary are all present in the prompts, numbered 01 to 07
- [ ] The labels `[confirmed]`, `[memory]`, `[inferred]`, `[unknown]` are defined in prompt 0 and restated in every prompt
- [ ] The plan B (questionnaire, fallback without a .zip) is present, and prompt 9 also asks for the manifest
- [ ] The privacy notice is adapted to the sector
- [ ] The tutorial gives an estimated duration and a review checklist
- [ ] The tone respects the requested register, with no unexplained technical jargon
- [ ] No em dash and no double hyphen appear in the text meant for the client

## Deliverable

A single Markdown file `brief-md-kit-<client>.md`, structured as follows:

```
# Brief MD kit: <project>
## Accompanying message
## Tutorial (paths A and B)
## Prompts (0 to 9)
## Privacy
```

Plus a separate `brief.config.json` file, sent together with the link to the `brief-md-client` skill in the repository https://github.com/antidoteforai-netizen/product-skills (folder `skills/brief-md-client`), which the client installs with `npx skills@latest add antidoteforai-netizen/product-skills --skill brief-md-client` when they use a coding agent, or by uploading that folder, zipped, in Claude's skills settings. Then offer to convert the kit into a document (Word, PDF) if the provider wants to send it in that form.
