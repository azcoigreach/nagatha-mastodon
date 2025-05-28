import pytest
from fastapi.testclient import TestClient
from app.main import app
import os
from unittest.mock import AsyncMock

client = TestClient(app)

@pytest.fixture(autouse=True)
def reset_llm_env(monkeypatch):
    monkeypatch.setenv("USE_LLM_ACTIVITY", "false")
    yield
    monkeypatch.delenv("USE_LLM_ACTIVITY", raising=False)

def test_activity_summary_basic():
    payload = {
        "username": "janedoe",
        "recent_posts": [
            {
                "content": "Just posted a new art piece!",
                "created_at": "2025-05-20T10:00:00Z",
                "favorites": 15,
                "reblogs": 2
            },
            {
                "content": "Excited for the next federated tech meetup.",
                "created_at": "2025-05-19T09:00:00Z",
                "favorites": 8,
                "reblogs": 1
            }
        ]
    }
    response = client.post("/api/v1/users/activity", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["post_count"] == 2
    assert data["avg_engagement"]["favorites"] == pytest.approx(11.5)
    assert data["avg_engagement"]["reblogs"] == pytest.approx(1.5)
    assert data["posting_frequency"] == "daily"
    assert data["summary"].startswith("User posts daily")
    assert data["category"] is None

def test_activity_summary_with_llm(mocker, monkeypatch):
    monkeypatch.setenv("USE_LLM_ACTIVITY", "true")
    mocker.patch("app.services.llm.classify_activity_pattern", return_value="engaged community member")
    payload = {
        "username": "janedoe",
        "recent_posts": [
            {
                "content": "Just posted a new art piece!",
                "created_at": "2025-05-20T10:00:00Z",
                "favorites": 15,
                "reblogs": 2
            },
            {
                "content": "Excited for the next federated tech meetup.",
                "created_at": "2025-05-19T09:00:00Z",
                "favorites": 8,
                "reblogs": 1
            }
        ]
    }
    response = client.post("/api/v1/users/activity", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["category"] == "engaged community member"

def test_activity_summary_auto_success(mocker):
    dummy_posts = [
        {
            "content": "Just posted a new art piece!",
            "created_at": "2025-05-20T10:00:00Z",
            "favorites": 15,
            "reblogs": 2
        },
        {
            "content": "Excited for the next federated tech meetup.",
            "created_at": "2025-05-19T09:00:00Z",
            "favorites": 8,
            "reblogs": 1
        }
    ]
    mocker.patch("app.services.mastodon.get_recent_posts", AsyncMock(return_value=dummy_posts))
    payload = {"username": "janedoe"}
    response = client.post("/api/v1/users/activity/auto", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["post_count"] == 2
    assert data["avg_engagement"]["favorites"] == pytest.approx(11.5)
    assert data["avg_engagement"]["reblogs"] == pytest.approx(1.5)
    assert data["posting_frequency"] == "daily"
    assert data["summary"].startswith("User posts daily")
    assert data["category"] is None

def test_activity_summary_auto_not_found(mocker):
    from fastapi import HTTPException
    async def raise_not_found(username, limit=5):
        raise HTTPException(status_code=404, detail="User not found")
    mocker.patch("app.services.mastodon.get_recent_posts", raise_not_found)
    payload = {"username": "ghostuser"}
    response = client.post("/api/v1/users/activity/auto", json=payload)
    assert response.status_code == 422
    assert "not found" in response.json()["detail"] 