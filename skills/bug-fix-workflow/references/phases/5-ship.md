# Phase 5 — Livrer

But : les branches sont poussées et les pull requests ouvertes, après un oui clair de l'utilisateur.

## Contraintes

- **Base saine.** Tout est commité, `git status` est propre (les fichiers de plan et de notes ne sont pas
  commités), et les commits n'ont pas changé depuis le dernier passage de la phase 4. Sinon, retourne à la
  phase 4.
- **Résumé avant le oui.** Montre : le tableau avant/après de la phase 4, la cause en une ligne, les
  commits et les branches à pousser, les pull requests à ouvrir (le titre de chacune), et les
  avertissements (un scénario `needs a human` répondu par l'utilisateur ; des données déjà touchées sans
  réparation ; un défaut voisin laissé en `Hors périmètre`). Demande ensuite s'il faut pousser et ouvrir,
  pousser seulement, ou arrêter.
- **Rien vers l'extérieur sans oui** donné dans cette phase. Ne force jamais le push. Ne change jamais les
  labels, le milestone, les assignés : dis à l'utilisateur d'assigner un reviewer.
- **Format.** Une seule PR (le cas normal) : `tnx-dev-standards-dev-and-git-workflow` (branche
  `bugfix/<issue>/<slug>`, message `bugfix(<issue>): ...`, corps de PR : Description / Related Issue / Is
  this covered by automated tests). La description dit la cause et le correctif en quelques puces, et
  nomme le test de non-régression. Plusieurs PR : étapes 6 et 7 de `split` dans `../../stack/SKILL.md`.
  Titres et corps en anglais simple.
- **Hotfix.** Après l'ouverture, demande si le correctif doit aussi aller en demo ou en production. Si oui,
  propose `Skill hotfix` avec la branche. Ne l'appelle qu'après un oui.
- **Données à réparer.** Si `## Données déjà touchées` demande une réparation (migration déjà dans la PR, ou
  script à lancer par l'équipe), dis-le dans la conclusion : c'est une action à suivre après le déploiement.
- **Clore le run.** Mets `phase: done` dans les plans et donne les liens des pull requests.

## Conditions de sortie

- [ ] L'utilisateur a dit oui au push dans cette phase.
- [ ] Chaque branche est poussée (`git status -sb` ne montre aucun commit en avance sur son remote).
- [ ] Chaque pull request est ouverte, son corps suit le format, et son titre et son numéro sont affichés.
- [ ] La question du hotfix a été posée, et la réponse est notée.
- [ ] `phase: done` est dans les plans.
