---
name: qa-workflow
description: Depuis le workspace Orca "QA", ouvre la QA d'une issue ou d'une pull request dans un workspace enfant. Prend un numéro ou une URL d'issue ou de PR, retrouve l'issue et la PR liées, crée un workspace Orca enfant sur le code de la PR, y dépose les consignes de QA, puis lance run-qa-scenarios dans un agent Claude. À utiliser quand l'utilisateur donne seulement un numéro ou un lien d'issue ou de PR dans le workspace QA, ou dit "QA de la PR 123", "teste le ticket 456 dans un workspace" (open a QA run in a child Orca workspace).
allowed-tools: Bash(gh *), Bash(git *), Bash(orca-ide *), Bash(orca *), Bash(/home/jcontent/.config/orca/linux-orca-cli-shim/orca *), Read, Write, AskUserQuestion
---

# Lancer la QA d'une issue ou d'une PR

Entrée : un numéro (`25123`, `#25123`) ou une URL GitHub d'issue ou de PR. Rien d'autre à demander,
sauf aux étapes 2 et 3 si le résultat est ambigu.

Le test lui-même est fait par `run-qa-scenarios`, dans le workspace enfant. Ce skill prépare seulement le
workspace.

## 1. Vérifier le contexte

Choisis la CLI Orca une fois : `$ORCA_CLI_COMMAND` si elle est définie, sinon `orca-ide`. Jamais `orca` nu
sur Linux : c'est le lecteur d'écran GNOME. Dans la suite, `ORCA` est cette commande.

```bash
ORCA worktree current --json
```

Le `displayName` doit être `QA`. Sinon, arrête-toi : ce skill ne se lance que depuis le workspace parent QA.

## 2. Retrouver l'issue et la PR

Une URL dit si c'est une issue (`/issues/`) ou une PR (`/pull/`). Un numéro seul : essaie
`gh pr view <n>`, puis `gh issue view <n>` (un numéro GitHub est une PR ou une issue, jamais les deux).

**Entrée = PR :**

```bash
gh pr view <PR> --repo Traace-co/traace --json number,title,url,state,headRefName,headRefOid,closingIssuesReferences
```

L'issue est dans `closingIssuesReferences`. Vide : cherche son numéro dans `headRefName`
(`feature/<issue>/...`). Toujours vide : arrête-toi et demande l'issue. Les scénarios viennent de l'issue.

**Entrée = issue :**

```bash
gh issue view <n> --repo Traace-co/traace --json number,title,url,state
gh pr list --repo Traace-co/traace --search "<n>" --state all --json number,title,url,state,headRefName,headRefOid,closingIssuesReferences
```

Garde les PR dont `closingIssuesReferences` contient l'issue, ou dont `headRefName` contient `/<n>/`.

- Aucune PR : arrête-toi. Il n'y a encore rien à tester. Dis-le.
- Une seule PR : prends-la.
- Plusieurs (une pile de PR) : une `AskUserQuestion` avec une option par PR (numéro, titre, état). Le code
  d'une PR plus haute dans la pile contient celui des PR du dessous.

Garde `issue.number`, `issue.title`, `pr.number`, `pr.url`, `pr.state`, `pr.headRefOid`.

Une PR `CLOSED` non fusionnée : dis-le et demande si on continue.

## 3. Éviter le doublon

```bash
ORCA worktree list --json
```

Un workspace enfant `qa-<issue>` existe déjà : n'en crée pas un second. Donne son id et demande s'il faut
relancer la QA dedans.

## 4. Créer le workspace enfant

Avec le setup du dépôt : la QA a besoin d'une app qui tourne (dépendances, fichiers d'environnement).

```bash
ORCA worktree create --name qa-<issue> --parent-worktree active --issue <issue> --pr <pr> --setup run --json
```

Garde `result.worktree.id` et `result.worktree.path`.

## 5. Mettre le code de la PR sur disque

La QA teste le code de la PR, pas celui de `main`.

```bash
git -C <path> fetch origin pull/<pr>/head
git -C <path> checkout --detach <headRefOid>
```

Si `FETCH_HEAD` ne correspond pas à `headRefOid`, la PR a reçu un push entre-temps : utilise `FETCH_HEAD` et
dis-le. Une PR `MERGED` : le code est déjà dans `main` : `git -C <path> checkout --detach origin/main` après
un `fetch origin main`, et dis-le.

## 6. Déposer les consignes et l'email de dev

Copie `qa-guidelines.md` (à côté de ce fichier) vers `<path>/CLAUDE.local.md`. Ce fichier est ignoré par git
et Claude Code le lit au démarrage.

Si le workspace parent a un `frontend/.claude/mcp.dev_user_email`, copie-le au même endroit dans
`<path>`. Ce fichier est ignoré par git, donc un workspace neuf ne l'a pas. Le parent n'en a pas : dis-le
dans la réponse, `run-qa-scenarios` le demandera.

## 7. Nommer et lancer

```bash
ORCA worktree set --worktree id:<id> --display-name "QA #<issue> — <title>" --comment "QA en cours (PR #<pr>)" --workspace-status in-review --json
ORCA agent launch --agent claude --worktree id:<id> --prompt "/jcontent-traace:run-qa-scenarios <issue>" --json
```

Le prompt doit commencer par la commande : le skill ne se lance que par une commande slash. Le serveur MCP
Chrome est déclaré au niveau utilisateur : il n'y a pas de dossier de lancement à choisir.

## 8. Répondre

Donne seulement : l'id du workspace enfant, le titre de l'issue et le numéro de la PR testée. N'attends pas
la fin de la QA.

Si un autre workspace `qa-*` est encore ouvert, ajoute une ligne : les apps dev partagent les mêmes ports
et la même base, donc deux QA en parallèle se gênent.
