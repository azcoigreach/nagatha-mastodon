from fastapi import APIRouter, HTTPException
from app.schemas.user_eval import UserProfileIn, UserEvaluationOut
from app.services.llm import evaluate_user_profile
from app.schemas.user_activity import UserActivityIn, UserActivityOut, RecentPost
from app.services.activity import analyze_user_activity
from app.services import mastodon as mastodon_service
from typing import List
from app.schemas.user_common import UserIdentifierIn
import logging
from app.utils.mastodon import normalize_mastodon_username

router = APIRouter()

@router.post(
    "/evaluate",
    response_model=UserEvaluationOut,
    summary="Evaluate user profile",
    tags=["users"],
)
async def evaluate_user(user: UserProfileIn) -> UserEvaluationOut:
    return await evaluate_user_profile(user)

@router.post(
    "/evaluate/auto",
    response_model=UserEvaluationOut,
    summary="Evaluate user profile (auto-fetch from Mastodon)",
    tags=["users"],
)
async def evaluate_user_auto(data: UserIdentifierIn) -> UserEvaluationOut:
    normalized_username = normalize_mastodon_username(data.username)
    try:
        profile = await mastodon_service.get_user_profile(normalized_username)
        logging.info(f"Fetched Mastodon profile for {normalized_username}: success")
    except HTTPException as e:
        logging.warning(f"Failed to fetch Mastodon profile for {normalized_username}: {e.detail}")
        raise HTTPException(status_code=422, detail=f"Mastodon user not found: {normalized_username}")
    return await evaluate_user_profile(profile)

@router.post(
    "/activity",
    response_model=UserActivityOut,
    summary="Summarize user activity",
    tags=["users"],
)
async def user_activity_summary(data: UserActivityIn) -> UserActivityOut:
    return await analyze_user_activity(data)

@router.post(
    "/activity/auto",
    response_model=UserActivityOut,
    summary="Summarize user activity (auto-fetch from Mastodon)",
    tags=["users"],
)
async def user_activity_summary_auto(data: UserIdentifierIn) -> UserActivityOut:
    normalized_username = normalize_mastodon_username(data.username)
    try:
        posts = await mastodon_service.get_recent_posts(normalized_username)
        logging.info(f"Fetched Mastodon posts for {normalized_username}: success")
    except HTTPException as e:
        logging.warning(f"Failed to fetch Mastodon posts for {normalized_username}: {e.detail}")
        raise HTTPException(status_code=422, detail=f"Mastodon user not found: {normalized_username}")
    user_activity = UserActivityIn(username=normalized_username, recent_posts=posts)
    return await analyze_user_activity(user_activity)

@router.get("/{username}/profile", response_model=UserProfileIn, summary="Get Mastodon user profile", tags=["users"])
async def get_profile(username: str) -> UserProfileIn:
    normalized_username = normalize_mastodon_username(username)
    return await mastodon_service.get_user_profile(normalized_username)

@router.get("/{username}/posts", response_model=List[RecentPost], summary="Get Mastodon user's recent posts", tags=["users"])
async def get_posts(username: str, limit: int = 5) -> List[RecentPost]:
    normalized_username = normalize_mastodon_username(username)
    return await mastodon_service.get_recent_posts(normalized_username, limit)