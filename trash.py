import datetime
import arxiv
from typing import List, Type, Any
from pydantic import BaseModel, Field
from crewai.tools import BaseTool 

target_date=datetime.date(year=2025,month=6,day=13)
AI_CATEGORIES = ["cs.AI"]  # Add both categories
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
        # Properly extract author names
        author_names = [author.name for author in result.authors]
        
        papers.append({
            'title': result.title,
            'authors': author_names,  # Store as a proper list
            'summary': result.summary,
            'url': result.entry_id,
            'categories': result.categories
        })
print(papers)