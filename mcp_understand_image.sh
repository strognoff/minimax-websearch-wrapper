#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -lt 2 ]; then
  echo "Usage: ./mcp_understand_image.sh \"prompt\" \"image_source\""
  exit 2
fi

prompt="$1"
image_source="$2"

python3 /home/cechinel/.openclaw/workspace/minimax_mcp_web_search.py understand_image "$prompt" "$image_source"
