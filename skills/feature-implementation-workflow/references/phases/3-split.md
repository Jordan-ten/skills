# Phase 3 — Découpage en commits et en pull requests

But : une pull request que le reviewer lit facilement, avec une pile de commits cohérente pour la
relecture. Le découpage sert la lisibilité de la PR, pas la séparation des packages.

## Principes

- **La taille se mesure en fichiers que quelqu'un relit** : code, tests, migration, sources i18n, backend
  et frontend ensemble. Les fichiers générés par les frameworks (`schema.gql`, `sdk/generated/`,
  `frontend/src/gql/`, `i18n-types.ts`...) ne comptent pas : personne ne les relit.
- **Repère : environ 30 fichiers.** C'est une recommandation, pas une limite. En dessous, une seule PR
  convient, même avec backend et frontend. Au-dessus, sépare quand cela aide le reviewer : le backend
  avant le frontend, car le frontend a besoin du schéma GraphQL ; un package encore trop gros se coupe
  par préoccupation (règles de couches de `split` dans `../stack/SKILL.md`).
- **Les commits portent la lisibilité.** Atomiques, chacun relisible et vert seul, refacto à part,
  fichiers générés à part, chaque test avec le code qu'il couvre. Choisis l'ordre qui raconte le mieux
  l'histoire.

## Travail

Estime la taille, propose un découpage et dis pourquoi en une ligne, avec le chiffre. L'utilisateur
tranche. À la validation, écris les tableaux dans chaque plan (`## Pull requests` et `### Commits`,
format dans `../write-implementation-plan/references/plan-template.md`) et mets `phase: implement`. Ne crée ni branche ni PR ici.

## Conditions de sortie

- [ ] Le nombre de fichiers (hors générés) est affiché, avec le détail par package.
- [ ] Chaque plan a `## Pull requests` avec les tableaux validés.
- [ ] Chaque étape est dans exactement un commit, et chaque commit dans exactement une pull request.
- [ ] Chaque test est dans le commit qui contient le code qu'il couvre.
- [ ] Une pull request frontend n'est jamais sous la pull request backend dont elle dépend.
- [ ] Chaque pull request passe ses tests seule, sans dépendre d'une pull request au-dessus.

Au passage, donne la commande pour reprendre après le compactage :
`/feature-implementation-workflow <issue>`. Une nouvelle session marche aussi : les plans portent l'état.

## Compactage

Rien : les tableaux sont dans les plans.
