# Where the creation recipes are already written

`frontend/tests/fixtures/` holds the fixtures of the e2e tests. Each one creates real records through
the same API. They are the reference for **what a creation needs first**, which is the part a schema
never tells you.

Read the fixture before composing your own sequence. Do not import it, do not run it: take the
mutations and what each one needs, and send them with `scripts/graphql.sh`.

## Find the right file

```bash
ls frontend/tests/fixtures/ | grep -i <domain>
grep -rn "mutation Create" frontend/tests/fixtures/<file>.ts
```

The files are named after the domain (`<domain>Fixtures.ts`). Do not rely on a list: it would age.

## Read a fixture as a recipe

A fixture file gives three things:

| What | How it shows |
|---|---|
| The mutations and their input shape | The GraphQL strings in the file. |
| What it needs first | The lookups and arguments of the `create*` helpers. |
| The cleanup | The matching `delete*` helpers. |

Example, `campaignFixtures.ts`. What the code shows, and nothing more:

- `createCampaignFixture` first looks up a **business domain id**, then creates the campaign for the
  current year.
- `launchCampaignFixture` is the `scheduleCampaign` mutation, with a start date and two end dates.
- `createCampaignTasksForQuestionnaire` needs a campaign id, a **published questionnaire found by name**
  and a list of contributing entity ids, then bulk-creates the tasks.

The fixtures do not prove that these steps must run in this order. They show what each one needs. When
the order matters for your case, check it by reading the screen after each call.

## Rules of thumb

- A `create*Fixture` that takes an id as an argument tells you what has to exist first.
- A fixture with `unique...Name()` creates names that cannot clash. Do the same: prefix what you
  create so the user can tell your records from theirs.
- When a fixture does something the API cannot (waiting for a job, reading a token), the case needs
  that step too. Say so instead of creating a half record.
