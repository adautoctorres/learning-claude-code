from mcp.server.fastmcp import FastMCP

mcp = FastMCP("mcp-mensagem")

@mcp.tool()
def enviar_mensagem(mensagem: str) -> str:
    return f"Mensagem enviada: {mensagem}"

if __name__ == "__main__":
    mcp.run()