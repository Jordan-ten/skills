---
name: deployment-instructions
description: Slash-only. Use only when the user explicitly invokes /deployment-instructions to deploy main to production or demo. Never trigger from natural-language requests.
disable-model-invocation: true
argument-hint: "[production|demo]"
allowed-tools: Bash(gh pr create:*), Bash(gh pr list:*), Bash(gh pr view:*), Bash(gh run list:*), Bash(gh run view:*), mcp__claude_ai_Datadog__search_datadog_logs
---

# Deploy

Guide a deployment of `main` to `production` or `demo`, in four steps: checklist, pull request,
monitoring, closing.

## Target

`$ARGUMENTS` is `production` (default) or `demo`. Treat `prod` as `production`. Any other value:
stop and ask.

## Hard rules

Only the user merges and pushes. Merging the deploy PR starts the deployment.

- Never run `gh pr merge`, and never merge by the API or any other command.
- Never run `git push` to `production` or `demo`, even with `-f`. The user saying that force push is
  allowed, or that branch protection is off, is not a request to push. Wait for an explicit request.
- Never say the PR is ready to merge, and never ask the user to merge it, before both conditions are
  met (see Step 2): the CI pipeline has passed, and a reviewer has approved the PR. A missing
  condition means no merge, even if the user is in a hurry.
- Never cancel or re-run a deploy GitHub Actions run without an explicit request.
- For conflicts: explain the procedure at the end of this file and give the commands. Do not run them.

## Step 1 — Checklist

Ask the user to confirm each point. Do not go on before all are confirmed.

- [ ] `#tech-esg-deploy-sync` and `#tech-esg-code-review` are set to 🔴 `Freeze merge on staging except fixes`.
- [ ] The [list of untested or failing issues](https://github.com/orgs/Traace-co/projects/2/views/48) is empty.
- [ ] `demo` only: the "Demo" calendar shows no demo in progress.

## Step 2 — Open the pull request

Check first that no deploy PR is already open:

```bash
gh pr list --base "$TARGET" --head main --state open
```

If one is open, show it and use it. Otherwise create it. The heredoc delimiter is not quoted, so
`$TARGET` is expanded in the body.

```bash
gh pr create --base "$TARGET" --head main \
  --title "Deploy main to $TARGET" \
  --body "$(cat <<BODY
## Description
- Deploy the latest \`main\` to \`$TARGET\`

## Related Issue
Deployment procedure. All issues are tested and validated.

## Is this covered by automated tests
Yes. GitHub Actions CI runs on \`main\`.
BODY
)"
```

Show the PR link.

### Wait for CI and a reviewer approval

A release PR is never merged unless the CI pipeline has passed and a reviewer has approved it. Ask a
reviewer to review the PR, then check both conditions:

```bash
gh pr view <number> --json reviewDecision,reviews,statusCheckRollup,headRefOid
```

CI is passed only if **every** check in `statusCheckRollup` is `SUCCESS` (or `SKIPPED`, or `NEUTRAL`).
- A check still `PENDING` or `IN_PROGRESS`: stop and wait.
- A check `FAILURE`, `CANCELLED` or `TIMED_OUT`: stop. Show the failing checks with their links. Do not
  re-run them (see the hard rules).
- No check at all: stop. The pipeline did not start, so CI has not passed.

The review is valid only if `reviewDecision` is `APPROVED`.
- Any other value (`REVIEW_REQUIRED`, `CHANGES_REQUESTED`, empty): stop.
- An approval on an older commit than `headRefOid` is outdated: ask for a new review.
- Do not accept "the reviewer said OK in Slack". The approval must be on the PR.

If a condition is missing, tell the user which one and wait. Check again when the user asks.

When both are met, say so, with the reviewer's name. Then ask the user to merge the PR and to tell
you when it is done.

Remind the user to post in `#tech-esg-deploy-sync`: deployment in progress, with the link to the
[GitHub Actions run](https://github.com/Traace-co/traace/actions).

## Step 3 — Monitoring

Wait until the user says the deployment succeeded. Check it if needed with
`gh run list --branch "$TARGET" --limit 3`.

Search Datadog for the last 30 minutes with the Datadog MCP. Use `env:production` for production.
For `demo`, use the `env` value of the demo logs (look at one log first, do not guess).

```
env:<env> status:(error OR critical OR alert OR emergency)
```

Read the results:

- Ignore Node.js warnings (`UnsupportedWarning`).
- Report GraphQL schema errors (field not found). Often a browser cache: see if they continue.
- Report unexpected 500 errors.
- Say for each error if it is old (before the deployment time) or new.

End with one verdict: ✅ nothing unusual, 🟡 points to watch, or 🔴 urgent action needed.

## Step 4 — Closing

Remind the user to:

- [ ] Test the app on the target environment (login and navigation).
- [ ] Post in `#tech-esg-deploy-sync`: deployment succeeded ✅.
- [ ] Set `#tech-esg-deploy-sync` and `#tech-esg-code-review` back to 🟢 `OK to merge on staging`.

## If the deployment fails

- Notify `#tech-esg-deploy-sync`.
- Critical case: SQL migration succeeded but backend or frontend failed. Alert the team with `@here` now.
- Usual causes:
  - **Migration timeout**: run it on AlloyDB and make it idempotent.
  - **Deadlock**: retry, split the migration, or run it in the evening.
  - **Random GitHub Action failure**: re-run the failed jobs (the user does it).

## If `production` or `demo` has conflicts with `main`

Do not run these commands. Give them to the user (see the hard rules).

```bash
# 1. GitHub Settings > Branches: "Do not allow bypassing" off, "Allow force pushes" on
git fetch origin
git push -f origin origin/main:production   # or origin/main:demo
# 2. Turn the branch protections back on
```
