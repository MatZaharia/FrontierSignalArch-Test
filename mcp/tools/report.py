import datetime
from typing import List, Type
from pydantic import BaseModel, Field
from crewai.tools import BaseTool

class ReportInputSchema(BaseModel):
    recommendations: dict = Field(..., description="推荐列表")
    summaries: List[dict] = Field(..., description="文献摘要列表")

class GenerateReportTool(BaseTool):
    name = "generate_report"
    description = "根据推荐和摘要生成 HTML/Markdown/飞书报告"
    args_schema: Type[BaseModel] = ReportInputSchema

    def _run(self, recommendations: dict, summaries: List[dict]) -> str:
        report = "<html><body><h1>研究报告</h1></body></html>"
        return report