import datetime
from typing import List, Type
from pydantic import BaseModel, Field
from crewai.tools import BaseTool

class MetadataInputSchema(BaseModel):
    raw_signals: List[dict] = Field(..., description="Collector 输出的原始信号列表（每项为 dict）")

class ExtractMetadataTool(BaseTool):
    name = "extract_metadata"
    description = "从原始信号中提取并规范化元数据字段"
    args_schema: Type[BaseModel] = MetadataInputSchema

    def _run(self, raw_signals: List[dict]) -> List[dict]:
        results = []
        for s in raw_signals:
            results.append({
                "id": s.get("id"),
                "title": s.get("title"),
                "authors": s.get("authors", []),
                "abstract": s.get("abstract") or s.get("raw_content",""),
                "published_date": s.get("timestamp", "")[:10],
                "institution": s.get("institution", "unknown"),
                "categories": s.get("categories", [])
            })
        return results
