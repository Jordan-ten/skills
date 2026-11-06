---
name: create-local-data
description: >
  Crée des enregistrements dans un environnement local en appelant l'API GraphQL du backend, avec un
  token offline-auth auto-signé (pas de login, aucun fichier écrit, pas de SQL brut). À utiliser quand
  un cas local manque et doit être créé pour voir un écran, reproduire un bug, préparer une démo ou
  débloquer un test : "crée-moi une campagne en local", "il me faut une tâche de groupe", "génère les
  données pour reproduire ce bug", "seed local data", ou /create-local-data. Aussi utilisé par d'autres
  skills qui ont besoin d'un enregistrement avant de continuer.
allowed-tools: Bash(bash ${CLAUDE_PLUGIN_ROOT}/skills/create-local-data/scripts/*), Read, Grep, Glob, AskUserQuestion
---

# Créer des données locales

Crée ce qui manque à un environnement local, par l'API que le produit utilise lui-même. Le backend
valide chaque appel, donc les enregistrements sont cohérents, ce que le SQL brut ne garantit jamais.

## Règles

- **Ne jamais écrire en SQL.** Le skill `sql-query` lit l'état. L'écriture passe par l'API, donc les
  règles métier, les valeurs par défaut et les événements sont appliqués.
- **Dire dans quelle base on écrit, avant d'écrire.** Le backend sur le port 3000 est celui de dev dans
  une session dev, celui de l'e2e dans une session e2e. Même port, données différentes. Le nommer à
  chaque fois.
- **Demander avant la première écriture.** Montrer ce qui sera créé, avec les mots du domaine, puis une
  `AskUserQuestion`. Une lecture pour vérifier le terrain ne demande aucune question. Quand un autre
  skill a déjà montré le même plan et obtenu un oui, ne pas demander une deuxième fois.
- **Rapporter les ids.** Chaque enregistrement créé est listé avec son id et son nom, pour que
  l'utilisateur puisse le retrouver ou le supprimer.
- **Proposer le nettoyage, ne jamais le lancer seul.** L'utilisateur veut souvent garder le cas.

## L'appel

```bash
GQL_EMAIL=<dev user email> bash ${CLAUDE_PLUGIN_ROOT}/skills/create-local-data/scripts/graphql.sh \
  --variables '{"input":{...}}' <<'GQL'
mutation CreateX($input: XInput!) { createX(input: $input) { id name } }
GQL
```

Le script signe le même token offline-auth que `frontend/tests/fixtures/graphql.ts`, donc il n'a besoin
d'aucun login. Il exige que le backend tourne avec `OFFLINE_AUTH=true`.

| Env | Défaut | Quand le changer |
|---|---|---|
| `GQL_EMAIL` | aucun, obligatoire | L'utilisateur dont les droits servent à l'appel. |
| `GQL_ORG` | `1` | Une autre organisation. |
| `GQL_ENDPOINT` | `http://localhost:3000/graphql` | Un autre backend local. |
| `GQL_ADMIN` | non défini | `1` pour une opération d'administrateur de la plateforme (mode sudo), comme créer une organisation. Cela retire l'en-tête d'organisation. |

Une erreur revient sous la forme `{"errors":[...]}` avec un HTTP 200. Le script affiche le corps et sort
avec le code `1` quand il contient une erreur, donc une création échouée ne peut pas passer pour un
succès. Il parle uniquement aux hôtes locaux (`localhost`, `127.0.0.1`) et refuse tout autre endpoint.

## Méthode

1. **Vérifier ce qui existe déjà.** Le cas est souvent là sous un autre nom. Interroger avant de créer.
2. **Trouver la mutation** : `grep -n "createX" backend/src/schema.gql`, puis lire son type d'entrée de
   la même façon. Ne jamais lire `schema.gql` en entier, il fait plus de 10 000 lignes.
3. **Trouver l'ordre des appels.** Une mutation suffit rarement : une campagne doit être créée, puis
   lancée, puis recevoir ses tâches. Cette séquence est déjà écrite dans les fixtures e2e. Lire le
   `frontend/tests/fixtures/*.ts` correspondant avant de composer la sienne — voir
   `references/recipes.md`.
4. **Créer, puis vérifier** en relisant l'enregistrement, ou en ouvrant l'écran.
5. **Lister les ids** et proposer les mutations de suppression.

## Quand l'API n'a pas de mutation

Certaines préparations vivent hors de GraphQL : `npm run _dev command <name>` (voir
`backend/command.ts`), par exemple la configuration initiale d'une organisation. Chercher là avant de
conclure qu'un cas ne peut pas être créé. Lire d'abord le code de la commande, et demander avant de la
lancer : une commande backend peut faire plus que créer un enregistrement. Elle n'est pas pré-approuvée
pour cette raison.

Si aucun des deux n'existe, dire que le cas ne peut pas être créé par un chemin supporté. Ne pas se
rabattre sur du SQL.
