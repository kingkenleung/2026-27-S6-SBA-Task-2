#!/bin/sh
set -e

mkdir -p /data
if [ ! -f /data/app.db ]; then
  cp /seed/app.db /data/app.db
  date -u +"%Y-%m-%dT%H:%M:%SZ" > /data/restore.log
  echo "[init] seeded /data/app.db"
fi

chown -R www-data:www-data /data
chmod 775 /data
chmod 664 /data/app.db 2>/dev/null || true

exec "$@"
