from pydantic import BaseModel
from typing import List, Optional

class NotionHelpSection(BaseModel):
    title: str
    subtitle: Optional[str] = None
    items: List[dict] = []

class NotionHelpArticle(BaseModel):
    title: str
    breadcrumbs: List[dict]
    content: str
    video_url: Optional[str] = None
    next_article: Optional[dict] = None