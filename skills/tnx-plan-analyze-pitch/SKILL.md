---
name: tnx-plan-analyze-pitch
description: Slash-only. Use only when the user explicitly invokes /tnx-plan-analyze-pitch with a captured pitch name. Reads a local pitch capture and writes an analysis: summary, lexicon grounded in the code, and GIVEN/WHEN/THEN scenarios filtered by MoSCoW. Never trigger from natural-language requests.
disable-model-invocation: true
allowed-tools: Read, Write, Bash, Glob, Grep, AskUserQuestion
---

# Analyze Pitch

Turn a local pitch capture into a business context: summary, lexicon, scenarios. No technical implementation details.

The capture is made by `/tnx-plan-capture-pitch`. This skill never calls Notion.

## Arguments

`$ARGUMENTS` — pitch name or path of a capture, then optional flags. If the pitch is empty, list `backend/.claude/plans/pitch/*.md` (without `*.analysis.md`) and ask the user to choose.

Optional flag: `--milestone <title|number>` — compare the selected tasks with the issues of an existing GitHub milestone. Without it, the skill never calls GitHub.

If no capture exists, tell the user to run `/tnx-plan-capture-pitch` first and stop.

## Steps

1. **Read the capture.** `backend/.claude/plans/pitch/<pitch-slug>.md`. Show its `fetched_at` date to the user. If the pitch may have changed since, suggest a refresh with `/tnx-plan-capture-pitch`.
2. **Ask the MoSCoW levels.** Show the tasks grouped by category with their priority. Ask which levels to keep (`1 = Must`, `2 = Should`, `3 = Could`, `4 = Won't`; answers like "1", "1 and 2", "all"). Continue with the selected tasks only.
3. **Read the code for the lexicon.** Do this silently. In `backend/src/` and `frontend/src/`:
   - find the NestJS module(s) of the pitch (`src/<domain>/`);
   - note the names already used: entities, properties, GraphQL types, services, queues.
   Use these names in the lexicon. Do not invent a new word when the code already has one.
4. **Check the milestone (only with `--milestone`).** Read `../tnx-plan-refine-issue/references/milestone-context.md` completely and follow its contract for the given milestone. Then, for each selected task, look for an open or closed issue of the milestone that already covers it. Match on meaning, not only on words. Note the issue number and its state. Do not change any scenario because of it. Do not mutate GitHub.
5. **Write the analysis.** Path: `backend/.claude/plans/pitch/<pitch-slug>.analysis.md`. Write the file at once, before any feedback. Overwrite an existing analysis only after telling the user.
6. **Iterate.** Give the path, the section titles, and the number of scenarios. Ask for corrections (scenario, lexicon term, scope). Update the file and ask again until the user says "ok".

## File format

```markdown
---
capture: <pitch-slug>.md
capture_fetched_at: <value from the capture>
moscow: [<selected levels>]
milestone: <title or number, only with --milestone>
generated_at: <YYYY-MM-DD HH:mm>
---

# Analysis: <pitch title>

## Summary

**Problem**: ...
**Proposed solution**: ...
**In scope**: ...
**Out of scope**: ...
**Key constraints**: ...

## Lexicon

| PM term | Existing code term | Module / file | Notes |
|---------|--------------------|---------------|-------|

> New terms: pitch terms that do not exist in the code yet.

## Selected tasks (MoSCoW <levels>)

### <Category>

- [Must] <task>

## Scenarios

### <Task title>

**Context**: <short need>

#### Nominal case

GIVEN <initial state>
WHEN <user action>
THEN <observable result>

#### Edge case / Error case (if the pitch gives enough information)

GIVEN ...
WHEN ...
THEN ...

## Already covered by existing issues

Only with `--milestone`. Omit this section otherwise.

| Task | Issue | State | Note |
|------|-------|-------|------|
| <task> | #123 | open / closed | <full or partial coverage> |

Tasks with no matching issue: <list, or "none">.

## Open questions

> **[Domain]** Precise question?
> _Why it matters_: short reason
```

## Rules

- Observable behavior only: no table names, resolvers, or migrations.
- At least one nominal scenario per selected task.
- Without `--milestone`, do not call GitHub.
- A milestone match is a hint for the user. Never remove a task or a scenario because an issue seems to cover it.
- Never change the capture file. Corrections go in the analysis.
- Write the analysis in the language of the pitch.
