#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -lt 1 ]; then
  echo "Usage: ./mcp_web_search.sh \"query\""
  exit 2
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON="$SCRIPT_DIR/.venv/bin/python"
if [ ! -x "$PYTHON" ]; then
  PYTHON="python3"
fi
export PATH="$SCRIPT_DIR/.venv/bin:$PATH"

"$PYTHON" "$SCRIPT_DIR/minimax_mcp_web_search.py" web_search "$*"
