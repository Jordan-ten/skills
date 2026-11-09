---
name: review-fix
description: Traite les commentaires de review d'une PR GitHub. Vérifie que chaque commentaire est pertinent, les regroupe par famille, corrige tout de suite ceux qui ne demandent aucune décision, et propose des solutions une par une pour ceux qui demandent un choix. Refuse avec argument les corrections inutiles ou fausses. À invoquer quand l'utilisateur tape /review-fix, dit "corrige les commentaires de la PR", "traite la review", "fix PR comments" (address PR review comments).
disable-model-invocation: true
allowed-tools: Bash(git *), Bash(gh *), Read, Edit, Grep, Glob, AskUserQuestion
---

# Review fix

Argument optionnel : URL de PR, numéro de PR, ou URL/id d'un commentaire. Sans argument, la PR est celle de la branche courante.

Les réponses à l'utilisateur sont en français, courtes et simples. Le code, les commits et les commentaires de code restent en anglais simple.

## 1. Récupérer les commentaires

Lance en parallèle :

- `git branch --show-current`
- `gh pr view [PR] --json number,title,url,state`
- `gh pr view [PR] --json comments -q '.comments[] | "\(.author.login): \(.body)"'`
- `gh pr view [PR] --json reviews -q '.reviews[] | select(.body != "") | "\(.author.login) [\(.state)]: \(.body)"'`
- `gh pr diff [PR] --name-only`

Puis les commentaires inline non résolus :

```bash
gh api repos/{owner}/{repo}/pulls/{number}/comments --jq '[.[] | select((.resolved // false) == false)]'
```

Écarte les commentaires déjà traités par un commit récent (compare la date du commentaire, les messages de commit et le diff).

## 2. Valider chaque commentaire

Ne corrige jamais un commentaire juste parce qu'un relecteur (humain ou bot) le demande. Les bots proposent souvent des changements plausibles mais faux.

Pour chaque commentaire :

1. Lis le code concerné.
2. Vérifie que l'hypothèse du commentaire est vraie.
3. Vérifie que le changement proposé fait bien ce que le commentaire annonce.

Verdict :

- **Pertinent** : le problème existe et le changement est juste.
- **Non pertinent** : faux, hors sujet, ou déjà géré. Ne change rien. Explique pourquoi en une ou deux phrases, avec la preuve (fichier, ligne, comportement).
- **Doute** : tu ne peux pas confirmer. Traite-le comme un commentaire à décision (étape 4).

## 3. Regrouper par famille

Regroupe les commentaires pertinents par famille : nommage, tests, gestion d'erreurs, architecture, performance, sécurité, style, documentation, etc. Une famille = un même type de problème, pas un même fichier.

Dans chaque famille, sépare :

- **Sans décision** : une seule bonne correction, évidente (faute, renommage, import, suppression de code mort, refactor mécanique sans changement de comportement).
- **Avec décision** : plusieurs solutions valables, un compromis, un changement de comportement, un choix d'architecture, ou un conflit entre commentaires.

En cas de doute, classe en « avec décision ».

Affiche un plan court avant d'agir :

```
Famille : Nommage (3)
  sans décision : #1, #2
  avec décision : #3
Famille : Tests (2)
  ...
Non pertinents : #7 (raison en une ligne)
```

## 4. Corriger sans décision

Applique tout de suite les corrections « sans décision », famille par famille.

- Lis chaque fichier avant de l'éditer.
- Garde le changement minimal et lié au commentaire.
- Ne touche à rien d'autre.

## 5. Décisions, une par une

Pour chaque commentaire « avec décision », dans l'ordre des familles, utilise `AskUserQuestion` :

- Rappelle le commentaire en une phrase.
- Donne 2 à 3 options, chacune avec une phrase sur l'effet et le risque.
- Mets ta recommandation en premier, marquée `(Recommended)`.
- Une seule question à la fois. Attends la réponse avant la suivante.

Applique le choix tout de suite, puis passe au commentaire suivant. Si l'utilisateur répond « ne pas corriger », ne change rien.

## 6. Vérifier

Lance les vérifications utiles pour les fichiers touchés (types, lint, tests liés). Dis clairement ce qui échoue.

## 7. Rapport

Une liste plate, une ligne par commentaire traité. Chaque ligne commence par un lien Markdown vers le commentaire, avec un titre court. Ensuite, au plus deux phrases : ce qui a été fait, ou pourquoi rien n'a été changé.

```
**Corrigés**
- [Nom de la variable](https://github.com/owner/repo/pull/123#discussion_r1) : renommé `data` en `userEmails`.

**Corrigés après ta décision**
- [Retry sur l'appel](url) : option B choisie, retry limité à 3 essais.

**Non corrigés**
- [Ajouter un index](url) : la colonne a déjà un index dans la migration `xxx`.

**Vérifications**
- `tsc` OK, tests liés OK.
```

Omet une section si elle est vide.

## Règles

- Ne corrige que ce que tu as validé. Tout doute passe par l'utilisateur.
- Changements minimaux : seulement ce que le commentaire demande.
- Ne corrige pas un commentaire déjà résolu.
- Ne réponds pas sur GitHub, ne résous aucun thread, ne soumets aucune review, sauf demande explicite.
- Ne fais pas de commit sauf demande explicite.
- Si deux commentaires se contredisent, montre le conflit avant d'agir.
