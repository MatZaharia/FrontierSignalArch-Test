import datetime
from typing import List, Type
from pydantic import BaseModel, Field
from crewai.tools import BaseTool

class MetadataInputSchema(BaseModel):
    raw_signals: List[List[dict]] = Field(..., description="Collector输出的原始信号列表（列表中包含多个来源的列表，子列表每项为dict）")

class ExtractMetadataTool(BaseTool):
    name: str = "extract_metadata"
    description: str = "从原始信号中提取并规范化元数据字段"
    args_schema: Type[BaseModel] = MetadataInputSchema

    def _run(self, raw_signals: List[List[dict]]) -> List[dict]:
        results = []
        for s in raw_signals:
            results.append({
                "id": s.get("id"),
                "title": s.get("title"),
                "authors": s.get("authors", []),
                "abstract": s.get("abstract") or s.get("raw_content",""),
                "timestamp": s.get("timestamp", ""),
                "categories": s.get("categories", []),
                "url": s.get("url", []),
            })
        return results
