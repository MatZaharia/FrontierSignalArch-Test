import os
from crewai import Task

def create_collector_task(agent,target_date):
    return Task(
        description=(
            f"Collect frontier research signals for {target_date} and create a raw data file, performing these steps:\n"
            "1. Fetch signals listings using the collector tools;\n"
            "2. Include sources: arXiv, bioRxiv, OpenReview, X, Reddit, and WeChat official accounts;\n"
            "3. Deduplicate results and add timestamps;\n"
            "4. Save output as a complete JSON array.\n"
        ),
        expected_output=(
            "Output JSON array with objects containing:\n"
            "{\n"
            "  \"id\": \"string\",\n"
            "  \"title\": \"string\",\n"
            "  \"url\": \"string\",\n"
            "  \"source\": \"arxiv|biorxiv|openreview|x|reddit|wechat\",\n"
            "  \"timestamp\": \"ISO-8601 datetime\",\n"
            "  \"raw_content\": \"string\"\n"
            "}\n"
        ),
        agent=agent,
        output_file=os.path.join("data", "collector", f"signals_{target_date}.json")
    )

def create_metadata_task(agent, context_task,target_date):
    return Task(
        description=(
            f"Transform raw signals for {target_date} into structured metadata, performing these steps:\n"
            "1. Read the raw JSON from Collector output;\n"
            "2. Extract and normalize fields: title, authors, abstract, published_date, institution, categories;\n"
            "3. Ensure dates use ISO‑8601 format;\n"
            "4. Save as a standardized JSON array.\n"
        ),
        expected_output=(
            "Output JSON array with objects containing:\n"
            "{\n"
            "  \"id\": \"string\",\n"
            "  \"title\": \"string\",\n"
            "  \"authors\": [\"string\", ...],\n"
            "  \"abstract\": \"string\",\n"
            "  \"published_date\": \"YYYY‑MM‑DD\",\n"
            "  \"institution\": \"string\",\n"
            "  \"categories\": [\"string\", ...]\n"
            "}\n"
        ),
        agent=agent,
        context=[context_task],
        output_file=os.path.join("data", "metadata", f"metadata_{target_date}.json")
    )

def create_documentation_task(agent, context_task,target_date):
    return Task(
        description=(
            f"Generate technical summaries for {target_date}, performing these steps:\n"
            "1. Load structured metadata from Metadata output;\n"
            "2. For each entry, draft a 200–300 word summary covering research question, methods, results, and contributions;\n"
            "3. Ensure clarity, accuracy, and coherence;\n"
            "4. Save summaries alongside original metadata entries.\n"
        ),
        expected_output=(
            "Output JSON array with objects containing all metadata fields plus:\n"
            "{\n"
            "  \"summary\": \"200–300 word technical summary\"\n"
            "}\n"
        ),
        agent=agent,
        context=[context_task],
        output_file=os.path.join("data", "documentation", f"summaries_{target_date}.json")
    )

def create_recommender_task(agent, context_task,target_date):
    return Task(
        description=(
            f"Produce Top 10 recommended signals for {target_date}, performing these steps:\n"
            "1. Read summaries from Documentation output;\n"
            "2. Score each item on innovation, impact, and relevance;\n"
            "3. Identify emergent themes;\n"
            "4. Select and rank the Top 10 items;\n"
            "5. Save the recommendation list.\n"
        ),
        expected_output=(
            "Output JSON object containing:\n"
            "{\n"
            "  \"recommendations\": [\n"
            "    {\"id\": \"string\", \"score\": float, \"rank\": int, \"theme_tags\": [\"string\", ...]},\n"
            "    ... up to 10 items ...\n"
            "  ]\n"
            "}\n"
        ),
        agent=agent,
        context=[context_task],
        output_file=os.path.join("data", "recommender", f"recommendations_{target_date}.json")
    )

def create_report_task(agent, context_task,target_date):
    return Task(
        description=(
            f"Assemble daily research report for {target_date}, performing these steps:\n"
            "1. Load Top 10 recommendations;\n"
            "2. Merge with corresponding summaries;\n"
            "3. Generate three formats: Markdown, HTML, and Feishu doc;\n"
            "4. Ensure formatting consistency and visual clarity;\n"
            "5. Save all outputs.\n"
        ),
        expected_output=(
            "Generate three files:\n"
            "- Markdown: daily_{target_date}.md\n"
            "- HTML: daily_{target_date}.html\n"
            "- Feishu Doc (Markdown format): feishu_daily_{target_date}.md\n"
            "Each file contains title, summaries, scores, and key insights.\n"
        ),
        agent=agent,
        context=[context_task],
        output_file=os.path.join("static", "reports", f"daily_{target_date}.html")
    )

def create_profile_task(agent, context_task,target_date):
    return Task(
        description=(
            f"Update user profiles based on behavior logs up to {target_date}, performing these steps:\n"
            "1. Read user events (clicks, reads, feedback);\n"
            "2. Extract interest keywords and preference tags;\n"
            "3. Update profile records with timestamp and weight vectors;\n"
            "4. Save the profiles JSON.\n"
        ),
        expected_output=(
            "Output JSON object mapping user IDs to profile data:\n"
            "{\n"
            "  \"user_123\": {\"interests\": [\"AI\", \"NLP\"], \"last_updated\": \"ISO‑8601 datetime\", \"score_weights\": {...}},\n"
            "  ...\n"
            "}\n"
        ),
        agent=agent,
        context=[context_task],
        output_file=os.path.join("data", "profiles", f"user_profiles_{target_date}.json")
    )
