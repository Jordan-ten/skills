# Phase 6 — Livrer

But : les branches sont poussées et les pull requests ouvertes, après un oui clair de l'utilisateur.

## Travail

1. **Vérifier la base.** Tout est commité, `git status` est propre (les fichiers de plan ne sont pas
   commités), et les conditions de sortie de la phase 5 sont toujours vraies : les commits n'ont pas
   changé depuis le dernier passage de la phase 5. S'ils ont changé, retourne à la phase 5.
2. **Montrer le résumé**, puis demander :
   - le tableau de vérification de la phase 5 (scénario | tests | verdict UI),
   - les commits et les branches à pousser, les pull requests à ouvrir (le titre de chacune),
   - les avertissements : label `scenarios-approved` avec des scénarios ajoutés, un scénario
     `needs a human` répondu par l'utilisateur.

   Options du passage : `Pousser et ouvrir la ou les pull requests` / `Pousser seulement` / `Arrêter`.
3. **Pousser et ouvrir**, seulement après le oui :
   - Une PR par plan : suis `tnx-dev-standards-dev-and-git-workflow` (nom de branche, message de commit,
     corps de PR : Description / Related Issue / Is this covered by automated tests). Titres et corps
     de PR en anglais simple.
   - Stack : suis les étapes 6 et 7 de `split` dans `../stack/SKILL.md`
     (`gh stack submit --auto`, puis réécriture des titres et des corps). Couches backend d'abord.
   - Ne force jamais le push. Ne change jamais les labels, le milestone, les assignés. Dis à
     l'utilisateur d'assigner un reviewer.
4. **Clore le run.** Mets `phase: done` dans les plans. Donne les liens des pull requests.

## Conditions de sortie

- [ ] L'utilisateur a dit oui au push dans cette phase.
- [ ] Chaque branche est poussée (`git status -sb` ne montre aucun commit en avance sur son remote).
- [ ] Chaque pull request est ouverte, son corps suit le format, et son titre et son numéro sont affichés.
- [ ] `phase: done` est dans les plans.
