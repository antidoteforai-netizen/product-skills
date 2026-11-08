---
name: journal
description: Appends a short entry to .memory/JOURNAL.md at each natural checkpoint of a session (a task finished, a change of subject, a coherent series of edits), saying what was done, what blocks and what comes next. Use when a task is finished, before switching subject, when the user asks to log or note the work, or when the checkpoint skill asks for a journal entry.
---

# Journal

The journal answers the question "what happened, and when". It takes one entry per checkpoint and never one per edited file or per tool call, because a single entry that covers everything since the last checkpoint keeps the file readable and cheap to reread.

## Format

Use the format of [TEMPLATE.md](TEMPLATE.md), and create the file from it if it does not exist yet.

```
## YYYY-MM-DD (n)
- **Done**: <what changed and why it matters, in one or two sentences>
- **Blocked**: <what stops progress, or "nothing">
- **Next**: <the next action>
```

`(n)` counts the entries of the same day, starting at 1.

## Rules

- Read the last entries before writing, and keep the order and the style the file already uses: the template adds new entries at the bottom, but some journals are kept newest first, and an existing file is never flipped.
- Write only what really happened in this session, since a change that was proposed but not made is not done and a test that was not run has not passed.
- Write nothing when the session was only a discussion with no change.
- Write in the language the user works in, and never copy a secret into the file.
