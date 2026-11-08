# Client tutorial (template)

Register: professional and warm. Variables: `{{PROVIDER}}`, `{{PROJECT_NAME}}`, `{{DURATION}}`, `{{SEND_VIA}}`.

---

# Prepare your brief with your AI assistant

Hello,

Before we start {{PROJECT_NAME}}, I would like us to begin on a solid footing. Rather than holding meeting after meeting so that I can understand your business, I suggest an exercise: ask your AI assistant (ChatGPT, Claude, Gemini or another one) to produce, from what it knows about you, 7 short files that describe your context.

**Estimated time: {{DURATION}}.** You stay in control at every step.

## What you gain
- A kickoff meeting focused on your real stakes rather than on introductions
- A project that is better aligned from the very first day
- A reference document that you can reuse elsewhere

## Two ways to do it, so pick yours

**Path A, with Claude (the simplest).** If you use Claude, first add the free `brief-md-client` skill, which you will find in the `skills/brief-md-client` folder of https://github.com/antidoteforai-netizen/product-skills. Download that folder, compress it into a .zip file, then upload it in Claude's settings, in the Skills section. If you work with a coding agent, a single command does the same job: `npx skills@latest add antidoteforai-netizen/product-skills --skill brief-md-client`. Then drop the `brief.config.json` file I sent you into the conversation and write: "Help me prepare my brief." Claude asks you the questions one by one, writes the files and prepares the archive to send me.

**Path B, with any assistant** (ChatGPT, Gemini, Mistral...). Follow the steps below: you copy the prompts, and the assistant does the rest.

**Level: Express or Standard.** If you are short on time, do only the **Express** level (4 files: project, customers, constraints, pains and doubts). It is the minimum I need to get started, and you can complete the rest later. In path B, it corresponds to Prompts 2, 3, 6 and 7.

## Before you start
1. Open the AI assistant you use most often, the one that knows you best.
2. Check whether its memory is turned on (in its settings). If you are not sure, that is no problem, because the kit covers both cases.
3. Read the privacy paragraph below.

[Insert the privacy notice here]

## Step 1: set the rules
Copy **Prompt 0** into your assistant, and it answers "Understood". Then copy the **Prompt 0b** that matches your situation (memory, questionnaire, or hybrid if you are not sure).

## Step 2: produce the files one by one
Copy **Prompts 1 to 7**, one after the other. For each one:
- Read the answer, and correct whatever is wrong by telling the assistant ("This is inaccurate, it is actually...").
- Answer the questions at the end of the file if you can. Otherwise, leave them.

The mentions in square brackets have a meaning:
- **[confirmed]**: you said it or it is documented
- **[memory]**: your assistant remembers it but has not rechecked it
- **[inferred]**: the assistant guessed it, so it needs checking
- **[unknown]**: nobody knows yet, and that is perfectly fine

## Step 3: the summary
Copy **Prompt 8**. It summarizes the 7 files and lists what remains to be checked.

## Step 4: reread
Take 10 minutes with this list:
- [ ] The figures are correct
- [ ] No name of a person and no sensitive data appear in the files
- [ ] File 06 truly says what you think, without a filter
- [ ] The [inferred] mentions are either corrected or knowingly left as they are
- [ ] You are comfortable with everything you are about to send

You can also edit the files by hand if you prefer.

## Step 5: compile and send
Copy **Prompt 9**. It creates the archive and a small information sheet (`manifest.json`) that tells me how the brief was produced. If your assistant cannot create a .zip file, use the backup version provided. Then send the result to {{PROVIDER}} {{SEND_VIA}}.

## Frequently asked questions
**My assistant says it does not know me.** Use the questionnaire mode, so that it asks you the questions one by one.

**My assistant makes things up.** Tell it: "Keep only what I have confirmed, and mark the rest as [unknown]." That is what the labels are for.

**I do not want to share one part.** Delete it before sending, or keep it for our meeting. Nothing is mandatory.

**I do not want to share file 06.** Keep it to yourself and let me know, so that we can talk about it in person.

**I am stuck.** Write to me, and we will produce the missing files together during a meeting.
