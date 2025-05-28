import logging
import os
from app.schemas.report import UserReportIn, ReportTriageOut, KNOWN_REASONS
from app.services.llm import triage_report

async def triage_user_report(data: UserReportIn) -> ReportTriageOut:
    # Basic validation
    if data.reason not in KNOWN_REASONS:
        logging.warning(f"Unknown report reason: {data.reason}")
        reason = "other"
    else:
        reason = data.reason
    use_llm = os.getenv("USE_LLM_TRIAGE", "false").lower() == "true"
    if use_llm:
        try:
            return await triage_report(data)
        except Exception as e:
            logging.error(f"LLM triage failed: {e}")
    # Fallback logic
    if reason == "harassment" or reason == "abuse":
        triage_level = "high"
        action = "flag_immediately"
        summary = "Report suggests possible harassment or abuse; prompt review required."
    elif reason == "spam":
        triage_level = "medium"
        action = "review"
        summary = "Report suggests spam; review recommended."
    else:
        triage_level = "low"
        action = "ignore"
        summary = "Report does not indicate urgent action."
    return ReportTriageOut(triage_level=triage_level, action=action, summary=summary) 