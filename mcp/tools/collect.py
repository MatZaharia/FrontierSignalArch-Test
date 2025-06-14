import datetime
import arxiv
from typing import List, Type, Any
from pydantic import BaseModel, Field
from crewai.tools import BaseTool

class DateInputSchema(BaseModel):
    target_date: datetime.date = Field(..., description="Target date to fetch papers for.")

class CollectFromArXivTool(BaseTool):
    name: str = "collect_from_arxiv"
    description: str = "Collect ArXiv articles from selected categories submitted on the target date."
    args_schema: Type[BaseModel] = DateInputSchema

    def _run(self, target_date: datetime.date) -> List[dict]:
        AI_CATEGORIES = ["cs.AI"]
        client = arxiv.Client(page_size=100, delay_seconds=3)
        
        start_date = target_date.strftime('%Y%m%d%H%M')
        end_date = (target_date + datetime.timedelta(days=1)).strftime('%Y%m%d%H%M')
        
        papers = []
        for category in AI_CATEGORIES:
            search = arxiv.Search(
                query=f"cat:{category} AND submittedDate:[{start_date} TO {end_date}]",
                sort_by=arxiv.SortCriterion.SubmittedDate
            )
            
            for result in client.results(search):

                author_names = [author.name for author in result.authors]
                
                papers.append({
                    'title': result.title,
                    'authors': author_names,
                    'abstract': result.summary,
                    'url': result.entry_id,
                    'categories': result.categories
                })
        
        return papers