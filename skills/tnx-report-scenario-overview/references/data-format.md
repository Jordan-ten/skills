# Overview data format

The page is built from one data file: `backend/.claude/plans/pitch/<pitch-slug>.overview.json`.
A complete example is in `references/example.overview.json`. Read it before you write a new file.

## Concepts

| Word | Meaning in the page |
|---|---|
| **Tâche** | One row of the pitch table "Main User Tasks". One capability seen by one role. Its number is its place in the pitch table. |
| **Issue (ticket)** | The GitHub issue of the milestone that covers the task. A task has zero or one main ticket. |
| **Lot** | A delivery batch of the pitch ("Lot 1", "Lot 2"). It is the Category column of the pitch table. A pitch with no lot has one lot. |
| **Parcours** | A story from start to end that chains several tasks, told through one or two roles. It shows how the tasks work together. |
| **MoSCoW** | The priority of a task. **Must** is in the delivery. **Should** can be cut. **Could** is shown like Should. |

## Fields

```jsonc
{
  "pitch": {
    "title": "Name of the pitch, as in Notion",
    "artifactTitle": "Two to four words",        // name of the Artifact
    "summary": "3 or 4 sentences: the problem, why now, what the pitch adds",
    "successIndicator": "optional, one sentence", // shown in a box under the summary
    "badges": ["fr", "en"],                       // optional chips about the pitch subject
    "badgesLabel": "optional, for screen readers",
    "source": { "capture": "...", "analysis": "...", "milestone": "270 — title" }
  },
  "issueBaseUrl": "https://github.com/<org>/<repo>/issues/",
  "artifactUrl": "set after the first publish",
  "lots": [{ "id": 1, "title": "Lot 1 · …", "sub": "optional line under the title" }],
  "tasks": [{
    "n": 1, "lot": 1, "p": "must",               // p: must | should | could
    "ticket": "25030",                            // optional, number as a string
    "title": "Role : action",
    "where": "UI : screen to open",               // optional, how to check it
    "note": "optional, one sentence",
    "scen": [{ "sit": "...", "res": "...", "tags": ["limite"] }]
  }],
  "parcours": [{
    "id": "p1", "label": "P1", "title": "...", "intro": "Lot 1. Acteurs : ...",
    "outcome": "optional, the expected end result",
    "steps": [{ "sit": "...", "res": "...", "tasks": [1, 4] }]
  }]
}
```

Write plain text only. The build script escapes it. Do not write HTML.

## Task rules

- Keep the pitch order. Never sort by priority. The Must filter does that in the page.
- Keep only the tasks that the analysis kept (its `moscow` list). A task with no value in Notion
  has the priority given in the analysis "Decisions". If the analysis gives none, ask the user.
- The title starts with the role, then a colon, then the action, as in the pitch. When the analysis changes a term of
  the pitch (for example interface language and content language), use the analysis wording and say so in `note`.
- When the priority was decided in the analysis and is not in Notion, say it in `note`.
- A Should task with no ticket needs no flag. The page already shows "pas de ticket".
- `where` starts with `UI :` (a screen), `Email :` (an email to trigger), or `Hors UI :`.
- `note` holds a fact the reader needs once, such as a conflict between the pitch and the analysis.

## Scenario rules

A scenario is one line: a situation, an arrow, a result. The arrow is drawn by the page.

- `sit`: what happens, with a person as the subject. No `GIVEN`, `WHEN`, `THEN`.
- `res`: what the person sees or receives. One sentence.
- Name people by business role (admin, chargé RSE, fournisseur invité). Name values as the user sees them (« Navigateur »).
- No code words (no entity, field, queue, or class names). Names of tools the team already uses, such as Novu or Auth0, are fine.
- Take scenarios from the analysis. Merge a GIVEN/WHEN/THEN block into one line. Do not invent a rule the analysis does not state.
- Put the nominal case first, then the edge cases.

Tags, only when true:

| Tag | Use when |
|---|---|
| `limite` | the scenario is an edge or error case |
| `confirmer` | the analysis marks it "to confirm" or lists it as an open question |
| `decide` | the analysis lists it in "Decisions". A decision with no scenario in the analysis may get its own line. |
| `ajout` | the analysis has no scenario for it. It comes from the pitch, an open question, or a decision. |
| `verifier` | the analysis says to check the ticket for it |

## Ticket rules

- The source is the analysis section "Already covered by existing issues". With `--refresh-tickets`,
  or when that section is missing, read the milestone with `gh issue list` (read only).
- Match on meaning, not on words. One main ticket per task. Put extra tickets in `note`.
- A ticket that covers only a part of the task is still the ticket of the task. Say what is missing in `note`.
- Never invent a number. No ticket found: leave `ticket` out. The page shows "pas de ticket".

## Parcours rules

- Write 3 to 6 parcours. Each one is a story with a clear start and end, for one or two roles.
- Give each parcours the lot of its tasks in `intro` ("Lot 1." or "Lot 2."). Prefer one lot per parcours, so a cut lot
  removes whole parcours. Mix lots only when the story needs it, and say so in `intro`.
- 3 to 8 steps. A step is one `sit → res` line, like a scenario. `tasks` lists the tasks whose scenario the step shows working. Do not list a task for a step that only touches it.
- Use the parcours to show what the single tasks cannot: a setting made by an admin, then its effect on another person.
- Every task that a person can see in the product is in at least one parcours. A task with no visible effect
  (for example translations done in a tool) may stay out. The build warns about it. Say so in your report.
- `outcome` is only the success indicator of the pitch, when it fits this parcours.
- Ids are `p1`, `p2`… and labels `P1`, `P2`… in the order shown.

## Page text

The page text is in French. This file and the skill are in English.
