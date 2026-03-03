# Minimax MCP Web Search Wrapper

A lightweight wrapper to run **MiniMax Coding Plan MCP** `web_search` from the command line.

## What this does

- Starts `uvx minimax-coding-plan-mcp` over MCP stdio
- Calls the `web_search` tool with your query
- Prints JSON results

## Files

- `minimax_mcp_web_search.py` — Python MCP client wrapper
- `mcp_web_search.sh` — shell helper script

## Prerequisites

- Python 3.11+
- `uvx` installed
- MiniMax credentials

## Credentials

Expected env vars:

- `MINIMAX_API_KEY`
- `MINIMAX_API_HOST` (example: `https://api.minimax.io`)

Example credentials file:

```bash
# ~/.openclaw/credentials/minimax_credentials
MINIMAX_API_KEY=your_key_here
MINIMAX_API_HOST=https://api.minimax.io
```

## Setup

1. Install Python dependency:

```bash
python3 -m pip install --user --break-system-packages mcp
```

2. Make shell wrapper executable:

```bash
chmod +x mcp_web_search.sh
```

3. Source credentials and run:

```bash
set -a
source /home/cechinel/.openclaw/credentials/minimax_credentials
set +a

./mcp_web_search.sh "Minimax coding plan mcp documentation"
```

## Output

Returns JSON with organic results, for example:

- title
- link
- snippet
- date (if available)

## Notes

- If you see `MINIMAX_API_KEY is not set`, load credentials before running.
- This wrapper is intended as a fallback/override for environments where built-in `web_search` is unavailable.
