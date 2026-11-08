---
name: ship
description: The last mile of a project, which keeps a delivery checklist in .memory/SHIP.md and refuses to move a shipped project to archived while a blocking item is missing (an up-to-date README, a real screenshot or run, publication or a written reason not to publish, a write-up of the project, at least one recorded lesson). Use when the user is finishing, publishing, delivering, wrapping up or archiving a project, says it is done, or asks for a delivery checklist. Do not use to decide whether a project should stop, which is the user's call.
---

# Ship

Projects that end without a trace teach nothing and leave nothing to show, and the usual reason is that the last mile (the README, a screenshot, a short write-up of what was done) feels optional once the thing works. This skill turns that last mile into a gate.

## Lifecycle

A project has one status among `idea`, `active`, `paused`, `shipping` and `archived`, written at the top of `SHIP.md`. Moving to `archived` goes through these gates:

| From | Rule for moving to `archived` |
|---|---|
| `shipping` | Refused while a blocking item is unticked, and the answer lists what is missing. |
| `paused` | Allowed, with a warning if `LEARNINGS.md` is empty, since a project dropped without a lesson is a pure loss. |
| `active` | Allowed, with a warning that the delivery gate is being skipped. |
| `idea` | Allowed, with a warning that the project is being given up before it started. |
| unknown | Refused until the status is set. |

## Steps

1. Read `.memory/SHIP.md`, or create it from [CHECKLIST.md](CHECKLIST.md) on the first call and ask the user for the current status if nothing says it. Always work from the file rather than from a checklist rebuilt from memory.
2. Check yourself what real files can prove. The README must say what the project does, how to run it and where its configuration lives, without ever containing the secrets themselves. `LEARNINGS.md` must hold at least one real entry, and a file reduced to its title or to template placeholders counts as empty, which is why this item is checked on the file and never on the box. Tick those items only on that evidence.
3. Go through the remaining items with the user one at a time, and tick an item only when the user confirms it or a file proves it.
4. Draft the write-up with the user, one question per section (context and need, for whom, the decision that shaped the project, what was done, the result, what was learned), using only facts found in the journal, the decision log, the learnings and the README. A section without material stays empty, because an invented figure or anecdote is worse than a missing one.
5. Archive only after an explicit yes from the user, by setting the status to `archived` in `SHIP.md`, adding a journal entry and rewriting `STATE.md`. Archiving changes a status and never deletes or moves any file.

## What it does not do

- It does not decide whether a project should stop.
- It does not write the write-up in place of the user: it asks, then drafts from facts.
- It does not tick a declarative item on its own, only the ones a file can prove.
