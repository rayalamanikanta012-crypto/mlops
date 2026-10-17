#!/bin/sh
# Starts the FastAPI backend (8000) and Flask frontend (5000) in one container.
set -eu

HOST=${HOST:-0.0.0.0}
API_PORT=${API_PORT:-8000}
PORT=${PORT:-5000}

uvicorn backend.main:app --host "$HOST" --port "$API_PORT" &
api_pid=$!
gunicorn frontend.app:app --bind "$HOST:$PORT" &
frontend_pid=$!

shutdown() {
    trap - TERM INT
    kill "$api_pid" "$frontend_pid" 2>/dev/null || true
    wait "$api_pid" 2>/dev/null || true
    wait "$frontend_pid" 2>/dev/null || true
}

trap shutdown TERM INT

# POSIX sh has no portable `wait -n`; poll so one failed server stops the
# container instead of leaving the other server running by itself.
while kill -0 "$api_pid" 2>/dev/null && kill -0 "$frontend_pid" 2>/dev/null; do
    sleep 1
done

status=0
wait "$api_pid" 2>/dev/null || status=$?
wait "$frontend_pid" 2>/dev/null || status=$?
shutdown
exit "$status"
