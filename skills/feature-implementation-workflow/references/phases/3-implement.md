# Phase 3 — Implémenter

But : le code et les tests de chaque pull request du tableau `## Pull requests` des plans, verts et
commités en une pile de commits atomiques que le reviewer lit facilement. Plan backend d'abord, puis plan
frontend.

Cette phase est la plus lourde : elle tourne dans **un sous-agent par PR** (`references/subagent.md`). La
session principale prépare, délègue, vérifie et passe à la PR suivante.

## Session principale

1. **Environnements.** Démarre avec le skill `launch` : `test` quand une PR a des tests d'intégration, une
   migration ou un e2e ; `dev` quand le schéma GraphQL, la spec OpenAPI ou le codegen du frontend changent
   (la génération a besoin de `dev`). Laisse-les tourner : la phase 4 les réutilise. Note les PID.
2. **Branches.** Demande une fois l'accord pour créer les branches du tableau. Suis
   `tnx-dev-standards-dev-and-git-workflow`. Plusieurs PR : étape 4 de `split` dans `../stack/SKILL.md`,
   une branche par ligne de `## Pull requests`. Une seule PR : une seule branche pour tous les commits,
   backend et frontend compris.
3. **Une PR après l'autre**, dans l'ordre des dépendances (backend avant frontend). Lance un sous-agent
   avec le brief de `references/subagent.md` et les contraintes ci-dessous. Vérifie son rapport, puis
   passe à la PR suivante sans demander à l'utilisateur, sauf question dans le rapport.
4. **Simplification.** Quand une PR est verte, propose une fois `tnx-dev-simplify-implementation`. Les
   retouches acceptées font un commit à part.
5. **Fin.** Quand chaque PR est faite, mets `phase: verify` dans les plans.

## Contraintes du sous-agent

- **Contexte.** Travaille depuis le dossier du package (`backend/` ou `frontend/`). Lis son plan, les
  scénarios de l'issue (le plan y renvoie par leur titre) et le style de code du package :
  `backend/docs/coding-style/*` (voir `backend/AGENTS.md`), `frontend/AGENTS.md`. Fichiers de test : skill
  `test-patterns`.
- **Périmètre.** Ne code jamais une étape qui ne sert aucun scénario, et n'implémente aucun comportement
  hors des scénarios.
- **Commits.** Atomiques : chacun est relisible seul et vert (contrôles ci-dessous). Refacto à part,
  fichiers générés à part, chaque test avec le code qu'il couvre, le test e2e avec le commit qui expose le
  comportement. Choisis l'ordre qui raconte le mieux l'histoire à la relecture. Message :
  `feature(<issue>): short description` (anglais simple). N'ajoute jamais un fichier de plan à un commit.
  Après chaque commit, mets à jour `Avancement` de la PR dans le plan (`en cours : étapes 1-2 (<sha>)`,
  puis `faite (<sha>)`).
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
- **Premier retour de bout en bout.** Dès que le code de la tranche 1 du plan backend est commité, lance
  l'e2e qui prouve le critère principal (serveur `test`, port 3007), seul. Un e2e rouge ici coûte un
  commit, pas un retour en arrière en phase 4. Les autres e2e et les e2e frontend attendent la phase 4.
  Jamais la suite complète.
- **Code généré, à chaque commit qui le change.** Régénère ce que le commit exige, avec les commandes des
  `AGENTS.md` : schéma GraphQL (une seule fois, après tous les changements GraphQL du commit), types du
  SDK des tests e2e, spec OpenAPI quand une API publique change (toujours `npm run _dev
  build:openapi:json`, avec le préfixe), `build:docs-index` quand un `*.doc.md` change, codegen GraphQL
  et i18n du frontend. Un commit backend qui change le schéma est régénéré avant le plan frontend, pour
  que celui-ci ait les nouveaux types. Les fichiers générés vont dans un commit séparé, juste après. Ne
  modifie jamais un fichier généré à la main et ne le lis jamais en entier : utilise `grep`.

## Conditions de sortie

- [ ] Chaque étape du plan est implémentée, et chaque test du tableau de tests qui lui appartient existe
      (sauf les e2e dont le plan renvoie à la phase 4).
- [ ] L'e2e de la tranche 1 passe. Montre la commande et le résultat.
- [ ] Type check, lint et OpenGrep : aucune erreur. Montre la commande et le résultat.
- [ ] Aucun problème IDE sur les fichiers modifiés.
- [ ] Les tests unitaires et d'intégration créés, modifiés ou impactés passent. Montre la commande et le
      résultat.
- [ ] La preuve de chaque étape a été jouée, avec son résultat.
- [ ] Le code généré est à jour et commité (`git status --short` ne montre aucun changement généré non
      commité).
- [ ] Aucun comportement implémenté en dehors des scénarios.
- [ ] Les commits de chaque PR sont atomiques et leur message suit la convention. `git status` est propre
      (hors fichiers de plan).
- [ ] `Avancement` vaut `faite (<sha>)` pour chaque PR de chaque plan, et le SHA est celui de la branche.
- [ ] À la fin de la phase : `phase: verify` est dans les plans.
