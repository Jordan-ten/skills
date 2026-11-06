# Quand un scénario n'a pas de données

Un scénario est souvent bloqué par un seul enregistrement manquant, pas par la fonctionnalité. Ne pas
l'abandonner, et ne pas changer ce qui existe pour qu'il rentre. Dire ce qui manque, laisser
l'utilisateur décider, et déléguer la création.

## 1. Dire exactement ce qui manque

Une ligne par enregistrement, avec les mots du domaine, et la propriété qui compte :

```
Scenario 2 (long label is readable in full)
  missing: one group task whose perimeter label is ~300 characters
  have:    "Division France" (15 characters), 4 sites
```

Ne jamais écrire "missing test data". L'utilisateur doit reconnaître l'enregistrement sans lire le code.

Vérifier d'abord que le cas est vraiment absent : il est souvent là sous un autre nom.

## 2. Demander, avec trois sorties

Une seule `AskUserQuestion` pour tout le plan, pas une par enregistrement. Dire dans quelle base on
écrirait (le backend sur le port 3000 est celui de dev dans une session dev).

| Option | Ce qui se passe |
|---|---|
| `Generate the data` | Suivre le skill `create-local-data`, puis exécuter les scénarios. |
| `I create it myself` | Donner le résumé, puis attendre. Rien n'est écrit. |
| `Skip these scenarios` | Ils vont dans le rapport en `NOT TESTABLE`, avec ce qui manquait. |

Par défaut, proposer, jamais faire. Écrire dans la base de l'utilisateur sans un oui est la seule chose
que ce skill ne doit pas faire.

## 3. La création

Le skill `create-local-data` s'en charge : il trouve la mutation, connaît l'ordre des appels, et les
envoie par l'API du backend avec un token offline-auth auto-signé. Ne pas réinventer le transport ici,
et ne jamais créer de données avec du SQL.

## 4. Après la création

- Exécuter les scénarios qui étaient bloqués.
- Lister chaque enregistrement créé dans le rapport, avec son id et son nom.
- Proposer les mutations de suppression à la fin du run. Ne pas supprimer de soi-même : l'utilisateur
  peut vouloir garder le cas pour un test ultérieur.
- Un enregistrement qui n'a pas pu être créé donne un scénario `NOT TESTABLE` avec l'erreur, pas un
  saut silencieux.
