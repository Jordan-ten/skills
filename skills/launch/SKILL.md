---
name: launch
description: >
  Start the backend server in dev or test environment. Checks Docker containers,
  starts them if needed, runs PostgreSQL and ClickHouse migrations, starts the
  NestJS server in watch mode, and polls until healthy.
  Invoke when the user types /launch, /launch dev, /launch test, or asks to
  start/lancer le serveur backend.
allowed-tools: Bash
model: claude-haiku-4-5-20251001
---

# Launch — démarrer le backend

Démarre le backend Traace (NestJS) dans l'environnement `dev` ou `test`.

## Arguments

`$ARGUMENTS` — environnement cible : `dev` (défaut) ou `test`.

## Variables selon l'environnement

| Env  | ENV_FILE       | PROJECT_NAME  | PORT | ENV_PREFIX |
|------|----------------|---------------|------|------------|
| dev  | `.dev.env`     | `backend_dev` | 3000 | `_dev`     |
| test | `.test.env`    | `backend_test`| 3007 | `_test`    |

```bash
BACKEND_DIR=/home/jcontent/code/traace/backend
ENV=${ARGUMENTS:-dev}

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
    exec postgres-15 pg_isready -q 2>/dev/null && break
  sleep 2
done
```

---

## Étape 2 — Appliquer les migrations

```bash
cd $BACKEND_DIR
npm run $ENV_PREFIX mikro:migration:up
```

Si une migration échoue → **stopper et reporter l'erreur** à l'utilisateur (ne pas démarrer le serveur sur une base incohérente).

---

## Étape 3 — Démarrer le serveur en arrière-plan

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

## Résumé des vérifications

| Étape | Vérification | Critère de succès |
|-------|-------------|-------------------|
| Docker | `docker compose ps` | Au moins un conteneur running |
| PostgreSQL | `pg_isready` | Exit 0 |
| Migrations PG | `mikro:migration:up` | Exit 0 |
| Serveur | `curl /health` | HTTP 200 ou 401 |