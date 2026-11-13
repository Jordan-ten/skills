# Phase 1 — Raffiner l'issue

But : l'issue contient des scénarios complets, cohérents avec le code et validés par l'utilisateur.

Langues : le grill et tous les échanges sont en français. Seul ce qui est écrit dans l'issue est en
anglais simple.

## Contraintes

- **Lecture.** Lis l'issue avec ses commentaires (`gh issue view <n> --json
  number,title,body,comments,labels,updatedAt,url`) : les décisions tardives y vivent souvent. Analyse le
  body avec `references/scenario-audit.md` (section « Lire l'issue »). Arrête-toi avec un message clair
  quand il n'y a aucun scénario `Nominal case` (dis à l'utilisateur de raffiner l'issue d'abord), ou quand
  l'issue est un bug (dis-lui d'utiliser le flow d'analyse de bug).
- **Exploration silencieuse.** Modules, entités, mots déjà utilisés (grep avant d'employer un mot), tests
  de la zone, `docs/product/<module>/overview.md`. Un agent `Explore` quand la zone est large. Garde des
  notes pour l'audit et les plans.
- **Audit.** Avec `references/scenario-audit.md`. Donne un verdict court en français (`ready`, `gaps` ou
  `blocked`) et les trouvailles, numérotées, une ligne chacune.
- **Grill.** Une question par trouvaille, dans l'ordre des dépendances (une décision peut supprimer des
  questions suivantes). Chaque question donne la trouvaille, le fait du code derrière et la réponse
  recommandée.
  - Tiens un journal des décisions : une décision produit va dans l'issue, une décision technique dans les
    plans.
  - Les edge cases refusés vont dans la ligne `Out of scope:` du Context de l'issue.
- **Écriture dans l'issue.** Seuls les scénarios, les groupes How to test correspondants, la ligne
  `Out of scope:` et la ligne `Design:` changent. Le texte écrit est en **anglais simple**. Chaque scénario
  ajouté ou modifié, et son groupe How to test, reçoit le flag (voir « Écrire dans l'issue » dans
  `references/scenario-audit.md`). Garde le format exact de l'issue.
- **Validation avant écriture.** Montre le diff du body et n'écris qu'après l'accord de l'utilisateur, avec
  `gh issue edit <n> --body-file <fichier>` (fichier temporaire dans le scratchpad). S'il arrête, le run
  s'arrête : les plans ne peuvent pas être prêts sans scénario.

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

## Compactage

Seulement dans la conversation : les décisions techniques du grill, mot pour mot (la phase 2 les écrit
dans les plans), et les faits du code utiles aux plans (chemins de modules, d'entités et de tests, une
ligne chacun).
