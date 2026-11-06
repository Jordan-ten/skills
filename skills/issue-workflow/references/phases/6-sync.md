# Phase 6 — Synchroniser l'analyse et la vue d'ensemble

But : l'analyse et la page reflètent les scénarios validés, les parcours validés et les issues créées.

## Travail

1. **Analyse.** Lis l'étape 4 de `../analyze-pitch/SKILL.md` et applique-la avec le milestone du fichier
   d'état (`--milestone`). Dis à l'utilisateur ce que tu vas changer, puis modifie seulement :
   - `milestone:` dans l'en-tête,
   - la section « Already covered by existing issues » (une ligne par tâche, avec l'issue, son état et la
     couverture) et la ligne « Tasks with no matching issue ».

   Ne change aucun scénario : ils sont déjà à jour depuis la phase 4. Ne modifie rien sur GitHub.
2. **Vue d'ensemble.** Lis `../build-scenario-overview/SKILL.md` et lance-le en mise à jour, avec
   `--milestone <milestone> --refresh-tickets` : réponds « mettre à jour » à son étape 2, c'est-à-dire
   rafraîchir les tâches (scénarios venant de l'analyse), les tickets, et garder les parcours validés en
   phase 4. Saute sa boucle de corrections de parcours (étape 5) : ils sont déjà validés. Construis, puis
   publie vers le même `artifactUrl`.
3. Mets `phase: done` dans le fichier d'état.

## Conditions de sortie

- [ ] Le tableau « Already covered by existing issues » de l'analyse liste chaque issue du fichier d'état.
- [ ] Dans `<slug>.overview.json`, chaque tâche qui a une issue a son `ticket`, et le nombre de scénarios par
      tâche est le même que dans l'analyse.
- [ ] Les parcours de la page sont ceux validés en phase 4.
- [ ] `build_overview.py` se termine sans `error:`.
- [ ] La page est republiée au même lien, ou l'utilisateur a refusé de publier.
- [ ] Le rapport final est donné : lien, nombres (tâches, Must, tickets, parcours), tâches `Must` sans ticket
      (il ne doit plus y en avoir sans choix explicite), tâches dans aucun parcours.

À la fin, dis la suite : chaque issue s'implémente avec `/feature-implementation-workflow <issue>`.
La phase 6 est la dernière : pas de compactage.
