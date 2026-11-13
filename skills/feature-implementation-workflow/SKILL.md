---
name: feature-implementation-workflow
description: >
  Slash uniquement. À utiliser seulement quand l'utilisateur lance explicitement
  /feature-implementation-workflow avec l'URL ou le numéro d'une issue GitHub de feature. Mène une
  feature de l'issue à la pull request en cinq phases, chacune avec des conditions de sortie à prouver
  avant la suivante : raffiner les scénarios de l'issue, écrire un plan par package et le découpage en
  pull requests, implémenter (un sous-agent par pull request), relire avec /code-review et vérifier
  (tous les tests, bout en bout dans l'UI), puis pousser. La session principale reste légère : le travail
  lourd tourne dans des sous-agents. Reprenable : relancer la commande sur la même issue continue là
  où on s'est arrêté. Ne jamais déclencher depuis une demande en langage naturel.
disable-model-invocation: true
allowed-tools: Bash(gh issue view *), Bash(gh pr view *), Bash(gh pr list *), Bash(gh stack view *), Bash(gh stack init *), Bash(gh stack add *), Bash(gh stack checkout *), Bash(git status *), Bash(git diff *), Bash(git log *), Bash(git show *), Bash(git rev-parse *), Bash(git add *), Bash(git commit *), Bash(git switch *), Bash(npm run *), Bash(npx vitest *), mcp__idea__get_file_problems, Read, Write, Edit, Grep, Glob, Agent, SendMessage, AskUserQuestion, Skill
---

# Workflow d'implémentation d'une feature

De l'issue d'une feature aux pull requests. Le workflow est découpé en phases. Une phase se termine
seulement quand ses conditions de sortie sont vraies et prouvées. Ensuite l'utilisateur décide de
continuer.

- **L'issue est la source de vérité** du comportement : contexte, scénarios, hors périmètre, lien design.
- **Un plan est la définition de l'implémentation** d'un package (backend, frontend) : approche,
  étapes, tests. Il ne recopie jamais le comportement. Il renvoie aux scénarios par leur titre.
- **Les fichiers portent l'état**, jamais la conversation (voir « Fichiers du run »).

Entrée : `/feature-implementation-workflow <url-ou-numéro-de-l-issue>`.

`allowed-tools` n'approuve volontairement ni `git push`, ni `gh pr create`, ni `gh issue edit`, ni
`gh stack push|submit` : le harnais demande une confirmation pour chaque action vers l'extérieur.

## Langues

| Texte | Langue |
|---|---|
| Échanges avec l'utilisateur, y compris le grill avant la mise à jour de l'issue | français |
| Plans et notes du run (`.claude/plans/`) | français |
| Mise à jour de l'issue (scénarios, How to test, `Out of scope:`, `Design:`, flag) | anglais simple |
| Commits et pull requests | anglais simple (`AGENTS.md`) |

Dans un plan, les titres de scénarios sont cités tels qu'ils sont dans l'issue (en anglais), et les
identifiants de code restent tels quels.

## Phases

Chaque phase a un fichier dans `references/phases/`. Lis le fichier d'une phase quand tu y entres, pas
avant. Les conditions de sortie sont dans ce fichier, et nulle part ailleurs.

| # | Phase | But | Où elle tourne | Fichier |
|---|---|---|---|---|
| 1 | Raffiner l'issue | L'issue contient les scénarios convenus, validés par l'utilisateur. | session principale | `1-refine.md` |
| 2 | Plans et découpage | Un plan par package touché, sans question ouverte, avec le découpage en pull requests, validés ensemble. | session principale | `2-plan.md` |
| 3 | Implémenter | Code, tests et commits atomiques de chaque PR, tout vert. | **un sous-agent par PR** | `3-implement.md` |
| 4 | Relire et vérifier | `/code-review high`, puis e2e et scénarios dans l'UI. | relecture : principale ; tests : **un sous-agent** | `4-verify.md` |
| 5 | Livrer | Branches poussées, PR ouvertes, après un oui. | session principale | `5-ship.md` |

Fichiers de référence : `references/scenario-audit.md` (phases 1 et 2), `references/subagent.md` (phases 3
et 4), `../write-implementation-plan/references/plan-template.md` (template unique des plans).

## Passage d'une phase à l'autre

À la fin d'une phase :

1. Affiche les conditions de sortie du fichier de la phase sous forme de liste. Chaque ligne : ✅ ou ❌,
   et la preuve en quelques mots (commande et résultat, ou fichier et section). Une condition sans
   preuve est ❌. Ce qui se vérifie en une commande (`git status --short`, `git log`, `gh issue view`),
   vérifie-le toi-même au lieu de croire un rapport.
2. Tout est ✅ : sauvegarde d'abord l'état (`phase:` dans les plans, issue déjà écrite). Puis pose une
   seule `AskUserQuestion` : `Passer à la phase <n+1>` (recommandé) / `Refaire quelque chose` /
   `Arrêter`.
3. Un ❌ : corrige-le, ou reviens à la phase qui possède la cause. Ne propose jamais de continuer avec
   un ❌.

Ne saute jamais une phase et ne commence jamais la suivante avant le passage. L'utilisateur peut
s'arrêter à n'importe quel passage.

## Contexte : une session principale légère

La session principale parle à l'utilisateur, décide, vérifie et délègue. Elle ne garde pas de diffs, de
logs ni de sorties de tests.

- **Sous-agents.** Les phases 3 et 4 (tests) tournent dans des sous-agents `general-purpose` au contexte
  vide : ils lisent les fichiers et ne renvoient qu'un rapport court. Brief, rapport et règles :
  `references/subagent.md`. Jamais un `fork` : il hérite de la conversation, ce qu'on veut éviter.
- **Exploration large.** Un agent `Explore`. Il renvoie des notes courtes (chemins, une ligne chacun),
  jamais des contenus de fichiers.
- **Sorties longues.** Redirige-les dans un fichier du scratchpad et lis la fin (`tail`) ou un `grep`.
  Ne lis jamais un fichier généré en entier.
- **Serveurs.** Seule la session principale démarre et arrête les environnements (skill `launch`). Les
  sous-agents les utilisent.
- **`/clear`.** Tout l'état est dans les fichiers : à chaque passage, `/clear` puis la même commande
  reprend sans perte. Conseille-le à l'utilisateur quand `/context` dépasse environ la moitié. Après un
  `/clear`, fais confiance aux fichiers (issue, plans, notes, git), pas au souvenir.

## Fichiers du run

- **Issue** : le comportement (scénarios, How to test, `Out of scope:`, `Design:`).
- **Plans** : `.claude/plans/<n>-<slug>.md` dans le dossier de chaque package, avec l'en-tête du
  workflow (`phase:`, `issue_updated_at:`) et le tableau `## Pull requests` (écrit en phase 2) dont la
  colonne `Avancement` suit chaque PR.
- **Notes du run** : `.claude/plans/<n>.notes.md`, dans le dossier où la phase 1 tourne (depuis la racine
  du repo : `backend/.claude/plans/`). Écrites en phase 1, lues en phase 2. Elles gardent ce qui n'existe
  nulle part ailleurs : les décisions techniques du grill, mot pour mot, et les faits du code utiles aux
  plans (chemins de modules, d'entités et de tests, une ligne chacun). Ni un plan, ni un en-tête.
- **Git** : branches et commits.

Ordre des valeurs de `phase:` : `plan` → `implement` → `verify` → `ship` → `done`.

## Reprise

Au début d'un run :

1. Lis l'issue. Cherche les plans et les notes dans le dossier de travail de chaque package :
   `.claude/plans/<n>-*.md` et `<n>.notes.md` dans le dossier courant (`backend/` ou `frontend/`), et le
   plan de l'autre package dans `../frontend/.claude/plans/` ou `../backend/.claude/plans/`. Depuis la
   racine du repo, regarde dans `backend/` et `frontend/`.
2. Aucun plan : commence à la phase 1 (lis les notes si elles existent). Des plans existent : prends la
   plus petite `phase` des plans, dans l'ordre ci-dessus.
3. Ne fais pas confiance à l'état. Revérifie les conditions de sortie de la phase juste avant (et la date
   de mise à jour de l'issue contre `issue_updated_at` des plans). Si l'une échoue, reviens à cette phase
   et dis pourquoi.
4. En phase 3, la colonne `Avancement` de `## Pull requests` dit où reprendre. Confirme-la avec
   `git log` sur la branche de la PR.
5. Dis à l'utilisateur où le run reprend, puis continue.

## Règles

- Réponds dans la langue de l'utilisateur (français). Voir le tableau « Langues » pour les textes écrits.
- Le produit s'appelle Tennaxia (règle de nommage de `AGENTS.md`).
- Pas de code, pas de branche, avant la phase 3. Avant la phase 3, la seule écriture sur GitHub est
  `gh issue edit --body-file`, après validation du diff par l'utilisateur. Ne touche jamais au titre,
  aux labels, au milestone, aux assignés ni à l'état, à aucune phase.
- Un sous-agent ne pousse jamais, n'écrit jamais sur GitHub et ne pose jamais de question à
  l'utilisateur : il s'arrête et rapporte.
- N'invente jamais une règle métier. Un edge case ou un cas d'erreur est une proposition : c'est
  l'utilisateur qui décide.
- Une question dont le code connaît la réponse ne se pose pas. Explore d'abord, ne demande que des décisions.
- Une seule question à la fois avec `AskUserQuestion`. La réponse recommandée est la première option.
- Les actions vers l'extérieur (push, pull request, modification de l'issue) n'ont lieu qu'après un oui
  donné dans cette phase.
- Réutilise l'existant. Appelle `launch`, `run-qa-scenarios` et `code-review` avec l'outil `Skill`. Les
  skills en slash uniquement (`stack`, `write-implementation-plan`) ne peuvent pas être appelés : lis leur
  `SKILL.md` et suis la sous-commande ou les étapes. Ne recopie pas leurs règles ici.

## Sous-skills

Les phases partagent un même état (issue, plans, notes) et une même règle de passage, et le modèle ne
peut pas appeler un sous-skill en slash uniquement. Les phases restent donc des fichiers de ce skill.
Extrais une phase dans son propre skill quand un deuxième usage en a besoin, pas avant.

Déjà extrait : la méthode de plan, dans `write-implementation-plan` (utilisable seule, hors de ce
workflow). La phase 2 la lit et ajoute l'en-tête, les chemins, le design, le contrat backend et le
découpage en PR. Prochain candidat : la vérification.
