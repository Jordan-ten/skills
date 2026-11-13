# Phase 2 — Plans

But : un plan par package touché, qui définit l'implémentation, sans question ouverte, et que
l'utilisateur a validé. Les plans sont écrits en **français**.

Méthode : `../write-implementation-plan/SKILL.md` (but, contraintes, conditions de sortie) et son
template `../write-implementation-plan/references/plan-template.md`. Applique-les, ne les recopie pas.
Le cadrage est déjà fait : les critères sont les scénarios de l'issue.

Pars des faits de code gardés après la phase 1, puis complète l'exploration. Les décisions techniques du
grill de la phase 1 vont dans `## Décisions techniques`. `## Approche` cite la fonctionnalité voisine et
ce qu'on réutilise (ou dit qu'il n'y en a pas).

## Contraintes

- Un plan par package qu'au moins une étape modifie, à l'emplacement du template. Trouve `backend/` et
  `frontend/` depuis la racine du repo (`git rev-parse --show-toplevel`), quel que soit le dossier
  courant. Crée les dossiers si besoin.
- Plan backend en premier : le plan frontend a besoin de son contrat.
- Une question que seule une autre personne peut trancher met `status: not-ready` : dis-le et n'avance
  pas.
- Mets `phase: split` dans l'en-tête quand l'utilisateur valide.

## Conditions de sortie

- [ ] Un plan existe pour chaque package touché, au bon emplacement, avec l'en-tête du workflow.
- [ ] Le contrôle de cohérence du template (parties communes et parties du workflow) passe sur les deux
      plans ensemble. Montre chaque ligne.
- [ ] Chaque scénario de l'issue est dans le tableau de tests d'au moins un plan.
- [ ] `Questions non résolues` vaut `aucune` et `status` vaut `ready` dans chaque plan.
- [ ] L'utilisateur a validé les plans.

## Compactage

Rien : tout est dans les plans.
