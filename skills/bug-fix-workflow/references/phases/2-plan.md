# Phase 2 — Diagnostic et plan du correctif

But : la cause racine est prouvée, et un plan de correctif minimal la traite, sans question ouverte,
avec le découpage en pull requests. L'utilisateur valide le tout en une seule fois. Les plans sont écrits
en **français**.

Méthode : `../write-implementation-plan/SKILL.md` (but, contraintes, conditions de sortie) et son
template `../write-implementation-plan/references/plan-template.md`. Applique-les, ne les recopie pas.
Le cadrage est déjà fait : le critère est le scénario de non-régression de l'issue.

Pars des notes du run (`.claude/plans/<n>.notes.md`).

## Diagnostic (avant le plan)

- **Cherche la cause, pas le symptôme.** Pars de l'hypothèse des notes (issue déjà analysée) et vérifie-la :
  si la preuve la contredit, dis-le. Sinon pars du point où le symptôme se voit et remonte le chemin du code
  jusqu'à la première ligne ou donnée qui est fausse. `git log` et `git blame` de la zone disent si une
  modification récente l'explique.
- **Prouve-la.** Une preuve qu'on peut rejouer : un log temporaire, une requête de lecture, un test qui isole la
  cause. Une instrumentation temporaire est permise, jamais commitée, et retirée avant la fin de la phase. Une hypothèse sans preuve n'est pas une
  cause. Après 3 hypothèses réfutées, arrête-toi et demande à l'utilisateur.
- **Cherche le même défaut ailleurs** (`grep` du même motif, des autres appelants). Chaque occurrence
  trouvée est corrigée dans ce plan, ou nommée dans `## Hors périmètre` avec la raison.
- **Données déjà touchées.** Des données abîmées existent-elles déjà en prod ou en demo ? Si oui, c'est une
  décision de l'utilisateur : réparer (migration, avec preuve manuelle, jamais un test automatique ; ou
  script lancé par l'équipe), ou laisser. Note la décision.

## Contraintes : plans

Le template de plan s'applique avec ces adaptations pour un bug :

- `## Résultat attendu` : le scénario de non-régression (par son titre, en anglais) et « le comportement
  voisin ne change pas ».
- Ajoute `## Cause` après `## Résultat attendu` : la cause racine en 2 à 4 lignes, la preuve (commande et
  résultat), et pourquoi le bug n'a pas été vu plus tôt (test manquant, cas non prévu, régression d'un
  commit).
- Ajoute `## Données déjà touchées` après `## Cause` : la décision, ou `aucune`.
- `## Étapes` : le correctif **minimal**. Tranche 1 = le test de non-régression (l'e2e de reproduction de la
  phase 1 s'il existe, listé `existant, non commité`) puis le correctif qui le fait passer. Pas de refacto,
  pas d'amélioration voisine. Un refacto utile mais non nécessaire va dans `## Hors périmètre`.
- `## Tests` : le type de test de non-régression part du mode noté dans l'issue. Un test e2e d'abord, sur le
  scénario réaliste du bug ; un test unitaire seulement si la cause est une règle métier précise à
  isoler.
- `## Pre-mortem` : comment le correctif peut passer au vert sans corriger le vrai bug (mauvaises données
  de test, cas voisin, ancien état en base, effets sur le frontend ou le SDK).
- Un plan par package modifié (le plus souvent un seul), même emplacement et même en-tête que le workflow
  de feature (`issue`, `issue_updated_at`, `package`, `sibling_plan`, `phase`, `status`).
- Une question que seule une autre personne peut trancher met `status: not-ready` : dis-le et n'avance
  pas.

## Contraintes : découpage

Un correctif tient presque toujours en **une seule PR**. Applique la règle de taille de
`feature-implementation-workflow` (`../feature-implementation-workflow/references/phases/2-plan.md`,
« Contraintes : découpage ») seulement au-dessus de 30 fichiers relus. Écris `## Pull requests` (une ligne)
avec la colonne `Avancement` à `—`. Branche : `bugfix/<issue>/<slug>`, ou la branche de travail déjà
dédiée à l'issue.

## Voie rapide

Tu tranches, pas l'utilisateur : applique la voie rapide seulement si **toutes** ces conditions sont
vraies, preuves à l'appui :

- le bug a été reproduit dès la première tentative de la phase 1 (notes du run), sans donnée difficile à
  construire ;
- la cause est prouvée et tient en une phrase ;
- un seul package, au plus 5 fichiers relus (hors générés) ;
- aucune migration, aucune réparation de données, aucun changement du schéma GraphQL ou de l'API publique ;
- aucun doute sur le comportement attendu.

Alors : le plan ne garde que `## Résultat attendu`, `## Cause`, `## Étapes`, `## Tests`, `## Pre-mortem` (une
ligne), `## Hors périmètre`, `## Pull requests` (une ligne, la phase 3 et la reprise s'en servent) et
`## Questions non résolues`, avec `fast_path: true` dans l'en-tête. Une seule PR. Un doute sur une condition, ou
une reproduction qui a demandé plusieurs tentatives : plan complet. Annonce ton choix en une ligne, avec les
preuves des conditions. Ne pose pas de question : l'utilisateur peut le changer à la validation.

## Validation

Montre le diagnostic (cause et preuve), les plans, le chiffre de taille et le découpage, puis demande une
seule validation. Mets `phase: implement` dans l'en-tête des plans seulement après la validation.

## Conditions de sortie

- [ ] La cause racine est prouvée : la preuve (commande et résultat) est dans `## Cause`.
- [ ] Aucune instrumentation temporaire ne reste (`git status --short` ne montre que l'e2e de
      reproduction).
- [ ] Le même défaut ailleurs a été cherché : chaque occurrence est corrigée ou en `## Hors périmètre`.
- [ ] `## Données déjà touchées` contient la décision de l'utilisateur, ou `aucune`.
- [ ] Un plan existe pour chaque package modifié, au bon emplacement, avec l'en-tête du workflow.
- [ ] Avec `fast_path: true` : les cinq conditions de la voie rapide sont prouvées, et le choix est annoncé
      avec ses preuves.
- [ ] Le contrôle de cohérence du template (parties communes et parties du workflow, `## Pull requests`
      comprises) passe. Montre chaque ligne.
- [ ] Le scénario de non-régression est dans le tableau de tests, et la tranche 1 le fait passer.
- [ ] Aucune étape ne sort du correctif de la cause (pas de refacto ni de comportement nouveau).
- [ ] `Questions non résolues` vaut `aucune` et `status` vaut `ready` dans chaque plan.
- [ ] Le nombre de fichiers (hors générés) est affiché.
- [ ] L'utilisateur a validé le diagnostic, les plans et le découpage.
- [ ] Le fichier de run est à jour : `phase: implement`, `status: ready`, plans et branches dans `Fichiers`.

Au passage, dis que `/clear` puis `/bug-fix-workflow <issue>` reprend à la phase 3 : les plans portent
l'état.
