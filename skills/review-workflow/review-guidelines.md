# Consignes de review (workspace enfant)

Tu relis la pull request du workspace. Le code de la PR est déjà sur disque (HEAD détaché). Le triage tourne avec `/jcontent-traace:review`.

## Rôle

- Tu es relecteur. Lecture seule : ne modifie pas le code, ne fais ni commit ni push.
- Ne poste rien sur la PR (commentaire, review, approbation) sans montrer le texte à l'utilisateur et avoir son accord.
- Ne lance ni tests, ni app, ni e2e. Ce que tu ne peux pas juger sans cela entre dans "À vérifier par un humain", seulement s'il porte un risque.

## Méthode

- Commence par `gh pr diff <n> --name-only` et la stat. Ne charge jamais tout le diff d'un coup : lis fichier par fichier, selon le besoin.
- Ignore les fichiers générés (`schema.gql`, `generated/`, `gql/`, `i18n-types.ts`, `package-lock.json`) : ne les lis pas, ne les cite pas dans le rapport. Vérifie seulement qu'ils ont bougé quand leur source a bougé ; ne le signale que si ce n'est pas le cas.
- Ordre de gravité : sécurité > bug > logique > amélioration. Pas de remarque de style hors règles ci-dessous.
- Un finding sans `file:line` précis ne compte pas. Ne devine jamais un numéro de ligne.
- Un point que l'agent peut juger ne va pas dans "à vérifier par un humain".

## Règles du projet à contrôler

- GraphQL : 2 `@Args` ou plus → un `@InputType()`. Mutation sans payload → `Success`, pas `Boolean`. `@ResolveField` qui expose une relation → `@HideField()` sur la propriété. `@ResolveField` d'une entité en liste → dataloader.
- Couches : un resolver n'appelle pas un repository (use case). Un use case n'appelle pas un autre use case (service de domaine) ni un repository (port).
- Base de données : CHECK bidirectionnel, identique dans la migration et dans le `@Check`. Une règle métier qui est un `CASCADE` ou `NO ACTION` va dans la contrainte DB. Requête sur une liste d'IDs : dédoublonner par entité.
- Tests : une nouvelle méthode publique est testée dans le spec existant de sa classe. IDs de fixtures unitaires : chaînes numériques (`'1'`). E2E d'abord pour un parcours métier ; pas de test e2e pour une simple garde d'input.
- Nommage : nom de classe = nom de fichier. Pas de terme nouveau sans avoir cherché le vocabulaire existant dans le domaine.
- Le produit s'appelle Tennaxia. `Traace` reste dans les identifiants de code existants, jamais comme nom de produit dans un texte.

## Écriture

- Rapport pour l'utilisateur : français, dans `.claude/plans/review/<n>.md`.
- Texte destiné à GitHub (commentaire de review) : anglais simple, phrases courtes, mots courants, sans idiome.

## Fin de review

Mets à jour la carte du workspace avec le verdict en une ligne, puis demande l'attention de l'utilisateur :

```bash
ORCA_CMD="${ORCA_CLI_COMMAND:-orca-ide}"
"$ORCA_CMD" worktree set --worktree active --comment "<verdict en une ligne>" --unread --json
```
