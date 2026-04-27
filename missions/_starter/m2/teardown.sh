#!/usr/bin/env bash
# teardown.sh — always-safe kill switch.
# No flags. No arguments. No "but I just want to..."
# If you're tempted to add a flag, write a different script.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
docker compose -f "$HERE/sandbox/docker-compose.yml" down -v --remove-orphans 2>/dev/null || true
docker network prune -f 2>/dev/null || true
echo "[teardown] complete."
