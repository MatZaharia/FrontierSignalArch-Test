
async def main():
    async with Client("http://127.0.0.1:8001/sse") as mcp_client:
        tools = await mcp_client.list_tools()
        print(f"Available tools: {tools}")
        result = await mcp_client.call_tool("collect", {"source": 'arXiv', "date": '2025-06-13'})
        print(f"Result: {result[0].text}")