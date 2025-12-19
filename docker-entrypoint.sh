#!/usr/bin/env bash
set -e

# Garante diretório do SQLite com permissão de escrita.
mkdir -p /app/instance
chmod 775 /app/instance || true

# Garante que o banco SQLite e as tabelas existam antes de subir o servidor.
python - <<'PY'
from run import app, db  # type: ignore

with app.app_context():
    db.create_all()
PY

exec gunicorn \
  --bind "0.0.0.0:${PORT:-5000}" \
  --workers "${GUNICORN_WORKERS:-3}" \
  --threads "${GUNICORN_THREADS:-2}" \
  --timeout "${GUNICORN_TIMEOUT:-120}" \
  run:app

