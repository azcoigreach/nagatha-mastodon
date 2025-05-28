from typing import Optional
from app.schemas.user_activity import UserActivityIn, UserActivityOut
from app.services.llm import classify_activity_pattern
from app.core.config import settings
import statistics
from datetime import datetime
import os

async def analyze_user_activity(data: UserActivityIn) -> UserActivityOut:
    posts = data.recent_posts
    post_count = len(posts)
    if post_count == 0:
        avg_engagement = {"favorites": 0.0, "reblogs": 0.0}
        posting_frequency = "none"
        summary = "No recent posts."
        category = None
    else:
        avg_favorites = statistics.mean([p.favorites for p in posts])
        avg_reblogs = statistics.mean([p.reblogs for p in posts])
        avg_engagement = {"favorites": avg_favorites, "reblogs": avg_reblogs}
        # Estimate posting frequency
        dates = sorted([p.created_at for p in posts], reverse=True)
        if len(dates) > 1:
            deltas = [(dates[i] - dates[i+1]).total_seconds() / 86400 for i in range(len(dates)-1)]
            avg_delta = statistics.mean(deltas)
            if avg_delta <= 1.5:
                posting_frequency = "daily"
            elif avg_delta <= 7:
                posting_frequency = "weekly"
            else:
                posting_frequency = "sporadic"
        else:
            posting_frequency = "sporadic"
        summary = f"User posts {posting_frequency} with positive engagement."
        category = None
        if os.getenv("USE_LLM_ACTIVITY", "false").lower() == "true":
            category = await classify_activity_pattern(posts)
            if category:
                category = category.lower()
    return UserActivityOut(
        post_count=post_count,
        avg_engagement=avg_engagement,
        posting_frequency=posting_frequency,
        category=category,
        summary=summary,
    ) 