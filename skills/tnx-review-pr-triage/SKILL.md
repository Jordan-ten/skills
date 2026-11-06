---
name: tnx-review-pr-triage
description: Triage a colleague's pull request. Runs /code-review (high by default), the coding-style checklists, the ticket check and the CI status, then writes one markdown report that separates what the agent verified from what a human must still check. Use when the user invokes /tnx-review-pr-triage or says "triage cette PR", "prépare ma review de la PR #N", "qu'est-ce que je dois vérifier à la main sur cette PR". To map a big PR by sub-feature, use tnx-review-plan-pr-review instead.
disable-model-invocation: true
context: fork
allowed-tools: Bash(git *), Bash(gh *), Read, Grep, Glob, Write, Skill
---

# PR triage

Goal: the human reviewer reads only what an agent cannot judge. The agent checks the rest and shows its proof.

Input: a PR number or URL (required). Optional level `low|medium|high|xhigh` for `/code-review`. Default: `high`. Use `max` only if the user asks for it.

## Step 1 — Collect

- `gh pr view <n> --json title,body,headRefName,baseRefName,files,closingIssuesReferences`
- `gh pr diff <n> --name-only`, then the stat. Never load the full diff at once. Read file by file, only what a check needs.
- `gh pr checks <n>`: CI status, including the OpenGrep and type checks.
- Linked issue: `gh issue view <number>`. No linked issue → say so in the report.
- Skip generated files (`schema.gql`, `generated/`, `gql/`, `package-lock.json`): name them, do not read them.

## Step 2 — Agent checks

Run all of these. Each one yields findings **and** a line of proof for the "verified" block.

1. **Bugs and cleanups**: invoke the `code-review` skill with the level and the PR number, e.g. `high <n>`. Never pass `--comment` or `--fix`.
2. **Focused controls** (same as `tnx-review-review-changes`), on the hunks of the PR. Skip what `/code-review` already reported:
   - **Bug**: wrong logic, off-by-one, wrong condition, unhandled edge case.
   - **Security**: injection, exposed secret, missing auth check, unsafe data handling.
   - **Logic**: race condition, missing null check, wrong assumption, broken invariant.
   - **Improvement**: missing error handling, only if clearly worth fixing.
   - **Atomicity**: one user action done as several independent mutations or endpoints, especially in loops or `Promise.all`. Look for partial failure, ordering dependency, validation against an intermediate state, optimistic cache rollback gap, missing transaction, broken final-state invariant. Report it as `Logic`, or as `Bug` if data is lost or invalid state is persisted.
3. **Coding-style rules**: the skill runs from `backend/` or `frontend/`. A PR can touch both. Check each touched package with its own rules.
   - **Backend files**: read the matching `backend/docs/coding-style/*.md` files and tick each "Review checklist" item against the diff. Mapping:
     - `*.usecase.ts`, `*.service.ts` → `use-cases.md`, `architecture.md`, `permissions.md`, `errors.md`
     - `*.resolver.ts`, `*.entity.ts` → `resolvers.md`, `graphql.md`, `dataloaders.md`
     - `*.repository.ts`, ports, adapters → `repositories.md`
     - `migrations/` → `migrations.md`
     - Always: `naming.md`, `typescript.md`
   - **Frontend files**: read `frontend/AGENTS.md` (sections "Critical Frontend Directives", "Coding Style", "Frontend Architecture Patterns", "File Naming Conventions", "Testing Guidelines", "Performance") and check each rule against the diff. Also read any `frontend/docs/` file that matches the touched area.
4. **Generated artifacts**:
   - Backend: schema and SDK files changed when GraphQL changed. `DOCS.md` changed when a `*.doc.md` changed. Migration and entity `@Check` agree.
   - Frontend: `src/gql/` changed when a `*.graphql.ts` changed. i18n types changed when a translation file changed.
5. **Tests**: list the new public methods and the new behavior. For each, name the test that covers it, or write "no test found". Do not run tests.
6. **Ticket conformance**: for each acceptance criterion or scenario of the issue, point to the code or test that covers it, or write "not found in the diff".
7. **CI**: copy the status of each check. A red check is a finding, not a verdict on the code.

Never run tests, the app or the e2e. Say what you did not check.

## Step 3 — Human checks

Pick at most **5** points, ranked by risk. Each one needs a precise question and a `file:line`. Look in these areas, in this order:

1. **Production risk**: migration on a big table, backfill, lock, behavior on existing data.
2. **Business intent**: does the behavior match what the product wants, beyond what the ticket says?
3. **Permission semantics**: is the check present (agent can see it) and is it the right role (only a human knows)?
4. **Design decisions**: new aggregate, new service, boundary between use case and service, an abstraction that may not pay off.
5. **Domain vocabulary**: a new term in names, API fields or user-facing strings.
6. **Test value**: do the tests cover a real business scenario, or only the code?
7. **Trade-offs**: performance, accepted debt, scope of the PR.

Also list what the agent **could not judge** (for example "migration on table X: volume not known").

If nothing needs a human, say so. Do not fill the list.

## Step 4 — Write the report

Path: `.claude/plans/review/<pr-number>.md`, relative to the current working directory (`backend/` or `frontend/`). If the working directory is the repo root, use the package with most touched files. Create the folder if needed. Overwrite an older report of the same PR. Both packages git-ignore `.claude/plans`.

**Links.** Every `file:line` in the report, in all blocks (also "Vérifié par l'agent"), is a clickable markdown link `[file:line](url)`. Get the data with `gh pr view <n> --json headRefOid,url`. Never guess a line number: read it in the file at `headRefOid` with `gh api -H 'Accept: application/vnd.github.raw' 'repos/<owner>/<repo>/contents/<path>?ref=<headRefOid>'`.
- Line changed by the PR: link to the PR diff, `<PR url>/files#diff-<sha256 of the path>R<line>` (a range: `R<start>-R<end>`). Hash: `printf %s '<path>' | sha256sum | cut -d' ' -f1`.
- Line outside the diff, or file not in the PR: `https://github.com/<owner>/<repo>/blob/<headRefOid>/<path>#L<line>`.
- A CI check: link to its run URL from `gh pr checks`.

Write the report in French (the reader is French). Use simple, short sentences. Keep code identifiers, file names and PR titles as they are. Use exactly this structure:

```markdown
# PR #<n> — <title>

Branche `<head>` → `<base>` · Niveau : <level> · Ticket : #<m> ou aucun · CI : <verte|rouge|en cours> · État : <OPEN|MERGED|CLOSED>

## Verdict
<2 phrases max. Peut-on approuver après les points humains ? Findings bloquants ?>

## À vérifier par un humain (par risque décroissant)
1. **<domaine>** [file:line](lien) — <question précise>
...

## Findings à corriger
1. **<Bug|Sécurité|Logique|Amélioration|Règle de style|Test|Artefact>** [file:line](lien) — <une ligne>. Source : <code-review|contrôles ciblés|nom de la checklist|CI>. Ordre : Sécurité > Bug > Logique > Amélioration > le reste.
...
(ou "Aucun")

## Vérifié par l'agent
- <contrôle> — <preuve : ce qui a été lu ou comparé>
...

## Non vérifié
- <ce que l'agent n'a pas pu juger, et pourquoi>

## Fichiers ignorés
- <fichiers générés ou bruit, par nom>
```

## Step 5 — Reply in the chat

Reply in French. Give only: the verdict, the path of the report, and the human points (titles only). Never post anything on the PR. If the user wants comments on the PR, they ask for it, and each comment is shown for approval first.

## Constraints

- Do not repeat the same issue in two blocks. A finding the agent can fix goes in "Findings à corriger", not in "À vérifier par un humain".
- A "Vérifié par l'agent" line needs proof. No proof → it goes in "Non vérifié".
- No style nitpicks outside the coding-style rules.
- Do not use the word "Traace" for the product. Use Tennaxia.
