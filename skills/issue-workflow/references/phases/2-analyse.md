# Phase 2 — Analyser le pitch

But : un premier jet d'analyse : résumé, lexique ancré dans le code, scénarios de chaque tâche gardée.
Il sera validé en phase 3 : ne cherche pas la perfection ici.

Utilise `${CLAUDE_PLUGIN_ROOT}/skills/analyze-pitch/SKILL.md`, étapes 1, 2, 3 et 5 (lire la capture,
niveaux MoSCoW, lexique ancré dans le code, écrire l'analyse).

Contraintes :
- **Subagent pour le code** : l'étape 3 (lexique) lit beaucoup de code. Confie-la à un subagent `Explore`
  avec les termes du pitch. Demande en retour un tableau court « terme du pitch → terme du code → fichier »,
  plus la liste des mots absents du code. Écris le lexique toi-même dans l'analyse.
- Demande une fois si un milestone GitHub existe déjà pour ce pitch. Si oui, passe-le à `analyze-pitch`
  (`--milestone`) et note-le dans `milestone:` du fichier d'état. Sinon `milestone: none` : il sera choisi
  en phase 5.
- Ne lance pas la boucle de corrections de l'étape 6 d'`analyze-pitch` : donne le chemin, les titres de
  sections et le nombre de scénarios. La validation se fait en phase 3.
- Remplis le tableau `Tâches` du fichier d'état : numéro, titre, lot (tableau « Main User Tasks » de la
  capture), MoSCoW, `Scénarios validés : non`, `Issue : —`. Mets `phase: scenarios`.

## Conditions de sortie

- [ ] `.claude/plans/pitch/<slug>.analysis.md` existe, avec l'en-tête (`capture`, `capture_fetched_at`,
      `moscow`, `generated_at`).
- [ ] Les niveaux MoSCoW gardés sont notés dans l'en-tête. Une tâche sans priorité dans Notion a sa priorité
      dans `Decisions`.
- [ ] Chaque tâche gardée a au moins un scénario `Nominal case`.
- [ ] Les questions ouvertes sont dans `Open questions`.
- [ ] Le milestone et les niveaux MoSCoW choisis sont dans l'analyse et le fichier d'état.
