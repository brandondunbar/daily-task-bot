#!/usr/bin/env bash
set -euo pipefail

# If first argument starts with a dash, assume they want options for main.py
if [ "${1:-}" = "" ] || [ "${1:0:1}" = "-" ]; then
  set -- python main.py "$@"
fi

# Replace shell with the final process (so it gets signals)
exec "$@"
