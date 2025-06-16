import os
from .task import create_collector_task,create_metadata_task,create_documentation_task,create_recommender_task,create_report_task,create_profile_task
from .agents import create_collector_agent,create_metadata_agent,create_documentation_agent,create_recommender_agent,create_report_agent,create_profile_agent
from mcp.tools.collect import CollectFromArXivTool
from crewai import LLM, Crew
from dotenv import load_dotenv

def assemble_crew(target_date):
    
    # model_path='/inspire/hdd/global_user/guozihan-p-guozihan/models/Qwen2.5-7B-Instruct'
    # llm_test=LLM(
    #     model=model_path
    # )
    load_dotenv()

    # Claude3模型相关配置
    ANTHROPIC_API_BASE = os.getenv("ANTHROPIC_API_BASE")
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
    ANTHROPIC_API_MODEL = os.getenv("ANTHROPIC_API_MODEL")

    llm_test = LLM(
            base_url=ANTHROPIC_API_BASE,  # 请求的API服务地址
            api_key=ANTHROPIC_API_KEY,  # API Key
            model=ANTHROPIC_API_MODEL,
            # temperature=0.7,
            # timeout=None,# 服务请求超时
            # max_retries=2,# 失败重试最大次数
        )

    
    arxiv_tool = CollectFromArXivTool()
    
    collector_agent=create_collector_agent(llm=llm_test, tools=[arxiv_tool])
    metadata_agent=create_metadata_agent(llm=llm_test, tools=[])
    documentation_agent=create_documentation_agent(llm=llm_test, tools=[])
    recommender_agent=create_recommender_agent(llm=llm_test, tools=[])
    report_agent=create_report_agent(llm=llm_test, tools=[])
    # profile_agent=create_profile_agent(llm=llm_test, tools=[])
    
    collector_task=create_collector_task(agent=collector_agent,target_date=target_date)
    metadata_task=create_metadata_task(agent=metadata_agent,context_task=collector_task,target_date=target_date)
    documentation_task=create_documentation_task(agent=documentation_agent,context_task=metadata_task,target_date=target_date)
    recommender_task=create_recommender_task(agent=recommender_agent,context_task=documentation_task,target_date=target_date)
    report_task=create_report_task(agent=report_agent,context_task=recommender_task,target_date=target_date)
    # profile_task=create_profile_task(agent=profile_agent,context_task=report_task,target_date=target_date)
    
        
    
    return Crew(
        agents=[collector_agent, metadata_agent, documentation_agent,recommender_agent,report_agent],
        tasks=[collector_task, metadata_task, documentation_task,recommender_task,report_task],
        # agents=[collector_agent, metadata_agent, documentation_agent,recommender_agent,report_agent,profile_agent],
        # tasks=[collector_task, metadata_task, documentation_task,recommender_task,report_task,profile_task],
        verbose=True,
        process="sequential"
    )
    
    