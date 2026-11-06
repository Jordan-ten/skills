#!/usr/bin/env bash
# Sends one GraphQL operation to a local backend that runs with OFFLINE_AUTH=true.
# It signs the same offline-auth token as frontend/tests/fixtures/graphql.ts, so no login is needed.
#
# Usage:  graphql.sh <<'GQL'
#         mutation CreateX($input: XInput!) { createX(input: $input) { id } }
#         GQL
#         graphql.sh --variables '{"input":{"name":"n"}}' <<'GQL' ... GQL
#
# Env:  GQL_EMAIL (required), GQL_ORG (default: 1),
#       GQL_ENDPOINT (default: http://localhost:3000/graphql, local hosts only)
#       GQL_ADMIN=1 drops the organization header, for sudo-mode admin operations.
#
# Exit code: 0 only when the response has no GraphQL error. HTTP 200 with "errors" exits 1.
set -euo pipefail

VARIABLES='{}'
if [[ "${1:-}" == "--variables" ]]; then
  if [[ $# -lt 2 ]]; then
    echo "--variables needs a JSON string after it." >&2
    exit 1
  fi
  VARIABLES="$2"
  shift 2
fi

QUERY="${1:-$(cat)}"
EMAIL="${GQL_EMAIL:-}"
ORG="${GQL_ORG:-1}"
ENDPOINT="${GQL_ENDPOINT:-http://localhost:3000/graphql}"

case "$ENDPOINT" in
  http://localhost:*|http://127.0.0.1:*) ;;
  *) echo "Refused: $ENDPOINT is not a local endpoint. This script only talks to a local backend." >&2; exit 1 ;;
esac

if [[ -z "$EMAIL" ]]; then
  echo "GQL_EMAIL is not set: give the dev user email." >&2
  exit 1
fi

TOKEN=$(EMAIL="$EMAIL" node -e '
const crypto = require("crypto")
const b64 = o => Buffer.from(JSON.stringify(o)).toString("base64url")
const head = b64({ alg: "HS256" })
const body = b64({
  email: process.env.EMAIL,
  "https://www.tennaxia.com/nodes": ["node/app_esg"],
  exp: Math.floor(Date.now() / 1000) + 3600
})
const data = `${head}.${body}`
const sig = crypto.createHmac("sha256", "some really secret secret").update(data).digest("base64url")
process.stdout.write(`${data}.${sig}`)
')

BODY=$(QUERY="$QUERY" VARIABLES="$VARIABLES" node -e '
process.stdout.write(JSON.stringify({ query: process.env.QUERY, variables: JSON.parse(process.env.VARIABLES) }))
')

if [[ "${GQL_ADMIN:-}" == "1" ]]; then
  ORG_HEADER=()
else
  ORG_HEADER=(-H "x-tennaxia-organization-id: $ORG")
fi

RESPONSE=$(curl -sS -X POST "$ENDPOINT" \
  -H "authorization: Bearer $TOKEN" \
  "${ORG_HEADER[@]}" \
  -H "content-type: application/json" \
  -d "$BODY")

echo "$RESPONSE"

RESPONSE="$RESPONSE" node -e '
let parsed
try { parsed = JSON.parse(process.env.RESPONSE) } catch { process.exit(1) }
process.exit(Array.isArray(parsed.errors) && parsed.errors.length > 0 ? 1 : 0)
'
