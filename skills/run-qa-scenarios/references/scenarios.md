# Construire la liste de scénarios

## D'où viennent les scénarios

Lire ces parties de l'issue, dans cet ordre :

1. **How to test** — la checklist écrite par l'auteur. Chaque case est un scénario.
2. **Scenarios** (Given / When / Then) — quand l'issue en a.
3. **Reproduction Steps** — pour un bug, les étapes sont le scénario : le bug doit avoir disparu.

**Si l'issue n'a rien de tout cela, arrêter le run.** Ne pas écrire les scénarios soi-même, et ne pas
les déduire du code ou du diff. Des scénarios inventés testent ce que fait le code, pas ce que l'issue
demandait : ils passent donc toujours et ne prouvent rien. Dire à l'utilisateur que l'issue n'a rien
contre quoi tester, et que les scénarios doivent d'abord être définis dans l'issue. Le skill
`generate-ticket-scenarios` peut les écrire, mais c'est une décision séparée, prise sur l'issue, avant
ce run.

Garder les mots de l'auteur. Ne pas renommer un scénario pour qu'il colle à ce que fait le code : l'écart
entre les deux est exactement ce que le test cherche.

## Dire comment chaque scénario sera vérifié

Pour chaque scénario, choisir une valeur :

| Comment | Quand |
|---|---|
| `browser` | Les données dev locales ont un cas pour lui. |
| `automated test` | Un test unitaire existant (`*.test.tsx`) le couvre. Nommer le fichier ; on l'exécutera avec `npx vitest run <file>`. Un spec e2e est nommé dans le rapport mais **n'est pas exécuté** : il écrirait dans la base de la session. |
| `by hand` | Il demande un rôle, un tenant, ou une action que le run ne doit pas faire (envoyer un mail, un long import, tout ce qui atteint un tiers). |
| `not testable` | Les données locales n'ont pas de cas pour lui. Dire ce qui manque, puis suivre `data.md` : le cas peut souvent être créé. |

Pour trouver un test existant, chercher (grep) le nom du composant ou du use case sous
`frontend/src/**/*.test.tsx` et `frontend/tests/**/*.spec.ts`.

Un scénario qui a besoin d'un deuxième utilisateur (un contributeur, un validateur) est en général
`by hand`, sauf si les données dev contiennent déjà cet utilisateur : le run ne doit pas créer de
comptes.

## Vérifier les données avant de promettre un run navigateur

Avant de marquer un scénario `browser`, confirmer que le cas existe. Exemple : un scénario sur une
tâche de groupe a besoin d'une tâche dont le `__typename` est celui du groupe, pas d'une tâche
quelconque. Ouvrir l'écran de liste et regarder, ou lire la réponse GraphQL avec
`mcp__chrome-devtools__list_network_requests`.

Un scénario promis `browser` qui se révèle sans données va à l'étape 2 (`data.md`), pas directement au
rapport. Ne pas l'abandonner en silence.
