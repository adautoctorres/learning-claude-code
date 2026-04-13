from mcp.server.fastmcp import FastMCP

mcp = FastMCP("mcp-somar")

@mcp.tool()
def somar(a: int, b: int) -> int:
    return a + b

if __name__ == "__main__":
    mcp.run()