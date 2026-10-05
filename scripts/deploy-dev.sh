#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."

set -a; source .env; set +a
: "${DEPLOY_SSH_HOST_ALIAS:?not set in .env}"
: "${DEPLOY_REMOTE_APP_PATH:?not set in .env}"

echo "ssh-add key for $DEPLOY_SSH_HOST_ALIAS"
eval "$(ssh-agent -s)" >/dev/null
trap 'ssh-agent -k >/dev/null' EXIT
ssh-add ~/.ssh/id_ed25519


echo "Deploying to $DEPLOY_SSH_HOST_ALIAS via local woodpecker..."

WOODPECKER_DIR="$PWD/.local-woodpecker"


docker run --rm -it --init \
  --group-add "$(stat -c %g /var/run/docker.sock)" \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v "$WOODPECKER_DIR":"$WOODPECKER_DIR":ro -w "$WOODPECKER_DIR" \
  woodpeckerci/woodpecker-cli:v3.18.1 exec \
    --repo-trusted-volumes \
    --env SSH_AUTH_SOCK_HOST_PATH="$SSH_AUTH_SOCK" \
    --env REMOTE_HOST="$DEPLOY_SSH_HOST_ALIAS" \
    --env REMOTE_APP_DIR="$DEPLOY_REMOTE_APP_PATH" \
    --env HOST_SSH_DIR="$HOME/.ssh/" \
    .deploy-dev.yml

echo "Server update finished"