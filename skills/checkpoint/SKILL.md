---
name: checkpoint
description: Reviews the current session and writes the project memory in .memory/ at a natural checkpoint, deciding file by file whether an entry is earned (journal, decisions, blockers, learnings) and then rewriting STATE.md. Use when a task is finished, before changing subject, before ending a session, when the user asks to capitalize, save progress, wrap up, take notes or update the memory (in any language), or when a long stretch of work has gone by without anything recorded.
---

# Checkpoint

A checkpoint makes sure that no session goes by without a trace while never forcing an entry that was not earned. Run it at each natural checkpoint and not only at the end, which means when a task is finished, when the subject changes, or when a series of edits forms a whole.

When the work ends with a commit, run the checkpoint just before committing, so that the memory goes into the same commit instead of becoming a step of its own.

## Steps

1. Find the memory folder, which is `.memory/` at the root of the project unless the project already keeps these files elsewhere (such as `.claude/memory/`), in which case that folder is used and no second one is created. If none exists, create `.memory/`, and create only the files you are about to write, each from the template of its skill.
2. Reread the session: which files changed, which choices were made between real alternatives, which traps cost time, which ways of working were proven, and which checks were run with which result.
3. Decide for each file, in this order, with the matching skill for its format and its bar:
   - `JOURNAL.md` with the `journal` skill, which gets one entry when real work happened and nothing when the session was only a discussion;
   - `DECISIONS.md` with the `decisions` skill, only for a structural choice;
   - `BLOCKERS.md` with the `blockers` skill, only for a concrete trap likely to come back;
   - `LEARNINGS.md` with the `learnings` skill, only for a way of working proven by a fact.

   Leave a file untouched when nothing earns an entry in it, rather than inventing a filler one.
4. Rewrite `STATE.md` in full with the `state` skill, so that the next session starts from it.
5. End with a short summary that lists what was added to each file, or says "nothing to record" for the files left untouched.

## The bar for every entry

- Proof comes before claims, so "the tests pass" is written only if they ran and passed in this session, and anything else is marked as not verified.
- Each file keeps the format and the level of brevity it already uses.
- One entry covers everything since the last checkpoint, and several small entries in a row are a sign that they should have been batched.
- No secret ever goes into these files, whether a key, a token or a password, even partially.
