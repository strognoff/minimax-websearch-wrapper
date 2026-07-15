#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -lt 2 ]; then
  echo "Usage: ./mcp_understand_image.sh \"prompt\" \"image_source\""
  exit 2
fi

prompt="$1"
image_source="$2"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON="$SCRIPT_DIR/.venv/bin/python"
if [ ! -x "$PYTHON" ]; then
  PYTHON="python3"
fi
export PATH="$SCRIPT_DIR/.venv/bin:$PATH"

"$PYTHON" "$SCRIPT_DIR/minimax_mcp_web_search.py" understand_image "$prompt" "$image_source"
