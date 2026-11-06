# Phase 4 — Implémenter

But : le code et les tests de chaque couche de pull request, verts et commités. Plan backend d'abord,
puis plan frontend. Dans un plan, couche par couche, de bas en haut.

## Avant de coder

- Travaille depuis le dossier de travail du package : `backend/` pour le plan backend, `frontend/` pour
  le plan frontend. Chaque commande `npm run` ci-dessous s'y lance, et le plan se lit dans son
  `.claude/plans/ticket/`.
- Lis le plan du package, et le style de code du package : backend `backend/docs/coding-style/*`
  (voir `backend/AGENTS.md`), frontend `frontend/AGENTS.md`.
- Relis les scénarios de l'issue. Le plan y renvoie par leur titre.
- Fichiers de test : utilise le skill `test-patterns`.
- Branches : suis `tnx-dev-standards-dev-and-git-workflow`. Pour une stack, suis l'étape 4 de `split`
  dans `../stack-pull-requests/SKILL.md` (`gh stack init`, `gh stack add`). Pour une seule PR, vérifie que
  la branche courante est la bonne. Demande avant de créer une branche.

## Travail, par couche

1. Code et tests ensemble, dans l'ordre du plan. Ne code jamais une étape qui ne sert aucun scénario.
2. Types et lint sur les fichiers que tu modifies, au fil de l'eau : MCP JetBrains `get_file_problems`
   (`mcp__idea__get_file_problems`), jamais `mcp__ide__getDiagnostics`. Passe `projectPath` (racine du
   repo) et un `filePath` relatif.
3. À la fin de la couche, lance les contrôles ci-dessous.
4. Quand la couche est verte, propose une fois `tnx-dev-simplify-implementation` pour le package, avant
   son dernier commit.
5. Commit : un commit atomique par couche, `feature(<issue>): short description` (en anglais simple).
   Un refactor a son propre commit. N'ajoute pas les fichiers de plan à un commit.
6. Couche backend qui change le schéma GraphQL : lance maintenant la génération de `5-verify.md`
   (groupe A), pour que le plan frontend puisse utiliser les nouveaux types. Commite les fichiers
   générés dans cette couche.

## Contrôles d'une couche (backend, depuis `backend/`)

- `npm run type:check`. Jamais `tsc` ni `npx tsc`. Pour quelques fichiers seulement :
  `npm run tsgo -- -p tsconfig.json --noEmit --pretty false | grep -F -e <fichier>`.
- `npm run lint`, et `npm run format` sur les fichiers modifiés.
- `npm run opengrep:diff` : aucune nouvelle violation.
- Tests unitaires de la zone : `npm run _test test -- <fichier>.spec.ts`. Tests d'intégration de la zone :
  `npm run _test test:itg -- <fichier>.itg-spec.ts`.
- Ne lance pas les tests e2e ici : ils appartiennent à la phase 5.

## Contrôles d'une couche (frontend, depuis `frontend/`)

Utilise les commandes de `frontend/AGENTS.md` : type check, `npm run lint`, `npm run test -- <fichier>`.

## Conditions de sortie

- [ ] Chaque étape du plan (ou de la couche en cours) est implémentée.
- [ ] Chaque test du tableau de tests qui appartient à cette couche existe.
- [ ] Type check, lint et OpenGrep : aucune erreur. Montre la commande et le résultat.
- [ ] Aucun problème IDE sur les fichiers modifiés.
- [ ] Les tests unitaires et d'intégration de la zone passent. Montre la commande et le résultat.
- [ ] Aucun comportement implémenté en dehors des scénarios (pas de dérive de périmètre).
- [ ] La couche est commitée, `git status` est propre pour la couche, et le message de commit suit la
      convention.
- [ ] À la fin de la phase : chaque couche de chaque plan est faite, et `phase: verify` est dans les plans.

## Compacter après cette phase

La phase 4 est la plus longue : propose le compactage après chaque couche commitée, et à la fin de la
phase. Mêmes règles, même ligne, avec la couche dedans.

Garde : numéro de l'issue, chemins des plans, couches faites (branche et SHA du commit), ce qui diffère
du plan (et pourquoi), un piège trouvé dans le code dont la couche suivante a besoin, la génération ou
les contrôles qui restent à lancer en phase 5.
Jette : contenus de fichiers, diffs, sorties de tests et de type check, les boucles d'erreurs de types,
les listes de problèmes IDE.

```
/compact Garde : issue <n> ; chemins des plans ; couches faites avec branche et SHA du commit ; écarts avec le plan ; pièges utiles à la couche suivante ; génération à lancer. Jette : contenus de fichiers, diffs, sorties de tests, de type check et de lint, boucles d'erreurs.
```
