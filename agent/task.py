import datetime
import os
from crewai import Task
from dotenv import load_dotenv



# ---------------------------------In Chinese---------------------------------

def create_collector_task(agent, target_date):
    load_dotenv()
    SAVE_OUTPUT_DIR=os.getenv("SAVE_OUTPUT_DIR")
    SAVE_OUTPUT_SUFFIX=os.getenv("SAVE_OUTPUT_SUFFIX")
    if SAVE_OUTPUT_DIR is None:
        raise ValueError("SAVE_OUTPUT_DIR is not set")
    return Task(
        description=(
            f"收集{target_date}内各指定信号源的前沿科研信号并生成原始数据文件，步骤如下：\n"
            "1. 使用抓取工具拉取信号列表，列表要尽可能长而不去裁剪；\n"
            "2. 包括来源：arXiv；\n"
            "3. 记录所有获取到的前沿信号，不要基于思考分析而删去其中的内容；\n"
            "4. 将输出保存为完整的JSON数组。\n"
        ),
        expected_output=(
            "输出一个JSON数组，每个对象包含：\n"
            "{\n"
            "  \"id\": \"string\",\n"
            "  \"title\": \"string\",\n"
            "  \"url\": \"string\",\n"
            "  \"source\": \"arxiv|biorxiv|openreview|x|reddit|wechat\",\n"
            "  \"timestamp\": \"ISO-8601 datetime\",\n"
            "}\n"
        ),
        agent=agent,
        output_file=os.path.join(SAVE_OUTPUT_DIR, "collector", f"signals_{target_date}_in_{SAVE_OUTPUT_SUFFIX}.json")
    )

def create_metadata_task(agent, context_task, target_date):
    load_dotenv()
    SAVE_OUTPUT_DIR=os.getenv("SAVE_OUTPUT_DIR")
    SAVE_OUTPUT_SUFFIX=os.getenv("SAVE_OUTPUT_SUFFIX")
    return Task(
        description=(
            f"将{target_date}的原始信号转换为结构化元数据，步骤如下：\n"
            "1. 读取Collector Agent的JSON输出；\n"
            "2. 基于其中的url读取信号来源；\n"
            "3. 提取并规范化字段：title、authors、abstract、published_date、categories、url；\n"
            "4. 对结果去重，并确保日期字段采用ISO‑8601格式；\n"
            "5. 将结果保存为标准化的JSON数组。\n"
        ),
        expected_output=(
            "输出一个JSON数组，每个对象包含：\n"
            "{\n"
            "  \"id\": \"string\",\n"
            "  \"title\": \"string\",\n"
            "  \"authors\": [\"string\", ...],\n"
            "  \"abstract\": \"string\",\n"
            "  \"published_date\": \"YYYY‑MM‑DD\",\n"
            "  \"url\": \"string\",\n"
            "  \"categories\": [\"string\", ...]\n"
            "}\n"
        ),
        agent=agent,
        context=[context_task],
        output_file=os.path.join(SAVE_OUTPUT_DIR, "metadata", f"metadata_{target_date}_in_{SAVE_OUTPUT_SUFFIX}.json")
    )

def create_documentation_task(agent, context_task, target_date):
    load_dotenv()
    SAVE_OUTPUT_DIR=os.getenv("SAVE_OUTPUT_DIR")
    SAVE_OUTPUT_SUFFIX=os.getenv("SAVE_OUTPUT_SUFFIX")
    return Task(
        description=(
            f"为{target_date}的元数据生成前沿信号解读，步骤如下：\n"
            "1. 加载Metadata Agent整理的结构化输出，并按需读取其中url对应的源文件；\n"
            "2. 对每条记录撰写200–400字的解读，涵盖研究问题、方法、结果与贡献等；\n"
            "3. 确保摘要内容清晰、准确且连贯；\n"
            "4. 将摘要与原元数据一起保存。\n"
        ),
        expected_output=(
            "输出一个JSON数组，每个对象包含原有元数据字段并新增：\n"
            "{\n"
            "  \"summary\": \"200–400字的前沿信号解读\"\n"
            "}\n"
        ),
        agent=agent,
        context=[context_task],
        output_file=os.path.join(SAVE_OUTPUT_DIR, "documentation", f"summaries_{target_date}_in_{SAVE_OUTPUT_SUFFIX}.json")
    )

def create_recommender_task(agent, context_task, target_date):
    load_dotenv()
    SAVE_OUTPUT_DIR=os.getenv("SAVE_OUTPUT_DIR")
    SAVE_OUTPUT_SUFFIX=os.getenv("SAVE_OUTPUT_SUFFIX")
    return Task(
        description=(
            f"生成{target_date}的Top 10前沿信号推荐，步骤如下：\n"
            "1. 读取Documentation Agent的技术解读；\n"
            "2. 按创新度、影响力和相关性对每项进行评分；\n"
            "3. 识别Emergent Themes；\n"
            "4. 选出并排序前10名；\n"
            "5. 保存推荐列表。\n"
        ),
        expected_output=(
            "输出一个JSON对象，包含：\n"
            "{\n"
            "  \"recommendations\": [\n"
            "    {\n"
            "    \"id\": \"string\",\n"
            "    \"score\": \"float\",\n"
            "    \"rank\": \"int\",\n"
            "    \"title\": \"string\",\n"
            "    \"theme_tags\": [\"字符串\", ...]\n"
            # "    \"summary\": \"200–400字的前沿信号解读\"\n"
            # "    \"authors\": [\"string\", ...],\n"
            # "    \"abstract\": \"string\",\n"
            # "    \"published_date\": \"YYYY‑MM‑DD\",\n"
            # "    \"url\": \"string\",\n"
            # "    \"categories\": [\"string\", ...]\n"
            "    },\n"
            "    …共 10 条…\n"
            "  ]\n"
            "}\n"
        ),
        agent=agent,
        context=[context_task],
        output_file=os.path.join(SAVE_OUTPUT_DIR, "recommender", f"recommendations_{target_date}_in_{SAVE_OUTPUT_SUFFIX}.json")
    )

def create_report_task(agent, context_task, target_date):
    load_dotenv()
    SAVE_OUTPUT_DIR=os.getenv("SAVE_OUTPUT_DIR")
    SAVE_OUTPUT_SUFFIX=os.getenv("SAVE_OUTPUT_SUFFIX")
    return Task(
        description=(
            f"为{target_date}汇总生成日报报告，步骤如下：\n"
            "1. 加载Recommender Agent的Top 10推荐列表；\n"
            "2. 提取对应元数据；\n"
            # "3. 生成三种格式：Markdown、HTML、飞书文档；\n"
            "3. 生成一种格式：Markdown；\n"
            "4. 确保格式一致且视觉清晰；\n"
            "5. 保存所有输出。\n"
        ),
        expected_output=(
            "生成以下文件：\n"
            "- Markdown: daily_{target_date}.md\n"
            # "- HTML: daily_{target_date}.html\n"
            # "- 飞书文档（Markdown 格式）: feishu_daily_{target_date}.md\n"
            "每个文件包含标题、摘要、评分和关键洞见。\n"
        ),
        agent=agent,
        context=[context_task],
        output_file=os.path.join(SAVE_OUTPUT_DIR, "reports", f"daily_{target_date}_in_{SAVE_OUTPUT_SUFFIX}.md")
    )

def create_profile_task(agent, context_task, target_date):
    load_dotenv()
    SAVE_OUTPUT_DIR=os.getenv("SAVE_OUTPUT_DIR")
    SAVE_OUTPUT_SUFFIX=os.getenv("SAVE_OUTPUT_SUFFIX")
    return Task(
        description=(
            f"根据至{target_date}的用户行为日志更新用户画像，步骤如下：\n"
            "1. 读取日志中的用户事件（点击、阅读、反馈）；\n"
            "2. 提取兴趣关键词和偏好标签；\n"
            "3. 更新画像记录并添加时间戳及权重向量；\n"
            "4. 保存用户画像 JSON。\n"
        ),
        expected_output=(
            "输出一个 JSON 对象，映射用户 ID 到画像数据：\n"
            "{\n"
            "  \"user_id\": {\"interests\": [...], \"last_updated\": \"ISO‑8601 日期时间\", \"score_weights\": {...}},\n"
            "  …\n"
            "}\n"
        ),
        agent=agent,
        context=[context_task],
        output_file=os.path.join(SAVE_OUTPUT_DIR, "profiles", f"user_profiles_{target_date}_in_{SAVE_OUTPUT_SUFFIX}.json")
    )


# ---------------------------------In English---------------------------------
# def create_collector_task(agent,target_date):
#     return Task(
#         description=(
#             f"Collect frontier research signals for {target_date} and create a raw data file, performing these steps:\n"
#             "1. Fetch signals listings using the collector tools;\n"
#             # "2. Include sources: arXiv, bioRxiv, OpenReview, X, Reddit, and WeChat official accounts;\n"
#             "2. Include sources: arXiv;\n"
#             "3. Deduplicate results and add timestamps;\n"
#             "4. Save output as a complete JSON array.\n"
#         ),
#         expected_output=(
#             "Output JSON array with objects containing:\n"
#             "{\n"
#             "  \"id\": \"string\",\n"
#             "  \"title\": \"string\",\n"
#             "  \"url\": \"string\",\n"
#             "  \"source\": \"arxiv|biorxiv|openreview|x|reddit|wechat\",\n"
#             "  \"timestamp\": \"ISO-8601 datetime\",\n"
#             "  \"raw_content\": \"string\"\n"
#             "}\n"
#         ),
#         agent=agent,
#         output_file=os.path.join(SAVE_OUTPUT_DIR, "collector", f"signals_{target_date}.json")
#     )

# def create_metadata_task(agent, context_task,target_date):
#     return Task(
#         description=(
#             f"Transform raw signals for {target_date} into structured metadata, performing these steps:\n"
#             "1. Read the raw JSON from Collector output;\n"
#             "2. Extract and normalize fields: title, authors, abstract, published_date, institution, categories;\n"
#             "3. Ensure dates use ISO‑8601 format;\n"
#             "4. Save as a standardized JSON array.\n"
#         ),
#         expected_output=(
#             "Output JSON array with objects containing:\n"
#             "{\n"
#             "  \"id\": \"string\",\n"
#             "  \"title\": \"string\",\n"
#             "  \"authors\": [\"string\", ...],\n"
#             "  \"abstract\": \"string\",\n"
#             "  \"published_date\": \"YYYY‑MM‑DD\",\n"
#             "  \"institution\": \"string\",\n"
#             "  \"categories\": [\"string\", ...]\n"
#             "}\n"
#         ),
#         agent=agent,
#         context=[context_task],
#         output_file=os.path.join(SAVE_OUTPUT_DIR, "metadata", f"metadata_{target_date}.json")
#     )

# def create_documentation_task(agent, context_task,target_date):
#     return Task(
#         description=(
#             f"Generate technical summaries for {target_date}, performing these steps:\n"
#             "1. Load structured metadata from Metadata output;\n"
#             "2. For each entry, draft a 200–300 word summary covering research question, methods, results, and contributions;\n"
#             "3. Ensure clarity, accuracy, and coherence;\n"
#             "4. Save summaries alongside original metadata entries.\n"
#         ),
#         expected_output=(
#             "Output JSON array with objects containing all metadata fields plus:\n"
#             "{\n"
#             "  \"summary\": \"200–300 word technical summary\"\n"
#             "}\n"
#         ),
#         agent=agent,
#         context=[context_task],
#         output_file=os.path.join(SAVE_OUTPUT_DIR, "documentation", f"summaries_{target_date}.json")
#     )

# def create_recommender_task(agent, context_task,target_date):
#     return Task(
#         description=(
#             f"Produce Top 10 recommended signals for {target_date}, performing these steps:\n"
#             "1. Read summaries from Documentation output;\n"
#             "2. Score each item on innovation, impact, and relevance;\n"
#             "3. Identify emergent themes;\n"
#             "4. Select and rank the Top 10 items;\n"
#             "5. Save the recommendation list.\n"
#         ),
#         expected_output=(
#             "Output JSON object containing:\n"
#             "{\n"
#             "  \"recommendations\": [\n"
#             "    {\"id\": \"string\", \"score\": float, \"rank\": int, \"theme_tags\": [\"string\", ...]},\n"
#             "    ... up to 10 items ...\n"
#             "  ]\n"
#             "}\n"
#         ),
#         agent=agent,
#         context=[context_task],
#         output_file=os.path.join(SAVE_OUTPUT_DIR, "recommender", f"recommendations_{target_date}.json")
#     )

# def create_report_task(agent, context_task,target_date):
#     return Task(
#         description=(
#             f"Assemble daily research report for {target_date}, performing these steps:\n"
#             "1. Load Top 10 recommendations;\n"
#             "2. Merge with corresponding summaries;\n"
#             "3. Generate three formats: Markdown, HTML, and Feishu doc;\n"
#             "4. Ensure formatting consistency and visual clarity;\n"
#             "5. Save all outputs.\n"
#         ),
#         expected_output=(
#             "Generate three files:\n"
#             "- Markdown: daily_{target_date}.md\n"
#             "- HTML: daily_{target_date}.html\n"
#             "- Feishu Doc (Markdown format): feishu_daily_{target_date}.md\n"
#             "Each file contains title, summaries, scores, and key insights.\n"
#         ),
#         agent=agent,
#         context=[context_task],
#         output_file=os.path.join(SAVE_OUTPUT_DIR, "reports", f"daily_{target_date}.html")
#     )

# def create_profile_task(agent, context_task,target_date):
#     return Task(
#         description=(
#             f"Update user profiles based on behavior logs up to {target_date}, performing these steps:\n"
#             "1. Read user events (clicks, reads, feedback);\n"
#             "2. Extract interest keywords and preference tags;\n"
#             "3. Update profile records with timestamp and weight vectors;\n"
#             "4. Save the profiles JSON.\n"
#         ),
#         expected_output=(
#             "Output JSON object mapping user IDs to profile data:\n"
#             "{\n"
#             "  \"user_123\": {\"interests\": [\"AI\", \"NLP\"], \"last_updated\": \"ISO‑8601 datetime\", \"score_weights\": {...}},\n"
#             "  ...\n"
#             "}\n"
#         ),
#         agent=agent,
#         context=[context_task],
#         output_file=os.path.join(SAVE_OUTPUT_DIR, "profiles", f"user_profiles_{target_date}.json")
#     )
