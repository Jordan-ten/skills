---
name: stack-pull-requests
description: Turn a validated plan into a stack of pull requests (one PR per layer), then manage the stack - status, review fixes on the right layer, rebase and sync. Built on top of the official gh-stack skill. Use when the user invokes /stack-pull-requests, says "split the plan into a stack", "stack de PR", "découpe le plan en stack", "corrige les retours de review sur la stack", "sync la stack", or wants dependent PRs.
disable-model-invocation: true
allowed-tools: Bash(git *), Bash(gh *), Bash(npm run *), Read, Edit, Write, Glob, Grep, AskUserQuestion
---

# Stack

Validated plan, then a stack of PRs, then review fixes, then rebase and sync.

**All git and GitHub mechanics go through the `gh-stack` skill** (non-interactive commands, exit codes,
conflicts). This skill only adds the Tennaxia workflow: split from a plan, PR format, artifact
regeneration, safety rules.

## Arguments

`$ARGUMENTS` is a sub-command: `split [plan]`, `status`, `fix [n]`, `sync`, `merge`. No argument: `status`.

## Prerequisites (check once)

```bash
gh --version        # >= 2.90
git --version       # >= 2.36
gh extension list   # gh-stack must be listed
gh stack view --json 2>&1 | head -20   # exit 9 = stacked PRs are not enabled on the repo: tell the user
```

If the extension or the `gh-stack` skill is missing, give the user these commands. Do not run them.
This keeps both up to date, which a copy in the repo would not.

```bash
gh extension install github/gh-stack
gh skill install github/gh-stack gh-stack
```

Update later with `gh extension upgrade gh-stack` and `gh skill update`.

## Rules for every sub-command

- Use only the non-interactive forms from the `gh-stack` skill: `view --json`, `submit --auto`,
  `init <branch>`, `add <branch>`, `checkout <target>`. Never `gh stack modify`.
- **Ask the user before** `gh stack push`, `submit`, `sync` (it pushes) and `merge`.
- Never commit on the top layer a change that belongs to a lower layer.
- One layer = one concern, described in one sentence. Each layer must pass its tests alone, with no
  dependency on a layer above.
- Branches, commits and PRs follow `tnx-dev-standards-dev-and-git-workflow`. Read it before `split`.
  - Branch: `<feature|bugfix|chore>/<issue>/<short-description>`, a different description per layer
    (`feature/23773/emission-factor-entity`, `feature/23773/update-version-usecase`). No number prefix.
    Take the type and the issue from the current branch.
  - Commit: `<type>(<issue>): short description`, **one commit per layer**. Review fixes are separate commits.
  - No `Co-Authored-By` line and no Claude attribution in commits or PRs (rule of that skill).
- Write PR text in simple English: short sentences, plain words, no idioms.

## `split` - plan to stack

1. **Read the plan** (`backend/.claude/plans/...`, or `$ARGUMENTS`). Read `references/stack-design.md` of the
   `gh-stack` skill too.
2. **Propose the layers** in a table: n, branch (per the convention), scope (one sentence), tests included,
   depends on.
   - Usual order: migration and entity, then port/domain/use case, then resolver/GraphQL (schema and SDK), then e2e.
   - A test goes with the code it covers. The e2e test goes in the layer that exposes the behavior.
   - Avoid a layer that does not compile alone.
3. **Wait for the user to approve.** Create nothing before.
4. **Create and implement**, layer by layer, bottom to top:
   ```bash
   gh stack init <type>/<issue>/<layer-1-slug>
   # code and tests of layer 1, type check, commit
   gh stack add <type>/<issue>/<layer-2-slug>
   # code and tests of layer 2, commit
   ```
   - *Branch already coded*: create the branches at the right commits (`git branch <name> <sha>`), then
     `gh stack init <b1> <b2> <b3>` adopts them. If a commit mixes several layers, say so and propose a split
     by cherry-pick before going further.
5. **Check**: `gh stack view --json`, then `npm run type:check` (from `backend/`) on the top layer.
   Never run `tsc` or `npx tsc`.
6. **Submit** (after the user agrees): `gh stack submit --auto` (draft PRs; add `--open` if asked).
7. **Rewrite the titles and bodies** (they are generated) with `gh pr edit <n> --title ... --body-file ...`:
   - Title: `<type>(<issue>): <layer description>`, same shape as the commit. No `[k/N]` prefix:
     GitHub already shows the stack and links the PRs.
   - Body: the 3 sections of `.github/pull_request_template.md`, for this layer only:
     ```
     ## Description

     - Bullets for this layer only

     ## Related Issue

     - #<issue>

     ## Is this covered by automated tests (unit, integration, e2e)?

     Yes/No + test files of this layer and what they assert, or why not.
     ```
   - Keep the length budget of the git workflow skill: Description at most 6 lines, tests at most 3 lines,
     body under 20 lines. No emoji, no "Stack" section, no closing summary. Do not add the "assign a
     reviewer" link of the template: tell the user.

## `status`

```bash
gh stack view --json
```

Show a table: n, branch, PR, state (OPEN / MERGED / QUEUED), `needsRebase`, CI (`gh pr checks <n>`),
review (`gh pr view <n> --json reviewDecision`). Put what needs an action first.

## `fix [n]` - review fixes

1. **Collect the comments** of PR `n` (or of all PRs of the stack if `n` is missing):
   ```bash
   gh pr view <pr> --comments
   gh api repos/Traace-co/traace/pulls/<pr>/comments
   ```
2. **Go to the layer that owns the code**: `gh stack checkout <branch>` (or `down`). Never the top layer.
3. **Apply the fixes** and commit, one commit per logical subject:
   `refactor(<issue>): address review comments ...`.
4. **Propagate upward**:
   ```bash
   gh stack rebase --upstack
   ```
   On a conflict (exit 3): resolve, `git add`, `gh stack rebase --continue`. Otherwise `--abort`.
5. **Regenerate the artifacts** if the schema or the entities changed (see below). Commit them on the
   layer that owns them.
6. **Run** `npm run type:check` (from `backend/`) on the changed layer and on the top of the stack.
7. **Ask the user, then** `gh stack push`, and `gh stack top` to go back.
8. Do not answer or resolve GitHub threads unless the user asks.

## `sync`

```bash
gh stack sync --prune     # fetch, reconcile, rebase, push, refresh PR state; after the user agrees
```

- Output `Sync aborted` with exit 0 = local and remote diverged. Force nothing. Read
  `references/troubleshooting.md` of the `gh-stack` skill and ask.
- After a rebase on a `main` that moved: regenerate the artifacts (below).
- Generated files in conflict (`schema.gql`, `sdk/generated/graphql/`, `frontend/src/gql/`): take the
  version of `main` (`--ours` during a rebase), then regenerate. Never edit them by hand.

## Regenerate the artifacts (after a rebase or a fix that touches GraphQL or entities)

Same steps as `/rebase`, from `backend/`: test migrations (`npm run _test mikro:migration:up`,
`npm run _test clickhouse:test-schema:up`), `npm run _dev build:graphql-schema`,
`npm run _test test:graphql-codegen`, the frontend codegen if needed (`npm run graphql:codegen` in
`frontend/`), then `npm run type:check`. Commit the regenerated files on the layer that introduces the
schema change.

## `merge`

1. Recall the order: bottom to top, one block from the lowest unmerged PR; all or nothing.
2. Check: approvals, green CI (`gh pr checks`), `needsRebase` false.
3. **Merge strategy**: the repo allows *merge commit* and *squash* (not *rebase*), and the history of `main`
   shows merge commits (`Merge pull request #...`). Propose `--merge` by default, never `--rebase`, and ask
   if the user wants `--squash`.
4. After the user agrees: `gh stack merge <pr> --yes --merge`.
5. Then `gh stack sync --prune`.
