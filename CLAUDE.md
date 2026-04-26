# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Install dependency
pip install mcp

# Run server (stdio transport — for use with MCP clients)
python app.py

# Configure kiro-cli path via env (default: /root/.local/bin/kiro-cli)
KIRO_CLI_PATH=/path/to/kiro-cli python app.py
```

## MCP Client Config

Add to `~/.claude/claude_desktop_config.json` or equivalent:

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

## Architecture

Single file (`app.py`) — minimal MCP server exposing one tool.

**Tool:** `ask_kiro(question: str) -> str`
- Invokes `kiro-cli` via bash heredoc (`subprocess.run`, timeout 300s)
- Returns stdout as markdown string
- Raises `RuntimeError` with stderr on non-zero exit

**Config** (env or `.env` file):
| Var | Default |
|-----|---------|
| `KIRO_CLI_PATH` | `/root/.local/bin/kiro-cli` |

Transport: stdio (MCP default). Stateless — no DB, no session state.
