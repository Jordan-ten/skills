---
name: review-workflow
description: Depuis le workspace Orca "Review", ouvre la review d'une pull request dans un workspace enfant. Prend un numéro ou une URL de PR, crée un workspace Orca enfant sur le code de la PR, y dépose les consignes de review, puis lance le triage de la PR dans un agent Claude. À utiliser quand l'utilisateur donne seulement un numéro ou un lien de PR dans le workspace Review, ou dit "review la PR 123", "lance la review de cette PR" (open a PR review in a child Orca workspace).
allowed-tools: Bash(gh *), Bash(git *), Bash(orca-ide *), Bash(orca *), Bash(/home/jcontent/.config/orca/linux-orca-cli-shim/orca *), Read, Write
---

# Lancer la review d'une PR

Entrée : un numéro (`25123`, `#25123`) ou une URL de PR GitHub. Rien d'autre à demander.

## 1. Vérifier le contexte

Choisis la CLI Orca une fois : `$ORCA_CLI_COMMAND` si elle est définie, sinon `orca-ide`. Jamais `orca` nu sur Linux : c'est le lecteur d'écran GNOME. Dans la suite, `ORCA` est cette commande.

```bash
ORCA worktree current --json
```

Le `displayName` doit être `Review`. Sinon, arrête-toi : ce skill ne se lance que depuis le workspace parent Review.

## 2. Lire la PR

```bash
gh pr view <PR> --json number,title,url,state,headRefName,headRefOid
```

Garde `number`, `title`, `url`, `headRefOid`. Une PR `MERGED` ou `CLOSED` : dis-le et demande si on continue.

## 3. Éviter le doublon

```bash
ORCA worktree list --json
```

Un workspace enfant `review-<number>` existe déjà : n'en crée pas un second. Donne son id et demande s'il faut relancer la review dedans.

## 4. Créer le workspace enfant

Sans agent et sans setup. Le `setup` du dépôt lance `pnpm install` : inutile pour lire du code.

```bash
ORCA worktree create --name review-<number> --parent-worktree active --pr <number> --setup skip --json
```

Garde `result.worktree.id` et `result.worktree.path`.

## 5. Mettre le code de la PR sur disque

L'agent doit lire les fichiers de la PR, pas ceux de `main`.

```bash
git -C <path> fetch origin pull/<number>/head
git -C <path> checkout --detach <headRefOid>
```

Si `FETCH_HEAD` ne correspond pas à `headRefOid`, la PR a reçu un push entre-temps : utilise `FETCH_HEAD` et dis-le.

## 6. Déposer les consignes

Copie `review-guidelines.md` (à côté de ce fichier) vers `<path>/CLAUDE.local.md`. Ce fichier est ignoré par git et Claude Code le lit au démarrage.

## 7. Nommer et lancer

```bash
ORCA worktree set --worktree id:<id> --display-name "PR #<number> — <title>" --comment "review en cours" --workspace-status in-review --json
ORCA agent launch --agent claude --worktree id:<id> --prompt "/jcontent-traace:review <number>" --json
```

Le prompt doit commencer par la commande : le skill de triage ne se lance que par une commande slash.

## 8. Répondre

Donne seulement : l'id du workspace enfant et le titre de la PR. N'attends pas la fin de la review.
