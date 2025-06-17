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
today_date=target_date.strftime('%Y%m%d')
id=0


papers = []
for category in AI_CATEGORIES:
    id+=1
    search = arxiv.Search(
        query=f"cat:{category} AND submittedDate:[{start_date} TO {end_date}]",
        sort_by=arxiv.SortCriterion.SubmittedDate
    )
    
    for result in client.results(search):

        author_names = [author.name for author in result.authors]
        
        papers.append({
            'id': f'{today_date}-ArXiv-{id}',
            'title': result.title,
            'authors': author_names,
            'abstract': result.summary,
            'url': result.entry_id,
            'categories': result.categories,
            'timestamp': result.updated.strftime('%Y%m%d%H%M')
        })
        break
raw_signals=papers
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
    
print()