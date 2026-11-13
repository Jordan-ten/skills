# Phase 5 — Vérifier

But : la preuve que la feature marche, du code généré jusqu'à l'UI, scénario par scénario. Au premier
échec, corrige (voir « En cas d'échec »), puis repars de l'étape en échec, pas du début.

## Contraintes

- **Tu lances toi-même les tests e2e et tu démarres les serveurs** avec le skill `launch` (`dev`, `test`,
  `dev front`). Cette règle de l'utilisateur remplace la ligne « never run e2e » de `backend/AGENTS.md`.
  Lance les commandes longues en arrière-plan et lis le résultat à leur fin.
- **Ordre.** Le code généré passe d'abord : les contrôles en dépendent. Ensuite, du moins cher au plus
  cher : contrôles statiques, tests unitaires, tests d'intégration (base de données de l'environnement
  `test`, pas le serveur HTTP ; réutilise l'environnement démarré en phase 4 s'il tourne), e2e backend (base de données et serveur de
  l'environnement `test`, port 3007), e2e frontend, puis l'UI (environnement `dev`).
- **Code généré.** Il a besoin de l'environnement `dev` : démarre-le avec `launch` (`dev`) s'il ne tourne
  pas (la phase 4 a pu le démarrer). Régénère ce que le changement exige, avec les commandes des
  `AGENTS.md` : schéma
  GraphQL (une seule fois, après tous les changements), types du SDK des tests e2e, spec OpenAPI quand une
  API publique change (toujours `npm run _dev build:openapi:json`, avec le préfixe), `build:docs-index`
  quand un `*.doc.md` change, codegen GraphQL et i18n du frontend. Ne modifie jamais un fichier généré à la
  main et ne le lis jamais en entier : utilise `grep`. Un changement généré non commité va dans un commit
  séparé de la PR qui l'a causé.
- **Tests : le harnais de l'implémentation, jamais une suite complète** (elle relève de la CI). Cela vaut
  pour les tests unitaires, d'intégration et e2e. Lance seulement :
  - les tests créés ou modifiés par l'implémentation (ceux des tableaux de tests des plans) ;
  - les tests potentiellement impactés : ceux qui touchent aux mêmes classes, opérations GraphQL,
    entités, use cases ou écrans que le diff (cherche-les avec `grep`).
  Dis en une ligne pourquoi chaque test impacté est retenu.
- **E2E backend** : environnement `test`. **E2E frontend** : seulement quand un plan en liste ou quand le
  diff impacte des e2e existants. Si l'environnement n'est pas prêt (voir le skill
  `tnx-tests-setup-front-e2e-tests`), arrête-toi et dis-le : ne saute jamais cette étape en silence.
- **UI.** `Skill run-qa-scenarios` avec le numéro de l'issue : il joue les scénarios dans le navigateur.
  Un scénario qu'il ne peut pas jouer va à l'utilisateur sous forme de checklist avec les étapes exactes,
  et tu attends sa réponse.
- **Jamais de succès sans exécution.** Ne marque pas une étape réussie parce qu'elle n'a pas pu tourner.

## Conditions de sortie

- [ ] Le code généré est à jour et commité (`git status --short` ne montre aucun changement généré non
      commité).
- [ ] Type check, lint et OpenGrep passent (backend), type check et lint passent (frontend).
- [ ] Chaque test unitaire et d'intégration créé, modifié ou impacté passe.
- [ ] Chaque e2e backend créé, modifié ou impacté passe.
- [ ] La liste des tests impactés (tous types) est affichée avec la raison de chacun.
- [ ] Les e2e frontend créés, modifiés ou impactés passent, ou il n'y en a aucun.
- [ ] Chaque scénario de l'issue a un verdict `pass`. Un scénario `needs a human` ne compte qu'après la
      réponse `pass` de l'utilisateur.
- [ ] Un tableau de rapport est affiché : scénario | tests | verdict UI. Aucune cellule vide.
- [ ] Les serveurs démarrés pour la phase sont arrêtés, après accord de l'utilisateur (les PID sont dans
      la sortie de `launch`).

## En cas d'échec

Classe-le, dis-le en une ligne, et agis :

- **Bug de code** : reviens à la phase 4, sur la couche qui possède le code (plusieurs PR :
  `gh stack checkout <branche>`). Corrige, commite, lance les contrôles de la couche, puis repars de
  l'étape en échec.
- **Bug de test** : corrige le test, même boucle.
- **Scénario faux ou incomplet** : reviens à la phase 1 pour ce scénario. Change l'issue avec le flag.
  Puis mets à jour les plans.
- **Environnement** : rapporte l'erreur exacte.

Après 3 boucles sur le même échec, arrête-toi et demande à l'utilisateur.

## Compactage

Seulement dans la conversation : le tableau de rapport (scénario | tests | verdict UI), les réponses de
l'utilisateur sur les scénarios `needs a human`, les échecs corrigés (une ligne chacun), les
avertissements pour la phase 6, les PID des serveurs encore démarrés.
