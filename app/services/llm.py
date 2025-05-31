import logging
import json

from openai import AsyncOpenAI

from app.core.config import settings
from app.schemas.user_eval import UserProfileIn, UserEvaluationOut
from app.schemas.user_activity import RecentPost
from app.schemas.report import UserReportIn, ReportTriageOut

async def evaluate_user_profile(user_data: UserProfileIn) -> UserEvaluationOut:
    client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
    system_prompt = (
        "You are a content moderation AI. Based on the user profile below, "
        "estimate a risk score, recommend a moderation action (approve, flag, deny), "
        "and explain briefly why. Return a JSON object with keys: "
        "risk_score (float between 0 and 1), recommendation (approve, flag, or deny), "
        "and summary (a concise explanation)."
    )
    try:
        response = await client.chat.completions.create(
            model=settings.OPENAI_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": json.dumps(user_data.dict(), default=str)},
            ],
        )
    except Exception as e:
        logging.error(f"OpenAI API error: {e}")
        raise RuntimeError("Error contacting OpenAI API")
    content = response.choices[0].message.content
    try:
        result = json.loads(content)
    except json.JSONDecodeError as e:
        logging.error(f"JSON parse error: {e}")
        raise RuntimeError("Invalid response from OpenAI API")
    try:
        return UserEvaluationOut(**result)
    except Exception as e:
        logging.error(f"Validation error: {e}")
        raise RuntimeError("Invalid data format from OpenAI API")

async def classify_activity_pattern(posts: list[RecentPost]) -> str:
    client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
    system_prompt = (
        "You are an expert in social media analysis. Given a user's recent posts, classify their activity pattern with a single label such as 'engaged community member', 'low-effort spammer', or 'new quiet user'. Respond with only the label."
    )
    try:
        response = await client.chat.completions.create(
            model=settings.OPENAI_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": json.dumps([p.dict() for p in posts], default=str)},
            ],
        )
        label = response.choices[0].message.content.strip()
        return label
    except Exception as e:
        logging.error(f"OpenAI API error (activity pattern): {e}")
        return None

async def triage_report(report: UserReportIn) -> ReportTriageOut:
    client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
    system_prompt = (
        "You are a moderation assistant. Given this user report, estimate severity (low, medium, high), "
        "suggest a moderation action (ignore, review, flag_immediately), and summarize briefly. "
        "Return a JSON object with keys: triage_level, action, summary."
    )
    try:
        response = await client.chat.completions.create(
            model=settings.OPENAI_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": json.dumps(report.dict(), default=str)},
            ],
        )
    except Exception as e:
        logging.error(f"OpenAI API error (triage): {e}")
        raise
    content = response.choices[0].message.content
    try:
        result = json.loads(content)
    except json.JSONDecodeError as e:
        logging.error(f"JSON parse error (triage): {e}")
        raise
    try:
        return ReportTriageOut(**result)
    except Exception as e:
        logging.error(f"Validation error (triage): {e}")
        raise