# Phase 3 — Vue d'ensemble : lots et tâches du pitch, scénarios, parcours

But : une vue d'ensemble publiée qui montre les lots et les tâches du pitch avec leurs scénarios, pour voir
ce qu'il faut compléter avant de raffiner. Les lots et les tâches ne sont pas discutés : ils viennent du
pitch. Les parcours sont un premier jet.

## Travail

1. Lis `../build-scenario-overview/SKILL.md` et suis ses étapes 1, 2, 3, 4, 6 et 7 (lire les entrées,
   vue d'ensemble existante, écrire les tâches, ajouter les tickets, enregistrer et construire,
   publier). Lis aussi `../build-scenario-overview/references/data-format.md`.
2. Écarts avec `build-scenario-overview` :
   - **Lots et tâches** : recopie-les depuis le tableau « Main User Tasks » du pitch, dans son ordre, avec
     ses numéros. Ne pose aucune question sur le découpage.
   - **Étape 5** (rédiger les parcours) : rédige les parcours selon ses règles, mais ne lance pas la boucle
     de corrections jusqu'au « ok ». Montre la courte liste (titre, étapes, numéros de tâches) et les
     tâches dans aucun parcours, puis passe au gate. La validation se fait en phase 4.
   - Avant la phase 5, il n'y a en général pas de tickets : n'appelle GitHub (`gh issue list`) que si un
     milestone est noté dans le fichier d'état.
   - **Étape 7** (publier) : demande avant de publier, comme le skill. Une page privée suffit.
3. Remplis les tableaux `Tâches` et `Parcours` du fichier d'état à partir de `<slug>.overview.json`
   (`Scénarios validés` : `non`, `Validé` : `non`). Mets `phase: refine`.

## Conditions de sortie

- [ ] `<slug>.overview.json` est écrit et `build_overview.py` s'est terminé sans `error:`.
- [ ] Les lots et les tâches de la page sont ceux du pitch : mêmes numéros, même ordre, même lot (compare avec
      le tableau « Main User Tasks » de la capture). Seules les tâches non gardées par l'analyse (MoSCoW)
      manquent.
- [ ] Chaque tâche gardée a ses scénarios (ceux de l'analyse).
- [ ] Des parcours existent. Les tâches dans aucun parcours sont listées.
- [ ] La page est publiée et son lien est dans `artifactUrl` du fichier de données, ou l'utilisateur a refusé de
      publier.
- [ ] Les tableaux `Tâches` et `Parcours` du fichier d'état sont remplis, avec les mêmes numéros que le pitch.

## Compacter après cette phase

Garde : le slug, le lien de la page, le nombre de tâches par lot, les tâches dans aucun parcours.
Jette : le contenu des fichiers de données, la sortie du script de construction.

```
/compact Garde : pitch <slug> ; lien de la page ; nombre de tâches par lot ; tâches dans aucun parcours. Jette : contenu des fichiers de données, sortie du script de construction. Tout est dans .claude/plans/pitch/.
```
