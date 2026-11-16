# Phase 3 — Implémenter

But : le test de non-régression et le correctif de chaque pull request du tableau `## Pull requests`, verts
et commités en commits atomiques que le reviewer lit facilement.

Cette phase tourne dans **un sous-agent par PR**
(`../feature-implementation-workflow/references/subagent.md`). La session principale prépare, délègue,
vérifie et passe à la PR suivante.

## Session principale

1. **Environnements.** Démarre avec le skill `launch` : `test` pour un e2e, une migration ou un test
   d'intégration ; `dev` quand le schéma GraphQL, la spec OpenAPI ou le codegen du frontend changent. Laisse-les
   tourner : la phase 4 les réutilise. Note les PID.
2. **Branche.** Si la branche courante n'est pas dédiée à l'issue, demande l'accord pour créer celle du
   tableau. Suis `tnx-dev-standards-dev-and-git-workflow`. Plusieurs PR : étape 4 de `split` dans
   `../stack/SKILL.md`.
3. **Une PR après l'autre**, dans l'ordre des dépendances. Lance un sous-agent avec le brief de
   `subagent.md` et les contraintes ci-dessous. Vérifie son rapport, puis passe à la PR suivante sans
   demander, sauf question dans le rapport.
4. **Simplification.** Quand une PR est verte, propose une fois `tnx-dev-simplify-implementation`. Les
   retouches acceptées font un commit à part.
5. **Fin.** Quand chaque PR est faite, mets `phase: verify` dans les plans.

## Voie rapide

Plan avec `fast_path: true` : la session principale fait elle-même les contraintes ci-dessous, sans
sous-agent, et garde ses sorties dans des fichiers du scratchpad (`tail`, `grep`). Les conditions de sortie
sont les mêmes.

## Contraintes du sous-agent

- **Contexte.** Travaille depuis le dossier du package. Lis son plan (cause comprise), le scénario de
  non-régression de l'issue, les notes du run (étapes de reproduction) et le style de code du package :
  `backend/docs/coding-style/*` (voir `backend/AGENTS.md`), `frontend/AGENTS.md`. Fichiers de test : skill
  `test-patterns`.
- **Rouge d'abord.** Avant d'écrire le correctif, lance le test de non-régression (l'e2e de reproduction
  non commité, ou le test nouveau) et vérifie qu'il **échoue pour la bonne raison** : le message d'échec
  montre le symptôme de l'issue, pas une erreur de test. Garde la sortie courte pour le rapport. Un test
  qui passe avant le correctif ne prouve rien : rapporte-le et arrête-toi.
- **Périmètre.** Corrige la cause du plan, rien d'autre. Pas de refacto, pas de renommage, pas de
  comportement hors du scénario. Un défaut vu en chemin va dans le rapport, pas dans le code.
- **Commits.** Atomiques et verts : le test de non-régression est commité **avec** le correctif (un commit
  rouge casserait la règle « chaque commit est vert »). Réparation de données (migration) dans son commit,
  fichiers générés à part, refacto prévu par le plan à part. Message : `bugfix(<issue>): short description`
  (anglais simple). N'ajoute jamais un fichier de plan ou de notes à un commit. Après chaque commit, mets à
  jour `Avancement` de la PR dans le plan (`en cours : étapes 1-2 (<sha>)`, puis `faite (<sha>)`).
- **Types et lint.** Au fil de l'eau sur les fichiers modifiés : MCP JetBrains
  `mcp__idea__get_file_problems` (avec `projectPath` = racine du repo et un `filePath` relatif), jamais
  `mcp__ide__getDiagnostics`. Contrôles complets à chaque commit : les commandes des `AGENTS.md` du
  package (type check, lint, format ; backend : `npm run opengrep:diff`, aucune nouvelle violation).
  Jamais `tsc` ni `npx tsc`.
- **Tests unitaires et d'intégration, pour échouer vite.** Lance ceux que le commit crée ou modifie, et
  ceux qu'il peut impacter (mêmes classes, use cases, entités : cherche avec `grep`). Jamais la suite
  complète : elle relève de la CI.
- **Serveurs.** Utilise ceux que la session principale a démarrés. Ne démarre et n'arrête rien. Après une
  nouvelle migration, applique-la (`npm run _test mikro:migration:up`). Un serveur absent : rapporte-le.
- **Preuves.** Joue la preuve de chaque étape du plan quand l'étape est faite, base de données comprise.
  Une migration n'a jamais de test automatisé : sa preuve est manuelle.
- **Vert ensuite.** Après le correctif, relance le test de non-régression, seul : il passe. C'est le
  premier retour de bout en bout. Les autres e2e attendent la phase 4. Jamais la suite complète.
- **Code généré, à chaque commit qui le change.** Même règle que la phase 3 de
  `feature-implementation-workflow` : régénère avec les commandes des `AGENTS.md` (schéma GraphQL, SDK des
  tests e2e, spec OpenAPI avec `npm run _dev build:openapi:json`, `build:docs-index`, codegen du
  frontend), dans un commit séparé juste après. Ne modifie jamais un fichier généré à la main et ne le lis
  jamais en entier : utilise `grep`.

## Conditions de sortie

- [ ] Chaque étape du plan est implémentée, et chaque test du tableau de tests qui lui appartient existe.
- [ ] Le test de non-régression a échoué avant le correctif, pour la bonne raison. Montre le message
      d'échec.
- [ ] Le test de non-régression passe après le correctif. Montre la commande et le résultat.
- [ ] Type check, lint et OpenGrep : aucune erreur. Montre la commande et le résultat.
- [ ] Aucun problème IDE sur les fichiers modifiés.
- [ ] Les tests unitaires et d'intégration créés, modifiés ou impactés passent. Montre la commande et le
      résultat.
- [ ] La preuve de chaque étape a été jouée, avec son résultat.
- [ ] Le diff ne contient que le correctif de la cause et son test : aucun refacto ni comportement hors
      scénario. `git diff --stat` est montré.
- [ ] Le code généré est à jour et commité (`git status --short` ne montre aucun changement généré non
      commité).
- [ ] Les commits de chaque PR sont atomiques et leur message suit la convention. `git status` est propre
      (hors fichiers de plan et de notes).
- [ ] `Avancement` vaut `faite (<sha>)` pour chaque PR de chaque plan, et le SHA est celui de la branche.
- [ ] À la fin de la phase : `phase: verify` est dans les plans.
