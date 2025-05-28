from pydantic import BaseModel, Field
from datetime import datetime

class UserProfileIn(BaseModel):
    username: str
    bio: str
    follower_count: int
    following_count: int
    statuses_count: int
    created_at: datetime

class UserEvaluationOut(BaseModel):
    risk_score: float = Field(..., ge=0.0, le=1.0)
    recommendation: str
    summary: str