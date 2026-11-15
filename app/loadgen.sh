#!/usr/bin/env bash
# Hit the checkout endpoint so Prometheus sees traffic.
set -euo pipefail
BASE_URL="${BASE_URL:-http://localhost:18000}"
echo "Posting checkouts to ${BASE_URL}/checkout (Ctrl+C to stop)"
while true; do
  curl -sS -X POST "${BASE_URL}/checkout" -o /dev/null -w "%{http_code}\n" || true
  sleep 0.5
done
