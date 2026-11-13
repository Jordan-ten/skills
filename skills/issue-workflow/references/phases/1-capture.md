# Phase 1 — Capturer le pitch

But : une copie locale fidèle du pitch Notion, avec la liste de ses tâches, et le fichier d'état du workflow.

Utilise `${CLAUDE_PLUGIN_ROOT}/skills/capture-pitch/SKILL.md` (entrée : le nom ou l'URL donnés à
`/issue-workflow`).

Contraintes :
- Si une capture existe, montre sa date `fetched_at` et demande `Rafraîchir` / `Garder cette capture`.
  Ne rafraîchis pas sans réponse.
- Ne modifie jamais le contenu copié. N'explore pas le code ici.
- Crée `.claude/plans/pitch/<slug>.workflow.md` (format dans `SKILL.md`) avec `phase: analyse`. Le
  tableau des tâches est rempli en phase 2, celui des parcours en phase 4.

## Conditions de sortie

- [ ] `.claude/plans/pitch/<slug>.md` existe, avec `source_url` et `fetched_at` dans l'en-tête.
- [ ] La capture est à jour, ou l'utilisateur a choisi de garder l'ancienne.
- [ ] Le nombre de sous-pages lues et de tâches trouvées est affiché.
- [ ] Chaque `> Not captured: <raison>` est listé à l'utilisateur, qui a dit s'il bloque ou non.
- [ ] Le fichier d'état existe avec `pitch:` et `phase: analyse`.
- [ ] Les choix de l'utilisateur (rafraîchir ou garder, parties non capturées) sont dans le fichier d'état
      ou la capture.
