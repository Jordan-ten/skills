# Audit des scénarios

Les scénarios sont ce que l'agent vérifie le plus. Tout le reste de l'issue est du contexte.

Langues : les trouvailles, les questions et le verdict sont en français. Ce qui est écrit dans l'issue
(scénarios, How to test, `Out of scope:`, `Design:`, flag) est en anglais simple.

## Lire l'issue

Deux formats de body existent. Détecte lequel.

**Feature checklist** (template `feature-checklist`) :

- `## Context` (la dernière ligne peut être `Out of scope: ...`)
- `## Reproduction steps` (parcours utilisateur jusqu'au cas nominal)
- `<details><summary>Scenarios</summary>` avec un titre en gras par scénario et un bloc `gherkin` :
  `**Nominal case: ...**`, `**Edge case: ...**`, `**Error case: ...**`
- `## How to test` avec des groupes `###` de cases `- [ ]`, un groupe par scénario important
- `### Technical notes` (optionnel)

**Issue raffinée** (le body a le marqueur `<!-- traace-agent-refined`) : les scénarios sont dans
`## Test scenarios`. Utilise les sections publiées telles quelles. Les `## Open questions` sont des
inconnues déjà connues : mets chacune dans le grill, ne réponds jamais seul. Le texte d'origine est
dans un bloc `<details>`.

Autre format : prends les scénarios là où ils sont, et dis dans le verdict que le format n'est pas
standard.

## Trouvailles

Vérifie dans cet ordre. Une trouvaille = une ligne = une question plus tard.

1. **Structure**
   - Au moins un `Nominal case`.
   - Chaque scénario a Given, When, Then, avec de vrais noms et de vraies valeurs.
   - Chaque `Then` est observable par un utilisateur (écran, message, fichier exporté), pas un état
     interne.
2. **Accord avec le code** (utilise les notes de code de l'exploration)
   - Chaque état du `Given` existe et peut être atteint. Les entités et champs qu'il nomme existent.
   - Les mots sont ceux du code. Signale un mot qui n'apparaît nulle part dans `src/`.
   - Deux scénarios ne se contredisent pas.
   - Les scénarios respectent `Out of scope`.
3. **Couverture.** Cherche des cas que l'issue ne dit pas, à partir du code de la zone. N'en propose un
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
4. **Synchro.** Chaque groupe `How to test` vient d'un scénario, et chaque scénario important a un
   groupe. `Reproduction steps` mène au cas nominal.
5. **Points ouverts.** Les marques `<to confirm>` et les `Open questions` de l'issue. Chacun est une
   trouvaille.
6. **Design.** Seulement quand un scénario montre un écran ou un changement d'UI. Cherche dans le body et
   les commentaires un lien design : Figma (`figma.com`) ou Claude Design (un lien
   `claude.ai/.../artifact/...`). Sans lien, c'est une trouvaille. Demande le lien, ou demande de
   confirmer qu'aucun design n'est nécessaire (composants existants du design system seulement).
   Signale aussi un scénario dont les états d'écran (vide, chargement, erreur) ne sont pas dans le
   design, quand le lien est connu et lisible.

Verdict : `ready` (aucune trouvaille), `gaps` (des trouvailles, toutes closables par l'utilisateur),
`blocked` (une trouvaille demande une autre personne que l'utilisateur, ou l'issue contredit le code
d'une façon que l'utilisateur ne peut pas trancher).

## Format d'une question

```
Trouvaille 3/7 — Edge case : un utilisateur sans le droit.
Code : `update.xxx.usecase.ts` vérifie `Permission.XXX` ; l'issue ne dit pas ce que l'utilisateur voit.
Recommandé : afficher l'erreur « non autorisé », rien n'est enregistré.
Options : <recommandé> / <autre> / Hors périmètre
```

## Écrire dans l'issue

Seules ces parties changent dans le body de l'issue : les scénarios, les groupes How to test
correspondants, `Out of scope:` et `Design:`. Tout le reste reste identique à l'octet près, y compris le
`<details>` d'origine d'une issue raffinée. Tout ce que tu écris est en **anglais simple**.

`Design:` est une ligne de `## Context`, après `Out of scope:` quand les deux existent :
`Design: <url>`. Le lien est un lien Figma ou Claude Design. Ajoute-la seulement quand l'utilisateur
donne un lien design dans le grill et que l'issue n'en a pas. Le skill n'ouvre jamais le lien : il le
stocke et vérifie qu'il est là.

- Nouveau scénario : titre en gras avec le bon préfixe, puis le flag (ci-dessous), puis un bloc
  `gherkin`, dans le `<details>` replié. Garde la ligne vide après `</summary>` et avant `</details>`.
- Nouveau groupe `How to test` seulement quand un utilisateur peut faire la vérification à la main.
  Sinon écris `Automated test: ...` dans `### Technical notes`. Le groupe a le même flag machine, juste
  sous son titre `###`.
- Un scénario modifié modifie son groupe. Scénarios et How to test restent synchronisés.
- Issue raffinée : écris dans `## Test scenarios` avec le même style que la section.
- Montre le diff du body avant d'écrire.

### Flag d'un scénario ajouté

Deux lignes juste sous le titre en gras du scénario :

```markdown
**Edge case: a user without the right**
<!-- feature-implementation-workflow: added YYYY-MM-DD -->
_Added during planning. To review by the PO._
```

- Le commentaire HTML est pour les outils. Il est invisible dans le rendu. Sers-t'en pour retrouver les
  scénarios ajoutés par ce skill. Au deuxième run, ne réécris jamais un scénario flaggé sans demander à
  l'utilisateur.
- La ligne en italique est pour les humains. Le PO la supprime, et peut supprimer le commentaire, une
  fois le scénario relu.
- Le titre ne change jamais : le plan le cite tel quel.
- Un scénario déjà existant garde son texte et n'a pas de flag. Un scénario que l'utilisateur modifie
  pendant le grill garde son texte avec la modification, et reçoit aussi le flag.

### Label d'approbation

Quand l'issue a le label `scenarios-approved`, l'approbation du PO ne couvre pas les scénarios ajoutés.
Dis-le à la fin du run. Ne retire et n'ajoute jamais un label.
