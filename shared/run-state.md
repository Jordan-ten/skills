# Fichier de run

Règle commune des workflows en phases (`feature-implementation-workflow`, `bug-fix-workflow`).
`issue-workflow` a son propre fichier d'état (`<slug>.workflow.md`) et applique les mêmes règles de
passage, de `/clear` et de `--phase`.

Le fichier de run dit **où reprendre** : la phase, et la prochaine action. Il permet un `/clear` à
n'importe quel moment, sans perte. Il ne contient ni comportement, ni plan, ni diff.

## Emplacement

`<racine>/<package>/.claude/plans/<n>.run.md`, à côté des notes du run (`<n>.notes.md`). `<racine>` vient
de `git rev-parse --show-toplevel`, `<package>` est le dossier où la première phase tourne (`backend` ou
`frontend`), `<n>` est le numéro de l'issue. Ce dossier est hors commit : le fichier ne finit jamais dans
une pull request. Un seul fichier par run, même quand il y a deux packages.

## Format

```markdown
---
workflow: feature | bug
issue: <n>
phase: <phase à lancer ou à continuer>
status: ready | in-progress | done
next_action: <une phrase : quoi faire, où>
updated_at: <AAAA-MM-JJ HH:mm>
---

## Phases terminées

| Phase | Terminée le | Preuve |
|---|---|---|
| plan | 2026-11-16 | plans validés, découpage validé |

## Fichiers

- Issue : <url>
- Notes : <chemin>
- Plans : <chemins>
- Branches : <branche> (<sha>), ...

## Décisions et points ouverts

- <ce qui n'est écrit nulle part ailleurs : décision, question en attente, piège rencontré>
```

- `phase` : `reproduce` (bug seulement, première phase), puis `plan`, `implement`, `verify`, `ship`, `done`.
  Mêmes valeurs que le `phase:` des plans à partir de `plan`.
- `status` : `ready` = la phase n'est pas commencée ; `in-progress` = elle est commencée ;
  `done` = le run est clos.
- `next_action` : assez précise pour reprendre sans rien relire. Exemple : « Phase implement, PR 2 du plan
  backend, étape 3 : `Avancement` dit `en cours : étapes 1-2 (a1b2c3d)` ».
- `Phases terminées` : une ligne par phase, avec la preuve en quelques mots (les ✅ de la phase).
- `Décisions et points ouverts` : court. Ce qui est déjà dans l'issue, les notes ou un plan n'est pas recopié.

## Quand l'écrire

1. **Création** : dans la première phase (`reproduce` pour un bug, `plan` pour une feature), dès le
   premier point d'étape (voir 3).
2. **Passage de phase** : après le tableau de conditions, tout ✅, **avant** l'`AskUserQuestion`. Mets
   `phase` à la phase suivante, `status: ready`, ajoute la ligne dans `Phases terminées`.
3. **Pendant une phase longue** : mets à jour `status: in-progress` et `next_action` après chaque décision
   validée (phases de cadrage : `reproduce`, `plan`) et après chaque pull request terminée (`implement`).
4. **Fin du run** (fin de la phase `ship`) : `phase: done`, `status: done`.

Le fichier de run résume. Les sources restent l'issue, les plans (`phase:`, `Avancement`) et git. En cas de
désaccord, les sources gagnent : corrige le fichier de run.

## Passage de phase et `/clear`

La question de passage a ces options, dans cet ordre :

1. `Clear, puis passer à la phase <n+1>` : **toujours recommandée** (le fichier de run porte l'état, et un
   contexte qui grossit se repaie à chaque message) ;
2. `Passer à la phase <n+1>` : seulement si la phase suivante est très courte et que `/context` est bas ;
3. `Refaire quelque chose` ;
4. `Arrêter`.

Si la phase se termine par un `Clear` : le fichier de run est déjà écrit. Dis à l'utilisateur de lancer
`/clear`, puis donne la commande exacte à relancer, par exemple
`/feature-implementation-workflow 123`, avec la phase de reprise en une ligne. Le modèle ne peut pas lancer
`/clear` lui-même. Arrête-toi. Pas de `/compact` : un résumé garde des souvenirs périmés.

## Reprise

La commande d'entrée accepte `--phase <nom>` après l'issue (exemple :
`/bug-fix-workflow 123 --phase verify`).

1. Cherche `<n>.run.md` dans `backend/.claude/plans/` et `frontend/.claude/plans/` (ou le dossier courant
   s'il est un package).
2. **Fichier présent** : lis-le, puis lis l'issue et les plans qu'il pointe. Ne lis rien d'autre pour
   décider de la phase.
3. **Fichier absent** : déduis la phase comme avant (aucun plan : première phase ; sinon la plus petite `phase:`
   des plans), puis crée le fichier de run.
4. Compare le fichier aux sources (`phase:` des plans, `Avancement`, `git log` de la branche, date de
   l'issue contre `issue_updated_at`). Désaccord : prends la phase la plus ancienne, corrige le fichier et
   dis pourquoi.
5. Revérifie les conditions de sortie de la phase **juste avant** celle de reprise. Si l'une échoue, reviens
   à cette phase et dis pourquoi.
6. **`--phase`** : l'utilisateur choisit la phase. Applique les points 1 à 4, puis dis quelles conditions
   des phases précédentes ne sont pas prouvées, sans bloquer. Mets `phase` et `status: ready` dans le
   fichier.
7. Dis où le run reprend (phase, `next_action`), puis continue.

Après un `/clear`, fais confiance aux fichiers (run, issue, plans, notes, git), pas au souvenir.
