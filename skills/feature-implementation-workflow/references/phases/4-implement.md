# Phase 4 — Implémenter

But : le code et les tests de chaque commit du tableau `### Commits` des plans, verts et commités. Plan
backend d'abord, puis plan frontend. Dans un plan, commit par commit, dans l'ordre du tableau. Une
« couche » ci-dessous est un commit du tableau ; une PR en contient un ou plusieurs.

## Contraintes

- **Contexte.** Travaille depuis le dossier du package (`backend/` ou `frontend/`). Lis son plan, les
  scénarios de l'issue (le plan y renvoie par leur titre) et le style de code du package :
  `backend/docs/coding-style/*` (voir `backend/AGENTS.md`), `frontend/AGENTS.md`. Fichiers de test : skill
  `test-patterns`.
- **Périmètre.** Ne code jamais une étape qui ne sert aucun scénario, et n'implémente aucun comportement
  hors des scénarios.
- **Branches.** Suis `tnx-dev-standards-dev-and-git-workflow`. Plusieurs PR : étape 4 de `split` dans
  `../stack/SKILL.md`, une branche par ligne de `## Pull requests`. Une seule PR : une seule branche pour
  tous les commits, backend et frontend compris. Demande avant de créer une branche.
- **Types et lint.** Au fil de l'eau sur les fichiers modifiés : MCP JetBrains
  `mcp__idea__get_file_problems` (avec `projectPath` = racine du repo et un `filePath` relatif), jamais
  `mcp__ide__getDiagnostics`. Contrôles complets d'une couche : les commandes des `AGENTS.md` du package
  (type check, lint, format ; backend : `npm run opengrep:diff`, aucune nouvelle violation). Jamais
  `tsc` ni `npx tsc`.
- **Tests unitaires et d'intégration, pour échouer vite.** Lance ceux que le commit crée ou modifie, et
  ceux qu'il peut impacter (mêmes classes, use cases, entités : cherche avec `grep`). Jamais la suite
  complète : elle relève de la CI.
- **Environnement `test`.** Les tests d'intégration et les preuves d'étapes qui touchent la base (une
  migration, une requête) ont besoin de PostgreSQL. Démarre l'environnement avec le skill `launch`
  (`test`) dès que le premier commit en a besoin, et laisse-le tourner : la phase 5 le réutilise. Après
  une nouvelle migration, applique-la (`npm run _test mikro:migration:up`).
- **Preuves.** Joue la preuve de chaque étape du plan à l'étape, base de données comprise.
- **Pas d'e2e ici** : ils attendent l'ensemble de la feature et appartiennent à la phase 5.
- **Commits.** Un commit atomique par ligne du tableau `### Commits`, `feature(<issue>): short description`
  (anglais simple). Un refactor a son propre commit. N'ajoute jamais un fichier de plan à un commit.
- **Schéma GraphQL.** Un commit backend qui le change déclenche la génération du code de `5-verify.md`
  avant le plan frontend, pour que celui-ci ait les nouveaux types. Les fichiers générés vont dans un
  commit séparé, juste après. La génération a besoin de l'environnement `dev` : démarre-le avec le skill
  `launch` (`dev`) s'il ne tourne pas.
- **Simplification.** Quand un package est vert, propose une fois `tnx-dev-simplify-implementation`, avant
  son dernier commit.

## Conditions de sortie

- [ ] Chaque étape du plan (ou du commit en cours) est implémentée, et chaque test du tableau de tests qui
      lui appartient existe.
- [ ] Type check, lint et OpenGrep : aucune erreur. Montre la commande et le résultat.
- [ ] Aucun problème IDE sur les fichiers modifiés.
- [ ] Les tests unitaires et d'intégration créés, modifiés ou impactés passent. Montre la commande et le
      résultat.
- [ ] La preuve de chaque étape du commit a été jouée, avec son résultat.
- [ ] Aucun comportement implémenté en dehors des scénarios.
- [ ] Le commit est fait, `git status` est propre pour le périmètre du commit, et le message suit la
      convention.
- [ ] À la fin de la phase : chaque commit de chaque plan est fait, et `phase: verify` est dans les plans.

## Compactage

La phase 4 est la plus longue : propose le compactage après chaque couche commitée, et à la fin de la
phase. Les couches faites sont dans git (branche et SHA).

Seulement dans la conversation : les écarts avec le plan (et pourquoi), un piège trouvé dans le code dont
la couche suivante a besoin, la génération ou les contrôles qui restent pour la phase 5, les serveurs
démarrés avec leurs PID (la phase 5 les arrête).
