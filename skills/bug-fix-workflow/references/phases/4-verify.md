# Phase 4 — Relire et vérifier

But : la preuve que le bug a disparu et que rien d'autre n'a bougé, une fois tous les commits en place :
une relecture indépendante, puis les e2e du harnais, puis les étapes de reproduction de la phase 1
rejouées dans l'UI ou l'API. Les contrôles statiques et les tests unitaires et d'intégration sont déjà
passés en phase 3, commit par commit.

Ordre : la relecture d'abord. Ses corrections changent les commits et rendraient des e2e déjà passés
périmés.

Au premier échec, corrige (voir « En cas d'échec »), puis repars de l'étape en échec, pas du début.

## Étape 1 — Relecture (session principale)

- Pour chaque PR du tableau, dans l'ordre des dépendances : `Skill code-review` avec les arguments `high`
  puis la branche de la PR. Sans `--fix` et sans `--comment`. Vérifie dans la sortie que le diff relu est
  bien celui de la PR (contre sa base).
- Toi-même, compare le diff de chaque PR à `## Cause` du plan : le correctif change-t-il la ligne ou la
  donnée fausse du diagnostic, ou seulement le symptôme ? Réponds oui ou non, avec le `fichier:ligne`.
- Montre les trouvailles à l'utilisateur en français, numérotées, une ligne chacune. L'utilisateur
  décide de ce qu'on corrige. Une trouvaille refusée est notée dans le rapport de la phase.
- Les corrections acceptées vont à un sous-agent de la phase 3 (même brief, une liste de trouvailles à la
  place des étapes). Contrôles de la phase 3 sur ces commits, puis relance `code-review high` sur la PR
  corrigée. Deux tours au plus par PR, puis demande à l'utilisateur.

## Étape 2 — Tests (un sous-agent)

Un sous-agent exécute les e2e et rejoue la reproduction, avec le brief de
`../feature-implementation-workflow/references/subagent.md` et les contraintes ci-dessous. Il renvoie
le tableau de rapport.

- **Serveurs.** La session principale démarre les environnements avec le skill `launch` (`test`,
  `dev front`) s'ils ne tournent pas déjà depuis la phase 3. Cette règle de l'utilisateur remplace la
  ligne « never run e2e » de `backend/AGENTS.md`. Les commandes longues tournent en arrière-plan : lis le
  résultat à leur fin.
- **Ordre.** Du moins cher au plus cher : e2e backend (environnement `test`, port 3007), e2e frontend, puis
  la reproduction (environnement `dev`).
- **E2E : le harnais du correctif, jamais la suite complète** (elle relève de la CI). Lance seulement :
  - le test de non-régression, et les e2e créés ou modifiés par le correctif ;
  - les e2e potentiellement impactés : ceux qui touchent aux mêmes opérations GraphQL, entités, use cases
    ou écrans que le diff (cherche-les avec `grep`).
  Dis en une ligne pourquoi chaque e2e impacté est retenu.
- **E2E frontend** : seulement quand un plan en liste ou quand le diff impacte des e2e existants. Si
  l'environnement n'est pas prêt (voir le skill `tnx-tests-setup-front-e2e-tests`), arrête-toi et dis-le :
  ne saute jamais cette étape en silence.
- **Reproduction rejouée.** Rejoue **les mêmes actions** que les notes du run (phase 1), sur le code
  corrigé, avec des données **neuves** créées de la même façon (`create-local-data`) : le symptôme
  n'apparaît plus. Un enregistrement produit par le code fautif avant le correctif reste abîmé : ne le
  réutilise pas pour conclure, ni dans un sens ni dans l'autre. `Skill run-qa-scenarios` avec le numéro de l'issue
  joue le scénario de non-régression dans le navigateur. Un bug sans écran se rejoue par l'API ou le job,
  avec la même commande que la phase 1. Un scénario qu'il ne peut pas jouer va à l'utilisateur sous forme
  de checklist avec les étapes exactes, via la session principale, qui attend la réponse.
- **Voisinage.** Joue aussi le chemin nominal de la fonctionnalité touchée (le comportement qui marchait
  avant le bug), pour voir que le correctif ne l'a pas cassé.
- **Jamais de succès sans exécution.** Ne marque pas une étape réussie parce qu'elle n'a pas pu tourner.

## Conditions de sortie

- [ ] `code-review high` a été lancé sur chaque PR, et ses trouvailles sont toutes closes : corrigées, ou
      refusées par l'utilisateur (liste affichée).
- [ ] Le test de non-régression passe, et chaque e2e backend créé, modifié ou impacté passe.
- [ ] Les e2e frontend créés, modifiés ou impactés passent, ou il n'y en a aucun.
- [ ] La liste des e2e impactés est affichée avec la raison de chacun.
- [ ] La reproduction rejouée (mêmes actions, données neuves) ne montre plus le symptôme.
- [ ] Le chemin nominal voisin marche, avec une preuve (snapshot, réponse d'API, test).
- [ ] Un tableau avant/après est affiché : étape de la reproduction | avant (phase 1) | après. Aucune
      cellule vide. Un scénario `needs a human` ne compte qu'après la réponse `pass` de l'utilisateur.
- [ ] Les serveurs démarrés pour la phase 3 ou 4 sont arrêtés, après accord de l'utilisateur (les PID sont
      dans la sortie de `launch`).
- [ ] `phase: ship` est dans les plans.

## En cas d'échec

Classe-le, dis-le en une ligne, et agis :

- **Le bug est toujours là** : la cause du plan est fausse ou incomplète. Reviens à la phase 2
  (diagnostic), pas à la phase 3 : un deuxième correctif sur une mauvaise cause ajoute du bruit.
- **Bug de code** (le correctif casse autre chose) : reviens à la phase 3, sur la couche qui possède le
  code (plusieurs PR : `gh stack checkout <branche>`), avec un sous-agent. Corrige, commite, relance les
  contrôles de la phase 3 sur ce commit, puis repars de l'étape en échec. Si des commits ont changé après
  la relecture, relance `code-review high` sur la PR.
- **Bug de test** : corrige le test, même boucle.
- **Scénario faux ou incomplet** : reviens à la phase 1 pour ce scénario. Change l'issue avec le flag.
  Puis mets à jour les plans.
- **Environnement** : rapporte l'erreur exacte.

Après 3 boucles sur le même échec, arrête-toi et demande à l'utilisateur.
