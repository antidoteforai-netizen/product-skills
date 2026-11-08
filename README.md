# Product Skills

Skills that give a coding agent a memory of your project, so that a new session picks up exactly where the last one stopped instead of asking you to explain everything again.

Each skill owns one small file in `.memory/`: the present lives in `STATE.md`, the past lives in `JOURNAL.md`, `DECISIONS.md`, `BLOCKERS.md` and `LEARNINGS.md`, and two more skills tie them together, `checkpoint` to write them at the right moment and `ship` to close a project without losing what it taught you.

## Install

```bash
npx skills@latest add antidoteforai-netizen/product-skills
```

Install the whole kit, because `checkpoint` and `ship` rely on the other skills for the format of each file.

## Why use it?

An agent forgets everything between sessions, so you either explain the project again every morning or let it guess, and guessing is how settled decisions get reopened and known traps get walked into twice.

Writing everything down at the very end does not work either, because by then the session is too long to summarize honestly and the useful details are already gone. These skills write a few lines at each natural checkpoint (a task finished, a change of subject, a coherent series of edits), keep the present on a single screen, and refuse to start a step that has no condition anyone can check to say it is finished.

## Reference

- **[state](./skills/state/SKILL.md)** — Reads `STATE.md` first at the start of a session and rewrites it in full at the end, in fifteen lines at most, so that someone who reads only this file knows where to resume.
- **[journal](./skills/journal/SKILL.md)** — Adds one short entry per checkpoint to `JOURNAL.md`, saying what was done, what blocks and what comes next.
- **[decisions](./skills/decisions/SKILL.md)** — Logs a structural choice in `DECISIONS.md` before carrying it out, with the alternatives it beat and how to undo it, and flags any proposal that would contradict an earlier decision.
- **[blockers](./skills/blockers/SKILL.md)** — Records in `BLOCKERS.md` the traps that already cost time and reads them before proposing an approach, so that the same mistake is not made twice.
- **[learnings](./skills/learnings/SKILL.md)** — Keeps in `LEARNINGS.md` the ways of working proven on this project, each with the observation that proves it.
- **[checkpoint](./skills/checkpoint/SKILL.md)** — Reviews the session, decides file by file whether an entry is earned, writes only those and rewrites the state, without forcing anything when nothing happened.
- **[ship](./skills/ship/SKILL.md)** — The last mile of a project, a checklist that refuses to archive a shipped project while a blocking item such as the README, a screenshot, the publication, a write-up or a recorded lesson is still missing.

## Where the files live

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
