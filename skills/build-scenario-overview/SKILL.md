---
name: build-scenario-overview
description: Slash-only. Use only when the user explicitly invokes /build-scenario-overview with a captured and analyzed pitch name. Builds a private Artifact page with an overview of the pitch scenarios - tasks by lot and MoSCoW priority with their scenarios and GitHub tickets, plus the end-to-end user parcours that link the tasks. Never trigger from natural-language requests.
disable-model-invocation: true
allowed-tools: Read, Write, Bash, Glob, Grep, AskUserQuestion, Artifact
---

# Scenario Overview

Show the scenarios of a pitch on one page, to check in a meeting that no scenario is missing.
The page has two views, linked by clickable chips:

- **Par tâche**: the tasks of the pitch in pitch order, grouped by lot. Each task has a Must or Should badge,
  its ticket (or "pas de ticket"), and its scenarios in one line each.
- **Par parcours**: end-to-end stories. Each step points to the tasks it uses.

The capture comes from `/capture-pitch`, the analysis from `/analyze-pitch`.
This skill never calls Notion and never writes to GitHub.

## Arguments

`$ARGUMENTS` — pitch name or path, then optional flags. If the pitch is empty, list
`backend/.claude/plans/pitch/*.analysis.md` and ask the user to choose.

- `--milestone <title|number>`: read the tickets from this milestone. Default: the `milestone` of the analysis.
- `--refresh-tickets`: read the tickets from GitHub even if the analysis already has a ticket table.

If the capture or the analysis is missing, tell the user which skill to run first and stop.

## Steps

Run every command from the repo root. The pitch files are in `backend/.claude/plans/pitch/`.

1. **Read the inputs.** In that folder: `<slug>.md`, `<slug>.analysis.md`, and `<slug>.overview.json`
   if it exists. In the analysis, `moscow: [1, 2, none]` means the tasks with no priority in Notion are kept too;
   their priority is in the section "Decisions". Read `references/data-format.md` completely. It defines the concepts (tâche, ticket, lot, parcours,
   MoSCoW) and the writing rules. Open `references/example.overview.json` as a model.
2. **Existing overview.** If `<slug>.overview.json` exists, ask: update it (refresh tasks and tickets, keep the
   parcours) or start again. When the analysis changed, tell the user what changed.
3. **Write the tasks.** Take the rows of the pitch table "Main User Tasks" that the analysis kept, in table order.
   Fill lot, priority, title, `where`, and the scenarios from the analysis. Follow the scenario rules.
4. **Add the tickets.** Use the analysis table "Already covered by existing issues". With `--refresh-tickets`, or when
   that table is missing, run `gh issue list --milestone "<title>" --state all --json number,title,state` (read only).
   Set `issueBaseUrl` with `gh repo view --json url -q .url` plus `/issues/`.
5. **Draft the parcours.** Follow the parcours rules. Show them to the user as a short list (title, steps, task
   numbers) with the tasks that are in no parcours. Ask for corrections. Repeat until the user says "ok".
   Do not build before that: a parcours that forgets a task misleads the meeting.
6. **Save and build.** Write `backend/.claude/plans/pitch/<slug>.overview.json`. Then run
   `python3 ${CLAUDE_PLUGIN_ROOT}/skills/build-scenario-overview/scripts/build_overview.py backend/.claude/plans/pitch/<slug>.overview.json <scratchpad>/<slug>.overview.html`.
   Put the HTML in the scratchpad directory, not in the repo. Fix every `error:` and run it again. Warnings are for the report.
7. **Publish.** Use the Artifact tool on the HTML file. Do not edit the page by hand: the layout is in
   `assets/overview-template.html`. If the data has an `artifactUrl`, publish to that `url` (read it first when this
   conversation has not published it). On a first publish, pass the icon `checklist` and a one-sentence description.
   Write the returned URL in `artifactUrl` of the data file. If the user does not want to publish, stop after the
   build and leave `artifactUrl` as it was.
8. **Report.** Give the link, the counts (tasks, Must, tickets, parcours), the Must tasks with no ticket, and the
   tasks in no parcours. Say that the page is private until the user shares it.

## Boundaries

- Do not change the capture or the analysis. If a scenario is wrong, tell the user and fix it in the analysis first.
- Do not invent a ticket number, a scenario, or a rule. Mark what the pitch says but the analysis misses with the `ajout` tag.
- The page text is in French. Keep the page layout: to change the look, edit the template and run the build again.
- The template and the data file are the source. Do not write a page from scratch.
