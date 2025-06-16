import datetime
from typing import List, Type
from pydantic import BaseModel, Field
from crewai.tools import BaseTool

class RecommendationInputSchema(BaseModel):
    summaries: List[dict] = Field(..., description="带 summary 的文献列表")

class ScoreAndRecommendTool(BaseTool):
    name = "score_and_recommend"
    description = "对文献进行评分并生成 Top10 推荐列表"
    args_schema: Type[BaseModel] = RecommendationInputSchema

    def _run(self, summaries: List[dict]) -> dict:
        scored = [
            {"id": e["id"], "score": 10.0, "rank": idx+1, "theme_tags": ["AI"]}
            for idx, e in enumerate(summaries[:10])
        ]
        return {"recommendations": scored}