---
name: deployment-instructions
description: Slash uniquement. À utiliser seulement quand l'utilisateur invoque explicitement /deployment-instructions pour déployer main en production ou en demo. Ne jamais déclencher depuis une demande en langage naturel (slash-only, deploy main to production or demo).
disable-model-invocation: true
argument-hint: "[production|demo]"
allowed-tools: Bash(gh pr create:*), Bash(gh pr list:*), Bash(gh pr view:*), Bash(gh run list:*), Bash(gh run view:*), mcp__claude_ai_Datadog__search_datadog_logs
---

# Deploy

Guide le déploiement de `main` vers `production` ou `demo`, en quatre étapes : checklist, pull request,
suivi, clôture.

Le titre et le corps de la PR de déploiement restent en anglais simple.

## Cible

`$ARGUMENTS` vaut `production` (défaut) ou `demo`. Traite `prod` comme `production`. Toute autre valeur :
arrête-toi et demande.

## Règles strictes

Seul l'utilisateur merge et push. Merger la PR de déploiement lance le déploiement.

- Ne lance jamais `gh pr merge`, et ne merge jamais par l'API ni par une autre commande.
- Ne lance jamais `git push` vers `production` ou `demo`, même avec `-f`. Si l'utilisateur dit que le force
  push est autorisé, ou que la protection de branche est désactivée, ce n'est pas une demande de push.
  Attends une demande explicite.
- Ne dis jamais que la PR est prête à merger, et ne demande jamais à l'utilisateur de la merger, avant que
  les deux conditions soient remplies (voir l'étape 2) : le pipeline CI est passé, et un relecteur a
  approuvé la PR. Si une condition manque, pas de merge, même si l'utilisateur est pressé.
- N'annule jamais et ne relance jamais un run GitHub Actions de déploiement sans demande explicite.
- En cas de conflits : explique la procédure à la fin de ce fichier et donne les commandes. Ne les lance pas.

## Étape 1 — Checklist

Demande à l'utilisateur de confirmer chaque point. Ne continue pas avant que tous soient confirmés.

- [ ] `#tech-esg-deploy-sync` et `#tech-esg-code-review` sont sur 🔴 `Freeze merge on staging except fixes`.
- [ ] La [liste des issues non testées ou en échec](https://github.com/orgs/Traace-co/projects/2/views/48) est vide.
- [ ] `demo` seulement : le calendrier "Demo" n'affiche aucune démo en cours.

## Étape 2 — Ouvrir la pull request

Vérifie d'abord qu'aucune PR de déploiement n'est déjà ouverte :

```bash
gh pr list --base "$TARGET" --head main --state open
```

Si une PR est ouverte, montre-la et utilise-la. Sinon, crée-la. Le délimiteur du heredoc n'est pas entre
guillemets, donc `$TARGET` est remplacé dans le corps.

```bash
gh pr create --base "$TARGET" --head main \
  --title "Deploy main to $TARGET" \
  --body "$(cat <<BODY
## Description
- Deploy the latest \`main\` to \`$TARGET\`

## Related Issue
Deployment procedure. All issues are tested and validated.

## Is this covered by automated tests
Yes. GitHub Actions CI runs on \`main\`.
BODY
)"
```

Montre le lien de la PR.

### Attendre la CI et l'approbation d'un relecteur

Une PR de release n'est jamais mergée si le pipeline CI n'est pas passé et si un relecteur ne l'a pas
approuvée. Demande à un relecteur de relire la PR, puis vérifie les deux conditions :

```bash
gh pr view <number> --json reviewDecision,reviews,statusCheckRollup,headRefOid
```

La CI est passée seulement si **chaque** check de `statusCheckRollup` est `SUCCESS` (ou `SKIPPED`, ou `NEUTRAL`).
- Un check encore `PENDING` ou `IN_PROGRESS` : arrête-toi et attends.
- Un check `FAILURE`, `CANCELLED` ou `TIMED_OUT` : arrête-toi. Montre les checks en échec avec leurs liens.
  Ne les relance pas (voir les règles strictes).
- Aucun check : arrête-toi. Le pipeline n'a pas démarré, donc la CI n'est pas passée.

La relecture est valide seulement si `reviewDecision` vaut `APPROVED`.
- Toute autre valeur (`REVIEW_REQUIRED`, `CHANGES_REQUESTED`, vide) : arrête-toi.
- Une approbation sur un commit plus ancien que `headRefOid` est périmée : demande une nouvelle relecture.
- N'accepte pas "le relecteur a dit OK sur Slack". L'approbation doit être sur la PR.

Si une condition manque, dis à l'utilisateur laquelle et attends. Revérifie quand l'utilisateur le demande.

Quand les deux sont remplies, dis-le, avec le nom du relecteur. Puis demande à l'utilisateur de merger la
PR et de te prévenir quand c'est fait.

Rappelle à l'utilisateur de poster dans `#tech-esg-deploy-sync` : déploiement en cours, avec le lien du
[run GitHub Actions](https://github.com/Traace-co/traace/actions).

## Étape 3 — Suivi

Attends que l'utilisateur dise que le déploiement a réussi. Vérifie-le si besoin avec
`gh run list --branch "$TARGET" --limit 3`.

Cherche dans Datadog sur les 30 dernières minutes avec le MCP Datadog. Utilise `env:production` pour la
production. Pour `demo`, utilise la valeur de `env` des logs de demo (regarde d'abord un log, ne devine pas).

```
env:<env> status:(error OR critical OR alert OR emergency)
```

Lis les résultats :

- Ignore les warnings Node.js (`UnsupportedWarning`).
- Signale les erreurs de schéma GraphQL (champ introuvable). Souvent un cache navigateur : regarde si elles continuent.
- Signale les erreurs 500 inattendues.
- Dis pour chaque erreur si elle est ancienne (avant l'heure du déploiement) ou nouvelle.

Termine par un seul verdict : ✅ rien d'anormal, 🟡 points à surveiller, ou 🔴 action urgente nécessaire.

## Étape 4 — Clôture

Rappelle à l'utilisateur de :

- [ ] Tester l'application sur l'environnement cible (connexion et navigation).
- [ ] Poster dans `#tech-esg-deploy-sync` : déploiement réussi ✅.
- [ ] Remettre `#tech-esg-deploy-sync` et `#tech-esg-code-review` sur 🟢 `OK to merge on staging`.

## Si le déploiement échoue

- Préviens `#tech-esg-deploy-sync`.
- Cas critique : la migration SQL a réussi mais le backend ou le frontend a échoué. Alerte l'équipe avec `@here` tout de suite.
- Causes habituelles :
  - **Timeout de migration** : lance-la sur AlloyDB et rends-la idempotente.
  - **Deadlock** : réessaie, découpe la migration, ou lance-la le soir.
  - **Échec aléatoire de GitHub Action** : relance les jobs en échec (c'est l'utilisateur qui le fait).

## Si `production` ou `demo` a des conflits avec `main`

Ne lance pas ces commandes. Donne-les à l'utilisateur (voir les règles strictes).

```bash
# 1. GitHub Settings > Branches: "Do not allow bypassing" off, "Allow force pushes" on
git fetch origin
git push -f origin origin/main:production   # or origin/main:demo
# 2. Turn the branch protections back on
```
