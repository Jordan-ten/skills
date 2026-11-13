# Template de plan

Le plan définit l'implémentation d'un package. Il vise un résultat observable : chaque étape existe
pour le prouver. Ce template sert `write-implementation-plan` seul et la phase 2 de
`feature-implementation-workflow`. Les parties propres au workflow sont marquées **(workflow)**.

Langue : le plan est écrit en **français**. Les identifiants de code, chemins et commandes restent tels
quels. Les clés de l'en-tête restent en anglais.

Style : extrêmement concis, supprime ce qui n'est pas nécessaire (`backend/AGENTS.md`). Phrases
courtes, mots courants. Suis les docs de style de code du package (`backend/docs/coding-style/`,
`frontend/AGENTS.md`). Utilise les mots déjà présents dans `src/`.

Un plan couvre un package seulement.

## Source des critères

- **Issue (workflow)** : l'issue est la source de vérité du comportement. Les critères sont ses
  scénarios. Le plan ne les recopie jamais : il les cite par leur titre, tel qu'il est dans l'issue (en
  anglais), par exemple `Edge case: a user without the right`. Dans les tableaux, la colonne `Critères`
  devient `Scénarios` et `Critère` devient `Scénario (titre de l'issue)`. Un scénario peut apparaître
  dans les deux plans : le plan backend a les tests de l'API, le plan frontend ceux de l'écran.
- **Description libre** : 2 à 5 critères observables, validés par l'utilisateur.

## Fichier

`<package>/.claude/plans/<numéro-issue>-<slug>.md`, dans le dossier de travail du package (`backend/` ou
`frontend/`). `<slug>` est le slug de branche de l'issue, ou un slug court de la tâche sans issue.
Préviens l'utilisateur avant d'écraser un plan existant.

**(workflow)** Écris le plan backend en premier : le plan frontend a besoin de son contrat.

## Structure

```markdown
---
status: ready | not-ready
generated_at: <AAAA-MM-JJ HH:mm>
---

# <titre> (<package>)

## Résultat attendu
<Les critères de réussite, numérotés, chacun observable : un utilisateur ou un test peut dire vrai ou
faux. Quand une issue ou un document décrit déjà le comportement, cite les titres, ne recopie pas.>
1. ...

## Approche
<3 à 6 lignes : la solution et son choix de conception principal. Cite la fonctionnalité voisine
trouvée à l'exploration et ce qu'on réutilise. Pas le comportement.>

## Design (frontend seulement)
<Lien(s) design de l'issue (Figma ou Claude Design) et écrans ou états qu'ils couvrent, ou la raison
pour laquelle il n'y en a pas (par exemple : composants existants du design system seulement).>

## Contrat backend (frontend seulement, avec un plan backend)
<Les queries, mutations et champs dont l'écran a besoin, par leur nom, tels que le plan backend les
crée. Rien que le plan backend ne crée pas.>

## Étapes
Les étapes de la tranche 1 produisent un chemin de bout en bout qui prouve le critère principal. Les
étapes suivantes enrichissent.

| n | Étape (ce qui change, où) | Critères | Preuve |
|---|---|---|---|
| 1 | ... | 1 | `<commande ou action>` : <résultat attendu> |
| 2 | ... | 1, 2 | ... |

## Tests
Tests existants de la zone (à garder, à lancer) :
- `<chemin>` — <ce qu'il couvre>

| Critère | Test | Type | État |
|---|---|---|---|
| 1 | `<chemin ou nouveau fichier>` | e2e | nouveau |
| 2 | `<chemin>` | e2e / unit / itg | nouveau / existant |

## Décisions techniques
- <décision> — <raison, une ligne>

## Pre-mortem
<2 à 3 lignes : comment tout pourrait passer au vert sans que le résultat attendu soit atteint ? Données
existantes, cas limites (null, doublons, anciennes données), effets sur le frontend, le SDK, les
imports.>

## Hors périmètre
- <ce que le plan ne fait pas>

## Pull requests (workflow, ajouté en phase 3, absent avant)
<Voir « Pull requests et commits ».>

## Questions non résolues
aucune
```

### En-tête (workflow)

Avec une issue, l'en-tête devient :

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
```

`sibling_plan` est relatif au plan, pour qu'il marche depuis les deux packages :
`../../../frontend/.claude/plans/<fichier>`.

## Règles du contenu

- **Résultat attendu** : un critère est observable ou il est réécrit. « Le code est propre » n'est pas
  un critère. « Un utilisateur sans le droit reçoit une erreur » en est un.
- **Étapes** : nomme les fichiers ou les couches, pas le code. Chaque étape liste les critères qu'elle
  sert. Une étape qui ne sert aucun critère est supprimée ou justifiée en une ligne.
  - **Tranche verticale d'abord.** La tranche 1 traverse toutes les couches utiles avec le minimum de
    comportement, jusqu'à un test de bout en bout qui passe. Ensuite, seulement, les cas limites et
    l'enrichissement. Ne planifie pas une couche entière avant la suivante.
- **Preuve** : ce qui montre que l'étape est faite : une commande et son résultat attendu (spec ciblé,
  `npm run type:check`, requête GraphQL), ou une action dans l'écran. Pas de « vérifier que ça marche ».
  Une migration n'a jamais de test automatisé : sa preuve est une vérification manuelle (la commande et
  la requête qui la montrent).
- **Tests** : choix et priorités dans `SKILL.md` (contraintes) et le skill `test-patterns`. Une nouvelle
  méthode publique d'un service va dans le spec existant de ce service. Test d'intégration seulement là
  où le code existant en fait autant.
- **Décisions techniques** : seulement celles qu'un lecteur pourrait remettre en question : une
  migration avec valeur par défaut, une contrainte CHECK, un DataLoader, un nouvel index.
- **Pre-mortem** : un risque réel avec sa parade (une étape, un test, une décision), ou une phrase qui
  dit pourquoi aucun risque ne se voit. Une parade qui n'est dans aucune étape n'est pas une parade.
- **Questions non résolues** : `aucune`, ou une liste avec un responsable pour chacune. Avec une
  question, `status` vaut `not-ready`.

## Pull requests et commits (workflow, phase 3)

Ajoutés à chaque plan après la validation des plans, avant `## Questions non résolues` :

```markdown
## Pull requests

| n | Branche | Périmètre (une phrase) | Fichiers (hors générés) | Dépend de |
|---|---|---|---|---|
| 1 | `feature/<issue>/<layer-slug>` | ... | 12 | — |
| 2 | `feature/<issue>/<layer-slug>` | ... | 9 | 1 |

### Commits

| PR | Commit (`feature(<issue>): ...`) | Étapes | Tests |
|---|---|---|---|
| 1 | ... | 1, 2 | ... |
| 1 | generated files | — | — |
| 2 | ... | 3 | ... |
```

Une seule PR : une seule ligne dans le premier tableau. Une PR peut contenir les commits des deux
packages : chaque plan liste alors ses propres commits, et la ligne de PR est la même dans les deux
plans. Dans un plan frontend, `Dépend de` peut nommer une PR du plan backend (`backend 2`).

## Contrôle de cohérence (avant de montrer le plan)

Échoue bruyamment et corrige le plan, ou retourne poser la question :

- [ ] Chaque critère est dans le tableau Tests, ou une ligne dit pourquoi un test n'apporte rien.
- [ ] Chaque étape sert au moins un critère.
- [ ] Chaque critère est servi par au moins une étape.
- [ ] Chaque étape a une preuve exécutable.
- [ ] Les premières étapes forment une tranche de bout en bout, et la preuve de la dernière étape de la
      tranche montre le critère principal.
- [ ] Aucun comportement n'est décrit dans le plan sans venir de la demande ou de l'issue.
- [ ] Chaque mot nouveau existe dans `src/`, ou figure dans les décisions techniques.
- [ ] Backend : aucune étape ne casse les couches de `backend/docs/coding-style/architecture.md`.
- [ ] Le pre-mortem nomme un risque avec sa parade dans une étape, ou dit pourquoi il n'y en a pas.
- [ ] `Questions non résolues` vaut `aucune` et `status` vaut `ready`, ou les deux disent le contraire.

**(workflow)** En plus, sur les deux plans ensemble :

- [ ] Chaque scénario de l'issue est dans le tableau Tests d'au moins un plan. Aucun ne manque, aucun
      n'est inventé.
- [ ] Chaque titre de scénario cité dans un plan existe dans l'issue tel quel.
- [ ] Plan frontend : `## Design` a un lien venant de l'issue ou une raison. Chaque élément de
      `## Contrat backend` est créé par une étape du plan backend.
- [ ] Après la phase 3 : dans chaque plan, chaque étape est dans exactement un commit et chaque test est
      dans le commit qui contient le code qu'il couvre (le test e2e dans celui qui expose le
      comportement). Une pull request frontend n'est jamais sous la pull request backend dont elle
      dépend.
