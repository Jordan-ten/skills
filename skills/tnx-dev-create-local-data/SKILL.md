---
name: tnx-dev-create-local-data
description: >
  Creates records in a local environment by calling the backend GraphQL API, with a self-signed
  offline-auth token (no login, no file written, no raw SQL). Use when a local case is missing and
  has to be created to see a screen, reproduce a bug, prepare a demo or unblock a test: "crée-moi
  une campagne en local", "il me faut une tâche de groupe", "génère les données pour reproduire ce
  bug", "seed local data", or /tnx-dev-create-local-data. Also used by other skills that need a
  record before they can go on.
allowed-tools: Bash(bash .claude/skills/tnx-dev-create-local-data/scripts/*), Read, Grep, Glob, AskUserQuestion
---

# Create local data

Creates what a local environment is missing, through the API the product itself uses. The backend
validates every call, so the records are coherent — which raw SQL never guarantees.

## Rules

- **Never write with SQL.** The `sql-query` skill reads state. Writing goes through the API, so the
  business rules, the defaults and the events are applied.
- **Say which database you are writing to, before writing.** The backend on port 3000 is the dev one
  in a dev session, the e2e one in an e2e session. Same port, different data. Name it every time.
- **Ask before the first write.** Show what will be created, in the words of the domain, then one
  `AskUserQuestion`. A read to check the ground needs no question. When another skill already showed
  the same plan and got a yes, do not ask a second time.
- **Report the ids.** Every created record is listed back with its id and name, so the user can find
  it or remove it.
- **Offer the cleanup, never run it on its own.** The user often wants to keep the case.

## The call

```bash
GQL_EMAIL=<dev user email> bash .claude/skills/tnx-dev-create-local-data/scripts/graphql.sh \
  --variables '{"input":{...}}' <<'GQL'
mutation CreateX($input: XInput!) { createX(input: $input) { id name } }
GQL
```

The script signs the same offline-auth token as `frontend/tests/fixtures/graphql.ts`, so it needs no
login. It requires the backend to run with `OFFLINE_AUTH=true`.

| Env | Default | When to change it |
|---|---|---|
| `GQL_EMAIL` | none, required | The user whose rights the call runs with. |
| `GQL_ORG` | `1` | Another organization. |
| `GQL_ENDPOINT` | `http://localhost:3000/graphql` | Another local backend. |
| `GQL_ADMIN` | unset | `1` for a platform-admin (sudo mode) operation, such as creating an organization. It drops the organization header. |

An error comes back as `{"errors":[...]}` with HTTP 200. The script prints the body and exits `1` when
it holds an error, so a failed creation cannot pass for a success. It talks to local hosts only
(`localhost`, `127.0.0.1`) and refuses any other endpoint.

## Method

1. **Check what already exists.** The case is often there under another name. Query before creating.
2. **Find the mutation**: `grep -n "createX" backend/src/schema.gql`, then read its input type the
   same way. Never read `schema.gql` whole, it is over 10 000 lines.
3. **Find the order of the calls.** One mutation is rarely enough: a campaign has to be created, then
   launched, then given its tasks. That sequence is already written in the e2e fixtures. Read the
   matching `frontend/tests/fixtures/*.ts` before composing your own — see `references/recipes.md`.
4. **Create, then verify** by reading the record back, or by opening the screen.
5. **List the ids** and offer the delete mutations.

## When the API has no mutation

Some setup lives outside GraphQL: `npm run _dev command <name>` (see `backend/command.ts`), for
example the initial setup of an organization. Look there before concluding that a case cannot be
created. Read the command's code first, and ask before running it: a backend command can do more than
create a record. It is not pre-approved for this reason.

If neither exists, say the case cannot be created through a supported path. Do not fall back to SQL.
