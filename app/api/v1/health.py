from fastapi import APIRouter
from app.core.config import settings
from datetime import datetime

router = APIRouter()

@router.get("", summary="Health check", tags=["Health"])
async def health():
    now = datetime.utcnow()
    uptime = (now - settings.START_TIME).total_seconds()
    return {"uptime": uptime, "instance_id": settings.INSTANCE_ID}