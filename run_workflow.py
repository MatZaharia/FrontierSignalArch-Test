import datetime
import os
from agent.crew import assemble_crew

os.environ["ANTHROPIC_API_BASE"] = "https://api.suanli.cn/v1"
os.environ["ANTHROPIC_API_KEY"] = "sk-GeCg52OjFA4zM68PYwtr7YVq8EMCzjmPLmyrdoeQk67oECpQ"
os.environ["ANTHROPIC_API_MODEL"] = "openai/free:Qwen3-30B-A3B"
# os.environ["ANTHROPIC_API_MODEL"] = "openai/Qwen3-32B"
# os.environ["ANTHROPIC_API_MODEL"] = "openai/deepseek-r1:7b"
# os.environ["ANTHROPIC_API_MODEL"] = "openai/QWQ-32B"
# os.environ["ANTHROPIC_API_MODEL"] = "openai/free:QwQ-32B"

os.environ["SAVE_OUTPUT_DIR"]="codes/FrontierSignalArch-Test/FrontierSignalArch-Test/outputs" 
os.environ["SAVE_OUTPUT_SUFFIX"]=datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')


def run_agent_workflow(target_date: str, generate_outputs: bool = True):
    
    SAVE_OUTPUT_DIR=os.getenv("SAVE_OUTPUT_DIR")
    SAVE_OUTPUT_SUFFIX=os.getenv("SAVE_OUTPUT_SUFFIX")
    
    # 创建 agent 团队
    crew = assemble_crew(target_date)

    # 启动 workflow ：传入 target_date 和输出选项
    result = crew.kickoff(inputs={
        "target_date": target_date,
        # "generate_outputs": generate_outputs
    })
    # return {"success": True, "result": result}

    # # 如果报告生成成功，重命名输出文件
    src_path = os.path.join(SAVE_OUTPUT_DIR, "reports", "daily_{timestamp}_in_{SAVE_OUTPUT_SUFFIX}.md")
    if os.path.exists(src_path) and generate_outputs:
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        dst_path = os.path.join(SAVE_OUTPUT_DIR, "reports", f"daily_{timestamp}_in_{SAVE_OUTPUT_SUFFIX}.md")
        os.rename(src_path, dst_path)
        return {"success": True, "report_path": dst_path, "result": result}
    else:
        return {"success": False, "error": "Report not generated", "result": result}

if __name__ == "__main__":
    # today = datetime.date.today().strftime("%Y-%m-%d")
    today = datetime.datetime(2025,6,13).strftime("%Y-%m-%d")
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

