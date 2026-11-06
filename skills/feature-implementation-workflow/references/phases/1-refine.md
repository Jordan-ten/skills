# Phase 1 — Raffiner l'issue

But : l'issue contient des scénarios complets, cohérents avec le code et validés par l'utilisateur.

Langues : le grill et tous les échanges sont en français. Seul ce qui est écrit dans l'issue est en
anglais simple.

## Travail

1. **Lire l'issue.** `gh issue view <n> --json number,title,body,comments,labels,updatedAt,url`.
   Lis les commentaires : les décisions tardives y vivent souvent. Analyse le body avec
   `references/scenario-audit.md` (section « Lire l'issue »). Arrête-toi avec un message clair quand :
   - il n'y a aucun scénario `Nominal case` (dis à l'utilisateur de raffiner l'issue d'abord), ou
   - l'issue est un bug (dis à l'utilisateur d'utiliser le flow d'analyse de bug).
2. **Explorer le code, en silence.** Modules, entités, mots déjà utilisés (grep avant d'employer un
   mot), tests existants de la zone, `docs/product/<module>/overview.md`. Utilise un agent `Explore`
   quand la zone est large. Garde des notes pour l'audit et pour les plans.
3. **Auditer les scénarios** avec `references/scenario-audit.md`. Donne à l'utilisateur un verdict
   court, en français : `ready`, `gaps` ou `blocked`, et la liste des trouvailles (numérotées, une ligne
   chacune).
4. **Grill, puis corriger l'issue.**
   - Une question par trouvaille, dans l'ordre des dépendances (une décision peut supprimer des
     questions suivantes). Chaque question : la trouvaille, le fait du code derrière, la réponse
     recommandée. Tout en français.
   - Tiens un journal des décisions. Une décision produit va dans l'issue. Une décision technique va
     dans les plans.
   - Les edge cases refusés vont dans la ligne `Out of scope:` du Context de l'issue.
   - Quand toutes les trouvailles sont closes, construis le nouveau body de l'issue : seuls les
     scénarios, les groupes How to test correspondants, la ligne `Out of scope:` et la ligne `Design:`
     changent. Tout ce qui est écrit dans l'issue est en **anglais simple**. Chaque scénario ajouté ou
     modifié, et son groupe How to test, reçoit le flag (voir « Écrire dans l'issue » dans
     `references/scenario-audit.md`). Garde le format exact de l'issue. Montre le diff. Options du
     passage : `Appliquer à l'issue` / `Changer quelque chose` / `Arrêter`.
   - `Arrêter` termine le run : les plans ne peuvent pas être prêts tant que l'issue n'a pas un scénario.
   - Applique avec `gh issue edit <n> --body-file <fichier temporaire>` (fichier temporaire dans le
     scratchpad).

## Conditions de sortie

- [ ] L'audit n'a aucune trouvaille ouverte. Chacune a une réponse, ou est passée en `Out of scope:`.
- [ ] Le body de l'issue dans GitHub contient tous les scénarios convenus (relis-le avec
      `gh issue view` et vérifie).
- [ ] Le texte ajouté dans l'issue est en anglais simple.
- [ ] Chaque scénario ajouté ou modifié, et son groupe How to test, porte le flag.
- [ ] Scénarios et How to test sont synchronisés.
- [ ] Un scénario qui montre un écran a un lien design (Figma ou Claude Design) dans l'issue, ou
      l'utilisateur a confirmé qu'aucun n'est nécessaire.
- [ ] L'utilisateur a validé le diff avant l'écriture.

Au passage, si l'issue a le label `scenarios-approved` et que des scénarios ont été ajoutés, dis que le
PO doit les relire.

## Compacter après cette phase

Garde : numéro et URL de l'issue, verdict, titres des scénarios tels qu'ils sont maintenant dans
l'issue, lien `Design:`, décisions techniques du grill (mot pour mot, elles ne sont dans aucun fichier),
faits du code utiles aux plans (chemins de modules, d'entités et de tests, une ligne chacun).
Jette : texte de l'issue et des commentaires, contenus de fichiers et sorties de grep, trouvailles et
réponses résolues, le diff.

```
/compact Garde : issue <n> <url> ; titres des scénarios ; lien design ; décisions techniques du grill, mot pour mot ; chemins des modules, entités et tests existants utiles aux plans. Jette : texte de l'issue et des commentaires, sorties de fichiers et de grep, trouvailles et questions résolues, le diff.
```
