---
name: hotfix
description: >
  Crée des PRs de hotfix ciblant demo et/ou production, et/ou une PR de revert ciblant main,
  à partir d'une branche existante ou d'un SHA de commit. Déduit le numéro d'issue et la PR principale
  depuis le nom de la branche. Utilise le format minimal de PR défini dans pr-template.md.
  À invoquer quand l'utilisateur tape /hotfix, /revert, dit "crée un hotfix", "hotfix sur demo/prod",
  "crée la PR de revert", ou veut backporter ou revert une feature
  (create hotfix PRs, create a revert PR, backport or revert a feature).
allowed-tools: Bash
---

# Hotfix / Revert — créer des PRs de backport ou de revert

Crée des PRs de hotfix (ciblant `demo` et/ou `production`) et/ou une PR de revert (ciblant `main`).

Les titres et les corps de PR, les messages de commit et les noms de branche restent en anglais simple.

## Arguments

`$ARGUMENTS` — une combinaison de :
- Branche source (ex: `bugfix/22094/fix-email-validation`) — défaut : branche courante
- Commit SHA (ex: `286afaf58d`) — utilise ce commit comme source
- Cible : `demo`, `prod` / `production`, `revert`, `both` — défaut : demander à l'utilisateur

Exemples :
```
/hotfix                                              # branche courante → demander cible
/hotfix demo                                         # branche courante → demo seulement
/hotfix prod revert                                  # branche courante → production + revert
/hotfix bugfix/22094/fix-email-validation both       # branche explicite → demo + production
/hotfix 286afaf58d prod                              # commit SHA → production seulement
/hotfix revert                                       # branche courante → revert seulement
```

---

## Étape 1 — Résoudre la source

Si `$ARGUMENTS` contient un SHA de commit (format hexadécimal 7-40 chars) :
- Extraire le SHA
- Récupérer la branche d'origine via `git branch --contains <SHA> --remote`
- Si aucune branche ne contient ce commit → signaler l'erreur

Si `$ARGUMENTS` contient un nom de branche explicite → l'utiliser.

Sinon → utiliser la branche courante :
```bash
git branch --show-current
```

---

## Étape 2 — Détecter les cibles

Si `$ARGUMENTS` contient une ou plusieurs de : `demo`, `prod`/`production`, `revert`, `both` → utiliser ces valeurs (`both` = demo + production).

Sinon → demander avec `AskUserQuestion` (multiSelect) :
```
Que souhaitez-vous créer ?
- Hotfix → demo
- Hotfix → production
- Revert → main
```

---

## Étape 3 — Détecter le contexte (issue + PR principale)

Depuis le nom de branche (ex: `bugfix/22094/fix-email-validation`) :

```bash
BRANCH=<branche source>
ISSUE_NUMBER=$(echo "$BRANCH" | grep -oP '\d+' | head -1)
```

Trouver la PR principale ciblant `main` depuis cette branche :
```bash
gh pr list --repo Traace-co/traace \
  --head "$BRANCH" \
  --base main \
  --json number,title \
  --jq '.[0] | "\(.number) \(.title)"'
```

Si aucune PR trouvée → demander à l'utilisateur le numéro et le titre de la PR principale.

---

## Étape 4a — Créer les PRs hotfix (demo et/ou production)

Vérifier d'abord que la branche source existe sur le remote :
```bash
git ls-remote --heads origin <branche source>
```
Si elle n'existe pas → signaler l'erreur.

Vérifier qu'une PR n'existe pas déjà sur la même cible :
```bash
gh pr list --repo Traace-co/traace --head <branche> --base <cible> --json number
```
Si une PR existe déjà → afficher son URL, ne pas en créer une nouvelle.

Pour chaque nouvelle cible (`demo` et/ou `production`) :

**Résolution des conflits de cherry-pick :**
La branche cible (demo/production) peut avoir un schéma GraphQL différent de main.
Les fichiers générés conflictuels (`schema.gql`, `sdk/generated/graphql/graphql.ts`, `src/gql/graphql.ts`, `src/gql/gql.ts`) doivent être résolus avec `--theirs` (version cherry-pick) :

```bash
# Créer la branche hotfix depuis la cible
git checkout -b hotfix/$ISSUE_NUMBER/<slug> origin/<cible>

# Cherry-pick — peut avoir des conflits sur les fichiers générés
git cherry-pick <commit(s) de la branche source>

# Si conflit sur les fichiers générés uniquement → prendre --theirs et continuer
git checkout --theirs \
  backend/src/schema.gql \
  backend/sdk/generated/graphql/graphql.ts \
  frontend/src/gql/graphql.ts \
  frontend/src/gql/gql.ts 2>/dev/null || true
git add backend/src/schema.gql backend/sdk/generated/graphql/graphql.ts \
  frontend/src/gql/graphql.ts frontend/src/gql/gql.ts 2>/dev/null || true
git cherry-pick --continue --no-edit

# Push
git push origin hotfix/$ISSUE_NUMBER/<slug>
```

```bash
gh pr create \
  --repo Traace-co/traace \
  --base <cible> \
  --head hotfix/$ISSUE_NUMBER/<slug> \
  --title "hotfix($ISSUE_NUMBER): <titre de la PR principale>" \
  --body "$(cat <<'EOF'
- #<ISSUE_NUMBER>
- hotfix of #<MAIN_PR_NUMBER>
EOF
)"
```

> Si la branche source cible directement `production` (branche nommée `hotfix/...`), l'utiliser directement sans créer de nouvelle branche.

---

## Étape 4b — Créer la PR revert (ciblant main)

La PR de revert prépare la suppression de la feature une fois qu'elle n'est plus utile.
Elle cible `main` et doit être mergée après la feature, quand on veut retirer le code.

```bash
# Obtenir le ou les commits de la feature sur la branche source
FEATURE_COMMITS=$(git log origin/main..origin/<branche source> --oneline --reverse | awk '{print $1}')

# Créer la branche revert depuis main
git checkout -b revert/$ISSUE_NUMBER/<slug> origin/main

# Cherry-pick les commits de la feature (peut ne pas avoir de conflits si depuis main)
git cherry-pick $FEATURE_COMMITS

# Revert le cherry-pick
git revert HEAD --no-edit   # si un seul commit
# ou : git revert HEAD~N..HEAD --no-edit   # si plusieurs commits

# Push
git push origin revert/$ISSUE_NUMBER/<slug>
```

```bash
gh pr create \
  --repo Traace-co/traace \
  --base main \
  --head revert/$ISSUE_NUMBER/<slug> \
  --title "revert($ISSUE_NUMBER): <titre de la PR principale>" \
  --body "$(cat <<'EOF'
- #<ISSUE_NUMBER>
- revert of #<MAIN_PR_NUMBER>
EOF
)"
```

> Ne pas merger cette PR immédiatement — elle est préparée à l'avance pour faciliter le revert quand le moment vient.

---

## Étape 5 — Résumé

Afficher les URLs de toutes les PRs créées ou déjà existantes :

```
PRs créées :
- hotfix → demo       : https://github.com/Traace-co/traace/pull/XXXXX
- hotfix → production : https://github.com/Traace-co/traace/pull/XXXXX
- revert → main       : https://github.com/Traace-co/traace/pull/XXXXX
```

---

## Règles

- Ne pas récupérer les labels de la PR principale — les omettre
- Si la branche source n'existe pas sur le remote → signaler l'erreur avant toute création
- Si une PR existe déjà sur la même cible → afficher son URL, ne pas en créer une nouvelle
- Fichiers générés en conflit → toujours `--theirs` (version cherry-pick) — ces fichiers se régénèrent au démarrage du serveur
- Ne jamais merger la PR de revert automatiquement — c'est une PR de préparation
