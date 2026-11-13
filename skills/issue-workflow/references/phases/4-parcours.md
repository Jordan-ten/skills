# Phase 4 — Parcours et vue d'ensemble

But : des parcours de bout en bout validés par l'utilisateur, et une vue d'ensemble publiée qui montre les
lots, les tâches, leurs scénarios validés et les parcours. Elle est construite une seule fois, avec des
scénarios déjà validés.

Utilise `${CLAUDE_PLUGIN_ROOT}/skills/build-scenario-overview/SKILL.md` en entier (y compris la boucle de
corrections des parcours, étape 5) et son `references/data-format.md`.

Contraintes :
- **Lots et tâches** : recopie-les depuis le tableau « Main User Tasks » du pitch, dans son ordre, avec ses
  numéros. Aucune question sur le découpage. Les tâches `hors périmètre` ne sont pas dans la page : liste-les
  à l'utilisateur.
- **Parcours** : vérifie pour chacun que
  - chaque numéro de tâche d'une étape existe et n'est pas `hors périmètre` ;
  - le résultat d'une étape alimente la situation de la suivante ;
  - les rôles sont ceux des tâches citées ;
  - le parcours est **relié à la phrase « Problem »** de l'analyse : dis quelle partie du problème il
    prouve résolue, en une ligne. Un parcours qu'on ne peut relier à rien est une trouvaille : demande si
    on le garde. Marque aussi un parcours de bout en bout `candidat e2e` quand un seul test e2e peut le
    parcourir (propose, l'utilisateur tranche).

  Corrige avec l'utilisateur jusqu'à un « ok » explicite, puis mets `Validé : oui` dans le fichier d'état.
  Quand tous sont validés, liste les tâches `Must` dans aucun parcours : l'utilisateur décide pour chacune
  (l'ajouter à un parcours, ou accepter qu'elle soit seule).
- Les scénarios de la page viennent de l'analyse, jamais d'ailleurs. Une correction va d'abord dans
  l'analyse.
- Avant la phase 5 il n'y a en général pas de tickets : n'appelle `gh issue list` que si un milestone est
  noté dans le fichier d'état.
- Publie seulement après un oui de l'utilisateur. Une page privée suffit.
- Remplis le tableau `Parcours` du fichier d'état à partir de `<slug>.overview.json`. Mets `phase: issues`.

## Conditions de sortie

- [ ] `<slug>.overview.json` est écrit et `build_overview.py` s'est terminé sans `error:`.
- [ ] Lots et tâches identiques au tableau « Main User Tasks » de la capture (mêmes numéros, même ordre,
      même lot), sauf les tâches écartées par le MoSCoW ou `hors périmètre`.
- [ ] Le nombre de scénarios par tâche est le même dans l'analyse et dans `overview.json`.
- [ ] Chaque parcours est validé, et chaque étape renvoie à des tâches existantes.
- [ ] Chaque parcours validé a une ligne `Problème couvert` dans le fichier d'état (ou la décision de le
      garder sans lien), et un parcours `candidat e2e` est marqué comme tel.
- [ ] Chaque tâche `Must` dans aucun parcours a une décision explicite.
- [ ] La page est publiée (lien dans `artifactUrl`), ou l'utilisateur a refusé de publier.
- [ ] Le tableau `Parcours` du fichier d'état est rempli, et chaque décision de l'utilisateur (parcours
      validé, tâche `Must` seule) est écrite dans `overview.json` ou le fichier d'état.
