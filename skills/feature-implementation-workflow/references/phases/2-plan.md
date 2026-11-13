# Phase 2 — Plans et découpage en pull requests

But : un plan par package touché, qui définit l'implémentation, sans question ouverte, avec le découpage
en pull requests. L'utilisateur valide les plans et le découpage en une seule fois. Les plans sont écrits
en **français**.

Méthode : `../write-implementation-plan/SKILL.md` (but, contraintes, conditions de sortie) et son
template `../write-implementation-plan/references/plan-template.md`. Applique-les, ne les recopie pas.
Le cadrage est déjà fait : les critères sont les scénarios de l'issue.

Pars des notes du run (`.claude/plans/<n>.notes.md`, écrites en phase 1), puis complète l'exploration. Les
décisions techniques du grill de la phase 1 vont dans `## Décisions techniques`. `## Approche` cite la
fonctionnalité voisine et ce qu'on réutilise (ou dit qu'il n'y en a pas).

## Contraintes : plans

- Un plan par package qu'au moins une étape modifie, à l'emplacement du template (section « Fichier »).
- Plan backend en premier : le plan frontend a besoin de son contrat.
- Une question que seule une autre personne peut trancher met `status: not-ready` : dis-le et n'avance
  pas.

## Contraintes : découpage

Une fois les étapes écrites, avant la validation. Le découpage sert la lisibilité de la PR, pas la
séparation des packages. Les commits de chaque PR se décident en phase 3, selon des principes.

- **La taille se mesure en fichiers que quelqu'un relit** : code, tests, migration, sources i18n, backend
  et frontend ensemble. Les fichiers générés par les frameworks (`schema.gql`, `sdk/generated/`,
  `frontend/src/gql/`, `i18n-types.ts`...) ne comptent pas : personne ne les relit.
- **Repère : environ 30 fichiers.** C'est une recommandation, pas une limite. En dessous, une seule PR
  convient, même avec backend et frontend. Au-dessus, sépare quand cela aide le reviewer : le backend
  avant le frontend, car le frontend a besoin du schéma GraphQL ; un package encore trop gros se coupe
  par préoccupation (règles de couches de `split` dans `../stack/SKILL.md`).
- Estime la taille à partir des fichiers nommés dans les étapes des plans. Écris le découpage proposé dans
  chaque plan (`## Pull requests`, format dans le template, colonne `Avancement` à `—`). Dis pourquoi en
  une ligne, avec le chiffre. Ne crée ni branche ni PR ici.

## Validation

Montre les plans, le chiffre de taille et le découpage, puis demande une seule validation. Si
l'utilisateur change le découpage, corrige le tableau dans les plans et relance les contrôles. Mets
`phase: implement` dans l'en-tête des plans seulement après la validation.

## Conditions de sortie

- [ ] Un plan existe pour chaque package touché, au bon emplacement, avec l'en-tête du workflow.
- [ ] Le contrôle de cohérence du template (parties communes et parties du workflow, `## Pull requests`
      comprises) passe sur les deux plans ensemble. Montre chaque ligne.
- [ ] Chaque scénario de l'issue est dans le tableau de tests d'au moins un plan.
- [ ] `Questions non résolues` vaut `aucune` et `status` vaut `ready` dans chaque plan.
- [ ] Chaque décision technique des notes du run est dans un plan.
- [ ] Le nombre de fichiers (hors générés) est affiché, avec le détail par package.
- [ ] Chaque plan a `## Pull requests` : chaque étape est dans exactement une pull request, chaque test
      dans la pull request qui contient le code qu'il couvre (l'e2e dans celle qui expose le
      comportement), et chaque pull request passe ses tests seule.
- [ ] Une pull request frontend n'est jamais sous la pull request backend dont elle dépend.
- [ ] L'utilisateur a validé les plans et le découpage.

Au passage, dis que `/clear` puis `/feature-implementation-workflow <issue>` reprend à la phase 3 : les
plans portent l'état.
