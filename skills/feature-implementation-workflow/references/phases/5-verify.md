# Phase 5 — Vérifier

But : la preuve que la feature marche, du code généré jusqu'à l'UI. Lance les groupes dans l'ordre. Au
premier échec, corrige (voir « En cas d'échec »), puis repars de ce groupe, pas du début.

Règle de l'utilisateur pour ce workflow : tu lances toi-même les tests e2e, et tu démarres les serveurs
avec le skill `launch`. Cela remplace la ligne « never run e2e » de `backend/AGENTS.md`.

Lance les commandes longues en arrière-plan et lis le résultat quand elles se terminent.

## Groupe A — Le code généré est à jour (environnement backend `dev`)

1. `Skill launch` avec `dev`. Il démarre Docker, lance les migrations, démarre le backend sur le port 3000.
2. Depuis `backend/`, dans cet ordre, seulement ce que le changement exige :
   - `npm run _dev build:graphql-schema` (après tous les changements GraphQL, une seule fois)
   - `npm run _test test:graphql-codegen` (types du SDK pour les tests e2e)
   - `npm run _dev build:openapi:json` quand une API publique a changé (toujours avec le préfixe `_dev`)
   - `npm run build:docs-index` quand un `*.doc.md` a changé
3. Depuis `frontend/`, quand le plan frontend existe :
   - `npm run graphql:codegen`
   - `npm run i18n-no-watch` quand des clés de traduction ont changé
4. Ne modifie jamais un fichier généré à la main. Ne le lis jamais en entier : utilise `grep` pour
   chercher un nom.

Preuve : après la génération, `git status --short` ne montre aucun changement qui ne soit pas déjà
commité. Un changement généré non commité va dans le commit de la couche qui l'a causé.

## Groupe B — Contrôles statiques

- Backend : `npm run type:check`, `npm run lint`, `npm run opengrep:diff`.
- Frontend : type check et lint de `frontend/AGENTS.md`.

## Groupe C — Tests unitaires et d'intégration

- Backend : `npm run _test test` (tous les tests unitaires). Tests d'intégration des modules touchés :
  `npm run _test test:itg -- <fichier>.itg-spec.ts`.
- Frontend : `npm run test`.

## Groupe D — E2E backend (environnement `test`)

1. `Skill launch` avec `test` (port 3007).
2. Lance les fichiers e2e listés dans les tableaux de tests des plans :
   `npm run _test test:e2e -- <fichier>.e2e-spec.ts`. Ajoute les autres fichiers e2e des modules touchés
   (grep le nom du module dans le dossier e2e).
3. Demande une fois s'il faut lancer toute la suite e2e (elle est longue). Ne la lance que sur un oui.

## Groupe E — E2E automatisés du frontend

Seulement quand le plan frontend liste des tests e2e (`frontend/tests/`). La mise en place est décrite par
le skill `tnx-tests-setup-front-e2e-tests` et `frontend/AGENTS.md`. Si l'environnement n'est pas prêt,
arrête-toi et dis-le à l'utilisateur : ne saute pas le groupe en silence.

## Groupe F — Bout en bout dans l'UI (environnement `dev`, backend et frontend)

1. `Skill launch` avec `dev front`.
2. `Skill run-qa-scenarios` avec le numéro de l'issue. Il construit la liste des scénarios depuis l'issue
   et les joue dans le navigateur. Un scénario qu'il ne peut pas jouer va à l'utilisateur sous forme de
   checklist, avec les étapes exactes.
3. Attends la réponse de l'utilisateur sur chaque scénario qui demande un humain.

## Conditions de sortie

- [ ] Groupe A : le code généré est à jour et commité.
- [ ] Groupe B : type check, lint, OpenGrep passent.
- [ ] Groupe C : tous les tests unitaires passent, et les tests d'intégration des modules touchés.
- [ ] Groupe D : chaque test e2e backend des plans passe (et toute la suite, si l'utilisateur l'a demandé).
- [ ] Groupe E : passe, ou les plans ne listent aucun test e2e frontend.
- [ ] Groupe F : chaque scénario de l'issue a un verdict `pass`. Un scénario `needs a human` ne compte
      qu'après la réponse `pass` de l'utilisateur.
- [ ] Un tableau de rapport est affiché : scénario | tests | verdict UI. Aucune cellule vide.
- [ ] Les serveurs démarrés pour la phase sont arrêtés, après accord de l'utilisateur (les PID sont dans
      la sortie de `launch`).

## En cas d'échec

Classe-le, dis-le en une ligne, et agis :

- **Bug de code** : reviens à la phase 4, sur la couche qui possède le code (stack :
  `gh stack checkout <branche>`). Corrige, commite, lance les contrôles de la couche, puis repars du
  groupe en échec de la phase 5.
- **Bug de test** : corrige le test, même boucle.
- **Scénario faux ou incomplet** : reviens à la phase 1 pour ce scénario. Change l'issue avec le flag.
  Puis mets à jour les plans.
- **Environnement** : rapporte l'erreur exacte. Ne marque jamais un groupe comme réussi parce qu'il n'a
  pas pu tourner.

Après 3 boucles sur le même échec, arrête-toi et demande à l'utilisateur.

## Compacter après cette phase

Garde : numéro de l'issue, chemins des plans, le tableau de rapport (scénario | tests | verdict UI), les
commandes qui ont passé (leurs noms seulement), les échecs corrigés (une ligne chacun), les réponses de
l'utilisateur sur les scénarios `needs a human`, les branches et SHA à pousser, les avertissements pour
la phase 6.
Jette : logs de tests, de `launch` et de génération, snapshots et captures du navigateur, messages de
console.

```
/compact Garde : issue <n> ; chemins des plans ; tableau de rapport scénario/tests/verdict UI ; noms des commandes passées ; échecs corrigés en une ligne ; réponses de l'utilisateur sur les scénarios humains ; branches et SHA ; avertissements. Jette : logs de tests, de launch et de génération, snapshots et captures du navigateur, messages de console.
```
