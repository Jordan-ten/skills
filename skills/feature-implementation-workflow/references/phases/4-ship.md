# Phase 4 — Livrer

But : les branches sont poussées et les pull requests ouvertes, après un oui clair de l'utilisateur.

## Contraintes

- **Base saine.** Tout est commité, `git status` est propre (les fichiers de plan ne sont pas commités), et
  les commits n'ont pas changé depuis le dernier passage de la phase 3. Sinon, retourne à la phase 3.
- **Résumé avant le oui.** Montre : le rapport de la phase 3 (e2e lancés et résultats, trouvailles de
  relecture refusées), les commits et les branches à pousser, les pull requests à ouvrir (le titre de
  chacune). Rappelle que la QA des scénarios se lance à part, avec `qa-workflow`. Demande ensuite s'il
  faut pousser et ouvrir, pousser seulement, ou arrêter.
- **Rien vers l'extérieur sans oui** donné dans cette phase. Ne force jamais le push. Ne change jamais les
  labels, le milestone, les assignés : dis à l'utilisateur d'assigner un reviewer.
- **Format.** Une seule PR (une ligne dans `## Pull requests`) : `tnx-dev-standards-dev-and-git-workflow`
  (nom de branche, message de commit, corps de PR : Description / Related Issue / Is this covered by
  automated tests). Le corps couvre backend et frontend. Plusieurs PR : étapes 6 et 7 de `split` dans
  `../stack/SKILL.md` (`gh stack submit --auto`, puis réécriture des titres et des corps), PR backend
  d'abord. Titres et corps en anglais simple.
- **Clore le run.** Mets `phase: done` dans les plans et dans le fichier de run (`status: done`, liens des
  pull requests dans `Fichiers`), et donne les liens des pull requests.

## Conditions de sortie

- [ ] L'utilisateur a dit oui au push dans cette phase.
- [ ] Chaque branche est poussée (`git status -sb` ne montre aucun commit en avance sur son remote).
- [ ] Chaque pull request est ouverte, son corps suit le format, et son titre et son numéro sont affichés.
- [ ] `phase: done` est dans les plans, et `phase: done`, `status: done` dans le fichier de run.
