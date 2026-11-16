# Phase 3 — Relire et vérifier

But : la preuve que la feature est bien écrite et que ses e2e passent, une fois tous les commits en place :
une relecture indépendante, puis les e2e du harnais. Le code généré, les contrôles statiques et les tests
unitaires et d'intégration sont déjà passés en phase 2, commit par commit.

**La QA des scénarios dans l'UI n'est pas dans ce workflow.** Elle se lance à part, depuis le workspace
« QA », avec `qa-workflow` (qui lance `run-qa-scenarios`).

Ordre : la relecture d'abord. Ses corrections changent les commits et rendraient des e2e déjà passés
périmés.

Au premier échec, corrige (voir « En cas d'échec »), puis repars de l'étape en échec, pas du début.

## Étape 1 — Relecture (session principale)

- Pour chaque PR du tableau, dans l'ordre des dépendances : `Skill code-review` avec les arguments `medium`
  puis la branche de la PR. Sans `--fix` et sans `--comment`. Vérifie dans la sortie que le diff relu est
  bien celui de la PR (contre sa base).
- Montre les trouvailles à l'utilisateur en français, numérotées, une ligne chacune. L'utilisateur
  décide de ce qu'on corrige. Une trouvaille refusée est notée dans le rapport de la phase.
- **Un seul tour de relecture par PR** : ne relance `code-review` que si l'utilisateur le demande. Les
  corrections acceptées sont faites à l'étape 2, par le même sous-agent que les e2e.

## Étape 2 — Corrections et e2e (un seul sous-agent)

**Un seul sous-agent** fait tout : d'abord les corrections acceptées à l'étape 1 (une liste de trouvailles
dans le brief), avec les contrôles de la phase 2 sur ces commits ; puis les e2e. Brief de
`references/subagent.md` et contraintes ci-dessous. Il renvoie le tableau de rapport. En cas d'échec,
corrige avec `SendMessage` au même sous-agent (voie rapide : la session principale fait cette étape
elle-même). Lis toi-même le diff des commits de correction (`git show --stat`, puis les fichiers
touchés) avant d'afficher un ✅.

- **Serveurs.** La session principale démarre l'environnement `test` avec le skill `launch` s'il ne tourne
  pas déjà depuis la phase 2. Cette règle de l'utilisateur remplace la ligne « never run e2e » de
  `backend/AGENTS.md`. Les commandes longues tournent en arrière-plan : lis le résultat à leur fin. Pas de
  serveur `dev` ici : il n'y a plus de parcours dans le navigateur.
- **Ordre.** Du moins cher au plus cher : e2e backend (base de données et serveur de l'environnement
  `test`, port 3007), puis e2e frontend.
- **E2E : le harnais de l'implémentation, jamais la suite complète** (elle relève de la CI). Lance
  seulement :
  - les e2e créés ou modifiés par l'implémentation (ceux des tableaux de tests des plans) ;
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
- [ ] Un tableau de rapport est affiché : scénario | tests (e2e, unitaires) | résultat. Aucune cellule
      vide.
- [ ] Les serveurs démarrés pour la phase 2 ou 3 sont arrêtés, après accord de l'utilisateur (les PID sont
      dans la sortie de `launch`).
- [ ] `phase: ship` est dans les plans et dans le fichier de run.

## En cas d'échec

Classe-le, dis-le en une ligne, et agis :

- **Bug de code** : sur la couche qui possède le code (plusieurs PR :
  `gh stack checkout <branche>`), avec le même sous-agent (`SendMessage`). Corrige, commite, relance les contrôles de la phase 2
  sur ce commit (génération, contrôles statiques, tests unitaires et d'intégration), puis repars de
  l'étape en échec.
- **Bug de test** : corrige le test, même boucle.
- **Scénario faux ou incomplet** : dis-le à l'utilisateur. L'issue se corrige hors de ce workflow
  (`issue-workflow`), puis mets à jour les plans.
- **Environnement** : rapporte l'erreur exacte.

Après 3 boucles sur le même échec, arrête-toi et demande à l'utilisateur.
