#!/bin/sh
# Nightly backup with no model in it. Install: cp kits/company/scripts/backup.sh ~/.hermes/scripts/backup.sh
# Job:     hermes -p ops cron create "every day at 03:00" --no-agent --script backup.sh --name "backup-nightly"
# --no-agent delivers this script's stdout verbatim; empty stdout is silent, so print only when something is wrong.
set -u
OUT="${BACKUP_DIR:-$HOME/hermes-backups}"
mkdir -p "$OUT"
if hermes backup --quick --label nightly -o "$OUT/hermes-$(date +%Y%m%d).zip" >"$OUT/last.log" 2>&1; then
  # keep the newest 14, quietly
  /bin/ls -1t "$OUT"/hermes-*.zip 2>/dev/null | tail -n +15 | while read -r f; do rm -f "$f"; done
else
  echo "backup FAILED at $(date): $(tail -3 "$OUT/last.log")"
fi
