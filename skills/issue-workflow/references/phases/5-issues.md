# Phase 5 — Créer une issue par tâche

But : une issue GitHub par tâche validée, créée avec `tnx-plan-create-issue`, sans doublon. C'est la
première phase qui écrit sur GitHub : rien n'est créé avant un oui.

Langue : les issues sont en **anglais simple**. L'analyse peut être dans la langue du pitch : traduis le
titre et les scénarios en anglais simple avant de les mettre dans l'issue. Les mots-clés `Given`, `When`,
`Then` restent tels quels.

## Travail

1. **Chercher l'existant.** Lecture seule :
   `gh issue list --milestone "<milestone>" --state all --json number,title,state` (et la section
   « Already covered by existing issues » de l'analyse). Une tâche déjà couverte : demande `Réutiliser
   #<n>` / `Créer quand même` / `Pas d'issue`. Note le choix dans le fichier d'état (`existante #n` ou
   `aucune (choix)`).
2. **Réglages communs, une seule fois** (`AskUserQuestion`, 4 questions maximum par lot, ≤ 4 options) :
   milestone (il doit exister : sinon dis-le et arrête-toi, ne le crée pas), équipe, labels, priorité par
   niveau MoSCoW (recommandé : Must → P1, Should → P2, Could → P3), planning, assignation. Écris les
   réglages dans `Réglages communs` du fichier d'état et mets le milestone dans `milestone:`.
3. **Préparer les issues.** Pour chaque tâche à créer, prépare titre et corps selon
   `references/issue-from-task.md`. Montre le tableau : n, titre de l'issue, Type, priorité, nombre de
   scénarios.
4. **Valider le contenu.** Montre les corps complets par lot de 5 issues au plus, avec une question par lot :
   `Créer ces issues` / `Changer quelque chose`. Boucle jusqu'au oui. C'est la validation du contenu que
   `tnx-plan-create-issue` demande à son étape 3 : ne la redemande pas ensuite.
5. **Créer.** Pour chaque tâche validée, une par une : lis
   `<racine du repo>/.claude/skills/tnx-plan-create-issue/SKILL.md` (`git rev-parse --show-toplevel`) et suis
   ses étapes 1, 5, 6, 7, 8 et 9 :
   - formulaire : le template `feature-checklist` (Type `Feature`), body préparé à l'étape 3 ;
   - saute son étape 3 (contenu déjà validé) et son étape 4 (réglages déjà donnés : utilise ceux de
     `Réglages communs`) ;
   - n'utilise jamais « Yes, and start right away » : aucune branche n'est créée ici.
   Après chaque création, écris `#<numéro>` dans la ligne de la tâche du fichier d'état, avant de passer à
   la suivante.
6. **Échec.** Arrête-toi à la première erreur et rapporte-la. Avant de recréer quoi que ce soit, relance la
   recherche de l'étape 1 : une création a pu réussir sans que le numéro soit noté.

Mets `phase: sync` dans le fichier d'état quand tout est fait.

## Conditions de sortie

- [ ] Chaque tâche `oui` a dans le fichier d'état `#<numéro>`, `existante #<numéro>` ou `aucune (choix)`.
- [ ] Chaque numéro créé répond à `gh issue view <n>` et a le bon milestone, le bon Type et les bons champs du
      board (prouve avec le rapport de `tnx-plan-create-issue`).
- [ ] Le texte de chaque issue créée est en anglais simple.
- [ ] Aucune tâche n'a deux issues : relis `gh issue list` du milestone et compare avec le fichier d'état.
- [ ] L'utilisateur a dit oui avant la première création.

## Compacter après cette phase

Garde : le slug, le milestone, les numéros d'issues créées par tâche, les échecs éventuels.
Jette : les corps d'issues préparés, les sorties de `gh`, les réponses du formulaire.

```
/compact Garde : pitch <slug> ; milestone ; numéros d'issues par tâche ; échecs éventuels. Jette : corps d'issues préparés, sorties de gh, réglages déjà notés. L'état est dans .claude/plans/pitch/<slug>.workflow.md.
```
