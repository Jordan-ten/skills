---
name: issue-workflow
description: >
  Slash uniquement. À utiliser seulement quand l'utilisateur lance explicitement /issue-workflow avec
  le nom ou l'URL Notion d'un pitch. Mène un pitch PM jusqu'aux issues GitHub en six phases, chacune
  avec des conditions de sortie à prouver : capture, analyse, scénarios, parcours et vue d'ensemble,
  création des issues. Reprenable : relancer la commande continue là où on s'est arrêté. Ne jamais
  déclencher depuis une demande en langage naturel.
disable-model-invocation: true
allowed-tools: Bash(gh *), Bash(git *), Bash(python3 ${CLAUDE_PLUGIN_ROOT}/skills/build-scenario-overview/scripts/*), Read, Write, Edit, Glob, Grep, Agent, AskUserQuestion, Skill, Artifact
---

# Workflow du pitch aux issues

But : passer d'un pitch Notion à une issue GitHub par tâche, avec des scénarios et des parcours validés
par l'utilisateur. Ensuite chaque issue s'implémente avec `/feature-implementation-workflow <issue>`.

Entrée : `/issue-workflow <nom-ou-url-notion-du-pitch>`.

Le workflow a cinq phases. Chaque phase a un but et des conditions de sortie : elle se termine seulement
quand elles sont vraies et prouvées. Ensuite l'utilisateur décide de continuer. Lis le fichier d'une phase
quand tu y entres, pas avant.

| # | Phase | Skill utilisé | Fichier |
|---|---|---|---|
| 1 | Capturer le pitch | `capture-pitch` | `1-capture.md` |
| 2 | Analyser (premier jet de scénarios) | `analyze-pitch` | `2-analyse.md` |
| 3 | Construire et valider les scénarios | — | `3-scenarios.md` |
| 4 | Valider les parcours, construire et publier la vue d'ensemble | `build-scenario-overview` | `4-parcours.md` |
| 5 | Créer une issue par tâche, puis mettre à jour analyse et page | `tnx-plan-create-issue`, `analyze-pitch`, `build-scenario-overview` | `5-issues.md` |

Fichiers de phase : `${CLAUDE_PLUGIN_ROOT}/skills/issue-workflow/references/phases/`.

## Skills appelés

Les skills `capture-pitch`, `analyze-pitch` et `build-scenario-overview` sont en slash uniquement. Lis
leur `SKILL.md` dans `${CLAUDE_PLUGIN_ROOT}/skills/<nom>/SKILL.md` et suis-le, avec les écarts écrits dans
le fichier de phase. Ne recopie pas leurs règles.

Les fichiers du pitch sont dans `.claude/plans/pitch/`, relatif au dossier de travail courant
(`backend/` ou `frontend/`). Le workflow s'exécute toujours depuis le même dossier.

## Fichier d'état

`.claude/plans/pitch/<slug>.workflow.md`, créé en phase 1, tenu à jour par chaque phase. C'est la mémoire
du workflow : il permet la reprise.

```markdown
---
pitch: <slug>
phase: capture | analyse | scenarios | parcours | issues | done   # prochaine phase à lancer
milestone: <titre ou numéro, ou none>
updated_at: <AAAA-MM-JJ HH:mm>
---

## Réglages communs
<rempli en phase 5 : milestone, équipe, labels, priorité par niveau MoSCoW, planning, assignation>

## Tâches

| n | Titre | Lot | MoSCoW | Scénarios validés | Issue |
|---|---|---|---|---|---|
| 1 | ... | 1 | Must | non | — |

## Parcours

| id | Titre | Validé |
|---|---|---|
| p1 | ... | non |
```

Le tableau `Tâches` est rempli en phase 2, le tableau `Parcours` en phase 4.
`Scénarios validés` : `oui`, `non` ou `hors périmètre`. `Issue` : `#<numéro>`, `existante #<numéro>`,
`aucune (choix)` ou `—`. Les numéros `n` sont ceux du tableau du pitch.

## Passage d'une phase à l'autre

À la fin d'une phase :

1. Affiche les conditions de sortie en liste. Chaque ligne : ✅ ou ❌, et la preuve en quelques mots
   (fichier et section, commande et résultat). Une condition sans preuve est ❌.
2. Tout est ✅ : mets à jour `phase:` dans le fichier d'état, puis pose une seule `AskUserQuestion` :
   `Clear, puis passer à la phase <n+1>` / `Passer à la phase <n+1>` / `Refaire quelque chose` /
   `Arrêter`. Recommande `Clear` après les phases 1 et 2 et après chaque lot de tâches de la phase 3 ;
   recommande `Passer` sinon.
3. Un ❌ : corrige-le, ou reviens à la phase qui possède la cause. Ne propose jamais de continuer avec un ❌.

Ne saute jamais une phase et ne commence jamais la suivante avant ce passage.

## Garder un contexte léger

Tout le workflow se joue en une session. Les fichiers sont la mémoire (capture, analyse, vue d'ensemble,
fichier d'état, GitHub) : un `/clear` ne perd rien si tout est écrit. On n'utilise pas `/compact` : un
résumé perd des détails et garde un souvenir périmé.

- **Avant chaque gate** : toute décision de l'utilisateur est écrite dans un fichier. C'est une condition
  de sortie de chaque phase.
- **Sur `Clear`** : dis à l'utilisateur de lancer `/clear` (le modèle ne peut pas le faire), puis de relancer
  `/issue-workflow <pitch>`. Arrête-toi. Au retour, suis « Reprise ».
- **Subagents** : pour lire beaucoup et rendre peu (code du lexique en phase 2, code d'une tâche en phase 3).
  Les questions et les décisions restent dans l'agent principal, ainsi que toute la phase 5 (écritures
  GitHub irréversibles).
- Après un `/clear`, fais confiance aux fichiers, jamais au souvenir.

## Reprise

1. Lis `.claude/plans/pitch/<slug>.workflow.md`. Absent : commence à la phase 1.
2. Ne fais pas confiance à `phase:`. Revérifie les conditions de sortie de la phase juste avant. Si l'une
   échoue, reviens à cette phase et dis pourquoi.
3. Dis à l'utilisateur où le run reprend, puis continue.

## Règles

- Réponds en français. Les issues (titre, corps, commentaires) sont en anglais simple.
- Le produit s'appelle Tennaxia (règle de nommage de `AGENTS.md`).
- Les lots et les tâches viennent du tableau « Main User Tasks » du pitch. Ne les redécoupe pas, ne les
  renomme pas, n'en ajoute pas, n'en fusionne pas. Un changement est une demande au PM : note-la dans
  `Open questions` de l'analyse. Le travail du workflow porte sur les scénarios et les parcours.
- N'invente jamais un scénario, une règle métier ou un numéro d'issue. Un cas que le pitch ne dit pas est
  une proposition : l'utilisateur décide. Une capacité absente du pitch devient une question pour le PM
  dans `Open questions`, jamais une tâche.
- Une question dont le code connaît la réponse ne se pose pas. Explore d'abord, ne demande que des décisions.
- Une seule question à la fois avec `AskUserQuestion`. La réponse recommandée est la première option.
- Aucune écriture sur Notion. Avant la phase 5, aucune écriture sur GitHub. Les actions vers l'extérieur
  (créer des issues, publier la page) n'ont lieu qu'après un oui donné dans la phase.
- La capture n'est jamais modifiée. Les corrections vont dans l'analyse.
