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

mcp = FastMCP("kiro-mcp")

@mcp.tool()
def ask_kiro(question: str) -> str:
    """Ask a technical/IT question to Kiro. Returns a markdown-formatted answer."""
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

if __name__ == '__main__':
    mcp.run()
