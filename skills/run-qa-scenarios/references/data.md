# When a scenario has no data

A scenario is often blocked by one missing record, not by the feature. Do not drop it, and do not
change what exists to make it fit. Say what is missing, let the user decide, and delegate the
creation.

## 1. Say exactly what is missing

One line per record, in the words of the domain, with the property that matters:

```
Scenario 2 (long label is readable in full)
  missing: one group task whose perimeter label is ~300 characters
  have:    "Division France" (15 characters), 4 sites
```

Never write "missing test data". The user has to recognise the record without reading the code.

Check first that the case is really absent: it is often there under another name.

## 2. Ask, with three ways out

One `AskUserQuestion` for the whole plan, not one per record. Say which database would be written to
(the backend on port 3000 is the dev one in a dev session).

| Option | What happens |
|---|---|
| `Generate the data` | Follow the `create-local-data` skill, then run the scenarios. |
| `I create it myself` | Give the summary, then wait. Nothing is written. |
| `Skip these scenarios` | They go to the report as `NOT TESTABLE`, with what was missing. |

Default to proposing, never to doing. Writing into the user's database without a yes is the one thing
this skill must not do.

## 3. Creating it

The `create-local-data` skill owns this: it finds the mutation, knows the order of the calls,
and sends them through the backend API with a self-signed offline-auth token. Do not re-invent the
transport here, and never create data with SQL.

## 4. After creating

- Run the scenarios that were blocked.
- List every record created in the report, with its id and name.
- Offer the delete mutations at the end of the run. Do not delete on your own: the user may want to
  keep the case for a later test.
- A record that could not be created is a `NOT TESTABLE` scenario with the error, not a silent skip.
