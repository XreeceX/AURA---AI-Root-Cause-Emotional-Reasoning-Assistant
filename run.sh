#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

if [ -d .venv ]; then
  :
else
  python -m venv .venv
fi

ACTIVATE=".venv/bin/activate"
if [ -f ".venv/Scripts/activate" ]; then
  ACTIVATE=".venv/Scripts/activate"
fi

. "$ACTIVATE"

pip install -r backend/requirements.txt >/dev/null

cleanup() {
  if [ -n "${UVICORN_PID:-}" ] && kill -0 "$UVICORN_PID" 2>/dev/null; then
    kill "$UVICORN_PID" 2>/dev/null || true
  fi
}
trap cleanup EXIT INT TERM

uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload --reload-dir backend &
UVICORN_PID=$!

OPENED=0
if command -v cmd.exe >/dev/null 2>&1; then
  cmd.exe /C start "" "$(pwd | sed 's|/|\\|g')\\frontend\\index.html" && OPENED=1 || true
elif command -v xdg-open >/dev/null 2>&1; then
  xdg-open frontend/index.html && OPENED=1 || true
elif command -v open >/dev/null 2>&1; then
  open frontend/index.html && OPENED=1 || true
fi

if [ "$OPENED" -eq 0 ]; then
  echo "Open frontend/index.html in your browser. API at http://localhost:8000"
fi

wait "$UVICORN_PID"

