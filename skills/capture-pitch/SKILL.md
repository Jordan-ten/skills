---
name: capture-pitch
description: Slash-only. Use only when the user explicitly invokes /capture-pitch with a Notion pitch name or URL. Saves a local copy of a PM pitch from Notion. Never trigger from natural-language requests.
disable-model-invocation: true
allowed-tools: Read, Write, Bash, Glob, AskUserQuestion
---

# Capture Pitch

Pitch files live in `.claude/plans/pitch/` at the repo root, whatever the working directory.

Save a local copy of one PM pitch from Notion. The copy is the input for ticket writing, plans, and `/analyze-pitch`.

This skill copies. It does not interpret, summarize, or judge.

## Arguments

`$ARGUMENTS` — pitch name or Notion URL. If empty, ask the user.

## Steps

1. **Find the pitch.** Follow the `tnx-doc-notion-access` skill to read Notion.
   - URL given: fetch the page.
   - Name given: search. If there are several results, list them and ask the user to choose.
2. **Read the sub-pages.** Fetch every sub-page and internal link of the pitch. Look first for "Main User Tasks", "User Tasks", "Tâches utilisateur", and detail pages per category or per task.
3. **Write the capture.** Path: `.claude/plans/pitch/<pitch-slug>.md`.
   - `<pitch-slug>`: pitch title, lowercase, spaces replaced by hyphens, no date (the name must stay stable).
   - If the file exists, tell the user it will be refreshed, then overwrite it.
   - Create the folder if needed.
4. **Report.** Give the file path, the number of sub-pages read, and the number of tasks found. Nothing else.

## File format

```markdown
---
title: <pitch title>
source_url: <Notion URL>
fetched_at: <YYYY-MM-DD HH:mm>
---

# <pitch title>

<pitch content, copied as written, same language, same section titles>

## Main User Tasks

| Category | MoSCoW | Task | Details |
|----------|--------|------|---------|
| ...      | Must   | ...  | ...     |

## Sub-pages

### <sub-page title>

<sub-page content, copied as written>
```

## Rules

- Copy the words of the PM. Do not rewrite, shorten, or translate.
- Keep the MoSCoW value as written in Notion (Must / Should / Could / Won't, or 1 to 4).
- Do not explore the code. Do not add lexicon, scenarios, or questions. That is the job of `/analyze-pitch`.
- If a part of the pitch cannot be read (permission, empty page), write `> Not captured: <reason>` in its place.
