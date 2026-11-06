---
name: build-scenario-overview
description: Slash-only. À utiliser uniquement quand l'utilisateur lance explicitement /build-scenario-overview avec le nom d'un pitch capturé et analysé. Construit une page Artifact privée avec une vue d'ensemble des scénarios du pitch - les tâches par lot et par priorité MoSCoW avec leurs scénarios et leurs tickets GitHub, plus les parcours utilisateur de bout en bout qui relient les tâches. Ne jamais déclencher depuis une demande en langage naturel.
disable-model-invocation: true
allowed-tools: Read, Write, Bash, Glob, Grep, AskUserQuestion, Artifact
---

# Scenario Overview

Les fichiers de pitch sont dans `.claude/plans/pitch/`, relatif au répertoire de travail courant (`backend/` ou `frontend/`).

Montre les scénarios d'un pitch sur une seule page, pour vérifier en réunion qu'aucun scénario ne manque.
La page a deux vues, reliées par des pastilles cliquables :

- **Par tâche** : les tâches du pitch dans l'ordre du pitch, groupées par lot. Chaque tâche a un badge Must ou Should,
  son ticket (ou « pas de ticket »), et ses scénarios sur une ligne chacun.
- **Par parcours** : des histoires de bout en bout. Chaque étape renvoie aux tâches qu'elle utilise.

La capture vient de `/capture-pitch`, l'analyse de `/analyze-pitch`.
Ce skill n'appelle jamais Notion et n'écrit jamais sur GitHub.

## Arguments

`$ARGUMENTS` — nom ou chemin du pitch, puis des options. Si le pitch est vide, liste
`.claude/plans/pitch/*.analysis.md` et demande à l'utilisateur de choisir.

- `--milestone <title|number>` : lit les tickets de ce milestone. Par défaut : le `milestone` de l'analyse.
- `--refresh-tickets` : lit les tickets sur GitHub même si l'analyse a déjà un tableau de tickets.

Si la capture ou l'analyse manque, dis à l'utilisateur quel skill lancer d'abord et arrête-toi.

## Étapes

Lance chaque commande depuis le répertoire de travail courant. Les fichiers du pitch sont dans `.claude/plans/pitch/`.

1. **Lire les entrées.** Dans ce dossier : `<slug>.md`, `<slug>.analysis.md`, et `<slug>.overview.json`
   s'il existe. Dans l'analyse, `moscow: [1, 2, none]` veut dire que les tâches sans priorité dans Notion sont gardées aussi ;
   leur priorité est dans la section « Decisions ». Lis entièrement `references/data-format.md`. Il définit les concepts (tâche, ticket, lot, parcours,
   MoSCoW) et les règles d'écriture. Ouvre `references/example.overview.json` comme modèle.
2. **Vue d'ensemble existante.** Si `<slug>.overview.json` existe, demande : le mettre à jour (rafraîchir les tâches et les tickets, garder les
   parcours) ou recommencer. Quand l'analyse a changé, dis à l'utilisateur ce qui a changé.
3. **Écrire les tâches.** Prends les lignes du tableau du pitch « Main User Tasks » que l'analyse a gardées, dans l'ordre du tableau.
   Remplis le lot, la priorité, le titre, `where`, et les scénarios depuis l'analyse. Suis les règles de scénario.
4. **Ajouter les tickets.** Utilise le tableau de l'analyse « Already covered by existing issues ». Avec `--refresh-tickets`, ou quand
   ce tableau manque, lance `gh issue list --milestone "<title>" --state all --json number,title,state` (lecture seule).
   Renseigne `issueBaseUrl` avec `gh repo view --json url -q .url` plus `/issues/`.
5. **Rédiger les parcours.** Suis les règles de parcours. Montre-les à l'utilisateur sous forme de courte liste (titre, étapes, numéros
   de tâches) avec les tâches qui sont dans aucun parcours. Demande des corrections. Répète jusqu'à ce que l'utilisateur dise « ok ».
   Ne construis pas avant : un parcours qui oublie une tâche trompe la réunion.
6. **Enregistrer et construire.** Écris `.claude/plans/pitch/<slug>.overview.json`. Puis lance
   `python3 ${CLAUDE_PLUGIN_ROOT}/skills/build-scenario-overview/scripts/build_overview.py .claude/plans/pitch/<slug>.overview.json <scratchpad>/<slug>.overview.html`.
   Mets le HTML dans le dossier scratchpad, pas dans le repo. Corrige chaque `error:` et relance. Les avertissements vont dans le rapport.
7. **Publier.** Utilise l'outil Artifact sur le fichier HTML. Ne modifie pas la page à la main : la mise en page est dans
   `assets/overview-template.html`. Si les données ont un `artifactUrl`, publie vers cette `url` (lis-la d'abord quand cette
   conversation ne l'a pas publiée). À la première publication, passe l'icône `checklist` et une description d'une phrase.
   Écris l'URL retournée dans `artifactUrl` du fichier de données. Si l'utilisateur ne veut pas publier, arrête-toi après la
   construction et laisse `artifactUrl` comme il était.
8. **Rapporter.** Donne le lien, les nombres (tâches, Must, tickets, parcours), les tâches Must sans ticket, et les
   tâches dans aucun parcours. Dis que la page est privée tant que l'utilisateur ne la partage pas.

## Limites

- Ne modifie ni la capture ni l'analyse. Si un scénario est faux, dis-le à l'utilisateur et corrige-le d'abord dans l'analyse.
- N'invente ni numéro de ticket, ni scénario, ni règle. Marque avec le tag `ajout` ce que le pitch dit mais que l'analyse oublie.
- Le texte de la page est en français. Garde la mise en page : pour changer l'apparence, modifie le template et relance la construction.
- Le template et le fichier de données sont la source. N'écris pas une page de zéro.
