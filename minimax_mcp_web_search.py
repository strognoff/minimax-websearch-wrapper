#!/usr/bin/env python3
"""
Wrapper to call minimax-coding-plan-mcp web_search via MCP stdio.
Usage:
  python minimax_mcp_web_search.py "your query"

Env required:
  MINIMAX_API_KEY
Optional:
  MINIMAX_API_HOST (default: https://api.minimax.chat)
"""

import asyncio
import json
import os
import sys
from typing import Any

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

DEFAULT_HOST = "https://api.minimax.chat"


def normalize_result(content: Any):
    if isinstance(content, list):
        out = []
        for c in content:
            text = getattr(c, "text", None)
            if text is not None:
                try:
                    out.append(json.loads(text))
                except Exception:
                    out.append(text)
            else:
                out.append(str(c))
        return out
    return content


async def run(query: str):
    api_key = os.getenv("MINIMAX_API_KEY")
    api_host = os.getenv("MINIMAX_API_HOST", DEFAULT_HOST)

    if not api_key:
        raise RuntimeError("MINIMAX_API_KEY is not set")

    params = StdioServerParameters(
        command="uvx",
        args=["minimax-coding-plan-mcp"],
        env={
            **os.environ,
            "MINIMAX_API_KEY": api_key,
            "MINIMAX_API_HOST": api_host,
        },
    )

    async with stdio_client(params) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()
            result = await session.call_tool("web_search", {"query": query})
            print(json.dumps(normalize_result(result.content), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python minimax_mcp_web_search.py \"query\"")
        sys.exit(2)

    q = " ".join(sys.argv[1:]).strip()
    try:
        asyncio.run(run(q))
    except Exception as e:
        print(f"ERROR: {e}")
        sys.exit(1)
