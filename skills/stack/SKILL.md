---
name: stack
description: Transforme un plan validé en stack de pull requests (une PR par couche), puis gère la stack (status, corrections de review sur la bonne couche, rebase et sync). Construit sur le skill officiel gh-stack. À utiliser quand l'utilisateur lance /stack, dit "split the plan into a stack", "stack de PR", "découpe le plan en stack", "corrige les retours de review sur la stack", "sync la stack", ou veut des PR dépendantes. (Turn a validated plan into a stack of pull requests, then manage the stack.)
disable-model-invocation: true
allowed-tools: Bash(git *), Bash(gh *), Bash(npm run *), Read, Edit, Write, Glob, Grep, AskUserQuestion
---

# Stack

Plan validé, puis une stack de PR, puis corrections de review, puis rebase et sync.

**Toute la mécanique git et GitHub passe par le skill `gh-stack`** (commandes non interactives, codes de
sortie, conflits). Ce skill n'ajoute que le workflow Tennaxia : le découpage depuis un plan, le format
des PR, la régénération des artefacts, les règles de sécurité.

## Arguments

`$ARGUMENTS` est une sous-commande : `split [plan]`, `status`, `fix [n]`, `sync`, `merge`. Sans argument : `status`.

## Prérequis (à vérifier une fois)

```bash
gh --version        # >= 2.90
git --version       # >= 2.36
gh extension list   # gh-stack must be listed
gh stack view --json 2>&1 | head -20   # exit 9 = stacked PRs are not enabled on the repo: tell the user
```

Si l'extension ou le skill `gh-stack` manque, donner ces commandes à l'utilisateur. Ne pas les lancer.
Cela garde les deux à jour, ce qu'une copie dans le repo ne ferait pas.

```bash
gh extension install github/gh-stack
gh skill install github/gh-stack gh-stack --agent claude-code --scope user
```

Mettre à jour plus tard avec `gh extension upgrade gh-stack` et `gh skill update`.

## Règles pour toutes les sous-commandes

- N'utiliser que les formes non interactives du skill `gh-stack` : `view --json`, `submit --auto`,
  `init <branch>`, `add <branch>`, `checkout <target>`. Jamais `gh stack modify`.
- **Demander à l'utilisateur avant** `gh stack push`, `submit`, `sync` (il pousse) et `merge`.
- Ne jamais committer sur la couche du haut un changement qui appartient à une couche plus basse.
- Une couche = une préoccupation, décrite en une phrase. Chaque couche doit passer ses tests seule, sans
  dépendre d'une couche au-dessus.
- Les branches, commits et PR suivent `tnx-dev-standards-dev-and-git-workflow`. Le lire avant `split`.
  - Branche : `<feature|bugfix|chore>/<issue>/<short-description>`, une description différente par couche
    (`feature/23773/emission-factor-entity`, `feature/23773/update-version-usecase`). Pas de préfixe numérique.
    Prendre le type et l'issue depuis la branche courante.
  - Commit : `<type>(<issue>): short description`, **un commit par couche**. Les corrections de review sont des commits séparés.
  - Pas de ligne `Co-Authored-By` ni d'attribution Claude dans les commits ou les PR (règle de ce skill).
- Écrire le texte des PR en anglais simple : phrases courtes, mots simples, pas d'idiomes.

## `split` - du plan à la stack

1. **Lire le plan** (`$ARGUMENTS`, sinon `.claude/plans/ticket/<issue>-*.md` dans le répertoire de travail, sinon
   `backend/.claude/plans/...`). Lire aussi `references/stack-design.md` du skill `gh-stack`.
   Si le plan a une section `## Pull requests` (écrite par `/feature-implementation-workflow`), l'utiliser comme proposition :
   la montrer, sauter l'étape 2, et aller à l'étape 3.
   Si le front matter a un `sibling_plan`, le lire aussi et montrer les deux tableaux comme une seule stack,
   couches backend d'abord, couches frontend au-dessus.
2. **Proposer les couches** dans un tableau : n, branche (selon la convention), périmètre (une phrase), tests inclus,
   dépend de. Les couches front vont au-dessus des couches back dont elles ont besoin (schéma GraphQL, SDK, codegen).
   - Ordre habituel : migration et entité, puis port/domaine/use case, puis resolver/GraphQL (schéma et SDK), puis e2e.
   - Un test va avec le code qu'il couvre. Le test e2e va dans la couche qui expose le comportement.
   - Éviter une couche qui ne compile pas seule.
3. **Attendre l'accord de l'utilisateur.** Ne rien créer avant.
4. **Créer et implémenter**, couche par couche, de bas en haut :
   ```bash
   gh stack init <type>/<issue>/<layer-1-slug>
   # code and tests of layer 1, type check, commit
   gh stack add <type>/<issue>/<layer-2-slug>
   # code and tests of layer 2, commit
   ```
   - *Branche déjà codée* : créer les branches aux bons commits (`git branch <name> <sha>`), puis
     `gh stack init <b1> <b2> <b3>` les adopte. Si un commit mélange plusieurs couches, le dire et proposer un découpage
     par cherry-pick avant d'aller plus loin.
5. **Vérifier** : `gh stack view --json`, puis `npm run type:check` (depuis `backend/`) sur la couche du haut.
   Ne jamais lancer `tsc` ni `npx tsc`.
6. **Soumettre** (après l'accord de l'utilisateur) : `gh stack submit --auto` (PR en brouillon ; ajouter `--open` si demandé).
7. **Réécrire les titres et les corps** (ils sont générés) avec `gh pr edit <n> --title ... --body-file ...` :
   - Titre : `<type>(<issue>): <layer description>`, même forme que le commit. Pas de préfixe `[k/N]` :
     GitHub montre déjà la stack et lie les PR.
   - Corps : les 3 sections de `.github/pull_request_template.md`, pour cette couche seulement :
     ```
     ## Description

     - Bullets for this layer only

     ## Related Issue

     - #<issue>

     ## Is this covered by automated tests (unit, integration, e2e)?

     Yes/No + test files of this layer and what they assert, or why not.
     ```
   - Garder le budget de longueur du skill de workflow git : Description 6 lignes au maximum, tests 3 lignes au maximum,
     corps sous 20 lignes. Pas d'emoji, pas de section "Stack", pas de résumé final. Ne pas ajouter le lien
     "assign a reviewer" du template : le dire à l'utilisateur.

## `status`

```bash
gh stack view --json
```

Montrer un tableau : n, branche, PR, état (OPEN / MERGED / QUEUED), `needsRebase`, CI (`gh pr checks <n>`),
review (`gh pr view <n> --json reviewDecision`). Mettre en premier ce qui demande une action.

## `fix [n]` - corrections de review

1. **Collecter les commentaires** de la PR `n` (ou de toutes les PR de la stack si `n` manque) :
   ```bash
   gh pr view <pr> --comments
   gh api repos/Traace-co/traace/pulls/<pr>/comments
   ```
2. **Aller à la couche qui possède le code** : `gh stack checkout <branch>` (ou `down`). Jamais la couche du haut.
3. **Appliquer les corrections** et committer, un commit par sujet logique :
   `refactor(<issue>): address review comments ...`.
4. **Propager vers le haut** :
   ```bash
   gh stack rebase --upstack
   ```
   En cas de conflit (exit 3) : résoudre, `git add`, `gh stack rebase --continue`. Sinon `--abort`.
5. **Régénérer les artefacts** si le schéma ou les entités ont changé (voir plus bas). Les committer sur la
   couche qui les possède.
6. **Lancer** `npm run type:check` (depuis `backend/`) sur la couche modifiée et sur le haut de la stack.
7. **Demander à l'utilisateur, puis** `gh stack push`, et `gh stack top` pour revenir.
8. Ne pas répondre aux threads GitHub ni les résoudre, sauf si l'utilisateur le demande.

## `sync`

```bash
gh stack sync --prune     # fetch, reconcile, rebase, push, refresh PR state; after the user agrees
```

- Sortie `Sync aborted` avec exit 0 = le local et le remote ont divergé. Ne rien forcer. Lire
  `references/troubleshooting.md` du skill `gh-stack` et demander.
- Après un rebase sur un `main` qui a bougé : régénérer les artefacts (voir plus bas).
- Fichiers générés en conflit (`schema.gql`, `sdk/generated/graphql/`, `frontend/src/gql/`) : prendre la
  version de `main` (`--ours` pendant un rebase), puis régénérer. Ne jamais les éditer à la main.

## Régénérer les artefacts (après un rebase ou une correction qui touche le GraphQL ou les entités)

Mêmes étapes que `/rebase`, depuis `backend/` : tester les migrations (`npm run _test mikro:migration:up`,
`npm run _test clickhouse:test-schema:up`), `npm run _dev build:graphql-schema`,
`npm run _test test:graphql-codegen`, le codegen frontend si besoin (`npm run graphql:codegen` dans
`frontend/`), puis `npm run type:check`. Committer les fichiers régénérés sur la couche qui introduit le
changement de schéma.

## `merge`

1. Rappeler l'ordre : de bas en haut, un seul bloc à partir de la PR non mergée la plus basse ; tout ou rien.
2. Vérifier : approbations, CI verte (`gh pr checks`), `needsRebase` à false.
3. **Stratégie de merge** : le repo autorise *merge commit* et *squash* (pas *rebase*), et l'historique de `main`
   montre des merge commits (`Merge pull request #...`). Proposer `--merge` par défaut, jamais `--rebase`, et demander
   si l'utilisateur veut `--squash`.
4. Après l'accord de l'utilisateur : `gh stack merge <pr> --yes --merge`.
5. Puis `gh stack sync --prune`.
