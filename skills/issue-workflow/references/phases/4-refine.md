# Phase 4 — Raffiner et compléter : les scénarios, puis les parcours

But : compléter les scénarios de chaque tâche à partir de l'analyse, puis les faire valider par
l'utilisateur (nominal, edge, erreur), puis valider chaque parcours. Tout se dit en français. C'est le
cœur du workflow et la phase la plus longue.

Les lots et les tâches viennent du pitch : ils ne sont pas discutés ici. Si l'utilisateur veut en changer
un, note-le dans `Open questions` de l'analyse (demande au PM) et continue.

## A. Scénarios, une tâche à la fois

Prends les tâches dans l'ordre du pitch, en sautant celles déjà `oui` ou `hors périmètre` dans le fichier
d'état (la phase est reprenable).

### Compléter à partir de l'analyse

Pour chaque tâche, avant de la montrer, cherche ce qui manque dans ses scénarios, avec ce que l'analyse
sait déjà :

- le **lexique** et le code qu'elle a trouvé : un état ou un champ que le code montre atteignable et
  qu'aucun scénario ne couvre ;
- ses **contraintes** (« Key constraints ») et son **hors-périmètre** : un scénario qui les contredit, ou
  une contrainte sans scénario ;
- ses **questions ouvertes** (`Open questions`) qui touchent la tâche : chacune est une trouvaille ;
- ce que dit le pitch pour cette tâche (capture, sous-pages) et que l'analyse a oublié : tag `ajout` ;
- les **autres tâches** : un scénario qui dépend du résultat d'une autre tâche, ou deux tâches qui
  disent la même chose autrement ;
- le **milestone**, s'il y en a un : une issue existante qui couvre déjà le cas.

Ce sont des propositions : l'utilisateur décide. N'ajoute jamais un scénario que ni le pitch ni le code ne
justifient.

### Valider la tâche

Pour chaque tâche :

1. Montre ses scénarios en liste courte (situation → résultat, avec leurs tags).
2. Audite-les avec `../feature-implementation-workflow/references/scenario-audit.md`, section
   « Trouvailles », points 1 (structure), 2 (accord avec le code), 3 (couverture) et 6 (design, quand un
   scénario montre un écran). Le point 4 (How to test) ne s'applique pas encore. Explore le code en
   silence avant de poser une question. Adapte « issue » en « tâche du pitch » : un scénario du pitch n'a ni
   flag ni How to test.
3. Une question par trouvaille, avec le fait du code derrière et ta réponse recommandée en premier
   (format de question du même fichier). Un cas que le pitch ne dit pas est une proposition.
4. Écris chaque changement dans `<slug>.analysis.md` tout de suite (section `Scenarios`), avec les mêmes
   règles que l'analyse : observable, GIVEN / WHEN / THEN, vrais noms et vraies valeurs, au moins un
   `Nominal case`. Une capacité absente du pitch va dans `Open questions`, pas dans une tâche.
5. Une `AskUserQuestion` pour clore la tâche : `Valider la tâche` / `Changer quelque chose` / `Hors
   périmètre`. `Hors périmètre` demande une ligne de raison, écrite dans `Decisions` de l'analyse.
6. Mets à jour la ligne de la tâche dans le fichier d'état : `oui` ou `hors périmètre`.

## B. Parcours, un à la fois

Quand toutes les tâches sont `oui` ou `hors périmètre`. Pour chaque parcours de `<slug>.overview.json` :

1. Montre-le : titre, acteurs, étapes (situation → résultat, numéros de tâches).
2. Vérifie :
   - chaque numéro de tâche d'une étape existe et n'est pas `hors périmètre` ;
   - le résultat d'une étape alimente la situation de la suivante ;
   - les rôles sont les mêmes que ceux des tâches citées.
3. Corrige avec l'utilisateur jusqu'à un « ok » explicite. Écris les changements dans `<slug>.overview.json`
   (règles de `../build-scenario-overview/references/data-format.md`).
4. Mets `Validé : oui` dans le fichier d'état.

Quand tous les parcours sont validés, liste les tâches `Must` dans aucun parcours. Chacune a une décision
de l'utilisateur : l'ajouter à un parcours, ou accepter qu'elle soit seule.

Ne reconstruis pas la page ici : c'est la phase 6. Mets `phase: issues` dans le fichier d'état quand tout
est validé.

## Conditions de sortie

- [ ] Chaque tâche du fichier d'état est `oui` ou `hors périmètre`. Chaque `hors périmètre` a une raison dans
      `Decisions`.
- [ ] Chaque tâche `oui` a au moins un `Nominal case` dans l'analyse, et plus aucune trouvaille ouverte.
- [ ] Chaque parcours du fichier d'état est validé, et chaque étape renvoie à des tâches existantes.
- [ ] Chaque tâche `Must` dans aucun parcours a une décision explicite.
- [ ] L'analyse et `<slug>.overview.json` ont les mêmes tâches et les mêmes parcours (compte les scénarios
      par tâche pour le prouver).
- [ ] Les questions pour le PM sont dans `Open questions` de l'analyse. Aucune ne bloque la création des
      issues, ou l'utilisateur a dit lesquelles bloquent.

## Compacter après cette phase

La phase 4 est longue : propose le compactage aussi après chaque lot de tâches validées. Tout est dans les
fichiers.

Garde : le slug, les numéros de tâches `oui` et `hors périmètre`, les décisions de l'utilisateur qui ne
sont pas encore écrites.
Jette : les audits et le code lu, les questions déjà résolues.

```
/compact Garde : pitch <slug> ; tâches validées et hors périmètre (numéros) ; décisions pas encore écrites. Jette : audits, code lu, questions résolues. L'état est dans .claude/plans/pitch/<slug>.workflow.md.
```
