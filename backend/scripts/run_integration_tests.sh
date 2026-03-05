#!/usr/bin/env bash
set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
PYTHON_BIN="$PROJECT_ROOT/backend/venv/bin/python"

cd "$PROJECT_ROOT"
docker compose up -d db

cd backend
if [[ -x "$PYTHON_BIN" ]]; then
  "$PYTHON_BIN" -m pytest -m integration -v
else
  python -m pytest -m integration -v
fi
