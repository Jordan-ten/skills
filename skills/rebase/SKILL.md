---
name: rebase
description: Rebase the current branch on a target branch (default main). Resolves conflicts in generated files, applies migrations, regenerates the GraphQL schema and SDK types, checks the types, runs the related tests, then force-pushes. Use when the user invokes /rebase, says "rebase sur main", "rebase on main", "rebase la branche", or wants to bring a feature branch up to date.
disable-model-invocation: true
allowed-tools: Bash(git *), Bash(gh *), Bash(docker compose *), Bash(npm run *), Bash(npx dotenvx run *), Read, Edit, Grep, Glob, AskUserQuestion
---

# Rebase

Run all commands from `backend/` unless a step says otherwise. `TARGET` is the argument, or `main`.

## 1. Check the branch

```bash
git branch --show-current
git status --short
```

Rebase the branch the user named. If the current branch is not the one they expect, stop and ask.
Do not rebase with uncommitted changes to tracked files.

## 2. Rebase

```bash
git pull --rebase origin $TARGET
```

If the command fails with `Permission denied (publickey)`, retry a few times: the SSH agent can fail
at random. Do not change the remote URL.

## 3. Resolve conflicts

Generated files: take the version of the target branch. During a rebase, that is `--ours`.

Git reads paths from the current folder, so run this step from the repo root.

```bash
cd "$(git rev-parse --show-toplevel)"
git checkout --ours backend/src/schema.gql backend/sdk/generated/graphql/ frontend/src/gql/ 2>/dev/null || true
git add backend/src/schema.gql backend/sdk/generated/graphql/ frontend/src/gql/ 2>/dev/null || true
```

Business code: resolve by hand, then `git add`. Never edit a generated file by hand.

```bash
git rebase --continue
```

Repeat until the rebase ends, then go back to `backend/`.

## 4. Pick the steps from the diff

```bash
git diff origin/$TARGET --name-only
```

If every changed file is a doc or a skill (`.claude/`, `*.md`), skip to step 10.
Run the steps below only for what changed:

- `migrations/` or an entity changed: steps 5 to 6.
- A resolver, an input or an entity with GraphQL decorators changed: steps 7 to 8.
- Any `.ts` file changed: steps 9 to 10.

## 5. Docker (test environment)

```bash
docker compose -f docker-compose.yml --env-file .test.env -p backend_test ps
docker compose -f docker-compose.yml --env-file .test.env -p backend_test up -d   # only if stopped
```

## 6. Migrations

```bash
npm run _test mikro:migration:up
npm run _test clickhouse:test-schema:up
```

## 7. GraphQL schema

```bash
npm run _dev build:graphql-schema
```

## 8. GraphQL types

```bash
npm run _test test:graphql-codegen
cd ../frontend && npm run graphql:codegen && cd ../backend
```

## 9. Type check

```bash
npm run type:check
```

Never run `tsc` or `npx tsc`.

## 10. Regressions from the target branch

List the commits of the target branch that touch files of this branch. `git diff --name-only` prints
paths from the repo root, so run this step from the repo root.

```bash
cd "$(git rev-parse --show-toplevel)"
BRANCH_FILES=$(mktemp)
git diff origin/$TARGET...HEAD --name-only > "$BRANCH_FILES"
git log --oneline ORIG_HEAD..origin/$TARGET -- $(tr '\n' ' ' < "$BRANCH_FILES")
rm "$BRANCH_FILES"
cd backend
```

For each commit, run `git show <sha> -- <file>`. Check that this branch still uses the right APIs:
a renamed or removed method, a new required parameter, an import that no longer exists.
Fix what is broken in a separate commit: `chore(<issue>): adapt to <change> from #<PR>`.

## 11. Related tests

```bash
FILES=$(git diff origin/$TARGET --name-only --relative | tr '\n' ' ')
npx dotenvx run -f .test.env -- npx cross-env TESTING=true vitest related --run --passWithNoTests --config vitest-ut.config.ts $FILES
npx dotenvx run -f .test.env -- npx cross-env TESTING=true vitest related --run --passWithNoTests --config vitest-itg.config.ts $FILES
```

`--relative` gives paths from `backend/`. `vitest related` replaces the Jest option `--findRelatedTests`.

Never start the test server and never run e2e tests. If the schema changed, give the user the e2e
command to run (see `backend/AGENTS.md`).

## 12. Push

```bash
git push --force-with-lease
```

Never use `--force`. Report the result and anything skipped.
