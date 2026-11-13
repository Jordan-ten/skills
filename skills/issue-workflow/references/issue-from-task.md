# Issue à partir d'une tâche

Une tâche du pitch donne une issue de type `Feature`, avec le template `feature-checklist` de
`tnx-plan-create-issue` (fichier `templates/feature-checklist.md` de ce skill). Le corps est écrit par
l'aide `tnx-plan-write-issue-description` (skill du repo projet, lu par `tnx-plan-create-issue` : ne
l'appelle pas toi-même), qui suit ses propres règles (anglais simple, mots du produit,
pas de noms de code). Ce fichier dit seulement quoi lui donner.

## Ce que tu donnes (en anglais simple)

| Entrée | Source dans l'analyse ou la vue d'ensemble |
|---|---|
| Description | Titre de la tâche (`Rôle : action`) et `note` de la tâche. Traduits. |
| Contexte (2 à 4 lignes) | Qui a besoin de quoi, et pourquoi : « Problem » et « Proposed solution » de l'analyse, ce qui concerne la tâche seulement. |
| `Out of scope:` | Le « Out of scope » de l'analyse qui concerne la tâche, et les décisions `hors périmètre` voisines. |
| Parcours utilisateur jusqu'au cas nominal | `where` de la tâche (l'écran) et le scénario nominal. |
| Scénarios | Tous les scénarios de la tâche, un par bloc : `Nominal case`, `Edge case`, `Error case`. Chaque tag de la tâche (`limite`, `confirmer`, …) donne le type du scénario. Sans tag, un scénario après le premier est un `Edge case`. |
| How to test | Un groupe par scénario important (le nominal, et les cas à vrai risque). Seulement ce qu'un utilisateur peut faire à la main. |
| Lien design | S'il existe dans l'analyse ou le pitch : ligne `Design: <url>` dans le contexte. |
| Source | L'URL Notion du pitch (`source_url` de la capture), pour la traçabilité. |

## Règles

- Titre : `[Module] ...` avec les mots du produit. `tnx-plan-create-issue` infère le module ; montre-le dans
  le tableau de l'étape 3 de la phase 5.
- Un scénario marqué `confirmer` ou une question dans `Open questions` qui touche la tâche devient une
  marque `<to confirm>` pour l'aide : ne crée pas l'issue avant que l'utilisateur ait tranché.
- Ne copie jamais le pitch en entier : seulement la tâche. Un parcours n'est pas copié non plus : l'issue
  décrit une tâche.
- N'invente aucun scénario pour « compléter » : tous les scénarios viennent de l'analyse validée en phase 3.
