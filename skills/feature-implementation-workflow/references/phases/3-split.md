# Phase 3 — Découpage en pull requests

But : chaque plan a un découpage en pull requests validé, assez petit pour être relu.

## Travail

Lis les règles de couches de `split` (étape 2) dans `../stack-pull-requests/SKILL.md` et applique-les
aux étapes de chaque plan. Ne les recopie pas ici.

- Propose un tableau par plan : n, branche, périmètre (une phrase), étapes, tests, dépend de. Une couche
  frontend dépend de la couche backend qui lui donne le schéma GraphQL.
- Recommande une seule PR par plan quand il n'a qu'une préoccupation, et une stack quand il en a
  plusieurs indépendantes. Dis pourquoi en une ligne.
- Options du passage : `Valider le découpage` / `Changer quelque chose` / `Une seule PR par plan`.
- À la validation, écris chaque tableau dans son plan, dans `## Pull requests`, et mets
  `phase: implement`.
- Ne crée ni branche ni PR ici.

## Conditions de sortie

- [ ] Chaque plan a `## Pull requests` avec le tableau validé.
- [ ] Chaque étape est dans exactement une pull request.
- [ ] Chaque test est dans la pull request qui contient le code qu'il couvre. Le test e2e est dans celle
      qui expose le comportement.
- [ ] Une pull request frontend n'est jamais sous la pull request backend dont elle dépend.
- [ ] Chaque couche passe ses tests seule, sans dépendre d'une couche au-dessus.

Au passage, donne la commande pour reprendre après le compactage :
`/feature-implementation-workflow <issue>`. Une nouvelle session marche aussi : les plans portent l'état.

## Compacter après cette phase

Garde : le numéro de l'issue, les chemins des plans, la branche courante.
Jette : la discussion sur le découpage et les options non choisies.

```
/compact Garde : issue <n> ; chemins des plans ; branche courante. Jette : la discussion sur le découpage et les options refusées. Les tableaux de pull requests sont dans les plans.
```
