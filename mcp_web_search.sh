#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -lt 1 ]; then
  echo "Usage: ./mcp_web_search.sh \"query\""
  exit 2
fi

python3 /home/cechinel/.openclaw/workspace/minimax_mcp_web_search.py "$*"
