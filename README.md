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

`stack-pull-requests` needs the `gh stack` extension and the `gh-stack` skill:

```
gh extension install github/gh-stack
gh skill install github/gh-stack gh-stack --agent claude-code --scope user
```

Without `--agent` and `--scope`, `gh` installs the skill in the current project.

## Use

A plugin skill is called with the plugin name: `/jcontent-traace:<skill>`, for example `/jcontent-traace:rebase`.
The tables below show the short name.

Skills marked **slash-only** run only when you type their command. Claude never starts them from a normal sentence.

## Glossary

### Pitch

| Skill | What it does | Slash-only |
|---|---|---|
| `capture-pitch` | Saves a local copy of a PM pitch from Notion. | yes |
| `analyze-pitch` | Reads a captured pitch. Writes a summary, a lexicon grounded in the code, and GIVEN/WHEN/THEN scenarios sorted by MoSCoW. | yes |
| `build-scenario-overview` | Builds an Artifact page with the pitch scenarios: tasks by lot and priority, GitHub tickets, and user journeys. | yes |

### Dev

| Skill | What it does | Slash-only |
|---|---|---|
| `rebase` | Rebases the current branch on a target branch (default `main`). Fixes generated-file conflicts, applies migrations, regenerates the GraphQL schema and SDK types, checks types, runs related tests, then force-pushes. | no |
| `stack-pull-requests` | Splits a validated plan into a stack of pull requests, one per layer. Then manages the stack: status, review fixes, rebase, sync. | no |
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
| `triage-code-review-pull-request` | Prepares the review of a colleague's pull request. Runs `/code-review`, the coding-style checklists, the ticket check and the CI status. Writes one report: what the agent checked, and what a human must still check. | no |

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
