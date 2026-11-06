# Phase 1 — Capturer le pitch

But : une copie locale fidèle du pitch Notion, avec la liste de ses tâches.

## Travail

1. Lis `../capture-pitch/SKILL.md` et suis-le (il est en slash uniquement : tu ne peux pas l'appeler).
   Entrée : le nom ou l'URL Notion donnés à `/issue-workflow`.
2. Si une capture existe déjà, montre sa date `fetched_at` et demande : `Rafraîchir` / `Garder cette
   capture`. Ne rafraîchis pas sans réponse.
3. Crée le fichier d'état `.claude/plans/pitch/<slug>.workflow.md` (format dans `SKILL.md`) avec
   `phase: analyse`. Le tableau des tâches est rempli en phase 3, à partir de l'analyse.

Ne modifie jamais le contenu copié. N'explore pas le code ici.

## Conditions de sortie

- [ ] `.claude/plans/pitch/<slug>.md` existe et son en-tête a `source_url` et `fetched_at`.
- [ ] La capture est à jour, ou l'utilisateur a choisi de garder l'ancienne.
- [ ] Le nombre de sous-pages lues et le nombre de tâches trouvées sont affichés.
- [ ] Chaque `> Not captured: <raison>` de la capture est listé à l'utilisateur, qui a dit s'il bloque ou non.
- [ ] Le fichier d'état existe avec `pitch:` et `phase: analyse`.

## Compacter après cette phase

Garde : le slug du pitch, l'URL Notion, les nombres de sous-pages et de tâches, les parties non capturées.
Jette : le contenu des pages Notion lues.

```
/compact Garde : pitch <slug> ; URL Notion ; nombre de sous-pages et de tâches ; parties non capturées. Jette : le contenu des pages Notion. La capture est dans .claude/plans/pitch/.
```
