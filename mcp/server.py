from fastmcp import FastMCP

mcp = FastMCP(name="TestMCPServer")

@mcp.tool()
def collect(source,date):
    return

if __name__ == "__main__":
    mcp.run(transport='sse', host="127.0.0.1", port=8001)