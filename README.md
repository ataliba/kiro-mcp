# kiro-mcp

MCP server that exposes [Kiro CLI](https://kiro.dev) as tools inside any MCP-compatible client (Claude Desktop, Claude Code, etc.).

---

## Tools

| Tool | Description |
|------|-------------|
| `ask_kiro` | Ask any technical question to Kiro. Returns a structured markdown answer. |
| `get_kiro_quota` | Check current quota: % used, overages status, and reset date. |

---

## Requirements

- Python 3.10+
- [`kiro-cli`](https://kiro.dev) installed and authenticated
- `mcp` Python package

```bash
pip install mcp
```

---

## Setup

### 1. Clone & install

```bash
git clone https://github.com/your-user/kiro-mcp.git
cd kiro-mcp
pip install -r requirements.txt
```

### 2. Configure kiro-cli path (optional)

By default, the server expects `kiro-cli` at `/root/.local/bin/kiro-cli`.

Override via environment variable or `.env` file:

```bash
# .env
KIRO_CLI_PATH=/usr/local/bin/kiro-cli
```

### 3. Add to your MCP client

**Claude Desktop** (`~/.claude/claude_desktop_config.json`) or equivalent:

```json
{
  "mcpServers": {
    "kiro": {
      "command": "python",
      "args": ["/absolute/path/to/kiro-mcp/app.py"]
    }
  }
}
```

**Claude Code** (`.claude/settings.json`):

```json
{
  "mcpServers": {
    "kiro": {
      "command": "python",
      "args": ["/absolute/path/to/kiro-mcp/app.py"],
      "type": "stdio"
    }
  }
}
```

---

## Running directly

```bash
python app.py
```

Transport is `stdio` (MCP default). Stateless — no DB, no session.

---

## How it works

```
MCP Client
    │
    ▼
ask_kiro(question)
    │
    ├─ check quota via `kiro-cli chat "/usage"`
    │      └─ quota exhausted? → raise RuntimeError
    │
    └─ pipe question to `kiro-cli` via bash heredoc
           └─ return stdout as markdown string
```

Quota check happens **before** every `ask_kiro` call to avoid burning paid overage tokens silently.

---

## Environment variables

| Variable | Default | Description |
|----------|---------|-------------|
| `KIRO_CLI_PATH` | `/root/.local/bin/kiro-cli` | Path to the `kiro-cli` binary |

---

## License

MIT
