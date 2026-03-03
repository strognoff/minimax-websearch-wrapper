#!/usr/bin/env python3
"""
MiniMax Coding Plan MCP wrapper.

Tools:
- web_search(query)
- understand_image(prompt, image_source)

Usage:
  python minimax_mcp_web_search.py web_search "your query"
  python minimax_mcp_web_search.py understand_image "your prompt" "image_source"

Env required:
  MINIMAX_API_KEY
Optional:
  MINIMAX_API_HOST (default: https://api.minimax.io)
"""

import asyncio
import json
import os
import sys
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

DEFAULT_HOST = "https://api.minimax.io"
SUPPORTED_EXT = {".jpg", ".jpeg", ".png", ".webp"}


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


def strip_at_prefix(p: str) -> str:
    # "@/abs/path" -> "/abs/path", "@rel/path" -> "rel/path"
    return p[1:] if p.startswith("@") else p


def validate_image_source(image_source: str) -> str:
    image_source = strip_at_prefix(image_source.strip())

    parsed = urlparse(image_source)
    if parsed.scheme in {"http", "https"}:
        path = parsed.path.lower()
        ext = Path(path).suffix
        if ext and ext not in SUPPORTED_EXT:
            raise ValueError(
                f"Unsupported image format in URL: {ext}. Supported: JPEG, PNG, WebP"
            )
        return image_source

    p = Path(image_source)
    ext = p.suffix.lower()
    if ext not in SUPPORTED_EXT:
        raise ValueError(
            f"Unsupported image format: {ext or 'none'}. Supported: JPEG, PNG, WebP"
        )
    return image_source


async def call_tool(tool_name: str, args: dict):
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
            result = await session.call_tool(tool_name, args)
            print(json.dumps(normalize_result(result.content), ensure_ascii=False, indent=2))


def usage():
    print(
        "Usage:\n"
        "  python minimax_mcp_web_search.py web_search \"query\"\n"
        "  python minimax_mcp_web_search.py understand_image \"prompt\" \"image_source\""
    )


if __name__ == "__main__":
    if len(sys.argv) < 3:
        usage()
        sys.exit(2)

    cmd = sys.argv[1].strip()

    try:
        if cmd == "web_search":
            query = " ".join(sys.argv[2:]).strip()
            if not query:
                raise ValueError("query is required")
            asyncio.run(call_tool("web_search", {"query": query}))

        elif cmd == "understand_image":
            if len(sys.argv) < 4:
                usage()
                sys.exit(2)
            prompt = sys.argv[2].strip()
            image_source = validate_image_source(sys.argv[3])
            asyncio.run(
                call_tool(
                    "understand_image",
                    {"prompt": prompt, "image_source": image_source},
                )
            )
        else:
            raise ValueError(f"Unknown command: {cmd}")

    except Exception as e:
        print(f"ERROR: {e}")
        sys.exit(1)
