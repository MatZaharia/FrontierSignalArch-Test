import datetime
from typing import List, Type
from pydantic import BaseModel, Field
from crewai.tools import BaseTool


class ProfileInputSchema(BaseModel):
    user_events: List[dict] = Field(..., description="用户行为日志，如点击/阅读/反馈")
    recommendations: dict = Field(..., description="推荐列表")

class UpdateProfileTool(BaseTool):
    name: str = "update_user_profile"
    description: str = "根据用户行为与推荐更新并保存用户画像"
    args_schema: Type[BaseModel] = ProfileInputSchema

    def _run(self, user_events: List[dict], recommendations: dict) -> dict:
        return {"user_123": {"interests": ["AI"], "last_updated": datetime.datetime.now().isoformat(), "score_weights": {}}}