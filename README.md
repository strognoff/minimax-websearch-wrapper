# Minimax MCP Tool Wrapper

A lightweight wrapper to run **MiniMax Coding Plan MCP** tools from the command line.

## What this does

- Starts `uvx minimax-coding-plan-mcp` over MCP stdio
- Calls:
  - `web_search(query)`
  - `understand_image(prompt, image_source)`
- Prints JSON results

## Files

- `minimax_mcp_web_search.py` — Python MCP client wrapper (both tools)
- `mcp_web_search.sh` — shell helper for web search
- `mcp_understand_image.sh` — shell helper for image understanding

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

2. Make shell wrappers executable:

```bash
chmod +x mcp_web_search.sh mcp_understand_image.sh
```

3. Source credentials:

```bash
set -a
source /home/cechinel/.openclaw/credentials/minimax_credentials
set +a
```

## Usage

### 1) Web search

```bash
./mcp_web_search.sh "Minimax coding plan mcp documentation"
```

### 2) Understand image

```bash
./mcp_understand_image.sh "Describe this image in one sentence" "https://picsum.photos/300/200.jpg"
```

Supports `image_source` as:
- HTTP/HTTPS URL
- local relative path
- local absolute path

Rules:
- If path starts with `@`, wrapper strips it automatically.
- Supported image formats: **JPEG, PNG, WebP**.

## Output

Returns JSON/text result from MCP tool call.

## Notes

- If you see `MINIMAX_API_KEY is not set`, load credentials before running.
- If image URL format is unsupported (e.g., `.svg`), wrapper returns validation error before API call.
- This wrapper is intended as a fallback/override for environments where built-in search is unavailable.
