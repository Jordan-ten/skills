---
name: issue-workflow
description: >
  Slash uniquement. À utiliser seulement quand l'utilisateur lance explicitement /issue-workflow avec
  le nom ou l'URL Notion d'un pitch. Mène un pitch PM jusqu'aux issues GitHub en six phases, chacune
  avec des conditions de sortie à prouver avant la suivante : capturer le pitch, l'analyser (premiers
  scénarios), construire la vue d'ensemble des lots et des tâches du pitch avec leurs scénarios et les
  parcours, raffiner et compléter les scénarios avec l'utilisateur puis valider les parcours, créer une
  issue par tâche, puis resynchroniser l'analyse et la vue d'ensemble. Les lots et les tâches viennent du
  pitch : le workflow ne les redécoupe pas. Reprenable : relancer la commande sur le même pitch continue là où on s'est arrêté.
  Ne jamais déclencher depuis une demande en langage naturel.
disable-model-invocation: true
allowed-tools: Bash(gh *), Bash(git *), Bash(python3 *), Read, Write, Edit, Glob, Grep, Agent, AskUserQuestion, Skill, Artifact
---

# Workflow du pitch aux issues

Du pitch Notion aux issues GitHub. Le workflow est découpé en phases. Une phase se termine seulement
quand ses conditions de sortie sont vraies et prouvées. Ensuite l'utilisateur décide de continuer.

Il enchaîne des skills existants et ne recopie pas leurs règles : `capture-pitch`, `analyze-pitch`,
`build-scenario-overview` et `tnx-plan-create-issue`. Ces skills sont en slash uniquement (ou à
déclencher explicitement) : lis leur `SKILL.md` et suis-le, avec les écarts écrits dans les fichiers de phase.

Les issues créées ici sont ensuite implémentées avec `/feature-implementation-workflow <issue>`.

Entrée : `/issue-workflow <nom-ou-url-notion-du-pitch>`.

Les fichiers du pitch sont dans `.claude/plans/pitch/`, relatif au dossier de travail courant
(`backend/` ou `frontend/`). Le workflow s'exécute toujours depuis le même dossier.

## Langues

| Texte | Langue |
|---|---|
| Échanges avec l'utilisateur, y compris tout le raffinement | français |
| Capture, analyse, vue d'ensemble | celle de leur skill (capture : langue du pitch ; analyse : langue du pitch ; page : français) |
| Fichier d'état du workflow | français |
| Issues GitHub (titre, corps, commentaires) | anglais simple |

## Phases

Chaque phase a un fichier dans `references/phases/`. Lis le fichier d'une phase quand tu y entres, pas avant.

| # | Phase | Skill appelé | Conditions de sortie (toutes vraies et prouvées) | Fichier |
|---|---|---|---|---|
| 1 | Capturer | `capture-pitch` | La capture existe, à jour ou gardée par choix, et tout ce qui n'a pas pu être lu est connu. | `1-capture.md` |
| 2 | Analyser | `analyze-pitch` | L'analyse existe avec un premier jet de scénarios pour chaque tâche gardée. | `2-analyse.md` |
| 3 | Vue d'ensemble | `build-scenario-overview` | Les lots et les tâches du pitch, tels quels, avec leurs scénarios et un premier jet de parcours, sont construits et publiés. | `3-overview.md` |
| 4 | Raffiner et compléter | — | Les scénarios de chaque tâche sont complétés à partir de l'analyse et validés (ou la tâche est hors périmètre). Chaque parcours est validé. L'analyse est à jour. | `4-refine.md` |
| 5 | Créer les issues | `tnx-plan-create-issue` | Chaque tâche validée a une issue (ou un choix explicite d'absence), vérifiée sur GitHub. | `5-issues.md` |
| 6 | Synchroniser | `analyze-pitch`, `build-scenario-overview` | L'analyse et la vue d'ensemble reflètent les scénarios, les parcours et les issues créées. | `6-sync.md` |

## Fichier d'état

`.claude/plans/pitch/<slug>.workflow.md`, créé en phase 1, tenu à jour par chaque phase :

```markdown
---
pitch: <slug>
phase: capture | analyse | overview | refine | issues | sync | done   # prochaine phase à lancer
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

`Scénarios validés` : `oui`, `non` ou `hors périmètre`. `Issue` : `#<numéro>`, `existante #<numéro>`,
`aucune (choix)` ou `—`. Les numéros `n` sont ceux du tableau du pitch.

## Passage d'une phase à l'autre

À la fin d'une phase :

1. Affiche les conditions de sortie sous forme de liste. Chaque ligne : ✅ ou ❌, et la preuve en
   quelques mots (fichier et section, commande et résultat). Une condition sans preuve est ❌.
2. Tout est ✅ : mets à jour le fichier d'état (`phase:`). Puis pose une seule `AskUserQuestion` :
   `Compacter, puis passer à la phase <n+1>` (recommandé) / `Passer à la phase <n+1> sans compacter` /
   `Refaire quelque chose` / `Arrêter`.
3. Un ❌ : corrige-le, ou reviens à la phase qui possède la cause. Ne propose jamais de continuer avec
   un ❌.

Ne saute jamais une phase et ne commence jamais la suivante avant le passage.

## Compacter entre les phases

But : jeter ce dont la phase suivante n'a pas besoin. Le modèle ne peut pas lancer `/compact` lui-même.

Sur `Compacter, puis passer à la phase <n+1>` :

1. Lis la section `Compacter après cette phase` du fichier de la phase qui se termine.
2. Affiche la ligne `/compact` de cette section, dans un seul bloc de code, prête à coller. Dis en une
   ligne ce qu'elle garde et ce qu'elle jette.
3. Arrête-toi et attends. L'utilisateur lance la ligne, puis dit `continue` (ou relance la commande de ce
   skill). Suis alors « Reprise ».

Garde seulement les faits qui ne sont dans aucun fichier. Ne garde jamais un contenu de fichier, une
sortie de commande ou le contenu de pages Notion : on peut les relire. Après un compactage, fais
confiance aux fichiers (capture, analyse, vue d'ensemble, fichier d'état, GitHub), pas au souvenir de
l'ancienne conversation.

## Reprise

1. Lis `.claude/plans/pitch/<slug>.workflow.md`. Absent : commence à la phase 1.
2. Ne fais pas confiance à `phase:`. Revérifie les conditions de sortie de la phase juste avant. Si l'une
   échoue, reviens à cette phase et dis pourquoi.
3. Dis à l'utilisateur où le run reprend, puis continue.

## Règles

- Réponds en français. Le texte écrit dans les issues est en anglais simple (voir « Langues »).
- Le produit s'appelle Tennaxia (règle de nommage de `AGENTS.md`).
- Les lots et les tâches viennent du tableau « Main User Tasks » du pitch, déjà découpé. Ne les redécoupe
  pas, ne les renomme pas, n'en ajoute pas, n'en fusionne pas. Un changement de lot ou de tâche est une
  demande au PM : note-la dans `Open questions` de l'analyse. Le travail du workflow porte sur les
  scénarios et les parcours.
- N'invente jamais un scénario, une règle métier ou un numéro d'issue. Un cas que le pitch ne dit pas est
  une proposition : c'est l'utilisateur qui décide. Une capacité absente du pitch devient une question
  pour le PM dans `Open questions` de l'analyse, jamais une tâche.
- Une question dont le code connaît la réponse ne se pose pas. Explore d'abord, ne demande que des décisions.
- Une seule question à la fois avec `AskUserQuestion`. La réponse recommandée est la première option.
- Aucune écriture sur Notion. Avant la phase 5, aucune écriture sur GitHub.
- Les actions vers l'extérieur (créer des issues, publier la page) n'ont lieu qu'après un oui donné dans la
  phase.
- La capture n'est jamais modifiée. Les corrections vont dans l'analyse.
