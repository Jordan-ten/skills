---
name: bug-fix-workflow
description: >
  Slash uniquement. À utiliser seulement quand l'utilisateur lance explicitement /bug-fix-workflow
  avec l'URL ou le numéro d'une issue GitHub de bug. Mène un bug de l'issue à la pull request en cinq
  phases, chacune avec des conditions de sortie à prouver avant la suivante : reproduire le bug en
  local (serveur dev, ou e2e rouge), écrire le diagnostic et le plan du correctif, implémenter (un
  sous-agent par pull request, test de non-régression rouge avant le correctif), relire avec
  /code-review et vérifier (le bug a disparu, mêmes étapes qu'avant), puis pousser. La session
  principale reste légère : le travail lourd tourne dans des sous-agents. Reprenable : relancer la
  commande sur la même issue continue là où on s'est arrêté. Ne jamais déclencher depuis une demande en
  langage naturel.
disable-model-invocation: true
allowed-tools: Bash(gh issue view *), Bash(gh pr view *), Bash(gh pr list *), Bash(gh stack view *), Bash(gh stack init *), Bash(gh stack add *), Bash(gh stack checkout *), Bash(git status *), Bash(git diff *), Bash(git log *), Bash(git show *), Bash(git rev-parse *), Bash(git add *), Bash(git commit *), Bash(git switch *), Bash(npm run *), Bash(npx vitest *), Bash(tail *), mcp__idea__get_file_problems, mcp__claude_ai_Datadog__search_datadog_logs, mcp__claude_ai_Datadog__analyze_datadog_logs, mcp__claude_ai_Datadog__search_datadog_error_tracking_issues, mcp__chrome-devtools__list_pages, mcp__chrome-devtools__new_page, mcp__chrome-devtools__navigate_page, mcp__chrome-devtools__take_snapshot, mcp__chrome-devtools__take_screenshot, mcp__chrome-devtools__click, mcp__chrome-devtools__fill, mcp__chrome-devtools__fill_form, mcp__chrome-devtools__press_key, mcp__chrome-devtools__wait_for, mcp__chrome-devtools__evaluate_script, mcp__chrome-devtools__list_console_messages, mcp__chrome-devtools__list_network_requests, Read, Write, Edit, Grep, Glob, Agent, SendMessage, AskUserQuestion, Skill
---

# Workflow de correction d'un bug

De l'issue d'un bug aux pull requests. Le workflow est découpé en phases. Une phase se termine
seulement quand ses conditions de sortie sont vraies et prouvées. Ensuite l'utilisateur décide de
continuer.

- **L'issue est la source de vérité** du symptôme : ce qui est observé, ce qui est attendu, comment
  l'atteindre. La phase 1 y ajoute un scénario de non-régression.
- **Un bug n'est corrigé que s'il a été reproduit.** La reproduction est la preuve « avant » ; la phase 4
  rejoue les mêmes étapes pour la preuve « après ».
- **Un plan est la définition du correctif** d'un package : cause, étapes, tests. Il ne recopie jamais le
  comportement. Il renvoie au scénario par son titre.
- **Les fichiers portent l'état**, jamais la conversation (voir « Fichiers du run »).

Entrée : `/bug-fix-workflow <url-ou-numéro-de-l-issue> [--phase <nom>]`. Sans `--phase`, le run reprend
là où le fichier de run l'indique.

`allowed-tools` n'approuve volontairement ni `git push`, ni `gh pr create`, ni `gh issue edit`, ni
`gh stack push|submit` : le harnais demande une confirmation pour chaque action vers l'extérieur.

## Langues

| Texte | Langue |
|---|---|
| Échanges avec l'utilisateur, y compris le grill avant la mise à jour de l'issue | français |
| Plans et notes du run (`.claude/plans/`) | français |
| Mise à jour de l'issue (scénario de non-régression, How to test) | anglais simple |
| Commits et pull requests | anglais simple (`AGENTS.md`) |

Dans un plan, le titre du scénario est cité tel qu'il est dans l'issue (en anglais), et les identifiants
de code restent tels quels.

## Phases

Chaque phase a un fichier dans `references/phases/`. Lis le fichier d'une phase quand tu y entres, pas
avant. Les conditions de sortie sont dans ce fichier, et nulle part ailleurs.

| # | Phase | But | Où elle tourne | Fichier |
|---|---|---|---|---|
| 1 | Reproduire | Le bug est vu en local, avec la preuve « avant », et le scénario de non-régression est dans l'issue. | session principale | `1-reproduce.md` |
| 2 | Diagnostic et plan | La cause est prouvée. Un plan de correctif minimal, sans question ouverte, validé. | session principale | `2-plan.md` |
| 3 | Implémenter | Test de non-régression rouge, puis correctif, tests et commits atomiques, tout vert. | **un sous-agent par PR** | `3-implement.md` |
| 4 | Relire et vérifier | `/code-review high`, puis e2e, puis les étapes de la phase 1 rejouées : le bug a disparu. | relecture : principale ; tests : **un sous-agent** | `4-verify.md` |
| 5 | Livrer | Branches poussées, PR ouvertes, après un oui. | session principale | `5-ship.md` |

**Voie rapide** (phases 2 et 3) : quand le bug s'est reproduit du premier coup, que la cause est évidente et le correctif petit (l'agent
tranche, l'utilisateur peut changer à la validation), le plan est court et la
phase 3 tourne dans la session principale, sans sous-agent. Conditions et effets : « Voie rapide » dans
`2-plan.md`. Les phases 1, 4 et 5 ne changent pas.

Fichiers partagés avec `feature-implementation-workflow` (ne les recopie pas) :
`../feature-implementation-workflow/references/subagent.md` (phases 3 et 4),
`../feature-implementation-workflow/references/scenario-audit.md` (section « Écrire dans l'issue »),
`../write-implementation-plan/references/plan-template.md` (template des plans).

## Passage d'une phase à l'autre

À la fin d'une phase :

1. Affiche les conditions de sortie du fichier de la phase sous forme de liste. Chaque ligne : ✅ ou ❌,
   et la preuve en quelques mots (commande et résultat, ou fichier et section). Une condition sans
   preuve est ❌. Ce qui se vérifie en une commande (`git status --short`, `git log`, `gh issue view`),
   vérifie-le toi-même au lieu de croire un rapport.
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

- **Sous-agents.** La phase 3 et les tests de la phase 4 tournent dans des sous-agents `general-purpose`
  au contexte vide : ils lisent les fichiers et ne renvoient qu'un rapport court. Brief, rapport et
  règles : `../feature-implementation-workflow/references/subagent.md`. Jamais un `fork`.
- **Exploration large.** Un agent `Explore`. Il renvoie des notes courtes (chemins, une ligne chacun),
  jamais des contenus de fichiers.
- **Sorties longues.** Logs du backend (`tnx-dev-check-backend-logs`), réponses d'API, sorties de tests :
  redirige-les dans un fichier du scratchpad et lis la fin (`tail`) ou un `grep`. Ne lis jamais un
  fichier généré en entier.
- **Serveurs.** Seule la session principale démarre et arrête les environnements (skill `launch`). Les
  sous-agents les utilisent.
- **`/clear`.** Tout l'état est dans les fichiers : à chaque passage, `/clear` puis la même commande
  reprend sans perte. Règles : `${CLAUDE_PLUGIN_ROOT}/shared/run-state.md`. Recommande `Clear` après les phases 2 et 3, et quand `/context`
  dépasse environ la moitié.

## Fichiers du run

- **Issue** : le symptôme, et le scénario de non-régression ajouté en phase 1.
- **Notes du run** : `.claude/plans/<n>.notes.md`, dans le dossier du package où le bug se voit (depuis la
  racine du repo : `backend/.claude/plans/` ou `frontend/.claude/plans/`). Écrites en phase 1. Elles
  gardent la reproduction : étapes exactes, données utilisées, observé, attendu, preuve « avant », chemin
  d'un e2e de reproduction non commité. Le diagnostic de la phase 2 y est aussi résumé en une ligne.
- **Fichier de run** : `.claude/plans/<n>.run.md`, à côté des notes. Il dit où reprendre (phase, prochaine
  action). Format, écriture et reprise : `${CLAUDE_PLUGIN_ROOT}/shared/run-state.md`. Créé en phase 1.
- **Plans** : `.claude/plans/<n>-<slug>.md` dans le dossier de chaque package modifié (le plus souvent
  un seul), avec l'en-tête du workflow (`phase:`, `issue_updated_at:`) et le tableau `## Pull requests`
  (voir le template), dont la colonne `Avancement` suit chaque PR.
- **Git** : branches et commits.

Ordre des valeurs de `phase:` : `plan` → `implement` → `verify` → `ship` → `done`.

## Reprise

Règles complètes : `${CLAUDE_PLUGIN_ROOT}/shared/run-state.md` (section « Reprise »). Ordre : fichier de run, puis issue, notes et plans qu'il
pointe, puis revérification des conditions de sortie de la phase d'avant. `--phase <nom>` force la phase.

Propre à ce workflow :

- Sans fichier de run : lis l'issue, cherche les notes et les plans dans `backend/.claude/plans/` et
  `frontend/.claude/plans/` (`<n>.notes.md`, `<n>-*.md`). Aucun plan → phase 1 ; sinon la plus petite
  `phase:` des plans.
- L'e2e de reproduction non commité doit exister au chemin des notes. Sinon, réécris-le d'après les étapes
  des notes avant la phase 3.
- En phase 3, la colonne `Avancement` de `## Pull requests` dit où reprendre. Confirme-la avec `git log`
  sur la branche de la PR.

## Règles

- Réponds dans la langue de l'utilisateur (français). Voir le tableau « Langues » pour les textes écrits.
- Le produit s'appelle Tennaxia (règle de nommage de `AGENTS.md`).
- **Le symptôme exact.** Un bug est reproduit seulement quand le symptôme de l'issue est observé, pas
  « une erreur ». Jamais « reproduit » sans l'avoir vu.
- **Pas de correctif avant la phase 3.** Avant la phase 3, le seul code écrit est un e2e de reproduction
  non commité. La seule écriture sur GitHub est `gh issue edit --body-file`, après validation du diff par
  l'utilisateur. Ne touche jamais au titre, aux labels, au milestone, aux assignés ni à l'état.
- **Correctif minimal.** Il corrige la cause prouvée, rien d'autre. Un refacto ou un autre défaut vu en
  chemin va dans `## Hors périmètre` du plan, jamais dans le correctif.
- **Un test rouge d'abord.** Le test de non-régression échoue avant le correctif, pour la bonne raison.
- Un sous-agent ne pousse jamais, n'écrit jamais sur GitHub et ne pose jamais de question à
  l'utilisateur : il s'arrête et rapporte.
- N'invente jamais une règle métier. Quand le comportement attendu n'est pas dit par l'issue, le code ou la
  documentation produit, c'est l'utilisateur qui décide.
- Une question dont le code connaît la réponse ne se pose pas. Explore d'abord, ne demande que des décisions.
- Une seule question à la fois avec `AskUserQuestion`. La réponse recommandée est la première option.
- Les actions vers l'extérieur (push, pull request, modification de l'issue) n'ont lieu qu'après un oui
  donné dans cette phase.
- Réutilise l'existant. Appelle `launch`, `create-local-data`, `run-qa-scenarios`, `code-review`,
  `tnx-dev-mcp-local-dev` et `hotfix` avec l'outil `Skill`. Les skills en slash uniquement (`stack`,
  `write-implementation-plan`) ne peuvent pas être appelés : lis leur `SKILL.md` et suis la sous-commande
  ou les étapes. Ne recopie pas leurs règles ici.
