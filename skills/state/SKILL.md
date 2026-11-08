---
name: state
description: Reads and rewrites .memory/STATE.md, the one-screen present tense of a project (where it stands, the single next step with its done-when condition, and what is settled). Use at the very start of a session in a project before any other work, whenever the user asks to resume, continue, pick up where they left off or where things stand (in any language), and at the end of a session or after a checkpoint to rewrite the file in full.
---

# State

`STATE.md` holds the present of the project and nothing else, since the past belongs to the journal and the decision log while the future is reduced to the single next step written here. It is the first file read in a session and the last one rewritten.

The memory folder is `.memory/` at the root of the project. If the project already keeps these files in another folder, such as `.claude/memory/`, use that folder for every file and never create a second one.

## At the start of a session

1. Read `.memory/STATE.md` before doing anything else, then `BLOCKERS.md` if it exists, because a known trap is cheaper to read than to rediscover.
2. Tell the user in two or three sentences where the project stands and what the next step is, quoting its `Done when:` line, and ask whether to go on with it.
3. If the file does not exist, say so plainly, look at what the folder already contains (README, recent commits) and offer to create the memory at the first checkpoint, rather than presenting a guess as the state of the project.

When the conversation, a recollection or another file contradicts `STATE.md`, the file wins: point out the gap to the user and correct the file instead of working around it.

## Before starting a step

Never start a step that has no `Done when:` line. Ask the user for that condition rather than deducing it, because a step without a checkable end never finishes. A good condition is something a command, a file or a screenshot can confirm, such as "the tests pass" or "the page answers at this address", while "the page looks better" is a wish and not a condition.

## At the end of a session or after a checkpoint

Rewrite the whole file from [TEMPLATE.md](TEMPLATE.md), never by appending to it, in fifteen lines at most. Before saving, apply one test: someone who has read only this file knows where to resume without asking anything.

- "Where it stands" holds three bullets at most, covering what is in progress, what was just finished and what blocks.
- "Next step" holds a single step in a single sentence, followed by its `Done when:` line.
- "Settled" lists the decisions that are not to be reopened, one line each with its ID from `DECISIONS.md`.
- Use plain words the project owner understands, because this file is read by people as well as agents, and leave the technical detail to the journal.
- Update the date line and write in the language the user works in.
