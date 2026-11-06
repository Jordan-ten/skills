# Où les recettes de création sont déjà écrites

`frontend/tests/fixtures/` contient les fixtures des tests e2e. Chacune crée de vrais enregistrements
par la même API. Elles sont la référence pour **ce dont une création a besoin d'abord**, la partie
qu'un schéma ne dit jamais.

Lire la fixture avant de composer sa propre séquence. Ne pas l'importer, ne pas l'exécuter : prendre
les mutations et ce dont chacune a besoin, et les envoyer avec `scripts/graphql.sh`.

## Trouver le bon fichier

```bash
ls frontend/tests/fixtures/ | grep -i <domain>
grep -rn "mutation Create" frontend/tests/fixtures/<file>.ts
```

Les fichiers portent le nom du domaine (`<domain>Fixtures.ts`). Ne pas se fier à une liste : elle
vieillirait.

## Lire une fixture comme une recette

Un fichier de fixture donne trois choses :

| Quoi | Comment ça se voit |
|---|---|
| Les mutations et la forme de leur entrée | Les chaînes GraphQL du fichier. |
| Ce dont elle a besoin d'abord | Les recherches et les arguments des helpers `create*`. |
| Le nettoyage | Les helpers `delete*` correspondants. |

Exemple, `campaignFixtures.ts`. Ce que le code montre, et rien de plus :

- `createCampaignFixture` cherche d'abord un **id de business domain**, puis crée la campagne pour
  l'année en cours.
- `launchCampaignFixture` est la mutation `scheduleCampaign`, avec une date de début et deux dates de
  fin.
- `createCampaignTasksForQuestionnaire` a besoin d'un id de campagne, d'un **questionnaire publié
  trouvé par son nom** et d'une liste d'ids de contributing entities, puis crée les tâches en masse.

Les fixtures ne prouvent pas que ces étapes doivent s'exécuter dans cet ordre. Elles montrent ce dont
chacune a besoin. Quand l'ordre compte pour votre cas, le vérifier en lisant l'écran après chaque appel.

## Règles pratiques

- Un `create*Fixture` qui prend un id en argument dit ce qui doit exister d'abord.
- Une fixture avec `unique...Name()` crée des noms qui ne peuvent pas entrer en conflit. Faire pareil :
  préfixer ce qu'on crée pour que l'utilisateur distingue ses enregistrements des vôtres.
- Quand une fixture fait quelque chose que l'API ne peut pas faire (attendre un job, lire un token), le
  cas a besoin de cette étape aussi. Le dire plutôt que de créer un enregistrement à moitié.
