---
name: rebase
description: Rebase la branche courante sur une branche cible (par défaut main). Résout les conflits dans les fichiers générés, applique les migrations, régénère le schéma GraphQL et les types du SDK, vérifie les types, lance les tests liés, puis fait un force-push. À utiliser quand l'utilisateur invoque /rebase, dit "rebase sur main", "rebase on main", "rebase la branche", ou veut remettre une branche de feature à jour (rebase the current branch on a target branch).
disable-model-invocation: true
allowed-tools: Bash(git *), Bash(gh *), Bash(docker compose *), Bash(npm run *), Bash(npx dotenvx run *), Read, Edit, Grep, Glob, AskUserQuestion
---

# Rebase

Lance toutes les commandes depuis `backend/`, sauf si une étape dit autre chose. `TARGET` est l'argument, ou `main`.

Les messages de commit restent en anglais simple.

## 1. Vérifier la branche

```bash
git branch --show-current
git status --short
```

Rebase la branche que l'utilisateur a nommée. Si la branche courante n'est pas celle qu'il attend, arrête-toi et demande.
Ne fais pas de rebase avec des changements non commités sur des fichiers suivis.

## 2. Rebase

```bash
git pull --rebase origin $TARGET
```

Si la commande échoue avec `Permission denied (publickey)`, réessaie plusieurs fois : l'agent SSH peut échouer
au hasard. Ne change pas l'URL du remote.

## 3. Résoudre les conflits

Fichiers générés : prends la version de la branche cible. Pendant un rebase, c'est `--ours`.

Git lit les chemins depuis le dossier courant, donc lance cette étape depuis la racine du dépôt.

```bash
cd "$(git rev-parse --show-toplevel)"
git checkout --ours backend/src/schema.gql backend/sdk/generated/graphql/ frontend/src/gql/ 2>/dev/null || true
git add backend/src/schema.gql backend/sdk/generated/graphql/ frontend/src/gql/ 2>/dev/null || true
```

Code métier : résous à la main, puis `git add`. Ne modifie jamais un fichier généré à la main.

```bash
git rebase --continue
```

Répète jusqu'à la fin du rebase, puis retourne dans `backend/`.

## 4. Choisir les étapes selon le diff

```bash
git diff origin/$TARGET --name-only
```

Si tous les fichiers modifiés sont des docs ou des skills (`.claude/`, `*.md`), va directement à l'étape 10.
Lance les étapes ci-dessous seulement pour ce qui a changé :

- `migrations/` ou une entité a changé : étapes 5 à 6.
- Un resolver, un input ou une entité avec des décorateurs GraphQL a changé : étapes 7 à 8.
- Un fichier `.ts` a changé : étapes 9 à 10.

## 5. Docker (environnement de test)

```bash
docker compose -f docker-compose.yml --env-file .test.env -p backend_test ps
docker compose -f docker-compose.yml --env-file .test.env -p backend_test up -d   # only if stopped
```

## 6. Migrations

```bash
npm run _test mikro:migration:up
npm run _test clickhouse:test-schema:up
```

## 7. Schéma GraphQL

```bash
npm run _dev build:graphql-schema
```

## 8. Types GraphQL

```bash
npm run _test test:graphql-codegen
cd ../frontend && npm run graphql:codegen && cd ../backend
```

## 9. Vérification des types

```bash
npm run type:check
```

Ne lance jamais `tsc` ni `npx tsc`.

## 10. Régressions venant de la branche cible

Liste les commits de la branche cible qui touchent des fichiers de cette branche. `git diff --name-only`
affiche les chemins depuis la racine du dépôt, donc lance cette étape depuis la racine du dépôt.

```bash
cd "$(git rev-parse --show-toplevel)"
BRANCH_FILES=$(mktemp)
git diff origin/$TARGET...HEAD --name-only > "$BRANCH_FILES"
git log --oneline ORIG_HEAD..origin/$TARGET -- $(tr '\n' ' ' < "$BRANCH_FILES")
rm "$BRANCH_FILES"
cd backend
```

Pour chaque commit, lance `git show <sha> -- <file>`. Vérifie que cette branche utilise encore les bonnes API :
une méthode renommée ou supprimée, un nouveau paramètre obligatoire, un import qui n'existe plus.
Corrige ce qui est cassé dans un commit séparé : `chore(<issue>): adapt to <change> from #<PR>`.

## 11. Tests liés

```bash
FILES=$(git diff origin/$TARGET --name-only --relative | tr '\n' ' ')
npx dotenvx run -f .test.env -- npx cross-env TESTING=true vitest related --run --passWithNoTests --config vitest-ut.config.ts $FILES
npx dotenvx run -f .test.env -- npx cross-env TESTING=true vitest related --run --passWithNoTests --config vitest-itg.config.ts $FILES
```

`--relative` donne les chemins depuis `backend/`. `vitest related` remplace l'option Jest `--findRelatedTests`.

Ne démarre jamais le serveur de test et ne lance jamais les tests e2e. Si le schéma a changé, donne à
l'utilisateur la commande e2e à lancer (voir `backend/AGENTS.md`).

## 12. Push

```bash
git push --force-with-lease
```

N'utilise jamais `--force`. Rapporte le résultat et tout ce qui a été sauté.
