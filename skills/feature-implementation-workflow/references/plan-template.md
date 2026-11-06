# Template de plan

Le plan définit l'implémentation. Le comportement est dans l'issue : ne le recopie jamais. Renvoie à un
scénario par son titre, par exemple `Edge case: a user without the right`.

Langue : le plan est écrit en **français**. Les titres de scénarios sont cités tels qu'ils sont dans
l'issue (en anglais). Les identifiants de code, chemins et commandes restent tels quels. Les clés de
l'en-tête restent en anglais.

Style : extrêmement concis, supprime ce qui n'est pas nécessaire (`backend/AGENTS.md`). Phrases
courtes, mots courants. Suis les docs de style de code du package (`backend/docs/coding-style/`,
`frontend/AGENTS.md`). Utilise les mots déjà présents dans `src/`.

## Fichier

Un plan par package que l'issue touche, dans le dossier de travail de ce package :
`backend/.claude/plans/ticket/<numéro-issue>-<slug>.md` et
`frontend/.claude/plans/ticket/<numéro-issue>-<slug>.md`. `<slug>` est le slug de branche de l'issue.
N'écrase un plan existant de la même issue qu'après avoir prévenu l'utilisateur.

Un plan couvre son package seulement. Un scénario peut apparaître dans les deux plans : le plan backend a
les tests de l'API, le plan frontend a les tests de l'écran.

```markdown
---
issue: <numéro>
issue_url: <url>
issue_updated_at: <updatedAt de l'issue après la phase 1>
package: backend | frontend
sibling_plan: <chemin de l'autre plan, relatif à ce fichier, ou none>
phase: split | implement | verify | ship | done   # prochaine phase à lancer
status: ready | not-ready
generated_at: <AAAA-MM-JJ HH:mm>
---

# <numéro de l'issue> — <titre de l'issue> (<package>)

## Approche
<3 à 6 lignes : la solution et son choix de conception principal. Pas le comportement.>

## Design
<Plan frontend seulement. Lien(s) design de l'issue (Figma ou Claude Design) et écrans ou états qu'ils
couvrent, ou la raison pour laquelle il n'y en a pas (par exemple : composants existants du design
system seulement).>

## Contrat backend
<Plan frontend seulement. Les queries, mutations et champs dont l'écran a besoin, par leur nom, tels que
le plan backend les crée. Rien que le plan backend ne crée pas.>

## Étapes
1. <étape : ce qui change, où> — <titres des scénarios qu'elle sert>
2. ...

## Tests
Tests existants de la zone (à garder, à lancer) :
- `<chemin>` — <ce qu'il couvre>

| Scénario (titre de l'issue) | Test | Type | État |
|---|---|---|---|
| Nominal case: ... | `<chemin ou nouveau fichier>` | e2e | nouveau |
| Edge case: ... | `<chemin>` | e2e / unit / itg | nouveau / existant |

## Décisions techniques
- <décision> — <raison, une ligne>

## Hors périmètre
- <ce que le plan ne fait pas. Le hors-périmètre produit reste dans l'issue.>

## Pull requests
<ajouté en phase 3, après la validation des plans. Absent avant.>

| n | Branche | Périmètre (une phrase) | Étapes | Tests | Dépend de |
|---|---|---|---|---|---|
| 1 | `feature/<issue>/<layer-slug>` | ... | 1, 2 | ... | — |
| 2 | `feature/<issue>/<layer-slug>` | ... | 3 | ... | 1 |

Une seule PR : une seule ligne. Dans un plan frontend, `Dépend de` peut nommer une couche du plan
backend (`backend 2`).

## Questions non résolues
aucune
```

## Règles du contenu

- **Étapes** : dans l'ordre d'implémentation (backend : domaine, port, adapter, use case, resolver,
  migration, codegen ; frontend : données, composants, écran). Chaque étape nomme les fichiers ou les
  couches, pas le code. Chaque étape liste les scénarios qu'elle sert. Une étape qui ne sert aucun
  scénario est supprimée ou justifiée en une ligne.
- **Tests** :
  1. E2E d'abord : il couvre le chemin complet. Jamais un test e2e pour une garde d'entrée : choisis un
     scénario métier réaliste.
  2. Test unitaire seulement pour une logique métier non triviale.
  3. Test d'intégration seulement là où le code existant en fait autant.
  4. Aucun test pour un wrapper trivial ou une simple délégation.
  Une nouvelle méthode publique d'un service va dans le spec existant de ce service.
- **Décisions techniques** : seulement celles prises dans le grill ou trouvées dans le code qu'un lecteur
  pourrait remettre en question : une migration avec valeur par défaut, une contrainte CHECK, un
  DataLoader, un nouvel index.
- **Questions non résolues** : `aucune`, ou une liste avec un responsable pour chacune. Avec une
  question, `status` vaut `not-ready`.

## Contrôle de cohérence (avant de montrer le plan)

Échoue bruyamment et corrige le plan, ou retourne au grill :

- [ ] Chaque scénario de l'issue est dans le tableau Tests d'au moins un plan. Aucun ne manque, aucun
      n'est inventé.
- [ ] Chaque étape sert au moins un scénario.
- [ ] Chaque scénario est servi par au moins une étape.
- [ ] Plan frontend : `## Design` a un lien venant de l'issue ou une raison. Chaque élément de
      `## Contrat backend` est créé par une étape du plan backend.
- [ ] Chaque titre de scénario cité dans le plan existe dans l'issue tel quel.
- [ ] Aucun comportement n'est décrit dans le plan sans être dit par l'issue.
- [ ] Chaque mot nouveau existe dans `src/`, ou figure dans les décisions techniques.
- [ ] Backend : aucune étape ne casse les couches de `backend/docs/coding-style/architecture.md`.
- [ ] `Questions non résolues` vaut `aucune` et `status` vaut `ready`, ou les deux disent le contraire.
- [ ] Après la phase 3 : dans chaque plan, chaque étape est dans exactement une pull request et chaque
      test est dans la pull request qui contient le code qu'il couvre (le test e2e dans celle qui
      expose le comportement). Une pull request frontend n'est jamais sous la pull request backend dont
      elle dépend.
