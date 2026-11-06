# Phase 2 — Plans

But : un plan par package touché, qui définit l'implémentation, sans question ouverte.

Langue : les plans sont écrits en **français**.

## Travail

Écris les plans avec `references/plan-template.md`. Un package est concerné quand au moins une étape le
modifie. Chaque plan vit dans le dossier de travail de son package, dans `.claude/plans/ticket/` :

- plan backend : `backend/.claude/plans/ticket/<numéro-issue>-<slug>.md`
- plan frontend : `frontend/.claude/plans/ticket/<numéro-issue>-<slug>.md`

Trouve `backend/` et `frontend/` depuis la racine du repo (`git rev-parse --show-toplevel`), quel que
soit le dossier courant. Crée les dossiers si besoin. `sibling_plan` est un chemin relatif au plan
(`../../../../frontend/.claude/plans/ticket/<fichier>`), pour qu'il marche depuis les deux packages.

Écris le plan backend en premier : le plan frontend a besoin de son contrat. Mets `phase: split` dans
l'en-tête quand l'utilisateur valide.

Les décisions techniques prises dans le grill de la phase 1 vont dans `## Décisions techniques`.

## Conditions de sortie

- [ ] Un plan existe pour chaque package touché, dans le bon dossier, avec l'en-tête du template.
- [ ] Les plans sont écrits en français.
- [ ] Le contrôle de cohérence de `references/plan-template.md` passe sur les deux plans ensemble.
      Montre chaque ligne.
- [ ] Chaque scénario de l'issue est dans le tableau de tests d'au moins un plan.
- [ ] `Questions non résolues` vaut `aucune` et `status` vaut `ready` dans chaque plan. Une question
      que seule une autre personne peut trancher met `status: not-ready` : dis-le et n'avance pas.
- [ ] Un plan frontend a `## Design` et `## Contrat backend`.
- [ ] L'utilisateur a validé les plans.

## Compacter après cette phase

Garde : le numéro de l'issue, les chemins des plans et la `phase` de chaque plan. Tout le reste est dans
les plans.
Jette : notes d'exploration, brouillons de plan, sortie du contrôle de cohérence, le grill.

```
/compact Garde : issue <n> ; chemins des plans (backend et frontend). Jette : notes d'exploration, brouillons de plan, sortie du contrôle de cohérence, le grill. Tout est dans les fichiers de plan.
```
