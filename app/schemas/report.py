from pydantic import BaseModel, Field, validator
from typing import Literal, Optional, List
from datetime import datetime
from app.schemas.user_activity import RecentPost

KNOWN_REASONS = ["abuse", "spam", "harassment", "impersonation", "other"]

class UserReportIn(BaseModel):
    reporter: str
    username: str
    reason: Literal["abuse", "spam", "harassment", "impersonation", "other"]
    comment: Optional[str] = None
    post_excerpt: Optional[str] = None
    created_at: datetime
    recent_posts: List[RecentPost]

class ReportTriageOut(BaseModel):
    triage_level: Literal["low", "medium", "high"]
    action: Literal["ignore", "review", "flag_immediately"]
    summary: str 