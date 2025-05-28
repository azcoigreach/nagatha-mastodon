import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock
from app.api.v1.reports import router as reports_router
from app.schemas.report import UserReportIn, ReportTriageOut

app = FastAPI()
app.include_router(reports_router, prefix="/api/v1/reports")

@pytest.fixture
def client():
    return TestClient(app)

def valid_report():
    return {
        "reporter": "alice",
        "username": "badactor123",
        "reason": "harassment",
        "comment": "This user keeps sending me inappropriate replies.",
        "post_excerpt": "You'd look better if you smiled more",
        "created_at": "2025-05-21T14:32:00Z",
        "recent_posts": [
            {
                "content": "Example post content",
                "created_at": "2025-05-20T10:00:00Z",
                "favorites": 2,
                "reblogs": 0
            }
        ]
    }

@patch("app.services.llm.triage_report", new_callable=AsyncMock)
@pytest.mark.asyncio
async def test_submit_report_llm(mock_triage, client):
    mock_triage.return_value = ReportTriageOut(
        triage_level="high",
        action="flag_immediately",
        summary="Report suggests possible harassment; prompt review required."
    )
    response = client.post("/api/v1/reports/submit", json=valid_report())
    assert response.status_code == 200
    data = response.json()
    assert data["triage_level"] == "high"
    assert data["action"] == "flag_immediately"
    assert "harassment" in data["summary"]

@patch("app.services.llm.triage_report", side_effect=Exception("LLM error"))
@pytest.mark.asyncio
async def test_submit_report_fallback(mock_triage, client):
    # Should fallback to default logic
    response = client.post("/api/v1/reports/submit", json=valid_report())
    assert response.status_code == 200
    data = response.json()
    assert data["triage_level"] == "high"
    assert data["action"] == "flag_immediately"
    assert "harassment" in data["summary"]

@pytest.mark.asyncio
async def test_submit_report_invalid_reason(client):
    bad = valid_report()
    bad["reason"] = "notareason"
    response = client.post("/api/v1/reports/submit", json=bad)
    # 422 is expected due to schema validation error
    assert response.status_code == 422

@pytest.mark.asyncio
async def test_submit_report_invalid_reason_fallback(client):
    bad = valid_report()
    bad["reason"] = "notareason"
    response = client.post("/api/v1/reports/submit", json=bad)
    # 422 is expected due to schema validation error
    assert response.status_code == 422 