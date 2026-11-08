---
name: decisions
description: Logs structural choices in .memory/DECISIONS.md (architecture, data format, tooling, process, or a trade-off that amends an earlier decision) before carrying them out, and checks the log before proposing a change so that a settled decision is never contradicted silently. Use when a choice between real alternatives is made, when the user says "let's go with", "we decided" or "from now on", before changing the architecture or a convention, or when the checkpoint skill asks for a decision entry.
---

# Decisions

The decision log keeps the reasons behind the shape of the project, so that a future session does not undo a choice it cannot see the reason for.

## When an entry is earned

A decision deserves an entry when it was a choice between real alternatives and its effects outlast the session, for example a library, a file format, a folder layout, a rule of work or a compromise accepted on purpose. A cosmetic adjustment, a variable name or a fix with only one obvious solution does not deserve one.

## Before proposing a change

Read the log first. If what you are about to propose contradicts a recorded decision, say so explicitly in your answer and name the entry before going any further, because a decision is never contradicted silently.

## Writing an entry

Write the entry before carrying out the decision, not afterwards, with the format of [TEMPLATE.md](TEMPLATE.md), and create the file from it if it does not exist. Number the entries DEC-001, DEC-002 and so on, continuing from the last number in the file.

```
## DEC-NNN: <short title>
- **Date**: YYYY-MM-DD
- **Context**: <the constraint or the need that forces a choice>
- **Options**: (a) ...; (b) ...
- **Choice**: <the option kept>
- **Rationale**: <why this one rather than the others, and which earlier decision it amends, if any>
- **Consequences**: <what it changes, including the trade-offs accepted>
- **Reversibility**: <easy, costly or hard, and how to go back>
```

## Rules

- Never delete an entry: when a decision is replaced, write the new one, say in it which entry it replaces, and add `[REPLACED BY DEC-NNN]` to the title of the old one.
- The reasons are the point of the entry, so an entry that lacks the rejected option and the reason it lost is only a note.
- A decision that must not be reopened also goes, in one line, under "Settled" in `STATE.md`.
- Write in the language the user works in.
