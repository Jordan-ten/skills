# Phase 3 — Construire les scénarios

But : des scénarios complets et validés pour chaque tâche (nominal, edge, erreur). Tout se dit en français.
C'est le cœur du workflow et la phase la plus longue.

Les lots et les tâches viennent du pitch : ils ne sont pas discutés. Si l'utilisateur veut en changer un,
note-le dans `Open questions` de l'analyse (demande au PM) et continue.

Prends les tâches dans l'ordre du pitch, en sautant celles déjà `oui` ou `hors périmètre` dans le fichier
d'état (la phase est reprenable).

## Compléter

Avant de montrer une tâche, cherche ce qui manque dans ses scénarios :

- un état ou un champ du **lexique** et du code qu'aucun scénario ne couvre ;
- une **contrainte** (« Key constraints ») sans scénario, ou un scénario qui contredit le **hors-périmètre** ;
- une `Open questions` de l'analyse qui touche la tâche ;
- ce que dit le pitch (capture, sous-pages) et que l'analyse a oublié : tag `ajout` ;
- une dépendance avec une **autre tâche**, ou deux tâches qui disent la même chose autrement ;
- une issue existante du **milestone** qui couvre déjà le cas (seulement si un milestone est noté).

Puis audite les scénarios avec `${CLAUDE_PLUGIN_ROOT}/skills/feature-implementation-workflow/references/scenario-audit.md`,
section « Trouvailles », points 1 (structure), 2 (accord avec le code), 3 (couverture) et 6 (design, quand
un scénario montre un écran). Le point 4 (How to test) ne s'applique pas encore. Lis « issue » comme
« tâche du pitch » : un scénario du pitch n'a ni flag ni How to test.

## Contraintes

- Ce sont des propositions : l'utilisateur décide. N'ajoute jamais un scénario que ni le pitch ni le code
  ne justifient. Une capacité absente du pitch va dans `Open questions`, pas dans une tâche.
- **Subagent pour le code** : explore le code d'une tâche avec un subagent `Explore`, pas dans cette
  conversation. Donne-lui la tâche, ses scénarios et le lexique. Demande en retour 15 lignes au plus :
  états atteignables, champs et mots du code (avec fichier), et ce qui contredit un scénario.
- Une question par trouvaille, avec le fait du code derrière et ta réponse recommandée en premier.
  Une question dont le code connaît la réponse ne se pose pas.
- Écris chaque changement dans `<slug>.analysis.md` (section `Scenarios`) tout de suite : observable,
  GIVEN / WHEN / THEN, vrais noms et vraies valeurs, au moins un `Nominal case`.
- Clos chaque tâche avec une `AskUserQuestion` : `Valider la tâche` / `Changer quelque chose` / `Hors
  périmètre`. `Hors périmètre` demande une ligne de raison, écrite dans `Decisions` de l'analyse.
  Mets à jour la ligne de la tâche dans le fichier d'état (`oui` ou `hors périmètre`).
- Mets `phase: parcours` quand toutes les tâches sont `oui` ou `hors périmètre`, et après la relecture
  d'ensemble ci-dessous si elle a eu lieu.

## Relecture d'ensemble (6 tâches validées ou plus)

L'audit regarde une tâche à la fois : il peut rater une contradiction entre deux tâches. Quand 6 tâches ou
plus sont `oui`, propose `Relire tous les scénarios ensemble` / `Passer aux parcours`. Si l'utilisateur
accepte, relis tous les scénarios validés de `<slug>.analysis.md` d'un coup et cherche :

- deux tâches qui posent des règles contradictoires (statut, droit, limite) ;
- un état produit par une tâche et jamais consommé, ou consommé sans être atteignable ;
- une même règle écrite de deux façons ;
- un cas à la frontière entre deux tâches (rôle, suppression, état intermédiaire) qu'aucune ne couvre.

Une question par trouvaille, avec la réponse recommandée en premier. N'en pose aucune déjà tranchée plus
haut. Écris chaque décision dans l'analyse tout de suite. Arrête-toi quand la liste est vide ou que
l'utilisateur dit stop. Sans trouvaille, ne pose aucune question.

## Conditions de sortie

- [ ] Chaque tâche du fichier d'état est `oui` ou `hors périmètre`. Chaque `hors périmètre` a une raison dans
      `Decisions`.
- [ ] Chaque tâche `oui` a au moins un `Nominal case` dans l'analyse, et plus aucune trouvaille ouverte.
- [ ] Chaque décision de l'utilisateur (scénario changé, `hors périmètre`, raison) est écrite dans l'analyse
      ou le fichier d'état : rien ne reste seulement dans la conversation.
- [ ] Avec 6 tâches `oui` ou plus : la relecture d'ensemble est faite, ou l'utilisateur l'a refusée.
- [ ] Les questions pour le PM sont dans `Open questions`. Aucune ne bloque la création des issues, ou
      l'utilisateur a dit lesquelles bloquent.
