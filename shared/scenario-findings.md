# Trouvailles sur des scénarios

Vérifications communes aux workflows qui auditent des scénarios : une issue GitHub
(`feature-implementation-workflow`) ou une tâche d'un pitch (`issue-workflow`). Chaque workflow dit quelles
vérifications il applique et ajoute les siennes.

« Source » veut dire l'endroit où les scénarios vivent : le body d'une issue, ou l'analyse du pitch.

Une trouvaille = une ligne = une question plus tard. Les trouvailles et les questions sont en français.

## Vérifications

1. **Structure**
   - Au moins un `Nominal case`.
   - Chaque scénario a Given, When, Then, avec de vrais noms et de vraies valeurs.
   - Chaque `Then` est observable par un utilisateur (écran, message, fichier exporté), pas un état
     interne.
   - Un `When` décrit l'intention de l'utilisateur (« supprime la ligne »), pas l'interface (« clique sur
     le bouton rouge », « remplit le champ »). Un `When` qui nomme un bouton, un champ ou un écran précis
     est une trouvaille : il casse dès que l'écran change.
   - Chaque scénario a un **mode de vérification** (`manual`, `e2e` ou `unit`, voir plus bas). Un scénario
     qu'aucun mode ne peut vérifier est une trouvaille : son `Then` n'est pas assez observable.
2. **Accord avec le code** (utilise les notes de code de l'exploration)
   - Chaque état du `Given` existe et peut être atteint. Les entités et champs qu'il nomme existent.
   - Les mots sont ceux du code. Signale un mot qui n'apparaît nulle part dans `src/`.
   - Deux scénarios ne se contredisent pas.
   - Les scénarios respectent `Out of scope`.
3. **Couverture.** Cherche des cas que la source ne dit pas, à partir du code de la zone. N'en propose un
   que si le code montre qu'il est atteignable :
   - permission : un utilisateur sans le droit
   - état vide, un seul élément, beaucoup d'éléments, une limite
   - valeur en double ou déjà existante
   - un élément supprimé, archivé ou dans un autre état entre deux actions
   - une autre organisation (multi-tenant)
   - données existantes avant la feature (migration, valeur par défaut)
   - entrée invalide, échec partiel
   - l'API ou le schéma GraphQL change (consommateurs, SDK, codegen)
   - un écran : chargement, erreur, traduction

   Reste sobre : plus de scénarios ne veut pas dire mieux. Ne propose un cas que s'il change le résultat
   que voit l'utilisateur. Deux scénarios qui vérifient la même règle avec d'autres valeurs sont une
   trouvaille : fusionne-les en un seul, et garde l'exemple le plus parlant.
4. **Design.** Seulement quand un scénario montre un écran ou un changement d'UI. Cherche dans la source
   (body et commentaires d'une issue, capture et analyse d'un pitch) un lien design : Figma
   (`figma.com`) ou Claude Design (un lien `claude.ai/.../artifact/...`). Sans lien, c'est une
   trouvaille. Demande le lien, ou demande de confirmer qu'aucun design n'est nécessaire (composants
   existants du design system seulement). Signale aussi un scénario dont les états d'écran (vide,
   chargement, erreur) ne sont pas dans le design, quand le lien est connu et lisible.

## Mode de vérification

Chaque scénario est vérifié d'une seule façon principale. Recommande le mode, l'utilisateur tranche.

| Mode | Quand | Où il vit dans l'issue |
|---|---|---|
| `e2e` | Un chemin métier complet, de l'action au résultat visible (le nominal, les cas à vrai risque). C'est le mode par défaut. | `Automated test: e2e — <titre du scénario>` dans `### Technical notes` |
| `unit` | Une règle de calcul ou de décision non triviale, qu'on isole du reste. | `Automated test: unit — <titre du scénario>` dans `### Technical notes` |
| `manual` | Ce qu'un test automatique ne voit pas bien : une mise en page, un fichier exporté à lire, un texte à relire. | Un groupe `### ...` dans `## How to test` |

Un scénario peut avoir un test automatique et un groupe How to test : le test prouve la règle, le groupe
guide la QA. Dans ce cas, le mode principal est le test automatique.

## Format d'une question

```
Trouvaille 3/7 — Edge case : un utilisateur sans le droit.
Code : `update.xxx.usecase.ts` vérifie `Permission.XXX` ; la source ne dit pas ce que l'utilisateur voit.
Recommandé : afficher l'erreur « non autorisé », rien n'est enregistré.
Options : <recommandé> / <autre> / Hors périmètre
```
