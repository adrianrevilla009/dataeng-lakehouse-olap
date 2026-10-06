#!/usr/bin/env bash
# Start ClickHouse, run orders.sql statement by statement over HTTP, check the aggregate.
set -euo pipefail
cd "$(dirname "$0")"
trap 'docker compose down -v' EXIT
docker compose up -d
for _ in $(seq 30); do curl -sf localhost:8123/ping >/dev/null && break; sleep 1; done
out=""
while IFS= read -r stmt; do
  [ -n "$stmt" ] && out=$(curl -sf localhost:8123/ --data-binary "$stmt")
done < orders.sql
printf '%s\n' "$out"
[ "$out" = "$(printf 'ana\t30\nbo\t5')" ] && echo OK
