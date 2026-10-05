#!/usr/bin/env bash
set -euo pipefail

HOST="${REMOTE_HOST:?REMOTE_HOST is not set}"
APP_DIR="${REMOTE_APP_DIR:?REMOTE_APP_DIR is not set}"

echo "Deploying to $HOST..."

ssh "$HOST" "APP_DIR=$(printf %q "$APP_DIR") bash -s" <<'EOF'
set -euo pipefail
cd "$APP_DIR"

git checkout development
git fetch origin development
LOCAL=$(git rev-parse HEAD)
REMOTE=$(git rev-parse origin/development)

if [ "$LOCAL" = "$REMOTE" ]; then
    echo "No new commits. Just checking for new Docker images..."
    docker compose pull && \
    docker compose up -d --remove-orphans
else
    echo "New commits detected! Pulling code and rebuilding everything..."
    # git pull origin development && \
    # docker compose pull && \
    # docker compose kill && \
    # docker compose up -d --remove-orphans
fi
EOF