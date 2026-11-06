# skills

Personal Claude Code skills for the Tennaxia (traace) project, packaged as a plugin.

- Plugin: `jcontent-traace`
- Marketplace: `jordan-skills`

## Install

From the local clone:

```
/plugin marketplace add ~/code/skills
/plugin install jcontent-traace@jordan-skills
```

From GitHub, on another machine:

```
/plugin marketplace add Jordan-ten/skills
/plugin install jcontent-traace@jordan-skills
```

To use it in one project only, choose the "local" scope when you install.

Quick test, without install: `claude --plugin-dir ~/code/skills`

Update after a `git pull`: `/plugin marketplace update jordan-skills`

## Requirements

`stack` needs the `gh stack` extension and the `gh-stack` skill:

```
gh extension install github/gh-stack
gh skill install github/gh-stack gh-stack --agent claude-code --scope user
```

Without `--agent` and `--scope`, `gh` installs the skill in the current project.

## Use

A plugin skill is called with the plugin name: `/jcontent-traace:<skill>`, for example `/jcontent-traace:rebase`.
The tables below show the short name.

Skills marked **slash-only** run only when you type their command. Claude never starts them from a normal sentence.

## Workflow

Three skills with `workflow` in the name. Each one runs a fixed list of steps.

```
pitch ─issue-workflow→ issues ─feature-implementation-workflow→ pull requests ─review-workflow→ review
```

`issue-workflow` and `feature-implementation-workflow` work in phases. At the end of each phase, Claude shows proof that it is done, then you choose: continue, compact, redo, or stop. You can run the same command again to resume.

### `issue-workflow`

From a PM pitch to GitHub issues. Command: `/jcontent-traace:issue-workflow <pitch name or Notion URL>`.

1. **Capture**: save a local copy of the pitch.
2. **Analyze**: write the summary and a first draft of the scenarios.
3. **Overview**: publish a page with the tasks, scenarios and user journeys.
4. **Refine**: complete and validate the scenarios with you.
5. **Create issues**: one GitHub issue per task.
6. **Sync**: update the analysis and the overview with the final result.

### `feature-implementation-workflow`

From a GitHub issue to pull requests. Command: `/jcontent-traace:feature-implementation-workflow <issue URL or number>`.

1. **Refine the issue**: fix the scenarios in the issue.
2. **Plans**: one plan per package (backend, frontend).
3. **Split**: decide the pull requests, one per layer.
4. **Implement**: code and tests, layer by layer, one commit per layer.
5. **Verify**: generated code, all tests, and each scenario checked in the UI.
6. **Ship**: push and open the pull requests, after your yes.

### `review-workflow`

From a PR number to a review report. Run it in the Orca "Review" workspace. No phases, no questions.

1. Read the PR.
2. Create a child workspace `review-<n>` with the PR code.
3. Start an agent that runs `/jcontent-traace:review <n>`.

The agent writes the report in `.claude/plans/review/<n>.md`. It never posts on the PR.

## Glossary

### Pitch

| Skill | What it does | Slash-only |
|---|---|---|
| `capture-pitch` | Saves a local copy of a PM pitch from Notion. | yes |
| `analyze-pitch` | Reads a captured pitch. Writes a summary, a lexicon grounded in the code, and GIVEN/WHEN/THEN scenarios sorted by MoSCoW. | yes |
| `build-scenario-overview` | Builds an Artifact page with the pitch scenarios: tasks by lot and priority, GitHub tickets, and user journeys. | yes |
| `issue-workflow` | Takes a PM pitch to GitHub issues in six phases, with exit conditions and a compact between phases: capture, analyze, overview of the pitch lots and tasks with scenarios and journeys, refine and complete the scenarios with the user, create one issue per task, then sync the analysis and the overview. Resumable. | yes |

### Dev

| Skill | What it does | Slash-only |
|---|---|---|
| `rebase` | Rebases the current branch on a target branch (default `main`). Fixes generated-file conflicts, applies migrations, regenerates the GraphQL schema and SDK types, checks types, runs related tests, then force-pushes. | no |
| `feature-implementation-workflow` | Takes a feature from its GitHub issue to pull requests in six phases, with exit conditions and a compact between phases: refine the issue scenarios, write one plan per package, split into PRs, implement, verify (generated code, all tests, end to end in the UI), push. Resumable. | yes |
| `stack` | Splits a validated plan into a stack of pull requests, one per layer. Then manages the stack: status, review fixes, rebase, sync. | no |
| `create-local-data` | Creates records in the local app through the GraphQL API with an offline-auth token. Used to see a screen, reproduce a bug, or prepare a demo. | no |
| `launch` | Starts the backend in dev or test. Checks Docker, runs PostgreSQL and ClickHouse migrations, starts NestJS in watch mode, and waits until it is healthy. | no |
| `hotfix` | Creates hotfix PRs for demo and/or production, or a revert PR for `main`, from a branch or a commit. Infers the issue number from the branch name. | no |

### QA

| Skill | What it does | Slash-only |
|---|---|---|
| `run-qa-scenarios` | Tests a GitHub issue against its own scenarios in the local app, with the Chrome DevTools MCP. Gives one verdict per scenario. Read-only. | no |

### Review

| Skill | What it does | Slash-only |
|---|---|---|
| `review` | Prepares the review of a colleague's pull request. Runs `/code-review`, the coding-style checklists, the ticket check and the CI status. Writes one report: what the agent checked, and what a human must still check. | no |
| `review-workflow` | Run from the Orca "Review" workspace with a PR number or URL. Creates a child Orca workspace on the PR code, drops the review rules in it, and starts the triage agent. | no |

### Deployment

| Skill | What it does | Slash-only |
|---|---|---|
| `deployment-instructions` | Step-by-step instructions to deploy `main` to production or demo. | yes |

### Maintenance

| Skill | What it does | Slash-only |
|---|---|---|
| `audit-skills` | Checks the skills of this repo against the current Claude Code docs and release notes. Runs a script for the mechanical rules, reports the gaps, and applies the fixes you choose. | yes |

## Add a skill

1. Create `skills/<name>/SKILL.md` with `name` and `description` in the front matter.
2. Add a line to the glossary above.
3. Commit and push. On each machine, run `/plugin marketplace update jordan-skills`.

## Naming

- Lowercase letters, digits and hyphens. Maximum 64 characters.
- `name` is the same as the folder name.
- Start with a verb, then the object: `rebase`, `capture-pitch`, `run-qa-scenarios`.
- No `tnx-` prefix. The plugin name already gives the namespace.
- No vague names like `helper` or `utils`.
- The `description` says what the skill does and when to use it. Claude reads it to choose the skill.
