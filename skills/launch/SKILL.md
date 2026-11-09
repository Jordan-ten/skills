---
name: launch
description: >
  Démarre le serveur backend en environnement dev ou test, et optionnellement
  le frontend (Vite, dev seulement). Vérifie les conteneurs Docker, les démarre
  si besoin, lance les migrations PostgreSQL et ClickHouse, démarre le serveur
  NestJS en mode watch, et attend qu'il soit en bonne santé. Garant de
  l'environnement local : si un service tourne déjà sur un port à utiliser
  (ce checkout ou un autre workspace), propose de l'arrêter avant de relancer.
  À invoquer quand l'utilisateur tape /launch, /launch dev, /launch test,
  /launch front, /launch dev front, ou demande de start/lancer le serveur
  backend ou le frontend. (Start the backend server in dev or test
  environment, and optionally the frontend.)
allowed-tools: Bash, AskUserQuestion
model: claude-haiku-4-5-20251001
---

# Launch — démarrer le backend (et le frontend)

Démarre le backend Traace (NestJS) dans l'environnement `dev` ou `test`.
Démarre aussi le frontend (React/Vite) si l'argument `front` est présent.

## Arguments

`$ARGUMENTS` — mots séparés par des espaces, dans n'importe quel ordre :

- `dev` (défaut) ou `test` : environnement du backend.
- `front` : démarre aussi le frontend, après le backend.

Exemples : `/launch`, `/launch test`, `/launch front`, `/launch dev front`.

Le frontend ne se lance qu'avec l'environnement `dev` (son `.dev.env` pointe vers le backend sur le port 3000).
Si `test` et `front` sont donnés ensemble : lancer le backend `test`, ignorer `front`
et le dire à l'utilisateur.

Ordre obligatoire, chaque étape bloque la suivante : ports → Docker → migrations → backend → frontend.
À la première étape en échec : stopper, reporter l'erreur, ne rien lancer d'autre.

## Variables selon l'environnement

| Env  | ENV_FILE       | PROJECT_NAME  | PORT | ENV_PREFIX |
|------|----------------|---------------|------|------------|
| dev  | `.dev.env`     | `backend_dev` | 3000 | `_dev`     |
| test | `.test.env`    | `backend_test`| 3007 | `_test`    |

```bash
ROOT_DIR=$(git rev-parse --show-toplevel)   # le checkout courant : workspace Orca ou dépôt principal
BACKEND_DIR=$ROOT_DIR/backend
FRONTEND_DIR=$ROOT_DIR/frontend
FRONT_PORT=3001

ENV=dev
WITH_FRONT=false
for ARG in $ARGUMENTS; do
  case "$ARG" in
    dev|test) ENV=$ARG ;;
    front) WITH_FRONT=true ;;
  esac
done

if [ "$ENV" = "test" ]; then
  ENV_FILE=".test.env"
  PROJECT_NAME="backend_test"
  PORT=3007
  ENV_PREFIX="_test"
else
  ENV_FILE=".dev.env"
  PROJECT_NAME="backend_dev"
  PORT=3000
  ENV_PREFIX="_dev"
fi
```

---

## Étape 0 — Libérer les ports

`launch` est le garant de l'environnement local : c'est lui qui décide quoi faire d'un service déjà
présent. Ne jamais tuer un processus sans un oui de l'utilisateur.

Ports concernés : `$PORT` (backend), et `$FRONT_PORT` si `WITH_FRONT=true`. Ne jamais toucher aux ports
Docker (PostgreSQL, Redis, ClickHouse) : Docker est géré à l'étape 1.

Pour chaque port, trouver le processus qui écoute et le checkout dont il vient :

```bash
port_pid()   { ss -ltnpH "sport = :$1" 2>/dev/null | grep -o 'pid=[0-9]*' | head -1 | cut -d= -f2; }
pid_dir()    { readlink "/proc/$1/cwd" 2>/dev/null; }
pid_cmd()    { ps -o args= -p "$1" 2>/dev/null | cut -c1-120; }

PID=$(port_pid $PORT)
[ -n "$PID" ] && echo "port $PORT : PID $PID, $(pid_cmd $PID), dossier $(pid_dir $PID)"
```

Port libre → rien à faire. Port occupé : classer le cas, puis poser UNE `AskUserQuestion` par port occupé.

| Cas | Test | Options |
|---|---|---|
| Ce checkout | le dossier du processus commence par `$ROOT_DIR` | `Restart it` (recommandé) / `Keep it` / `Abort` |
| Un autre checkout ou un processus inconnu | sinon | `Stop it and launch here` / `Abort` |

Dans la question, dire le port, le PID, la commande et le dossier. Pour un autre checkout, ne pas proposer
`Keep it` : réutiliser l'app d'un autre checkout testerait le mauvais code.

- `Restart it` / `Stop it and launch here` : arrêter le processus (ci-dessous), puis continuer.
- `Keep it` : ne pas relancer ce service. Passer son étape (3 pour le backend, 5 pour le frontend) en
  gardant seulement la vérification de santé.
- `Abort` : stopper le run, ne rien lancer.

Arrêter un service : le processus qui écoute, et ses parents `npm` / `nest` / `vite` du même dossier
(sinon le mode watch relance le serveur). Un `SIGTERM`, puis attendre que le port se libère (max 10 s) :

```bash
stop_service() {
  local PID=$1 TARGETS="$1"
  local PARENT=$(ps -o ppid= -p "$PID" | tr -d ' ')
  while [ -n "$PARENT" ] && [ "$PARENT" != "1" ] \
        && [ "$(pid_dir $PARENT)" = "$(pid_dir $PID)" ] \
        && pid_cmd "$PARENT" | grep -qE 'npm|nest|vite'; do
    TARGETS="$TARGETS $PARENT"
    PARENT=$(ps -o ppid= -p "$PARENT" | tr -d ' ')
  done
  kill -TERM $TARGETS 2>/dev/null
}

stop_service $PID
for i in $(seq 1 10); do [ -z "$(port_pid $PORT)" ] && break; sleep 1; done
```

Si le port est encore occupé après 10 s : dire quel processus reste et demander avant tout `SIGKILL`.
Jamais de `kill -9` sans oui, jamais de `pkill` par nom.

---

## Étape 0 bis — Fichiers d'environnement

Les workspaces neufs n'ont pas `backend/.dev.env` ni `frontend/.dev.env` (fichiers ignorés par git).
Des copies de référence sont dans `env/` à côté de ce skill (`env/backend.dev.env`, `env/frontend.dev.env`).
Ce dossier contient des secrets : il est dans le `.gitignore` du dépôt de skills, ne jamais le committer.

Si un fichier manque, le copier depuis `env/`. Ne jamais écraser un fichier existant.

```bash
SKILL_DIR=/home/jcontent/code/skills/skills/launch
[ -f $BACKEND_DIR/.dev.env ]  || cp $SKILL_DIR/env/backend.dev.env  $BACKEND_DIR/.dev.env
[ -f $FRONTEND_DIR/.dev.env ] || cp $SKILL_DIR/env/frontend.dev.env $FRONTEND_DIR/.dev.env
```

---

## Étape 1 — Vérifier et démarrer Docker

Compter le nombre de services attendus et le nombre de conteneurs running :

```bash
EXPECTED=$(docker compose \
  -f $BACKEND_DIR/docker-compose.yml \
  --env-file $BACKEND_DIR/$ENV_FILE \
  -p $PROJECT_NAME \
  config --services 2>/dev/null | wc -l)

RUNNING=$(docker compose \
  -f $BACKEND_DIR/docker-compose.yml \
  --env-file $BACKEND_DIR/$ENV_FILE \
  -p $PROJECT_NAME \
  ps --format json 2>/dev/null | grep -c '"State":"running"' || echo 0)
```

Si `RUNNING < EXPECTED` (au moins un conteneur manquant ou arrêté) → lancer `up -d` :

```bash
docker compose \
  -f $BACKEND_DIR/docker-compose.yml \
  --env-file $BACKEND_DIR/$ENV_FILE \
  -p $PROJECT_NAME \
  up -d
```

Si `RUNNING == EXPECTED` → afficher "Docker déjà démarré ($RUNNING/$EXPECTED), on continue." et passer à l'étape 2.

Après `up -d`, attendre que PostgreSQL accepte les connexions (max 30 s) :

```bash
for i in $(seq 1 15); do
  docker compose \
    -f $BACKEND_DIR/docker-compose.yml \
    --env-file $BACKEND_DIR/$ENV_FILE \
    -p $PROJECT_NAME \
    exec postgres-15 pg_isready -q 2>/dev/null && PG_READY=true && break
  sleep 2
done
```

Après `up -d`, recompter les conteneurs running. Si `RUNNING < EXPECTED`, ou si `PG_READY` n'est pas `true`
après 30 s → **stopper et reporter** quels conteneurs ne tournent pas (`docker compose ... ps`).
Ne pas lancer les migrations ni le serveur sans Docker complet.

---

## Étape 2 — Appliquer les migrations

```bash
cd $BACKEND_DIR
npm run $ENV_PREFIX mikro:migration:up
```

Si une migration échoue → **stopper et reporter l'erreur** à l'utilisateur (ne pas démarrer le serveur sur une base incohérente).

Puis vérifier qu'aucune migration n'est restée en attente :

```bash
cd $BACKEND_DIR
PENDING_OUTPUT=$(npx dotenvx run -f $ENV_FILE -- npx mikro-orm migration:pending 2>&1)
echo "$PENDING_OUTPUT" | grep -q "No pending migrations"
```

Si `grep` échoue → **stopper** et afficher `$PENDING_OUTPUT` (liste des migrations non passées).
Ne pas démarrer le serveur tant que toutes les migrations ne sont pas appliquées.

---

## Étape 3 — Démarrer le serveur en arrière-plan

Passer cette étape si l'utilisateur a choisi `Keep it` pour le backend à l'étape 0.

```bash
cd $BACKEND_DIR
npm run $ENV_PREFIX start:dev > /tmp/traace-backend-$ENV.log 2>&1 &
SERVER_PID=$!
echo "Serveur démarré en arrière-plan (PID $SERVER_PID), logs : /tmp/traace-backend-$ENV.log"
```

---

## Étape 4 — Attendre que le serveur soit prêt

Poller `/health` toutes les 5 secondes, max 120 secondes :

```bash
READY=false
for i in $(seq 1 24); do
  sleep 5
  HTTP_STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:$PORT/health 2>/dev/null)
  if [ "$HTTP_STATUS" = "200" ] || [ "$HTTP_STATUS" = "401" ]; then
    READY=true
    break
  fi
done
```

> Note : `401` est acceptable — cela signifie que le serveur tourne mais que l'endpoint est protégé. L'important est d'obtenir une réponse HTTP.

Si `READY=true` → afficher :
```
Serveur backend ($ENV) démarré sur http://localhost:$PORT
PID : $SERVER_PID — logs : /tmp/traace-backend-$ENV.log
```

Si `READY=false` après 120 s → afficher les 30 dernières lignes de log et signaler l'échec :
```bash
echo "--- Échec du démarrage ---"
tail -30 /tmp/traace-backend-$ENV.log
```

---

## Étape 5 — Démarrer le frontend (seulement si `front`)

Passer cette étape si `WITH_FRONT=false`, ou si `ENV=test` (voir Arguments).
Ne pas la lancer si une étape précédente a échoué : Docker complet, migrations toutes passées
et backend en bonne santé (`READY=true`) sont requis.

Le port `$FRONT_PORT` a été traité à l'étape 0. S'il tourne encore (`Keep it`), afficher
"Frontend gardé sur http://localhost:3001" et passer à la vérification de santé ci-dessous.

```bash
if [ -z "$(port_pid $FRONT_PORT)" ]; then
  cd $FRONTEND_DIR
  npm run _dev start > /tmp/traace-frontend-dev.log 2>&1 &
  FRONT_PID=$!
  echo "Frontend démarré en arrière-plan (PID $FRONT_PID), logs : /tmp/traace-frontend-dev.log"
fi
```

Poller `http://localhost:3001` toutes les 5 secondes, max 120 secondes (le premier démarrage de Vite peut être lent) :

```bash
FRONT_READY=false
for i in $(seq 1 24); do
  sleep 5
  HTTP_STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:$FRONT_PORT 2>/dev/null)
  if [ "$HTTP_STATUS" = "200" ]; then
    FRONT_READY=true
    break
  fi
done
```

Si `FRONT_READY=true` → afficher :
```
Frontend démarré sur http://localhost:3001
PID : $FRONT_PID — logs : /tmp/traace-frontend-dev.log
```

Si `FRONT_READY=false` après 120 s → afficher les 30 dernières lignes de log et signaler l'échec :
```bash
echo "--- Échec du démarrage du frontend ---"
tail -30 /tmp/traace-frontend-dev.log
```

---

## Résumé des vérifications

| Étape | Vérification | Critère de succès |
|-------|-------------|-------------------|
| Ports | `ss -ltnp` sur `$PORT` (et `$FRONT_PORT`) | Libres, ou gardés sur un oui de l'utilisateur |
| Docker | `docker compose ps` | Tous les services running (`RUNNING == EXPECTED`) |
| PostgreSQL | `pg_isready` | Exit 0 |
| Migrations PG | `mikro:migration:up` puis `migration:pending` | Exit 0 et "No pending migrations" |
| Serveur | `curl /health` | HTTP 200 ou 401 |
| Frontend (si `front`) | `curl localhost:3001` | HTTP 200 |