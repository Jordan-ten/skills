# Phase 4 — Relire et vérifier

But : la preuve que la feature est bien écrite et marche de bout en bout, une fois tous les commits en
place : une relecture indépendante, puis les e2e du harnais, puis les scénarios de l'issue dans l'UI. Le
code généré, les contrôles statiques et les tests unitaires et d'intégration sont déjà passés en phase 3,
commit par commit.

Ordre : la relecture d'abord. Ses corrections changent les commits et rendraient des e2e déjà passés
périmés.

Au premier échec, corrige (voir « En cas d'échec »), puis repars de l'étape en échec, pas du début.

## Étape 1 — Relecture (session principale)

- Pour chaque PR du tableau, dans l'ordre des dépendances : `Skill code-review` avec les arguments `high`
  puis la branche de la PR. Sans `--fix` et sans `--comment`. Vérifie dans la sortie que le diff relu est
  bien celui de la PR (contre sa base).
- Montre les trouvailles à l'utilisateur en français, numérotées, une ligne chacune. L'utilisateur
  décide de ce qu'on corrige. Une trouvaille refusée est notée dans le rapport de la phase.
- Les corrections acceptées vont à un sous-agent de la phase 3 (même brief, une liste de trouvailles à la
  place des étapes). Contrôles de la phase 3 sur ces commits, puis relance `code-review high` sur la PR
  corrigée. Deux tours au plus par PR, puis demande à l'utilisateur.

## Étape 2 — Tests (un sous-agent)

Un sous-agent exécute les e2e et le skill `run-qa-scenarios`, avec le brief de `references/subagent.md`
et les contraintes ci-dessous. Il renvoie le tableau de rapport.

- **Serveurs.** La session principale démarre les environnements avec le skill `launch` (`test`,
  `dev front`) s'ils ne tournent pas déjà depuis la phase 3. Cette règle de l'utilisateur remplace la
  ligne « never run e2e » de `backend/AGENTS.md`. Les commandes longues tournent en arrière-plan : lis le
  résultat à leur fin.
- **Ordre.** Du moins cher au plus cher : e2e backend (base de données et serveur de l'environnement
  `test`, port 3007), e2e frontend, puis l'UI (environnement `dev`).
- **E2E : le harnais de l'implémentation, jamais la suite complète** (elle relève de la CI). Lance
  seulement :
  - les e2e créés ou modifiés par l'implémentation (ceux des tableaux de tests des plans) ;
  - les e2e potentiellement impactés : ceux qui touchent aux mêmes opérations GraphQL, entités, use cases
    ou écrans que le diff (cherche-les avec `grep`).
  Dis en une ligne pourquoi chaque e2e impacté est retenu.
- **E2E frontend** : seulement quand un plan en liste ou quand le diff impacte des e2e existants. Si
  l'environnement n'est pas prêt (voir le skill `tnx-tests-setup-front-e2e-tests`), arrête-toi et dis-le :
  ne saute jamais cette étape en silence.
- **UI.** `Skill run-qa-scenarios` avec le numéro de l'issue : il joue les scénarios dans le navigateur.
  Un scénario qu'il ne peut pas jouer va à l'utilisateur sous forme de checklist avec les étapes exactes,
  via la session principale, qui attend la réponse.
- **Jamais de succès sans exécution.** Ne marque pas une étape réussie parce qu'elle n'a pas pu tourner.

## Conditions de sortie

- [ ] `code-review high` a été lancé sur chaque PR, et ses trouvailles sont toutes closes : corrigées, ou
      refusées par l'utilisateur (liste affichée).
- [ ] Chaque e2e backend créé, modifié ou impacté passe.
- [ ] Les e2e frontend créés, modifiés ou impactés passent, ou il n'y en a aucun.
- [ ] La liste des e2e impactés est affichée avec la raison de chacun.
- [ ] Chaque scénario de l'issue a un verdict `pass`. Un scénario `needs a human` ne compte qu'après la
      réponse `pass` de l'utilisateur.
- [ ] Un tableau de rapport est affiché : scénario | tests | verdict UI. Aucune cellule vide.
- [ ] Les serveurs démarrés pour la phase 3 ou 4 sont arrêtés, après accord de l'utilisateur (les PID sont
      dans la sortie de `launch`).
- [ ] `phase: ship` est dans les plans.

## En cas d'échec

Classe-le, dis-le en une ligne, et agis :

- **Bug de code** : reviens à la phase 3, sur la couche qui possède le code (plusieurs PR :
  `gh stack checkout <branche>`), avec un sous-agent. Corrige, commite, relance les contrôles de la phase 3
  sur ce commit (génération, contrôles statiques, tests unitaires et d'intégration), puis repars de
  l'étape en échec. Si des commits ont changé après la relecture, relance `code-review high` sur la PR.
- **Bug de test** : corrige le test, même boucle.
- **Scénario faux ou incomplet** : reviens à la phase 1 pour ce scénario. Change l'issue avec le flag.
  Puis mets à jour les plans.
- **Environnement** : rapporte l'erreur exacte.

Après 3 boucles sur le même échec, arrête-toi et demande à l'utilisateur.
