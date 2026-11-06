# Build the scenario list

## Where the scenarios come from

Read these parts of the issue, in this order:

1. **How to test** — the checklist written by the author. Each box is one scenario.
2. **Scenarios** (Given / When / Then) — when the issue has them.
3. **Reproduction Steps** — for a bug, the steps are the scenario: the bug must be gone.

**If the issue has none of these, stop the run.** Do not write the scenarios yourself, and do not
infer them from the code or the diff. Invented scenarios test what the code does, not what the issue
asked for, so they always pass and prove nothing. Tell the user the issue has nothing to test
against, and that the scenarios have to be defined in the issue first. The `generate-ticket-scenarios`
skill can write them, but that is a separate decision, taken on the issue, before this run.

Keep the author's words. Do not rename a scenario to match what the code does: the gap between the
two is exactly what the test is looking for.

## Say how each scenario will be checked

For every scenario, pick one:

| How | When |
|---|---|
| `browser` | The local dev data has a case for it. |
| `automated test` | An existing unit test (`*.test.tsx`) covers it. Name the file; you will run it with `npx vitest run <file>`. An e2e spec is named in the report but **not run**: it would write into the database of the session. |
| `by hand` | It needs a role, a tenant, or an action the run must not perform (sending a mail, a long import, anything that reaches a third party). |
| `not testable` | The local data has no case for it. Say what is missing, then follow `data.md`: the case can often be created. |

To find an existing test, grep the component or use case name under `frontend/src/**/*.test.tsx`
and `frontend/tests/**/*.spec.ts`.

A scenario that needs a second user (a contributor, a validator) is usually `by hand` unless the dev
data already holds that user: the run must not create accounts.

## Check the data before promising a browser run

Before marking a scenario `browser`, confirm the case exists. Example: a scenario about a group task
needs a task whose `__typename` is the group one, not any task. Open the list screen and look, or
read the GraphQL response through `mcp__chrome-devtools__list_network_requests`.

A scenario promised as `browser` that turns out to have no data goes to step 2 (`data.md`), not
straight to the report. Do not silently drop it.
