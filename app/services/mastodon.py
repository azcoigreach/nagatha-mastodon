import logging
from typing import List
from datetime import datetime
from fastapi import HTTPException
from concurrent.futures import ThreadPoolExecutor
import asyncio
import httpx

from app.core.mastodon_client import get_mastodon_client
from app.schemas.user_eval import UserProfileIn
from app.schemas.user_activity import RecentPost
from app.utils.mastodon import extract_local_username, get_local_server_domain
from app.core.config import settings

_executor = ThreadPoolExecutor(max_workers=4)

def _run_in_executor(func, *args, **kwargs):
    loop = asyncio.get_event_loop()
    return loop.run_in_executor(_executor, lambda: func(*args, **kwargs))

def parse_datetime(dt):
    if isinstance(dt, datetime):
        return dt
    if isinstance(dt, str):
        # Remove 'Z' if present, since fromisoformat doesn't accept it
        return datetime.fromisoformat(dt.replace('Z', '+00:00'))
    return None

async def get_user_profile(username: str) -> UserProfileIn:
    mastodon = get_mastodon_client()
    local_username = extract_local_username(username)
    domain = get_local_server_domain()
    acct = f"@{local_username}@{domain}" if "@" in username else f"@{local_username}@{domain}"
    try:
        user = await _run_in_executor(mastodon.account_search, acct, 1)
        if not user:
            raise RuntimeError("User not found")
        user = user[0]
        return UserProfileIn(
            username=user.get("acct"),
            bio=user.get("note", ""),
            follower_count=user.get("followers_count", 0),
            following_count=user.get("following_count", 0),
            statuses_count=user.get("statuses_count", 0),
            created_at=parse_datetime(user.get("created_at")),
        )
    except Exception as e:
        logging.error(f"Mastodon user profile error: {e}")
        raise RuntimeError("Error fetching user profile")

async def get_recent_posts(username: str, limit: int = 5) -> List[RecentPost]:
    mastodon = get_mastodon_client()
    local_username = extract_local_username(username)
    domain = get_local_server_domain()
    acct = f"@{local_username}@{domain}" if "@" in username else f"@{local_username}@{domain}"
    try:
        user = await _run_in_executor(mastodon.account_search, acct, 1)
        if not user:
            raise RuntimeError("User not found")
        user_id = user[0]["id"]
        statuses = await _run_in_executor(mastodon.account_statuses, user_id, limit=limit)
        posts = []
        for s in statuses:
            posts.append(RecentPost(
                content=s.get("content", ""),
                created_at=parse_datetime(s.get("created_at")),
                favorites=s.get("favourites_count", 0),
                reblogs=s.get("reblogs_count", 0),
            ))
        return posts
    except Exception as e:
        logging.error(f"Mastodon recent posts error: {e}")
        raise RuntimeError("Error fetching recent posts") 