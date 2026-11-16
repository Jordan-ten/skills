# Phase 1 — Reproduire

But : le bug est vu en local, avec la preuve « avant », et l'issue contient un scénario de non-régression
validé par l'utilisateur. Rien n'est corrigé ici.

Langues : le grill et tous les échanges sont en français. Seul ce qui est écrit dans l'issue est en
anglais simple.

## Contraintes

- **Lecture.** Lis l'issue avec ses commentaires (`gh issue view <n> --json
  number,title,body,comments,labels,updatedAt,url`) : les décisions tardives et les analyses y vivent
  souvent. Extrais : symptôme observé, comportement
  attendu, étapes, environnement, données concernées. Arrête-toi avec un message clair quand l'issue n'est
  pas un bug, ou quand le symptôme ou le comportement attendu manque et que le code ne le dit pas : demande
  à l'utilisateur de compléter l'issue d'abord.
- **Exploration silencieuse.** Modules, entités, mots déjà utilisés (grep avant d'employer un mot), tests
  de la zone, `docs/product/<module>/overview.md`. Un agent `Explore` quand la zone est large. Ne cherche
  pas encore la cause : repère seulement où le symptôme se produit.
- **Choisis le chemin le moins cher qui montre le symptôme exact :**
  1. **e2e** quand le symptôme est une réponse d'API ou un état de données. Écris-le dans l'arbre de travail
     (style : skill `test-patterns`), lance-le sur l'environnement `test`, constate qu'il échoue avec le
     bon message. Il n'est jamais commité ici : il devient le test de non-régression de la phase 3.
  2. **UI** quand le symptôme se voit à l'écran. `Skill launch` (`dev front`), puis `tnx-dev-mcp-local-dev`
     pour ouvrir l'app. Joue les étapes de l'issue et prends une capture ou un snapshot du symptôme.
  3. **Serveur dev et API** pour les cas intermédiaires (job, calcul, notification) : appelle l'API ou le
     job, lis le log (`tnx-dev-check-backend-logs`, `tail` ou `grep`).
- **Données.** Le cas manque en local : `Skill create-local-data`, par l'API du produit, après un oui de
  l'utilisateur. Jamais de SQL brut ni de données tordues pour faire apparaître le bug. Note les données
  créées.
- **Bug lié aux données de production.** Lecture seule : `tnx-dev-metabase-query` (lien de requête, tu ne
  vois jamais les lignes) pour les données, et les logs et erreurs Datadog (`search_datadog_logs`,
  `search_datadog_error_tracking_issues`) pour le message exact et la date. Ces faits servent à construire
  des données locales de même forme. Le bug doit tout de même se voir en local.
- **Pas reproduit.** Après 3 tentatives différentes (une tentative = un chemin ou un jeu de données
  différent), arrête-toi et dis ce qui a été essayé et ce qui manque. Ne passe jamais à la phase 2 sans
  reproduction. Si l'utilisateur le demande quand même, dis-le dans le plan.
- **Scénario de non-régression.** Écris un scénario `Nominal case: ...` (Given/When/Then) qui décrit le
  comportement attendu, avec de vrais noms et de vraies valeurs, observable par un utilisateur. Un
  scénario : celui du bug. Propose-le, puis fais-le valider (grill, une question à la fois). Le comportement
  attendu vient de l'issue, du code ou de la doc produit ; sinon l'utilisateur tranche.
- **Écriture dans l'issue.** Le scénario et son groupe How to test sont ajoutés avec le flag, dans le
  format de l'issue (voir « Écrire dans l'issue » dans
  `../../feature-implementation-workflow/references/scenario-audit.md`). Texte en **anglais simple**.
  Montre le diff du body et n'écris qu'après l'accord, avec `gh issue edit <n> --body-file <fichier>`
  (fichier du scratchpad).
- **Notes du run.** Écris `.claude/plans/<n>.notes.md` (voir « Fichiers du run » dans `SKILL.md`) :
  étapes exactes de la reproduction, données et environnement, observé, attendu, preuve « avant »
  (commande et sortie courte, ou capture), chemin de l'e2e de reproduction non commité, et les faits du
  code utiles au plan (chemins, une ligne chacun).

## Conditions de sortie

- [ ] Le symptôme exact de l'issue a été observé en local. Montre la preuve (sortie du test rouge, capture,
      ligne de log).
- [ ] Les étapes de la reproduction sont assez précises pour être rejouées par un sous-agent, données
      comprises.
- [ ] Le scénario de non-régression est dans le body de l'issue dans GitHub (relis avec `gh issue view`),
      en anglais simple, avec le flag, avec son groupe How to test.
- [ ] L'utilisateur a validé le diff avant l'écriture.
- [ ] Aucun fichier modifié hors e2e de reproduction : `git status --short` le montre, et rien n'est commité.
- [ ] Les notes du run existent avec tous les éléments ci-dessus.
