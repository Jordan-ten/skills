---
name: feature-implementation-workflow
description: >
  Slash uniquement. À utiliser seulement quand l'utilisateur lance explicitement
  /feature-implementation-workflow avec l'URL ou le numéro d'une issue GitHub de feature. Mène une
  feature d'une issue déjà raffinée (scénarios prêts) à la pull request en quatre phases, chacune avec des
  conditions de sortie à prouver avant la suivante : écrire un plan par package et le découpage en pull
  requests, implémenter (un sous-agent par pull request), relire avec /code-review et lancer les e2e,
  puis pousser. La QA dans l'UI se lance à part (qa-workflow). La session principale reste légère : le travail
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
  Elle arrive déjà raffinée (par `issue-workflow`). Ce workflow ne la modifie jamais.
- **Un plan est la définition de l'implémentation** d'un package (backend, frontend) : approche,
  étapes, tests. Il ne recopie jamais le comportement. Il renvoie aux scénarios par leur titre.
- **Les fichiers portent l'état**, jamais la conversation (voir « Fichiers du run »).

Entrée : `/feature-implementation-workflow <url-ou-numéro-de-l-issue> [--phase <nom>]`. Sans `--phase`, le
run reprend là où le fichier de run l'indique.

`allowed-tools` n'approuve volontairement ni `git push`, ni `gh pr create`, ni `gh stack push|submit` :
le harnais demande une confirmation pour chaque action vers l'extérieur.

## Langues

| Texte | Langue |
|---|---|
| Échanges avec l'utilisateur | français |
| Plans du run (`.claude/plans/`) | français |
| Commits et pull requests | anglais simple (`AGENTS.md`) |

Dans un plan, les titres de scénarios sont cités tels qu'ils sont dans l'issue (en anglais), et les
identifiants de code restent tels quels.

## Phases

Chaque phase a un fichier dans `references/phases/`. Lis le fichier d'une phase quand tu y entres, pas
avant. Les conditions de sortie sont dans ce fichier, et nulle part ailleurs.

| # | Phase | But | Où elle tourne | Fichier |
|---|---|---|---|---|
| 1 | Plans et découpage | Un plan par package touché, sans question ouverte, avec le découpage en pull requests, validés ensemble. | session principale | `1-plan.md` |
| 2 | Implémenter | Code, tests et commits atomiques de chaque PR, tout vert. | **un sous-agent par PR** (session principale en voie rapide) | `2-implement.md` |
| 3 | Relire et vérifier | `/code-review medium` (un tour), puis les e2e. | relecture : principale ; corrections et e2e : **un seul sous-agent** | `3-verify.md` |
| 4 | Livrer | Branches poussées, PR ouvertes, après un oui. | session principale | `4-ship.md` |

Fichiers de référence : `references/scenario-audit.md` (phase 1, section « Lire l'issue »),
`references/subagent.md` (phases 2 et 3), `../write-implementation-plan/references/plan-template.md` (template unique des plans).

## Passage d'une phase à l'autre

À la fin d'une phase :

1. Vérifie chaque condition de sortie du fichier de la phase. Une condition sans preuve est ❌. Ce qui se
   vérifie en une commande (`git status --short`, `git log`, `gh issue view`), vérifie-le toi-même au lieu
   de croire un rapport.
   Affichage court : **une ligne** `✅ <n>/<n> conditions` avec les preuves clés en une phrase. Détaille
   ligne par ligne (✅ ou ❌, preuve en quelques mots) seulement pour les ❌, ou si l'utilisateur le
   demande. Exception : les listes que la phase exige d'afficher (e2e impactés, nombre de fichiers, etc.).
2. Tout est ✅ : sauvegarde d'abord l'état (`phase:` dans les plans, issue déjà écrite, fichier de run).
   Puis pose une seule `AskUserQuestion` avec les options de « Passage de phase et `/clear` » de
   `${CLAUDE_PLUGIN_ROOT}/shared/run-state.md`.
3. Un ❌ : corrige-le, ou reviens à la phase qui possède la cause. Ne propose jamais de continuer avec
   un ❌.

Ne saute jamais une phase et ne commence jamais la suivante avant le passage. L'utilisateur peut
s'arrêter à n'importe quel passage.

## Contexte : une session principale légère

La session principale parle à l'utilisateur, décide, vérifie et délègue. Elle ne garde pas de diffs, de
logs ni de sorties de tests.

- **Sous-agents.** Les phases 2 et 3 (e2e) tournent dans des sous-agents `general-purpose` au contexte
  vide : ils lisent les fichiers et ne renvoient qu'un rapport court. Brief, rapport et règles :
  `references/subagent.md`. Jamais un `fork` : il hérite de la conversation, ce qu'on veut éviter.
- **Exploration large.** Un agent `Explore`. Il renvoie des notes courtes (chemins, une ligne chacun),
  jamais des contenus de fichiers.
- **Sorties longues.** Redirige-les dans un fichier du scratchpad et lis la fin (`tail`) ou un `grep`.
  Ne lis jamais un fichier généré en entier.
- **Serveurs.** Seule la session principale démarre et arrête les environnements (skill `launch`). Les
  sous-agents les utilisent.
- **`/clear`.** Tout l'état est dans les fichiers : à chaque passage, `/clear` puis la même commande
  reprend sans perte. Règles : `${CLAUDE_PLUGIN_ROOT}/shared/run-state.md`. Recommande `Clear` à chaque passage de phase.

## Fichiers du run

- **Issue** : le comportement (scénarios, How to test, `Out of scope:`, `Design:`).
- **Fichier de run** : `.claude/plans/<n>.run.md`, dans le dossier du premier package. Il dit où reprendre (phase, prochaine
  action). Format, écriture et reprise : `${CLAUDE_PLUGIN_ROOT}/shared/run-state.md`. Créé en phase 1.
- **Plans** : `.claude/plans/<n>-<slug>.md` dans le dossier de chaque package, avec l'en-tête du
  workflow (`phase:`, `issue_updated_at:`) et le tableau `## Pull requests` (écrit en phase 1) dont la
  colonne `Avancement` suit chaque PR.
- **Git** : branches et commits.

Ordre des valeurs de `phase:` : `plan` → `implement` → `verify` → `ship` → `done`.

## Reprise

Règles complètes : `${CLAUDE_PLUGIN_ROOT}/shared/run-state.md` (section « Reprise »). Ordre : fichier de run, puis issue et plans qu'il pointe,
puis revérification des conditions de sortie de la phase d'avant. `--phase <nom>` force la phase.

Propre à ce workflow :

- Sans fichier de run : aucun plan → phase 1 ; sinon la plus petite
  `phase:` des plans, dans l'ordre ci-dessus.
- Les plans sont dans le dossier de chaque package : `.claude/plans/<n>-*.md` dans le dossier courant
  (`backend/` ou `frontend/`), et le plan de l'autre package dans `../frontend/.claude/plans/` ou
  `../backend/.claude/plans/`. Depuis la racine du repo, regarde dans `backend/` et `frontend/`.
- En phase 2, la colonne `Avancement` de `## Pull requests` dit où reprendre. Confirme-la avec `git log`
  sur la branche de la PR.

## Règles

- Réponds dans la langue de l'utilisateur (français). Voir le tableau « Langues » pour les textes écrits.
- Le produit s'appelle Tennaxia (règle de nommage de `AGENTS.md`).
- Pas de code, pas de branche, avant la phase 2. N'écris jamais sur l'issue : ni body, ni titre, ni labels,
  ni milestone, ni assignés, ni état. Un scénario à corriger se corrige hors de ce workflow.
- Un sous-agent ne pousse jamais, n'écrit jamais sur GitHub et ne pose jamais de question à
  l'utilisateur : il s'arrête et rapporte.
- N'invente jamais une règle métier. Un edge case ou un cas d'erreur est une proposition : c'est
  l'utilisateur qui décide.
- Une question dont le code connaît la réponse ne se pose pas. Explore d'abord, ne demande que des décisions.
- Une seule question à la fois avec `AskUserQuestion`. La réponse recommandée est la première option.
- Les actions vers l'extérieur (push, pull request) n'ont lieu qu'après un oui
  donné dans cette phase.
- Réutilise l'existant. Appelle `launch` et `code-review` avec l'outil `Skill`. Les
  skills en slash uniquement (`stack`, `write-implementation-plan`) ne peuvent pas être appelés : lis leur
  `SKILL.md` et suis la sous-commande ou les étapes. Ne recopie pas leurs règles ici.

## Sous-skills

Les phases partagent un même état (issue, plans) et une même règle de passage, et le modèle ne
peut pas appeler un sous-skill en slash uniquement. Les phases restent donc des fichiers de ce skill.
Extrais une phase dans son propre skill quand un deuxième usage en a besoin, pas avant.

Déjà extrait : la méthode de plan, dans `write-implementation-plan` (utilisable seule, hors de ce
workflow). La phase 1 la lit et ajoute l'en-tête, les chemins, le design, le contrat backend et le
découpage en PR. Prochain candidat : la vérification.
