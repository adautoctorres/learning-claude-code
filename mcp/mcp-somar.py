from pathlib import Path

from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

load_dotenv(Path(__file__).parent.parent / ".env")

mcp = FastMCP("mcp-somar")

@mcp.tool()
def somar(a: int, b: int) -> int:
    return a + b

if __name__ == "__main__":
    mcp.run()