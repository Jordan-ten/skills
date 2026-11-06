# Le rapport

Un seul message, à la fin du run. Rien n'est posté sur l'issue.

## Verdicts

| Mark | Meaning |
|---|---|
| `PASS` | Run and observed. Evidence given. |
| `FAIL` | Run and observed to be wrong. Evidence given. |
| `PASS (test)` | Not run in the browser. An existing automated test covers it and was run green. Name the file. |
| `BY HAND` | Not run. Needs a human. Say what the human has to do. |
| `NOT TESTABLE` | Not run. No case in the local data, and it was not created (user skipped it, or creating it failed). Say what is missing and why. |

Ne jamais utiliser `PASS` pour un scénario qui a seulement été lu dans le code.

## Forme

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

## Règles du rapport

- La colonne scénario garde les mots de l'auteur. Le lecteur doit reconnaître sa propre checklist.
- Une ligne de preuve par scénario, pas une transcription.
- Compter les scénarios qui n'ont pas été exécutés. Un run où 4 scénarios sur 6 sont `BY HAND` n'est pas
  un ticket testé, et le rapport doit le dire en une phrase sous le tableau.
- Quand un scénario échoue, donner précisément le cas qui échoue : l'entrée, ce qui était attendu, ce
  qui s'est passé.
