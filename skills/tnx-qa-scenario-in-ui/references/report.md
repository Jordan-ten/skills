# The report

One message, at the end of the run. Nothing is posted on the issue.

## Verdicts

| Mark | Meaning |
|---|---|
| `PASS` | Run and observed. Evidence given. |
| `FAIL` | Run and observed to be wrong. Evidence given. |
| `PASS (test)` | Not run in the browser. An existing automated test covers it and was run green. Name the file. |
| `BY HAND` | Not run. Needs a human. Say what the human has to do. |
| `NOT TESTABLE` | Not run. No case in the local data, and it was not created (user skipped it, or creating it failed). Say what is missing and why. |

Never use `PASS` for a scenario that was only read in the code.

## Shape

```markdown
# <issue number> — <issue title>

Branch `<branch>`, commit `<sha>`. App: <URL>. Browser: <browser>.

| # | Scenario | Verdict | How it was checked |
|---|---|---|---|
| 1 | <the author's words, shortened> | PASS | <one line of evidence> |
| 2 | ... | PASS (test) | `<file>` — 3 tests green |
| 3 | ... | BY HAND | <what the human has to do> |

## Data created for this run
<Only when step 2 created records. One line each: what it is, its id, and the delete mutation that
removes it. Say "none" when the run created nothing.>

## Details
<One short block per scenario that is not a plain PASS: what was done, what was seen,
and the screenshot when there is one.>

## Outside the scenarios
<Anything noticed that the issue did not ask for: a neighbouring case that looks wrong,
a console error, a slow screen. One line each. Say it is an observation, not a defect of
this issue, and suggest its own issue when it deserves one.>
```

## Rules for the report

- The scenario column keeps the author's words. The reader has to recognise their own checklist.
- One line of evidence per scenario, not a transcript.
- Count the scenarios that were not run. A run where 4 scenarios out of 6 are `BY HAND` is not a
  tested ticket, and the report must say so in one sentence under the table.
- When a scenario fails, give the failing case precisely: input, what was expected, what happened.
