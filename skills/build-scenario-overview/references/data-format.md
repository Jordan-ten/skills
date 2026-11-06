# Format des données de la vue d'ensemble

La page est construite à partir d'un seul fichier de données : `.claude/plans/pitch/<pitch-slug>.overview.json`.
Un exemple complet est dans `references/example.overview.json`. Lis-le avant d'écrire un nouveau fichier.

## Concepts

| Mot | Sens dans la page |
|---|---|
| **Tâche** | Une ligne du tableau du pitch « Main User Tasks ». Une capacité vue par un rôle. Son numéro est sa place dans le tableau du pitch. |
| **Issue (ticket)** | L'issue GitHub du milestone qui couvre la tâche. Une tâche a zéro ou un ticket principal. |
| **Lot** | Un lot de livraison du pitch (« Lot 1 », « Lot 2 »). C'est la colonne Category du tableau du pitch. Un pitch sans lot a un seul lot. |
| **Parcours** | Une histoire du début à la fin qui enchaîne plusieurs tâches, racontée par un ou deux rôles. Elle montre comment les tâches fonctionnent ensemble. |
| **MoSCoW** | La priorité d'une tâche. **Must** est dans la livraison. **Should** peut être coupée. **Could** est affichée comme Should. |

## Champs

```jsonc
{
  "pitch": {
    "title": "Name of the pitch, as in Notion",
    "artifactTitle": "Two to four words",        // name of the Artifact
    "summary": "3 or 4 sentences: the problem, why now, what the pitch adds",
    "successIndicator": "optional, one sentence", // shown in a box under the summary
    "badges": ["fr", "en"],                       // optional chips about the pitch subject
    "badgesLabel": "optional, for screen readers",
    "source": { "capture": "...", "analysis": "...", "milestone": "270 — title" }
  },
  "issueBaseUrl": "https://github.com/<org>/<repo>/issues/",
  "artifactUrl": "set after the first publish",
  "lots": [{ "id": 1, "title": "Lot 1 · …", "sub": "optional line under the title" }],
  "tasks": [{
    "n": 1, "lot": 1, "p": "must",               // p: must | should | could
    "ticket": "25030",                            // optional, number as a string
    "title": "Role : action",
    "where": "UI : screen to open",               // optional, how to check it
    "note": "optional, one sentence",
    "scen": [{ "sit": "...", "res": "...", "tags": ["limite"] }]
  }],
  "parcours": [{
    "id": "p1", "label": "P1", "title": "...", "intro": "Lot 1. Acteurs : ...",
    "outcome": "optional, the expected end result",
    "steps": [{ "sit": "...", "res": "...", "tasks": [1, 4] }]
  }]
}
```

Écris du texte brut seulement. Le script de construction l'échappe. N'écris pas de HTML.

## Règles des tâches

- Garde l'ordre du pitch. Ne trie jamais par priorité. Le filtre Must de la page le fait.
- Garde seulement les tâches que l'analyse a gardées (sa liste `moscow`). Une tâche sans valeur dans Notion
  a la priorité donnée dans les « Decisions » de l'analyse. Si l'analyse n'en donne aucune, demande à l'utilisateur.
- Le titre commence par le rôle, puis un deux-points, puis l'action, comme dans le pitch. Quand l'analyse change un terme du
  pitch (par exemple langue d'interface et langue de contenu), utilise la formulation de l'analyse et dis-le dans `note`.
- Quand la priorité a été décidée dans l'analyse et n'est pas dans Notion, dis-le dans `note`.
- Une tâche Should sans ticket n'a pas besoin de marque. La page affiche déjà « pas de ticket ».
- `where` commence par `UI :` (un écran), `Email :` (un email à déclencher) ou `Hors UI :`.
- `note` contient un fait dont le lecteur a besoin une seule fois, comme un conflit entre le pitch et l'analyse.

## Règles des scénarios

Un scénario tient sur une ligne : une situation, une flèche, un résultat. La flèche est dessinée par la page.

- `sit` : ce qui se passe, avec une personne comme sujet. Pas de `GIVEN`, `WHEN`, `THEN`.
- `res` : ce que la personne voit ou reçoit. Une phrase.
- Nomme les personnes par rôle métier (admin, chargé RSE, fournisseur invité). Nomme les valeurs comme l'utilisateur les voit (« Navigateur »).
- Pas de mots de code (pas de nom d'entité, de champ, de queue ou de classe). Les noms d'outils que l'équipe utilise déjà, comme Novu ou Auth0, sont acceptés.
- Prends les scénarios dans l'analyse. Fusionne un bloc GIVEN/WHEN/THEN en une ligne. N'invente pas une règle que l'analyse ne dit pas.
- Mets le cas nominal en premier, puis les cas limites.

Tags, seulement quand c'est vrai :

| Tag | À utiliser quand |
|---|---|
| `limite` | le scénario est un cas limite ou un cas d'erreur |
| `confirmer` | l'analyse le marque « à confirmer » ou le liste comme question ouverte |
| `decide` | l'analyse le liste dans « Decisions ». Une décision sans scénario dans l'analyse peut avoir sa propre ligne. |
| `ajout` | l'analyse n'a pas de scénario pour lui. Il vient du pitch, d'une question ouverte ou d'une décision. |
| `verifier` | l'analyse dit de vérifier le ticket pour lui |

## Règles des tickets

- La source est la section de l'analyse « Already covered by existing issues ». Avec `--refresh-tickets`,
  ou quand cette section manque, lis le milestone avec `gh issue list` (lecture seule).
- Compare sur le sens, pas sur les mots. Un ticket principal par tâche. Mets les tickets en plus dans `note`.
- Un ticket qui ne couvre qu'une partie de la tâche reste le ticket de la tâche. Dis ce qui manque dans `note`.
- N'invente jamais un numéro. Aucun ticket trouvé : laisse `ticket` de côté. La page affiche « pas de ticket ».

## Règles des parcours

- Écris 3 à 6 parcours. Chacun est une histoire avec un début et une fin clairs, pour un ou deux rôles.
- Donne à chaque parcours le lot de ses tâches dans `intro` (« Lot 1. » ou « Lot 2. »). Préfère un seul lot par parcours, pour qu'un lot coupé
  retire des parcours entiers. Ne mélange les lots que si l'histoire l'exige, et dis-le dans `intro`.
- 3 à 8 étapes. Une étape est une ligne `sit → res`, comme un scénario. `tasks` liste les tâches dont l'étape montre le scénario qui fonctionne. Ne liste pas une tâche pour une étape qui ne fait que la toucher.
- Utilise les parcours pour montrer ce que les tâches seules ne peuvent pas montrer : un réglage fait par un admin, puis son effet sur une autre personne.
- Chaque tâche qu'une personne peut voir dans le produit est dans au moins un parcours. Une tâche sans effet visible
  (par exemple des traductions faites dans un outil) peut rester dehors. La construction avertit à ce sujet. Dis-le dans ton rapport.
- `outcome` est seulement l'indicateur de succès du pitch, quand il convient à ce parcours.
- Les ids sont `p1`, `p2`… et les labels `P1`, `P2`… dans l'ordre affiché.

## Texte de la page

Le texte de la page est en français. Ce fichier et le skill sont aussi en français.
