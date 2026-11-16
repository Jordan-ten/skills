# Phase 4 — Relire et vérifier

But : la preuve que le bug est corrigé et que rien d'autre n'a bougé, une fois tous les commits en place :
une relecture indépendante, puis les e2e du harnais. Le test de non-régression, rouge avant le correctif
(phase 3), est la preuve « après ». Les contrôles statiques et les tests unitaires et d'intégration sont
déjà passés en phase 3, commit par commit.

**Le rejeu dans l'UI n'est pas dans ce workflow.** La QA se lance à part, depuis le workspace « QA », avec
`qa-workflow` (qui lance `run-qa-scenarios` sur le scénario de non-régression de l'issue).

Ordre : la relecture d'abord. Ses corrections changent les commits et rendraient des e2e déjà passés
périmés.

Au premier échec, corrige (voir « En cas d'échec »), puis repars de l'étape en échec, pas du début.

## Étape 1 — Relecture (session principale)

- Pour chaque PR du tableau, dans l'ordre des dépendances : `Skill code-review` avec les arguments `medium`
  puis la branche de la PR. Sans `--fix` et sans `--comment`. Vérifie dans la sortie que le diff relu est
  bien celui de la PR (contre sa base).
- Toi-même, compare le diff de chaque PR à `## Cause` du plan : le correctif change-t-il la ligne ou la
  donnée fausse du diagnostic, ou seulement le symptôme ? Réponds oui ou non, avec le `fichier:ligne`.
- Montre les trouvailles à l'utilisateur en français, numérotées, une ligne chacune. L'utilisateur
  décide de ce qu'on corrige. Une trouvaille refusée est notée dans le rapport de la phase.
- **Un seul tour de relecture par PR** : ne relance `code-review` que si l'utilisateur le demande. Les
  corrections acceptées sont faites à l'étape 2, par le même sous-agent que les e2e.

## Étape 2 — Corrections et e2e (un seul sous-agent)

**Un seul sous-agent** fait tout : d'abord les corrections acceptées à l'étape 1 (une liste de trouvailles
dans le brief), avec les contrôles de la phase 3 sur ces commits ; puis les e2e. Brief de
`../feature-implementation-workflow/references/subagent.md` et contraintes ci-dessous. Il renvoie le
tableau de rapport. En cas d'échec, corrige avec `SendMessage` au même sous-agent (voie rapide : la
session principale fait cette étape elle-même). Lis toi-même le diff des commits de correction
(`git show --stat`, puis les fichiers touchés) avant d'afficher un ✅.

- **Serveurs.** La session principale démarre l'environnement `test` avec le skill `launch` s'il ne tourne
  pas déjà depuis la phase 3. Cette règle de l'utilisateur remplace la ligne « never run e2e » de
  `backend/AGENTS.md`. Les commandes longues tournent en arrière-plan : lis le résultat à leur fin.
- **Ordre.** Du moins cher au plus cher : e2e backend (environnement `test`, port 3007), puis e2e frontend.
- **E2E : le harnais du correctif, jamais la suite complète** (elle relève de la CI). Lance seulement :
  - le test de non-régression, et les e2e créés ou modifiés par le correctif ;
  - les e2e potentiellement impactés : ceux qui touchent aux mêmes opérations GraphQL, entités, use cases
    ou écrans que le diff (cherche-les avec `grep`).
  Dis en une ligne pourquoi chaque e2e impacté est retenu.
- **E2E frontend** : seulement quand un plan en liste ou quand le diff impacte des e2e existants. Si
  l'environnement n'est pas prêt (voir le skill `tnx-tests-setup-front-e2e-tests`), arrête-toi et dis-le :
  ne saute jamais cette étape en silence.
- **Jamais de succès sans exécution.** Ne marque pas une étape réussie parce qu'elle n'a pas pu tourner.

## Conditions de sortie

- [ ] `code-review medium` a été lancé une fois sur chaque PR, et ses trouvailles sont toutes closes :
      corrigées, ou refusées par l'utilisateur (liste affichée).
- [ ] Chaque e2e backend créé, modifié ou impacté passe.
- [ ] Les e2e frontend créés, modifiés ou impactés passent, ou il n'y en a aucun.
- [ ] La liste des e2e impactés est affichée avec la raison de chacun.
- [ ] Le test de non-régression, rouge avant le correctif en phase 3, est vert (commande et résultat).
- [ ] Un tableau est affiché : e2e lancés | raison | résultat. Aucune cellule vide.
- [ ] Les serveurs démarrés pour la phase 3 ou 4 sont arrêtés, après accord de l'utilisateur (les PID sont
      dans la sortie de `launch`).
- [ ] `phase: ship` est dans les plans et dans le fichier de run.

## En cas d'échec

Classe-le, dis-le en une ligne, et agis :

- **Le test de non-régression reste rouge, ou un e2e du voisinage casse sans bug de code évident** : la
  cause du plan est fausse ou incomplète. Reviens à la phase 2
  (diagnostic), pas à la phase 3 : un deuxième correctif sur une mauvaise cause ajoute du bruit.
- **Bug de code** (le correctif casse autre chose) : reviens à la phase 3, sur la couche qui possède le
  code (plusieurs PR : `gh stack checkout <branche>`), avec le même sous-agent (`SendMessage`). Corrige, commite, relance les
  contrôles de la phase 3 sur ce commit, puis repars de l'étape en échec.
- **Bug de test** : corrige le test, même boucle.
- **Scénario faux ou incomplet** : reviens à la phase 1 pour ce scénario. Change l'issue avec le flag.
  Puis mets à jour les plans.
- **Environnement** : rapporte l'erreur exacte.

Après 3 boucles sur le même échec, arrête-toi et demande à l'utilisateur.
