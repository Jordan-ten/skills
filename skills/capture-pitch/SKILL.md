---
name: capture-pitch
description: Slash-only. À utiliser uniquement quand l'utilisateur lance explicitement /capture-pitch avec le nom ou l'URL Notion d'un pitch. Sauvegarde une copie locale d'un pitch PM depuis Notion. Ne jamais déclencher depuis une demande en langage naturel.
disable-model-invocation: true
allowed-tools: Read, Write, Bash, Glob, AskUserQuestion
---

# Capture Pitch

Les fichiers de pitch sont dans `.claude/plans/pitch/`, relatif au répertoire de travail courant (`backend/` ou `frontend/`).

Sauvegarde une copie locale d'un pitch PM depuis Notion. La copie sert d'entrée pour écrire les tickets, les plans et `/analyze-pitch`.

Ce skill copie. Il n'interprète pas, ne résume pas, ne juge pas.

## Arguments

`$ARGUMENTS` — nom du pitch ou URL Notion. Si vide, demande à l'utilisateur.

## Étapes

1. **Trouver le pitch.** Suis le skill `tnx-doc-notion-access` pour lire Notion.
   - URL donnée : récupère la page.
   - Nom donné : cherche. S'il y a plusieurs résultats, liste-les et demande à l'utilisateur de choisir.
2. **Lire les sous-pages.** Récupère chaque sous-page et chaque lien interne du pitch. Cherche d'abord « Main User Tasks », « User Tasks », « Tâches utilisateur » et les pages de détail par catégorie ou par tâche.
3. **Écrire la capture.** Chemin : `.claude/plans/pitch/<pitch-slug>.md`.
   - `<pitch-slug>` : titre du pitch, en minuscules, espaces remplacés par des tirets, sans date (le nom doit rester stable).
   - Si le fichier existe, dis à l'utilisateur qu'il va être rafraîchi, puis écrase-le.
   - Crée le dossier si besoin.
4. **Rapporter.** Donne le chemin du fichier, le nombre de sous-pages lues et le nombre de tâches trouvées. Rien d'autre.

## Format du fichier

```markdown
---
title: <pitch title>
source_url: <Notion URL>
fetched_at: <YYYY-MM-DD HH:mm>
---

# <pitch title>

<pitch content, copied as written, same language, same section titles>

## Main User Tasks

| Category | MoSCoW | Task | Details |
|----------|--------|------|---------|
| ...      | Must   | ...  | ...     |

## Sub-pages

### <sub-page title>

<sub-page content, copied as written>
```

## Règles

- Copie les mots du PM. Ne réécris pas, ne raccourcis pas, ne traduis pas.
- Garde la valeur MoSCoW telle qu'écrite dans Notion (Must / Should / Could / Won't, ou 1 à 4).
- N'explore pas le code. N'ajoute ni lexique, ni scénarios, ni questions. C'est le travail de `/analyze-pitch`.
- Si une partie du pitch ne peut pas être lue (permission, page vide), écris `> Not captured: <reason>` à sa place.
