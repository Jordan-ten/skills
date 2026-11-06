---
name: triage-code-review-pull-request
description: Fait le triage de la pull request d'un collègue. Lance /code-review (high par défaut), les checklists de coding-style, la vérification du ticket et le statut de la CI, puis écrit un rapport markdown qui sépare ce que l'agent a vérifié de ce qu'un humain doit encore contrôler. À utiliser quand l'utilisateur lance /triage-code-review-pull-request ou dit "triage cette PR", "prépare ma review de la PR #N", "qu'est-ce que je dois vérifier à la main sur cette PR". Pour cartographier une grosse PR par sous-fonctionnalité, utiliser tnx-review-plan-pr-review à la place. (Triage a colleague's pull request, with a report split between agent-verified items and human checks.)
disable-model-invocation: true
context: fork
allowed-tools: Bash(git *), Bash(gh *), Read, Grep, Glob, Write, Skill
---

# Triage de PR

But : le relecteur humain ne lit que ce qu'un agent ne peut pas juger. L'agent vérifie le reste et montre sa preuve.

Entrée : un numéro ou une URL de PR (obligatoire). Niveau optionnel `low|medium|high|xhigh` pour `/code-review`. Défaut : `high`. N'utiliser `max` que si l'utilisateur le demande.

## Étape 1 — Collecter

- `gh pr view <n> --json title,body,headRefName,baseRefName,files,closingIssuesReferences`
- `gh pr diff <n> --name-only`, puis la stat. Ne jamais charger le diff complet d'un coup. Lire fichier par fichier, seulement ce dont un contrôle a besoin.
- `gh pr checks <n>` : statut de la CI, y compris OpenGrep et les vérifications de types.
- Issue liée : `gh issue view <number>`. Pas d'issue liée → le dire dans le rapport.
- Ignorer les fichiers générés (`schema.gql`, `generated/`, `gql/`, `package-lock.json`) : les nommer, ne pas les lire.

## Étape 2 — Contrôles de l'agent

Lancer tous ceux-ci. Chacun produit des findings **et** une ligne de preuve pour le bloc "vérifié".

1. **Bugs et nettoyages** : invoquer le skill `code-review` avec le niveau et le numéro de PR, par exemple `high <n>`. Ne jamais passer `--comment` ni `--fix`.
2. **Contrôles ciblés** (les mêmes que `tnx-review-review-changes`), sur les hunks de la PR. Sauter ce que `/code-review` a déjà remonté :
   - **Bug** : logique fausse, off-by-one, mauvaise condition, cas limite non géré.
   - **Sécurité** : injection, secret exposé, contrôle d'auth manquant, traitement de données dangereux.
   - **Logique** : race condition, null check manquant, mauvaise hypothèse, invariant cassé.
   - **Amélioration** : gestion d'erreur manquante, seulement si elle vaut clairement la peine d'être corrigée.
   - **Atomicité** : une action utilisateur faite par plusieurs mutations ou endpoints indépendants, surtout dans des boucles ou `Promise.all`. Chercher : échec partiel, dépendance d'ordre, validation contre un état intermédiaire, trou dans le rollback optimiste du cache, transaction manquante, invariant d'état final cassé. La remonter comme `Logic`, ou comme `Bug` si des données sont perdues ou si un état invalide est persisté.
3. **Règles de coding-style** : le skill tourne depuis `backend/` ou `frontend/`. Une PR peut toucher les deux. Vérifier chaque package touché avec ses propres règles.
   - **Fichiers backend** : lire les fichiers `backend/docs/coding-style/*.md` correspondants et cocher chaque item "Review checklist" contre le diff. Correspondance :
     - `*.usecase.ts`, `*.service.ts` → `use-cases.md`, `architecture.md`, `permissions.md`, `errors.md`
     - `*.resolver.ts`, `*.entity.ts` → `resolvers.md`, `graphql.md`, `dataloaders.md`
     - `*.repository.ts`, ports, adapters → `repositories.md`
     - `migrations/` → `migrations.md`
     - Toujours : `naming.md`, `typescript.md`
   - **Fichiers frontend** : lire `frontend/AGENTS.md` (sections "Critical Frontend Directives", "Coding Style", "Frontend Architecture Patterns", "File Naming Conventions", "Testing Guidelines", "Performance") et vérifier chaque règle contre le diff. Lire aussi tout fichier `frontend/docs/` qui correspond à la zone touchée.
4. **Artefacts générés** :
   - Backend : les fichiers de schéma et de SDK ont changé quand le GraphQL a changé. `DOCS.md` a changé quand un `*.doc.md` a changé. La migration et le `@Check` de l'entité sont d'accord.
   - Frontend : `src/gql/` a changé quand un `*.graphql.ts` a changé. Les types i18n ont changé quand un fichier de traduction a changé.
5. **Tests** : lister les nouvelles méthodes publiques et les nouveaux comportements. Pour chacun, nommer le test qui le couvre, ou écrire "no test found". Ne pas lancer les tests.
6. **Conformité au ticket** : pour chaque critère d'acceptation ou scénario de l'issue, pointer le code ou le test qui le couvre, ou écrire "not found in the diff".
7. **CI** : recopier le statut de chaque check. Un check rouge est un finding, pas un verdict sur le code.

Ne jamais lancer les tests, l'app ou l'e2e. Dire ce qui n'a pas été vérifié.

## Étape 3 — Contrôles humains

Choisir au plus **5** points, classés par risque. Chacun demande une question précise et un `file:line`. Chercher dans ces zones, dans cet ordre :

1. **Risque de production** : migration sur une grosse table, backfill, verrou, comportement sur les données existantes.
2. **Intention métier** : le comportement correspond-il à ce que veut le produit, au-delà de ce que dit le ticket ?
3. **Sémantique des permissions** : le contrôle est-il présent (l'agent peut le voir) et est-ce le bon rôle (seul un humain le sait) ?
4. **Décisions de conception** : nouvel agrégat, nouveau service, frontière entre use case et service, une abstraction qui ne vaut peut-être pas son coût.
5. **Vocabulaire du domaine** : un nouveau terme dans les noms, les champs d'API ou les textes visibles par l'utilisateur.
6. **Valeur des tests** : les tests couvrent-ils un vrai scénario métier, ou seulement le code ?
7. **Compromis** : performance, dette acceptée, périmètre de la PR.

Lister aussi ce que l'agent **n'a pas pu juger** (par exemple "migration on table X: volume not known").

Si rien ne demande un humain, le dire. Ne pas remplir la liste.

## Étape 4 — Écrire le rapport

Chemin : `.claude/plans/review/<pr-number>.md`, relatif au répertoire de travail courant (`backend/` ou `frontend/`). Si le répertoire de travail est la racine du repo, utiliser le package avec le plus de fichiers touchés. Créer le dossier si besoin. Écraser un ancien rapport de la même PR. Les deux packages ignorent `.claude/plans` dans git.

**Liens.** Chaque `file:line` du rapport, dans tous les blocs (aussi "Vérifié par l'agent"), est un lien markdown cliquable `[file:line](url)`. Obtenir les données avec `gh pr view <n> --json headRefOid,url`. Ne jamais deviner un numéro de ligne : le lire dans le fichier à `headRefOid` avec `gh api -H 'Accept: application/vnd.github.raw' 'repos/<owner>/<repo>/contents/<path>?ref=<headRefOid>'`.
- Ligne changée par la PR : lien vers le diff de la PR, `<PR url>/files#diff-<sha256 of the path>R<line>` (une plage : `R<start>-R<end>`). Hash : `printf %s '<path>' | sha256sum | cut -d' ' -f1`.
- Ligne hors du diff, ou fichier absent de la PR : `https://github.com/<owner>/<repo>/blob/<headRefOid>/<path>#L<line>`.
- Un check de CI : lien vers l'URL de son run, donnée par `gh pr checks`.

Écrire le rapport en français (le lecteur est français). Utiliser des phrases simples et courtes. Garder tels quels les identifiants de code, les noms de fichiers et les titres de PR. Utiliser exactement cette structure :

```markdown
# PR #<n> — <title>

Branche `<head>` → `<base>` · Niveau : <level> · Ticket : #<m> ou aucun · CI : <verte|rouge|en cours> · État : <OPEN|MERGED|CLOSED>

## Verdict
<2 phrases max. Peut-on approuver après les points humains ? Findings bloquants ?>

## À vérifier par un humain (par risque décroissant)
1. **<domaine>** [file:line](lien) — <question précise>
...

## Findings à corriger
1. **<Bug|Sécurité|Logique|Amélioration|Règle de style|Test|Artefact>** [file:line](lien) — <une ligne>. Source : <code-review|contrôles ciblés|nom de la checklist|CI>. Ordre : Sécurité > Bug > Logique > Amélioration > le reste.
...
(ou "Aucun")

## Vérifié par l'agent
- <contrôle> — <preuve : ce qui a été lu ou comparé>
...

## Non vérifié
- <ce que l'agent n'a pas pu juger, et pourquoi>

## Fichiers ignorés
- <fichiers générés ou bruit, par nom>
```

## Étape 5 — Répondre dans le chat

Répondre en français. Donner seulement : le verdict, le chemin du rapport, et les points humains (titres seulement). Ne jamais rien poster sur la PR. Si l'utilisateur veut des commentaires sur la PR, il le demande, et chaque commentaire lui est montré pour accord avant.

## Contraintes

- Ne pas répéter le même problème dans deux blocs. Un finding que l'agent peut corriger va dans "Findings à corriger", pas dans "À vérifier par un humain".
- Une ligne "Vérifié par l'agent" demande une preuve. Pas de preuve → elle va dans "Non vérifié".
- Pas de chipotage de style en dehors des règles de coding-style.
- Ne pas utiliser le mot "Traace" pour le produit. Utiliser Tennaxia.
