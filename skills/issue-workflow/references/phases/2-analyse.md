# Phase 2 — Analyser le pitch

But : un premier jet d'analyse : résumé, lexique ancré dans le code, scénarios de chaque tâche gardée.
Ce jet sera validé en phase 4 : ne cherche pas la perfection ici.

## Travail

1. Lis `../analyze-pitch/SKILL.md` et suis ses étapes 1, 2, 3 et 5 (lire la capture, demander les niveaux
   MoSCoW, lire le code pour le lexique, écrire l'analyse).
2. Demande une fois si un milestone GitHub existe déjà pour ce pitch. Si oui, passe-le à l'étape 4 de
   `analyze-pitch` (`--milestone`) et note-le dans `milestone:` du fichier d'état. Sinon, `milestone: none` :
   il sera choisi en phase 5.
3. Écarts avec `analyze-pitch` : ne lance pas la boucle de corrections de son étape 6. À la place, donne le
   chemin, les titres de sections et le nombre de scénarios, puis passe au gate. La validation se fait en
   phase 4.
4. Mets `phase: overview` dans le fichier d'état.

## Conditions de sortie

- [ ] `.claude/plans/pitch/<slug>.analysis.md` existe, avec l'en-tête (`capture`, `capture_fetched_at`,
      `moscow`, `generated_at`).
- [ ] Les niveaux MoSCoW gardés sont notés dans l'en-tête. Une tâche sans priorité dans Notion a sa priorité
      dans `Decisions`.
- [ ] Chaque tâche gardée a au moins un scénario `Nominal case`.
- [ ] Le lexique n'emploie que des mots du code, ou marque les mots nouveaux.
- [ ] Les questions ouvertes sont listées dans `Open questions`.
- [ ] Le nombre de scénarios par tâche est affiché.

## Compacter après cette phase

Garde : le slug, le milestone (ou `none`), les niveaux MoSCoW gardés, le nombre de tâches et de scénarios,
les questions ouvertes de l'analyse (une ligne chacune).
Jette : le contenu du code lu pour le lexique, la capture lue en entier.

```
/compact Garde : pitch <slug> ; milestone ; niveaux MoSCoW gardés ; nombre de tâches et de scénarios ; questions ouvertes en une ligne. Jette : fichiers de code lus, capture lue en entier. Tout est dans .claude/plans/pitch/.
```
