from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class RecentPost(BaseModel):
    content: str
    created_at: datetime
    favorites: int
    reblogs: int

class UserActivityIn(BaseModel):
    username: str
    recent_posts: List[RecentPost]

class UserActivityOut(BaseModel):
    post_count: int
    avg_engagement: dict
    posting_frequency: str
    category: Optional[str] = None
    summary: str 