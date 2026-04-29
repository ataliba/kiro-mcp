# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run server — local stdio (default)
python app.py

# Run server — remote SSE (HTTP)
TRANSPORT=sse python app.py
TRANSPORT=sse HOST=0.0.0.0 PORT=8000 python app.py

# Configure kiro-cli path via env (default: /root/.local/bin/kiro-cli)
KIRO_CLI_PATH=/path/to/kiro-cli python app.py
```

## MCP Client Config

### Local (stdio)

```json
{
  "mcpServers": {
    "kiro": {
      "command": "python",
      "args": ["/home/ataliba/Developing/kiro-mcp/app.py"]
    }
  }
}
```

### Remote (SSE)

```json
{
  "mcpServers": {
    "kiro": {
      "type": "sse",
      "url": "http://<server-ip>:8000/sse"
    }
  }
}
```

## Architecture

Single file (`app.py`) — minimal MCP server exposing two tools.

**Tools:**

| Tool | Signature | Description |
|------|-----------|-------------|
| `ask_kiro` | `(question: str) -> str` | Ask Kiro a question. Checks quota first, then pipes via heredoc. Returns markdown. |
| `get_kiro_quota` | `() -> dict` | Returns `{pct, overages, resets_on}` from `kiro-cli chat "/usage"`. |

**Quota guard:** `ask_kiro` calls `_get_usage()` before every invocation. Raises `RuntimeError` if `pct >= 100` and overages are disabled.

**ANSI stripping:** `kiro-cli` output contains ANSI escape codes — stripped via regex before parsing.

**Config** (env or `.env` file):

| Var | Default | Description |
|-----|---------|-------------|
| `KIRO_CLI_PATH` | `/root/.local/bin/kiro-cli` | Path to kiro-cli binary |
| `TRANSPORT` | `stdio` | `stdio` or `sse` |
| `HOST` | `0.0.0.0` | Bind host (SSE only) |
| `PORT` | `8000` | Bind port (SSE only) |

Transport: `stdio` by default. Set `TRANSPORT=sse` for remote HTTP access via uvicorn. Stateless — no DB, no session state.
