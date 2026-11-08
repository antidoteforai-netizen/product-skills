# Client prompts (template)

Variables to replace: `{{PROVIDER}}`, `{{PROJECT_TYPE}}`, `{{PROJECT_NAME}}`, `{{DATE}}`.
The prompts are written in a neutral imperative so that they work whatever the client's LLM is.

---

## Prompt 0: the ground rules (paste it first)

```
I am preparing a project ({{PROJECT_TYPE}}) with {{PROVIDER}}. I am going to ask you to produce, one by one, 7 Markdown files that describe my context, and then a summary.

These rules apply to everything that follows:

1. SOURCES. Use what you already know about me (memory, past conversations) and what I tell you here. Use nothing else.
2. NO INVENTION. If a piece of information is missing or if you are unsure, write [unknown]. Never guess just to make it look good.
3. LABELS. End every important piece of information with a label:
   - [confirmed]: I said it explicitly here or it is documented
   - [memory]: taken from your memory of our conversations, not rechecked
   - [inferred]: your own inference, not something I said
4. PERSONAL DATA. No names of people (use roles: "the managing director", "the technical lead"), no health data, no personal financial data, and no data about third parties that is not essential to the project.
5. FORMAT. Markdown, a YAML header, level 2 headings, short lists, simple sentences.
6. HONESTY. Do not flatter. If something is weak, vague or contradictory, say so.
7. END OF EACH FILE. Add a "Questions to complete" section with 3 questions at most.

Reply only "Understood" and wait for my next message.
```

## Prompt 0b: choosing the mode (paste it right after)

**Memory** mode (the LLM has a long history with the client):

```
For each file, start by writing what you already know. Point out clearly what is missing, and I will complete it afterwards.
```

**Questionnaire** mode (new account, free version, no memory):

```
You have no history about me. Run an interview: one question at a time, in the order of the 7 files. Every 3 questions, restate in one sentence what you have understood so that I can confirm it. If I answer "I don't know", write [unknown] and move on. When the 7 blocks are done, produce the files one after the other.
```

**Hybrid** mode (default):

```
For each file, first state what you already know about me, labeled [memory]. Then ask me, one at a time, the questions that fill the gaps. Write the file only once the gaps have been dealt with or marked [unknown].
```

---

## Prompt 1: 01-company.md

```
Write the file 01-company.md. Reminder of the rules: no invention, labels [confirmed] [memory] [inferred] [unknown], roles rather than names.

YAML header:
---
file: 01-company
project: {{PROJECT_NAME}}
date: {{DATE}}
version: 1
client_review: no
---

Sections:
## Identity (name, legal form, year founded, size, location)
## Business in one sentence
## Offer (products or services, from most to least important)
## Business model (how the company makes money)
## Key figures (order of magnitude and year: revenue, headcount, growth, volume)
## Organization and decision-making (who decides what, by role)
## History and key moments
## Values: stated and actually lived (tell the two apart)
## Current tools and environment
## Questions to complete (3 at most)
```

## Prompt 2: 02-project.md

```
Write the file 02-project.md. Same rules as before.

YAML header: file: 02-project, project: {{PROJECT_NAME}}, date: {{DATE}}, version: 1, client_review: no

Sections:
## Goal in one sentence
## Why now (the trigger)
## Scope: included
## Scope: excluded
## Expected deliverables
## Success criteria (measurable if possible)
## Deadlines and milestones
## Budget (a range or a ceiling, otherwise [unknown])
## Final decision-maker and stakeholders (by role)
## History (previous attempts, what was done or abandoned)
## Dependencies (what the project depends on)
## Questions to complete (3 at most)
```

## Prompt 3: 03-customers.md

```
Write the file 03-customers.md. Same rules as before.

YAML header: file: 03-customers, project: {{PROJECT_NAME}}, date: {{DATE}}, version: 1, client_review: no

Sections:
## Segments (2 to 4 at most)
For each segment: who they are, main need, buying trigger, frequent objections, channels through which they arrive.
## What customers say (real verbatim quotes only, and flag any paraphrase)
## Customers the company does not want to target
## Current journey (from discovery to purchase or order)
## Questions to complete (3 at most)
```

## Prompt 4: 04-market.md

```
Write the file 04-market.md. Same rules as before.

YAML header: file: 04-market, project: {{PROJECT_NAME}}, date: {{DATE}}, version: 1, client_review: no

Sections:
## Current positioning
## Direct competitors (3 to 5, named)
## Indirect competitors and substitutes
## What sets us apart (with supporting evidence, otherwise [inferred])
## Industry trends and threats
## Admired references (and why)
## Seasonality or business rhythm
## Questions to complete (3 at most)
```

## Prompt 5: 05-brand.md

```
Write the file 05-brand.md. Same rules as before.

YAML header: file: 05-brand, project: {{PROJECT_NAME}}, date: {{DATE}}, version: 1, client_review: no

Sections:
## Mission and promise
## Personality (5 adjectives at most)
## Tone of voice (with 2 example sentences that show it)
## What the brand is not
## Existing assets (logo, brand guidelines, typefaces, colors: yes or no, and where to find them)
## Content that represents the brand well (links or descriptions)
## Words to use and words to avoid
## Questions to complete (3 at most)
```

## Prompt 6: 06-pains-doubts.md

```
Write the file 06-pains-doubts.md. This is the most important file. Be direct, without embellishment and without marketing language. Same rules as before.

YAML header: file: 06-pains-doubts, project: {{PROJECT_NAME}}, date: {{DATE}}, version: 1, client_review: no

Sections:
## Current frustrations
## What failed before, and why
## Doubts about this project
## Fears (budget, deadline, loss of control, disappointing result)
## Sensitive topics or internal tensions (by role, without naming anyone)
## What is rarely said in meetings
## Questions to complete (3 at most)
```

## Prompt 7: 07-constraints.md

```
Write the file 07-constraints.md. Same rules as before.

YAML header: file: 07-constraints, project: {{PROJECT_NAME}}, date: {{DATE}}, version: 1, client_review: no

Sections:
## Budget and deadlines (reminder)
## Technical constraints (required tools, hosting, integrations)
## Legal and regulatory constraints (personal data, accessibility, legal notices, intellectual property)
## Available internal resources (time, people, by role)
## Required approvals (who approves what, and how quickly)
## Non-negotiables
## Access and items to provide to the provider
## Questions to complete (3 at most)
```

## Prompt 8: 00-summary.md

```
Write the file 00-summary.md based on the 7 files produced.

Content:
## Index (each file with a one-sentence summary)
## The 5 most important points
## Information to verify (every high-impact [inferred] and [memory] mention)
## Missing information (every [unknown] mention)
## Sensitive data possibly present (to remove before sending if it is not needed)
```

## Prompt 9: compilation and manifest

The manifest is a small information sheet that comes with the files. It lets the provider know how the brief was produced. If the client's LLM makes a mistake while filling it in, the provider's checking script will flag it, so perfection is not what matters here.

Version with a .zip:

```
Compile the files produced (00-summary.md and 01 to 07, only those that exist) into a .zip archive named brief-md-{{PROJECT_NAME}}.zip. Add at its root a manifest.json file in the format below. Fill it in with the real values, without inventing anything (if you do not know, write "unknown").

{
  "brief_md_version": "0.2",
  "project": "{{PROJECT_NAME}}",
  "date": "YYYY-MM-DD",
  "level": "express or standard",
  "mode": "memory, questionnaire or hybrid (whichever mode was actually used)",
  "llm": "name of the tool used",
  "llm_memory": "yes, no or unknown",
  "modules": [],
  "status": "input document, not contractual",
  "files": {
    "02-project.md": { "client_review": "no", "visibility": "shared" }
  }
}

One block per file in "files". Leave "client_review" at "no" except for the files I said I have reread. Give me the download link. Do not change the content of any file.
```

Plan B if the LLM cannot create a .zip:

```
Since you cannot create a .zip, display the files produced, then manifest.json (same format and same rules as above), in a single message, one after the other, each one preceded by this exact separator line:
=== FILE: file-name ===
Do not change the content of any file.
```

## Express version (only 4 files)

For a client in a hurry, run only **Prompts 0, 0b, 2, 3, 6 and 7**, then Prompt 9 with `"level": "express"`. These four files cover the six pieces of information without which a provider cannot frame a project: goal, success criterion, final decision-maker, budget, main deadline, main target.
