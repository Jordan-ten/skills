---
name: tnx-audit-list-sonarqube-issues
description: >
  List the open SonarQube issues of the backend and/or frontend on main, from the self-hosted
  SonarQube server, through an IAP tunnel and curl. Read-only. Use when the user asks to "list sonar
  issues", "what does sonarqube report", or runs /tnx-audit-list-sonarqube-issues [backend|frontend].
---

# List SonarQube Issues

CI scans only `main`, so the issues show `main`, not the current branch.

Rules:

- Read-only: call only `GET` on `/api/system/status` and `/api/issues/search`.
- Never print `$SONAR_TOKEN`.
- Do not use `https://sonar.tennaxia.com` from curl: IAP blocks it.

Projects: `backend` or `frontend` from the argument. No argument: both.

## 1. Check the token

```bash
[ -n "$SONAR_TOKEN" ] && echo set || echo missing
```

If missing, stop and tell the user:

1. Log in to https://sonar.tennaxia.com.
2. Open the user preferences (top left), then the Security tab.
3. Create a User Token named `tennaxia-esg-<email name>` (e.g. `tennaxia-esg-mleprince`).
4. Add `export SONAR_TOKEN=<token>` at the end of `~/.zshrc`.
5. Restart Claude Code.

## 2. Check the tunnel

```bash
curl -s --max-time 5 localhost:39000/api/system/status
```

If not `"status":"UP"`, ask the user if you can start the tunnel. If yes, run it with
`run_in_background: true`, then wait for it:

```bash
gcloud compute start-iap-tunnel sonarqube 9000 --local-host-port=localhost:39000 \
  --zone=europe-west9-b --project=tennaxia-esg-ci-tools
```

```bash
curl -s --retry 15 --retry-connrefused --retry-delay 1 localhost:39000/api/system/status
```

On a permission error, the user needs `roles/iap.tunnelResourceAccessor` on the VM.

## 3. Fetch the issues

For each project (`backend`, `frontend`):

```bash
P=backend
rm -f /tmp/sonar-$P-p*.json
curl -s -u "$SONAR_TOKEN:" \
  "http://localhost:39000/api/issues/search?components=tennaxia-esg-$P&resolved=false&ps=500&p=1" \
  > /tmp/sonar-$P-p1.json
jq '{total: .paging.total, errors}' /tmp/sonar-$P-p1.json
```

- 401: token wrong or expired. Stop.
- More than 500 issues: fetch `p=2`, `p=3`, ...
- Optional filters: `severities=BLOCKER,CRITICAL`, `types=BUG,VULNERABILITY`, `files=src/foo.ts`.

## 4. Show the result

```bash
jq -r '.issues[] | [.severity, .type, (.component | sub("^[^:]+:"; "")) + ":" + ((.line // "-") | tostring), .message, .rule] | @tsv' /tmp/sonar-$P-p*.json
```

Per project: one line with the total and counts by severity, then a table sorted by severity
(severity, type, `file:line`, message, rule). Max 50 rows; say how many are hidden.
