import re
import subprocess
import os
from mcp.server.fastmcp import FastMCP

if os.path.exists('.env'):
    with open('.env', 'r') as f:
        for line in f:
            if line.strip() and not line.startswith('#'):
                key, value = line.strip().split('=', 1)
                os.environ[key] = value

KIRO_CLI_PATH = os.getenv('KIRO_CLI_PATH', '/root/.local/bin/kiro-cli')
TRANSPORT = os.getenv('TRANSPORT', 'stdio')
HOST = os.getenv('HOST', '0.0.0.0')
PORT = int(os.getenv('PORT', '8000'))

mcp = FastMCP("kiro-mcp")

_ANSI = re.compile(r'\x1b\[[0-9;]*[a-zA-Z]')


def _strip_ansi(text: str) -> str:
    return _ANSI.sub('', text)


def _get_usage() -> dict:
    """Returns {'pct': int, 'overages': bool, 'resets_on': str}. Raises on failure."""
    bash_command = f"""{KIRO_CLI_PATH} chat "/usage" """

    result = subprocess.run(
        ['/usr/bin/bash', '-c', bash_command],
        capture_output=True,
        text=True,
        timeout=30
    )

    output = _strip_ansi(result.stdout + result.stderr)

    pct_match = re.search(r'(\d+)%', output)
    pct = int(pct_match.group(1)) if pct_match else 0

    overages = 'Overages: Disabled' not in output

    reset_match = re.search(r'resets on (\S+)', output)
    resets_on = reset_match.group(1) if reset_match else 'unknown'

    return {'pct': pct, 'overages': overages, 'resets_on': resets_on}


@mcp.tool()
def ask_kiro(question: str) -> str:
    """Ask a technical/IT question to Kiro. Returns a markdown-formatted answer."""
    usage = _get_usage()
    if usage['pct'] >= 100 and not usage['overages']:
        raise RuntimeError(
            f"Kiro quota exhausted ({usage['pct']}% used, overages disabled). "
            f"Resets on {usage['resets_on']}."
        )

    bash_command = f"""{KIRO_CLI_PATH} << 'EOF'
Responda em formato markdown estruturado com títulos, seções e exemplos de código.

{question}
EOF"""

    result = subprocess.run(
        ['/usr/bin/bash', '-c', bash_command],
        capture_output=True,
        text=True,
        timeout=300
    )

    if result.returncode == 0:
        return result.stdout.strip()

    raise RuntimeError(result.stderr.strip())


@mcp.tool()
def get_kiro_quota() -> dict:
    """Check current Kiro quota usage. Returns pct used, overages status, and reset date."""
    return _get_usage()


if __name__ == '__main__':
    if TRANSPORT == 'sse':
        mcp.run(transport='sse', host=HOST, port=PORT)
    else:
        mcp.run()
