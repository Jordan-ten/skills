---
name: review
description: Fait le triage de la pull request d'un collègue. Lance /code-review (high par défaut), les checklists de coding-style, la vérification du ticket et le statut de la CI, puis écrit un rapport markdown court : verdict, sujets à corriger, points à contrôler par un humain. À utiliser quand l'utilisateur lance /review ou dit "triage cette PR", "prépare ma review de la PR #N", "qu'est-ce que je dois vérifier à la main sur cette PR". Pour cartographier une grosse PR par sous-fonctionnalité, utiliser tnx-review-plan-pr-review à la place. (Triage a colleague's pull request, with a short report: verdict, issues to fix, human checks.)
disable-model-invocation: true
allowed-tools: Bash(git *), Bash(gh *), Read, Grep, Glob, Write, Skill
---

# Triage de PR

But : le relecteur humain ne lit que ce qui l'aide à décider. Le rapport est court. Il ne liste pas ce qui est correct : seulement les problèmes, les points à juger et de quoi comprendre la PR.

Entrée : un numéro ou une URL de PR (obligatoire). Niveau optionnel `low|medium|high|xhigh` pour `/code-review`. Défaut : `high`. N'utiliser `max` que si l'utilisateur le demande.

## Étape 1 — Collecter

- `gh pr view <n> --json title,body,headRefName,baseRefName,files,closingIssuesReferences`
- `gh pr diff <n> --name-only`, puis la stat. Ne jamais charger le diff complet d'un coup. Lire fichier par fichier, seulement ce dont un contrôle a besoin.
- `gh pr checks <n>` : statut de la CI, y compris OpenGrep et les vérifications de types.
- Issue liée : `gh issue view <number> --comments`. Les décisions sont souvent dans les commentaires. Garder : le problème, le comportement attendu, les critères d'acceptation, les scénarios. Pas d'issue liée → le dire dans le rapport.
- Ignorer les fichiers générés (`schema.gql`, `generated/`, `gql/`, `package-lock.json`) : ne pas les lire, ne pas les citer dans le rapport.

## Étape 2 — Contrôles de l'agent

Lancer tous ceux-ci. Chacun produit des findings. Un contrôle sans finding ne laisse aucune trace dans le rapport.

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
6. **Conformité à l'attendu** : comparer le contenu du ticket avec ce que le code fait vraiment.
   - Lister chaque exigence du ticket : problème à résoudre, comportement attendu, critère d'acceptation, scénario Given/When/Then.
   - Pour chacune, lire le code et dire en une phrase ce que l'implémentation fait. Ne pas recopier le ticket : décrire le comportement réel.
   - Donner un statut : **couvert** (code et test), **couvert sans test**, **partiel** (dire ce qui manque), **absent** ("not found in the diff").
   - Chercher aussi l'inverse : ce que la PR change **sans** que le ticket le demande (**hors ticket**). Dire si cela semble voulu.
   - La solution traite-t-elle la cause décrite dans le ticket, ou seulement le symptôme ? Une exigence absente ou une cause non traitée est un sujet **bloquant** de la famille `Ticket`.
   - Pas d'issue liée : utiliser la description de la PR comme référence, et le dire.
7. **Implémentation et conception** : comprendre comment la solution est construite, pour l'expliquer au relecteur.
   - Trouver le fil du changement : où il entre (resolver, composant, job), par quelles couches il passe, où il s'écrit (repository, migration, cache).
   - Relever les choix de conception : nouveau service, nouveau port, abstraction, nouvelle table ou colonne, nouveau terme de vocabulaire, écart avec le code voisin.
   - Pour chaque choix, juger : **cohérent avec l'existant** (dire avec quel code voisin), ou **à discuter** (dire pourquoi).
   - Lister les tests qui couvrent ce parcours.
8. **CI** : recopier le statut de chaque check. Un check rouge est un finding, pas un verdict sur le code.

Ne jamais lancer les tests, l'app ou l'e2e. Ce que l'agent ne peut pas juger sans cela (rendu réel, volume de données) devient un point de l'étape 3, seulement s'il porte un risque.

## Étape 3 — Contrôles humains

Choisir au plus **5** points, classés par risque. Chacun demande une question précise et un `file:line`. Chercher dans ces zones, dans cet ordre :

1. **Risque de production** : migration sur une grosse table, backfill, verrou, comportement sur les données existantes.
2. **Intention métier** : le comportement correspond-il à ce que veut le produit, au-delà de ce que dit le ticket ?
3. **Sémantique des permissions** : le contrôle est-il présent (l'agent peut le voir) et est-ce le bon rôle (seul un humain le sait) ?
4. **Décisions de conception** : nouvel agrégat, nouveau service, frontière entre use case et service, une abstraction qui ne vaut peut-être pas son coût.
5. **Vocabulaire du domaine** : un nouveau terme dans les noms, les champs d'API ou les textes visibles par l'utilisateur.
6. **Valeur des tests** : les tests couvrent-ils un vrai scénario métier, ou seulement le code ?
7. **Compromis** : performance, dette acceptée, périmètre de la PR.

Un point que l'agent n'a pas pu juger (par exemple "migration sur la table X : volume inconnu") entre dans cette liste, s'il porte un risque.

Si rien ne demande un humain, le dire. Ne pas remplir la liste.

## Étape 4 — Écrire le rapport

Chemin : `.claude/plans/review/<pr-number>.md`, relatif au répertoire de travail courant (`backend/` ou `frontend/`). Si le répertoire de travail est la racine du repo, utiliser le package avec le plus de fichiers touchés. Créer le dossier si besoin. Écraser un ancien rapport de la même PR. Les deux packages ignorent `.claude/plans` dans git.

**Liens.** Chaque `file:line` du rapport, dans tous les blocs, est un lien markdown cliquable `[file:line](url)`. Obtenir les données avec `gh pr view <n> --json headRefOid,url`. Ne jamais deviner un numéro de ligne : le lire dans le fichier à `headRefOid` avec `gh api -H 'Accept: application/vnd.github.raw' 'repos/<owner>/<repo>/contents/<path>?ref=<headRefOid>'`.
- Chaque lien de "Où aller" ouvre le code directement dans la PR. Ligne changée par la PR : lien vers le diff de la PR, `<PR url>/files#diff-<sha256 of the path>R<line>` (une plage : `R<start>-R<end>`). Hash : `printf %s '<path>' | sha256sum | cut -d' ' -f1`.
- Ligne hors du diff, ou fichier absent de la PR : `https://github.com/<owner>/<repo>/blob/<headRefOid>/<path>#L<line>`.
- Un check de CI : lien vers l'URL de son run, donnée par `gh pr checks`.

**Sujets bloquants et non bloquants.** Un finding est **bloquant** si la PR ne doit pas être mergée tel quel. Sinon il est **non bloquant**.

Bloquant :
- **Sécurité** : injection, secret exposé, contrôle d'auth ou de permission manquant, fuite entre tenants.
- **Bug** : comportement faux, perte de données, état invalide persisté, crash.
- **Ticket** : un critère d'acceptation ou un scénario du ticket n'est pas couvert.
- **Migration** : risque en production (verrou, backfill, table volumineuse, CHECK non bidirectionnel, migration différente de l'entité).
- **CI** : check rouge causé par le code de la PR.
- **Artefact** : fichier généré non mis à jour qui casse le build ou le contrat d'API.

Non bloquant :
- **Logique** : cas limite ou atomicité sans impact utilisateur démontré.
- **Règle de style** : règle de la checklist non respectée (architecture, GraphQL, base de données, frontend).
- **Test** : comportement ou méthode publique sans test.
- **Artefact** : fichier généré non mis à jour sans effet sur le build.
- **Amélioration** : gestion d'erreur, lisibilité, nommage, vocabulaire du domaine.

Un doute entre bloquant et non bloquant : choisir bloquant et le dire. Un check de CI rouge sans lien avec la PR n'est pas un finding : le dire dans la ligne d'en-tête (`CI : rouge, sans lien avec la PR`).

**Regrouper par famille, 5 sujets au maximum.** Un **sujet** réunit tous les findings d'une même famille (les catégories ci-dessus) qui ont la même cause ou le même thème. Exemple : trois `Test` manquants sur trois méthodes = un seul sujet "Test", avec trois liens. Ne jamais lister le même sujet deux fois. Un sujet = un titre, puis son explication, puis ses liens. Jamais de lien sans explication au-dessus.
- Au plus **5 sujets** en tout, bloquants et non bloquants ensemble.
- Plus de 5 sujets : garder les 5 les plus risqués (bloquants d'abord). Écrire sous la liste : "Autres sujets non listés : <n> (non bloquants mineurs)". Ne pas les détailler.
- Dans une section, trier du plus risqué au moins risqué.

Écrire le rapport en français (le lecteur est français). Utiliser des phrases simples et courtes. Garder tels quels les identifiants de code, les noms de fichiers et les titres de PR.

**Le rapport est court et se lit de haut en bas : décision d'abord, contexte ensuite.** Ne jamais ajouter de bloc "vérifié", "non vérifié" ou "fichiers ignorés". Ne pas écrire ce qui est correct. Une section sans contenu s'écrit en un mot ("Aucun", "Rien") ou disparaît (voir les notes dans le modèle). Utiliser exactement cette structure :

```markdown
# PR #<n> — <title>

`<head>` → `<base>` · Ticket : #<m> ou aucun · CI : <verte|rouge|en cours> · État : <OPEN|MERGED|CLOSED>

## Verdict
<2 phrases max. Peut-on approuver, et sous quelle condition ? Puis : <n> bloquant(s) · <n> non bloquant(s).>

## Sujets à corriger (5 maximum, regroupés par famille)

### 🔴 Bloquant
1. **<famille> — <le sujet en une phrase>**

   <Explication : 2 à 3 phrases courtes. Ce qui ne va pas, pourquoi c'est bloquant, ce qu'il faut faire.>

   Où aller :
   - [file:line](url du code dans la PR) — <ce qu'on y trouve>

(ou "Aucun")

### 🟢 Non bloquant
2. **<famille> — <le sujet en une phrase>**

   <Explication : 2 à 3 phrases courtes. Ce qui ne va pas et ce qu'il faudrait faire.>

   Où aller :
   - [file:line](url du code dans la PR) — <ce qu'on y trouve>

(ou "Aucun")

Autres sujets non listés : <n> (non bloquants mineurs). *(Cette ligne seulement s'il y en a.)*

## À vérifier par un humain
1. **<domaine>** [file:line](lien) — <question précise>

(Maximum 5, par risque décroissant. Ou "Rien ne demande un humain".)

## Conformité au ticket
**Ticket :** <1 phrase : le problème et le comportement attendu.>
**PR :** <1 phrase : ce que le code fait vraiment.>

| Exigence du ticket | Ce que le code fait | Statut |
|---|---|---|
| <critère ou scénario> | <comportement réel> — [file:line](url du code dans la PR) | <couvert / couvert sans test / partiel / absent> |

**Hors ticket :** <ce que la PR change sans que le ticket le demande.> *(Cette ligne seulement s'il y en a.)*

## Implémentation
<2 à 3 phrases : par où le changement entre, par quelles couches il passe, où il s'écrit.>

1. **<couche>** — <ce que fait ce morceau> — [file:line](url du code dans la PR)

**Choix de conception :** <le choix> — <cohérent avec <code voisin> ou à discuter : pourquoi> — [file:line](lien). *(Cette ligne seulement s'il y a un choix notable.)*

**Tests :** [file:line](url du code dans la PR) — <ce qu'ils couvrent>. (ou "Aucun test dans la PR")
```

Notes sur le modèle :
- Le parcours de "Implémentation" compte 5 étapes au maximum, une par couche touchée.
- Un sujet de "Conformité au ticket" au statut `partiel` ou `absent`, ou une cause non traitée, est aussi un sujet bloquant `Ticket` dans "Sujets à corriger". Dans ce cas, le tableau reste court et renvoie au sujet.
- Pas d'issue liée : remplacer "Ticket" par la description de la PR, et le dire en une phrase.

## Étape 5 — Montrer le rapport dans le chat

Afficher le rapport **en entier** dans la réponse, tel qu'il est écrit dans le fichier, en français. Ne pas le résumer. Ne pas répondre seulement avec le chemin. Mettre le chemin du fichier en dernière ligne.

Ne jamais rien poster sur la PR. Si l'utilisateur veut des commentaires sur la PR, il le demande, et chaque commentaire lui est montré pour accord avant.

## Contraintes

- Ne pas répéter le même problème dans deux blocs. Un finding que l'agent peut corriger va dans "Sujets à corriger", pas dans "À vérifier par un humain".
- Pas de chipotage de style en dehors des règles de coding-style.
- Ne pas utiliser le mot "Traace" pour le produit. Utiliser Tennaxia.
