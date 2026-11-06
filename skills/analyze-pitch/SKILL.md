---
name: analyze-pitch
description: Slash-only. À utiliser uniquement quand l'utilisateur lance explicitement /analyze-pitch avec le nom d'un pitch capturé. Lit une capture locale de pitch et écrit une analyse (résumé, lexique ancré dans le code, scénarios GIVEN/WHEN/THEN filtrés par MoSCoW). Ne jamais déclencher depuis une demande en langage naturel.
disable-model-invocation: true
allowed-tools: Read, Write, Bash, Glob, Grep, AskUserQuestion
---

# Analyze Pitch

Les fichiers de pitch sont dans `.claude/plans/pitch/`, relatif au répertoire de travail courant (`backend/` ou `frontend/`).

Transforme une capture locale de pitch en contexte métier : résumé, lexique, scénarios. Aucun détail d'implémentation technique.

La capture est faite par `/capture-pitch`. Ce skill n'appelle jamais Notion.

## Arguments

`$ARGUMENTS` — nom du pitch ou chemin d'une capture, puis des options. Si le pitch est vide, liste `.claude/plans/pitch/*.md` (sans `*.analysis.md`) et demande à l'utilisateur de choisir.

Option : `--milestone <title|number>` — compare les tâches choisies avec les issues d'un milestone GitHub existant. Sans cette option, le skill n'appelle jamais GitHub.

Si aucune capture n'existe, dis à l'utilisateur de lancer `/capture-pitch` d'abord et arrête-toi.

## Étapes

1. **Lire la capture.** `.claude/plans/pitch/<pitch-slug>.md`. Montre sa date `fetched_at` à l'utilisateur. Si le pitch a pu changer depuis, propose un rafraîchissement avec `/capture-pitch`.
2. **Demander les niveaux MoSCoW.** Montre les tâches groupées par catégorie avec leur priorité. Demande quels niveaux garder (`1 = Must`, `2 = Should`, `3 = Could`, `4 = Won't` ; réponses comme « 1 », « 1 et 2 », « tous »). Continue avec les tâches choisies seulement.
3. **Lire le code pour le lexique.** Fais-le en silence. Dans `backend/src/` et `frontend/src/` :
   - trouve le ou les modules NestJS du pitch (`src/<domain>/`) ;
   - note les noms déjà utilisés : entités, propriétés, types GraphQL, services, queues.
   Utilise ces noms dans le lexique. N'invente pas un nouveau mot quand le code en a déjà un.
4. **Vérifier le milestone (seulement avec `--milestone`).** Lis entièrement `../tnx-plan-refine-issue/references/milestone-context.md` et suis son contrat pour le milestone donné. Puis, pour chaque tâche choisie, cherche une issue ouverte ou fermée du milestone qui la couvre déjà. Compare sur le sens, pas seulement sur les mots. Note le numéro de l'issue et son état. Ne change aucun scénario à cause de cela. Ne modifie rien sur GitHub.
5. **Écrire l'analyse.** Chemin : `.claude/plans/pitch/<pitch-slug>.analysis.md`. Écris le fichier tout de suite, avant tout retour. N'écrase une analyse existante qu'après avoir prévenu l'utilisateur.
6. **Itérer.** Donne le chemin, les titres de sections et le nombre de scénarios. Demande des corrections (scénario, terme du lexique, périmètre). Mets à jour le fichier et redemande jusqu'à ce que l'utilisateur dise « ok ».

## Format du fichier

```markdown
---
capture: <pitch-slug>.md
capture_fetched_at: <value from the capture>
moscow: [<selected levels>]
milestone: <title or number, only with --milestone>
generated_at: <YYYY-MM-DD HH:mm>
---

# Analysis: <pitch title>

## Summary

**Problem**: ...
**Proposed solution**: ...
**In scope**: ...
**Out of scope**: ...
**Key constraints**: ...

## Lexicon

| PM term | Existing code term | Module / file | Notes |
|---------|--------------------|---------------|-------|

> New terms: pitch terms that do not exist in the code yet.

## Selected tasks (MoSCoW <levels>)

### <Category>

- [Must] <task>

## Scenarios

### <Task title>

**Context**: <short need>

#### Nominal case

GIVEN <initial state>
WHEN <user action>
THEN <observable result>

#### Edge case / Error case (if the pitch gives enough information)

GIVEN ...
WHEN ...
THEN ...

## Already covered by existing issues

Only with `--milestone`. Omit this section otherwise.

| Task | Issue | State | Note |
|------|-------|-------|------|
| <task> | #123 | open / closed | <full or partial coverage> |

Tasks with no matching issue: <list, or "none">.

## Open questions

> **[Domain]** Precise question?
> _Why it matters_: short reason
```

## Règles

- Comportement observable seulement : pas de noms de tables, de resolvers ou de migrations.
- Au moins un scénario nominal par tâche choisie.
- Sans `--milestone`, n'appelle pas GitHub.
- Une correspondance avec un milestone est un indice pour l'utilisateur. Ne retire jamais une tâche ou un scénario parce qu'une issue semble le couvrir.
- Ne modifie jamais le fichier de capture. Les corrections vont dans l'analyse.
- Écris l'analyse dans la langue du pitch.
