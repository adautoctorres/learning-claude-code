from pathlib import Path

from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

load_dotenv(Path(__file__).parent.parent / ".env")

mcp = FastMCP("mcp-mensagem")

@mcp.tool()
def enviar_mensagem(mensagem: str) -> str:
    return f"Mensagem enviada: {mensagem}"

if __name__ == "__main__":
    mcp.run()