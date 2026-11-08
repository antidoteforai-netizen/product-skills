---
name: blockers
description: Records in .memory/BLOCKERS.md the traps that already cost time (symptom, cause, workaround or prohibition) and reads them before proposing an approach. Use before planning work in a project that has this file, when a bug or a dead end took more than one attempt to understand, when the work has been going in circles for about thirty minutes, or when the checkpoint skill asks for a blocker entry.
---

# Blockers

A blocker entry is a warning sign on a road that has already been taken, written so that nobody, human or agent, pays twice for the same mistake.

## Read before proposing

Before proposing an approach, read the file and check whether the plan walks into a known trap; if it does, say so and use the recorded workaround instead.

## When an entry is earned

A trap deserves an entry when it is concrete and likely to come back, for example a tool that behaves differently from its documentation, a dependency between two parts that nobody anticipated, or a difference between two environments. A typo fixed at the first attempt does not deserve one.

## Going in circles

When the same problem has resisted for about thirty minutes, or for three attempts that fail the same way, stop, write the blocker with what was tried and ruled out, restate the problem in one sentence, and then either change angle or bring the problem back to the user.

## Format

Use the format of [TEMPLATE.md](TEMPLATE.md), create the file from it if it does not exist, and number the entries BLK-001, BLK-002 and so on.

```
## BLK-NNN: <short title>
- **Date**: YYYY-MM-DD
- **Symptom**: <what was seen, in plain words>
- **Cause**: <the technical reason once it is known, or "unknown">
- **Workaround / prohibition**: <what to do, or never do, from now on>
```

When a blocker is solved for good, keep the entry and add a `**Solved**:` line with the date and how it was solved, since the trap can still catch someone who does not know it was there. Write in the language the user works in.
