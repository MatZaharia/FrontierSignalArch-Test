import datetime
from typing import List, Type
from pydantic import BaseModel, Field
from crewai.tools import BaseTool


class SummarizationInputSchema(BaseModel):
    metadata_entries: List[dict] = Field(..., description="结构化好的元数据列表")

class GenerateSummaryTool(BaseTool):
    name = "generate_summary"
    description = "为每条元数据生成技术摘要"
    args_schema: Type[BaseModel] = SummarizationInputSchema

    def _run(self, metadata_entries: List[dict]) -> List[dict]:
        return [
            {**entry, "summary": f"这是对《{entry['title']}》的摘要，覆盖研究问题、方法与结果。"}
            for entry in metadata_entries
        ]