---
name: learnings
description: Keeps in .memory/LEARNINGS.md the ways of working proven on a project, each with the observed fact that proves it and the rule that follows from it. Use when something worked or failed in a way that should change how the work is done from now on, when the user asks to remember a way of working, or when the checkpoint or ship skill asks for a learning.
---

# Learnings

A learning is earned by a fact and not by an impression: something measured or observed in this project, such as a command that turned out to be the only reliable check or a method that saved a round of corrections. A rephrasing of generic documentation is not a learning.

A blocker and a learning differ in direction, since a blocker is a trap to avoid while a learning is a way of working to repeat. When the same event gives both, write the trap in `BLOCKERS.md` and the rule in this file.

## Format

Use the format of [TEMPLATE.md](TEMPLATE.md), create the file from it if it does not exist, and number the entries LRN-001, LRN-002 and so on.

```
## LRN-NNN: <short title>
- **Date**: YYYY-MM-DD
- **Observation**: <what really happened, measured if possible>
- **Rule**: <what to do systematically from now on>
- **Source**: <where it was seen: a file, a command, an incident>
```

Write in the language the user works in. A learning that turns out to be wrong is corrected in place with a dated note rather than silently deleted.
