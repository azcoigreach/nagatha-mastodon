from fastapi import APIRouter
from app.schemas.report import UserReportIn, ReportTriageOut
from app.services.moderation import triage_user_report

router = APIRouter()

@router.post(
    "/submit",
    response_model=ReportTriageOut,
    summary="Submit a user/content report for triage",
    tags=["reports"],
)
async def submit_report(report: UserReportIn) -> ReportTriageOut:
    return await triage_user_report(report) 