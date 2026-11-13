# Phase 6 — Livrer

But : les branches sont poussées et les pull requests ouvertes, après un oui clair de l'utilisateur.

## Contraintes

- **Base saine.** Tout est commité, `git status` est propre (les fichiers de plan ne sont pas commités), et
  les commits n'ont pas changé depuis le dernier passage de la phase 5. Sinon, retourne à la phase 5.
- **Résumé avant le oui.** Montre : le tableau de vérification de la phase 5 (scénario | tests | verdict
  UI), les commits et les branches à pousser, les pull requests à ouvrir (le titre de chacune), et les
  avertissements (label `scenarios-approved` avec des scénarios ajoutés ; un scénario `needs a human`
  répondu par l'utilisateur). Demande ensuite s'il faut pousser et ouvrir, pousser seulement, ou arrêter.
- **Rien vers l'extérieur sans oui** donné dans cette phase. Ne force jamais le push. Ne change jamais les
  labels, le milestone, les assignés : dis à l'utilisateur d'assigner un reviewer.
- **Format.** Une seule PR (une ligne dans `## Pull requests`) : `tnx-dev-standards-dev-and-git-workflow`
  (nom de branche, message de commit, corps de PR : Description / Related Issue / Is this covered by
  automated tests). Le corps couvre backend et frontend. Plusieurs PR : étapes 6 et 7 de `split` dans
  `../stack/SKILL.md` (`gh stack submit --auto`, puis réécriture des titres et des corps), PR backend
  d'abord. Titres et corps en anglais simple.
- **Clore le run.** Mets `phase: done` dans les plans et donne les liens des pull requests.

## Conditions de sortie

- [ ] L'utilisateur a dit oui au push dans cette phase.
- [ ] Chaque branche est poussée (`git status -sb` ne montre aucun commit en avance sur son remote).
- [ ] Chaque pull request est ouverte, son corps suit le format, et son titre et son numéro sont affichés.
- [ ] `phase: done` est dans les plans.
