#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ENV_FILE="$SCRIPT_DIR/.env"

[ -f "$ENV_FILE" ] || { echo ".env not found: $ENV_FILE" >&2; exit 1; }

set -a
source "$ENV_FILE"
set +a

HOST_USER="${HOST_USER:?HOST_USER is not set}"
HOST_DOMAIN="${HOST_DOMAIN:?HOST_DOMAIN is not set}"
SSH_KEY_PATH="${SSH_KEY_PATH:?SSH_KEY_PATH is not set}"
APP_DIR="${REMOTE_APP_DIR:?REMOTE_APP_DIR is not set}"

[ -r "$SSH_KEY_PATH" ] || { echo "SSH key not readable: $SSH_KEY_PATH" >&2; exit 1; }

echo "Deploying to $HOST_USER@$HOST_DOMAIN:$APP_DIR..."

ssh -i "$SSH_KEY_PATH" "$HOST_USER@$HOST_DOMAIN" "APP_DIR=$(printf %q "$APP_DIR") bash -s" <<'EOF'
set -euo pipefail
cd "$APP_DIR"

git checkout development
git fetch origin development
LOCAL=$(git rev-parse HEAD)
REMOTE=$(git rev-parse origin/development)

if [ "$LOCAL" = "$REMOTE" ]; then
    echo "No new commits. Just checking for new Docker images..."
    docker compose pull
    docker compose up -d --remove-orphans
else
    echo "New commits detected! Pulling code and rebuilding everything..."
    # git pull origin development
    # docker compose pull
    # docker compose kill
    # docker compose up -d --remove-orphans
fi
EOF

echo "Server update finished."