#!/bin/sh
set -eu

interval="${RESTORE_INTERVAL_SECONDS:-300}"
case "$interval" in
  ''|*[!0-9]*) interval=300 ;;
esac
[ "$interval" -ge 5 ] || interval=5

echo "[restore] resetting the database every ${interval}s"
while true; do
  sleep "$interval"
  cp /seed/app.db /data/.app.db.new
  chown 82:82 /data/.app.db.new
  chmod 664 /data/.app.db.new
  mv /data/.app.db.new /data/app.db
  rm -f /data/app.db-journal /data/app.db-wal /data/app.db-shm
  date -u +"%Y-%m-%dT%H:%M:%SZ" > /data/restore.log
  echo "[restore] database returned to its original state"
done
