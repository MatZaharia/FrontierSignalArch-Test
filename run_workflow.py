import datetime
import os
from agentic_crews.arxiv_crew import assemble_crew

def run_agent_workflow(target_date: str, generate_outputs: bool = True):
    """
    执行完整的 agent 工作流（无 UI），包括研究与报告生成。
    """

    # 创建 agent 团队
    crew = assemble_crew()

    # 启动 workflow ：传入 target_date 和输出选项
    result = crew.kickoff(inputs={
        "date": target_date,
        "generate_outputs": generate_outputs
    })

    # 如果报告生成成功，重命名输出文件
    src_path = os.path.join("static", "reports", "research_report.html")
    if os.path.exists(src_path) and generate_outputs:
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        dst_path = os.path.join("static", "reports", f"research_report_{timestamp}.html")
        os.rename(src_path, dst_path)
        return {"success": True, "report_path": dst_path, "result": result}
    else:
        return {"success": False, "error": "Report not generated", "result": result}

if __name__ == "__main__":
    today = datetime.date.today().strftime("%Y-%m-%d")
    output = run_agent_workflow(today)
    if output["success"]:
        print(f"✅ Workflow finished! Report at: {output['report_path']}")
    else:
        print(f"❌ Workflow failed: {output.get('error')}")
    print("Full result:", output["result"])
    
    
# async def main():
#     async with Client("http://127.0.0.1:8001/sse") as mcp_client:
#         tools = await mcp_client.list_tools()
#         print(f"Available tools: {tools}")
#         result = await mcp_client.call_tool("collect", {"source": 'arXiv', "date": '2025-06-13'})
#         print(f"Result: {result[0].text}")

