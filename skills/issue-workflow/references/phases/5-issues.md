# Phase 5 — Créer les issues et clore

But : une issue GitHub par tâche validée, créée avec `tnx-plan-create-issue`, sans doublon, puis l'analyse
et la page à jour avec les issues créées. C'est la première phase qui écrit sur GitHub : rien n'est créé
avant un oui.

Langue : les issues sont en **anglais simple**. L'analyse peut être dans la langue du pitch : traduis le
titre et les scénarios avant de les mettre dans l'issue. Les mots-clés `Given`, `When`, `Then` restent tels
quels.

Ici l'ordre est une contrainte : une création est irréversible et un échec au milieu ne doit ni créer de
doublon ni perdre un numéro.

## Étapes

1. **Chercher l'existant** (lecture seule) :
   `gh issue list --milestone "<milestone>" --state all --json number,title,state`, et la section
   « Already covered by existing issues » de l'analyse. Une tâche déjà couverte : demande `Réutiliser
   #<n>` / `Créer quand même` / `Pas d'issue`. Note le choix dans le fichier d'état (`existante #n` ou
   `aucune (choix)`).
2. **Réglages communs, une seule fois** (`AskUserQuestion`, 4 questions maximum par lot, ≤ 4 options) :
   milestone (il doit exister : sinon dis-le et arrête-toi, ne le crée pas), équipe, labels, priorité par
   niveau MoSCoW (recommandé : Must → P1, Should → P2, Could → P3), planning, assignation. Écris-les dans
   `Réglages communs` du fichier d'état et mets le milestone dans `milestone:`.
3. **Préparer** titre et corps de chaque issue selon `${CLAUDE_PLUGIN_ROOT}/skills/issue-workflow/references/issue-from-task.md`.
   Montre le tableau : n, titre, Type, priorité, nombre de scénarios.
4. **Valider le contenu** : montre les corps complets par lot de 5 issues au plus, avec une question par
   lot : `Créer ces issues` / `Changer quelque chose`. Boucle jusqu'au oui. C'est la validation que
   `tnx-plan-create-issue` demande à son étape 3 : ne la redemande pas.
5. **Créer**, une tâche à la fois : lis `<racine du repo>/.claude/skills/tnx-plan-create-issue/SKILL.md`
   (`git rev-parse --show-toplevel`) ; c'est un skill du repo projet, pas du plugin. Suis ses étapes 1, 5,
   6, 7, 8 et 9 :
   - formulaire : template `feature-checklist` (Type `Feature`), body préparé à l'étape 3 ;
   - saute son étape 3 (contenu déjà validé) et son étape 4 (utilise `Réglages communs`) ;
   - n'utilise jamais « Yes, and start right away » : aucune branche n'est créée ici.

   Après chaque création, écris `#<numéro>` dans la ligne de la tâche du fichier d'état, avant la suivante.
6. **Échec** : arrête-toi à la première erreur et rapporte-la. Avant de recréer quoi que ce soit, relance la
   recherche de l'étape 1 : une création a pu réussir sans que le numéro soit noté.

7. **Clore**, sans nouvelle question (rien à décider, on propage) :
   - **Analyse** : dis ce que tu vas changer, puis modifie seulement `milestone:` dans l'en-tête, la section
     « Already covered by existing issues » (une ligne par tâche : issue, état, couverture) et la ligne
     « Tasks with no matching issue ». Applique l'étape 4 de `${CLAUDE_PLUGIN_ROOT}/skills/analyze-pitch/SKILL.md`.
     Ne change aucun scénario. Ne modifie rien sur GitHub.
   - **Vue d'ensemble** : lance `${CLAUDE_PLUGIN_ROOT}/skills/build-scenario-overview/SKILL.md` en mise à jour
     avec `--milestone <milestone> --refresh-tickets` (réponds « mettre à jour » à son étape 2) : tâches,
     tickets, parcours validés en phase 4 gardés tels quels. Saute la boucle de corrections des parcours.
     Republie vers le même `artifactUrl`, sauf si l'utilisateur a refusé de publier en phase 4.

Mets `phase: done` dans le fichier d'état quand tout est fait. C'est la dernière phase : pas de `/clear`.

## Conditions de sortie

- [ ] Chaque tâche `oui` a dans le fichier d'état `#<numéro>`, `existante #<numéro>` ou `aucune (choix)`.
- [ ] Chaque numéro créé répond à `gh issue view <n>` et a le bon milestone, le bon Type et les bons champs du
      board (prouve avec le rapport de `tnx-plan-create-issue`).
- [ ] Le texte de chaque issue créée est en anglais simple.
- [ ] Aucune tâche n'a deux issues : relis `gh issue list` du milestone et compare avec le fichier d'état.
- [ ] L'utilisateur a dit oui avant la première création.
- [ ] Les réglages communs et le numéro de chaque issue créée sont dans le fichier d'état.
- [ ] Le tableau « Already covered by existing issues » de l'analyse liste chaque issue du fichier d'état.
- [ ] Dans `<slug>.overview.json`, chaque tâche qui a une issue a son `ticket`, le nombre de scénarios par
      tâche est celui de l'analyse, et `build_overview.py` se termine sans `error:`.
- [ ] La page est republiée au même lien, ou l'utilisateur avait refusé de publier.
- [ ] Le rapport final est donné : lien, nombres (tâches, Must, tickets, parcours), tâches `Must` sans ticket
      (aucune sans choix explicite), tâches dans aucun parcours.

À la fin, dis la suite : chaque issue s'implémente avec `/feature-implementation-workflow <issue>`.
