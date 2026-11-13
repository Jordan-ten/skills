---
name: feature-implementation-workflow
description: >
  Slash uniquement. À utiliser seulement quand l'utilisateur lance explicitement
  /feature-implementation-workflow avec l'URL ou le numéro d'une issue GitHub de feature. Mène une
  feature de l'issue à la pull request en six phases, chacune avec des conditions de sortie à prouver
  avant la suivante : raffiner les scénarios de l'issue, écrire un plan par package, découper en pull
  requests, implémenter, vérifier (code généré, tous les tests, bout en bout dans l'UI), puis pousser.
  Reprenable : relancer la commande sur la même issue continue là où on s'est arrêté. Ne jamais
  déclencher depuis une demande en langage naturel.
disable-model-invocation: true
allowed-tools: Bash(gh issue view *), Bash(gh issue edit *), Bash(gh pr *), Bash(git *), Bash(npm run *), Bash(npx vitest *), Read, Write, Edit, Grep, Glob, Agent, AskUserQuestion, Skill
---

# Workflow d'implémentation d'une feature

De l'issue d'une feature aux pull requests. Le workflow est découpé en phases. Une phase se termine
seulement quand ses conditions de sortie sont vraies et prouvées. Ensuite l'utilisateur décide de
continuer.

- **L'issue est la source de vérité** du comportement : contexte, scénarios, hors périmètre, lien design.
- **Un plan est la définition de l'implémentation** d'un package (backend, frontend) : approche,
  étapes, tests. Il ne recopie jamais le comportement. Il renvoie aux scénarios par leur titre.

Entrée : `/feature-implementation-workflow <url-ou-numéro-de-l-issue>`.

## Langues

| Texte | Langue |
|---|---|
| Échanges avec l'utilisateur, y compris le grill avant la mise à jour de l'issue | français |
| Plans (`.claude/plans/`) | français |
| Mise à jour de l'issue (scénarios, How to test, `Out of scope:`, `Design:`, flag) | anglais simple |
| Commits et pull requests | anglais simple (`AGENTS.md`) |

Dans un plan, les titres de scénarios sont cités tels qu'ils sont dans l'issue (en anglais), et les
identifiants de code restent tels quels.

## Phases

Chaque phase a un fichier dans `references/phases/`. Lis le fichier d'une phase quand tu y entres, pas avant.

| # | Phase | Conditions de sortie (toutes vraies et prouvées) | Fichier |
|---|---|---|---|
| 1 | Raffiner l'issue | Toutes les trouvailles de l'audit sont closes. L'issue contient les scénarios convenus (flaggés), How to test et le lien design. L'utilisateur a validé le diff. | `1-refine.md` |
| 2 | Plans | Un plan par package touché. Le contrôle de cohérence passe. `Questions non résolues : aucune`, `status: ready`. L'utilisateur a validé les plans. | `2-plan.md` |
| 3 | Découpage | Taille estimée (hors fichiers générés, seuil d'environ 30). Une PR ou plusieurs, avec la pile de commits de chacune, validées et écrites dans les plans. | `3-split.md` |
| 4 | Implémenter | Par commit : étapes faites et prouvées, tests écrits, type check, lint, problèmes IDE, OpenGrep, tests unitaires et d'intégration créés, modifiés ou impactés : tout est vert. Commit fait. | `4-implement.md` |
| 5 | Vérifier | Code généré à jour. Le harnais passe (tests unitaires, d'intégration et e2e créés, modifiés ou impactés, jamais la suite complète). Chaque scénario de l'issue a un verdict `pass` dans l'UI. | `5-verify.md` |
| 6 | Livrer | L'utilisateur a validé le push. Branches poussées, pull request(s) ouverte(s), plans marqués terminés. | `6-ship.md` |

Fichiers de référence utilisés par plusieurs phases : `references/scenario-audit.md`,
`../write-implementation-plan/references/plan-template.md` (template unique des plans).

## Passage d'une phase à l'autre

À la fin d'une phase :

1. Affiche les conditions de sortie sous forme de liste. Chaque ligne : ✅ ou ❌, et la preuve en
   quelques mots (commande et résultat, ou fichier et section). Une condition sans preuve est ❌.
2. Tout est ✅ : sauvegarde d'abord l'état (`phase:` dans les plans, issue déjà écrite). Puis pose une
   seule `AskUserQuestion` : `Compacter, puis passer à la phase <n+1>` (recommandé) / `Passer à la
   phase <n+1> sans compacter` / `Refaire quelque chose` / `Arrêter`.
3. Un ❌ : corrige-le, ou reviens à la phase qui possède la cause. Ne propose jamais de continuer avec
   un ❌.

Ne saute jamais une phase et ne commence jamais la suivante avant le passage. L'utilisateur peut
s'arrêter à n'importe quel passage.

## Compacter entre les phases

But : jeter ce dont la phase suivante n'a pas besoin. Le modèle ne peut pas lancer `/compact` lui-même.

**Principe : ne garde que ce qui n'existe dans aucun fichier.** Tout le reste se relit (issue, plans, git)
et se jette : contenus de fichiers, diffs, sorties de commandes, logs, discussions résolues. Garde
toujours le numéro de l'issue et les chemins des plans. Chaque phase dit dans sa section `Compactage` ce
qui n'existe que dans la conversation.

Sur `Compacter, puis passer à la phase <n+1>` :

1. Compose la ligne `/compact` : le numéro de l'issue, les chemins des plans, et ce que la section
   `Compactage` de la phase qui se termine liste.
2. Affiche-la dans un seul bloc de code, prête à coller. Dis en une ligne ce qu'elle garde.
3. Arrête-toi et attends. Ne commence pas la phase suivante. L'utilisateur lance la ligne, puis dit
   `continue` (ou relance la commande de ce skill). Suis alors « Reprise ».

Après un compactage, fais confiance aux fichiers (issue, plans, git), pas au souvenir de l'ancienne
conversation.

## Reprise

L'état est dans l'en-tête des plans (`phase: <prochaine phase à lancer>`) et dans l'issue. Au début
d'un run :

1. Lis l'issue. Cherche les plans dans le dossier de travail de chaque package :
   `.claude/plans/<n>-*.md` dans le dossier courant (`backend/` ou `frontend/`), et le plan de
   l'autre package dans `../frontend/.claude/plans/` ou `../backend/.claude/plans/`. Depuis
   la racine du repo, regarde dans `backend/` et `frontend/`.
2. Aucun plan : commence à la phase 1. Des plans existent : prends la plus petite `phase` des plans.
3. Ne fais pas confiance à l'état. Revérifie les conditions de sortie de la phase juste avant (et la date
   de mise à jour de l'issue contre `issue_updated_at` des plans). Si l'une échoue, reviens à cette phase
   et dis pourquoi.
4. Dis à l'utilisateur où le run reprend, puis continue.

Après la phase 3, une nouvelle session convient aussi : la même commande reprend à la phase 4. Seule la
phase 1 garde des faits hors des fichiers (les décisions techniques du grill, jusqu'à ce que la phase 2
les écrive dans les plans) : ne démarre pas de nouvelle session entre la phase 1 et la phase 2,
compacte à la place.

## Règles

- Réponds dans la langue de l'utilisateur (français). Voir le tableau « Langues » pour les textes écrits.
- Le produit s'appelle Tennaxia (règle de nommage de `AGENTS.md`).
- Pas de code, pas de branche, avant la phase 4. Avant la phase 4, la seule écriture sur GitHub est
  `gh issue edit --body-file`, après validation du diff par l'utilisateur. Ne touche jamais au titre,
  aux labels, au milestone, aux assignés ni à l'état, à aucune phase.
- N'invente jamais une règle métier. Un edge case ou un cas d'erreur est une proposition : c'est
  l'utilisateur qui décide.
- Une question dont le code connaît la réponse ne se pose pas. Explore d'abord, ne demande que des décisions.
- Une seule question à la fois avec `AskUserQuestion`. La réponse recommandée est la première option.
- Les actions vers l'extérieur (push, pull request, modification de l'issue) n'ont lieu qu'après un oui
  donné dans cette phase.
- Réutilise l'existant. Appelle `launch` et `run-qa-scenarios` avec l'outil `Skill`. Les skills en slash
  uniquement (`stack`, `write-implementation-plan`) ne peuvent pas être appelés : lis leur `SKILL.md` et
  suis la sous-commande ou les étapes. Ne recopie pas leurs règles ici.

## Sous-skills

Les phases partagent un même état (issue, plans, décisions) et une même règle de passage, et le modèle
ne peut pas appeler un sous-skill en slash uniquement. Les phases restent donc des fichiers de ce skill.
Extrais une phase dans son propre skill quand un deuxième usage en a besoin, pas avant.

Déjà extrait : la méthode de plan, dans `write-implementation-plan` (utilisable seule, hors de ce
workflow). La phase 2 la lit et ajoute l'en-tête, les chemins, le design, le contrat backend et le
découpage en PR. Prochain candidat : la vérification.
