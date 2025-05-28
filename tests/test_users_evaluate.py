import json

import pytest
from unittest.mock import AsyncMock, ANY
from fastapi.testclient import TestClient

from app.main import app
from app.core.config import settings
from app.schemas.user_eval import UserProfileIn

client = TestClient(app)

def test_evaluate_user_success(mocker):
    dummy_content = json.dumps({
        "risk_score": 0.13,
        "recommendation": "approve",
        "summary": "Test summary",
    })
    class DummyMessage:
        def __init__(self, content):
            self.content = content

    class DummyChoice:
        def __init__(self, message):
            self.message = message

    class DummyResponse:
        def __init__(self, choices):
            self.choices = choices

    dummy_response = DummyResponse([
        DummyChoice(DummyMessage(dummy_content))
    ])
    # Patch AsyncOpenAI so we can patch its instance's chat.completions.create
    mock_AsyncOpenAI = mocker.patch("app.services.llm.AsyncOpenAI")
    mock_client = mock_AsyncOpenAI.return_value
    mock_chat = mock_client.chat
    mock_completions = mock_chat.completions
    mock_completions.create = AsyncMock(return_value=dummy_response)

    payload = {
        "username": "janedoe",
        "bio": "Artist and coder. Into open tech.",
        "follower_count": 120,
        "following_count": 85,
        "statuses_count": 342,
        "created_at": "2024-11-10T12:42:00Z",
    }
    response = client.post("/api/v1/users/evaluate", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["risk_score"] == 0.13
    assert data["recommendation"] == "approve"
    assert data["summary"] == "Test summary"
    mock_completions.create.assert_awaited_once_with(
        model=settings.OPENAI_MODEL,
        messages=ANY,
    )

def test_evaluate_user_auto_success(mocker):
    # Mock Mastodon profile fetch with a UserProfileIn instance
    dummy_profile = UserProfileIn(
        username="janedoe",
        bio="Artist and coder. Into open tech.",
        follower_count=120,
        following_count=85,
        statuses_count=342,
        created_at="2024-11-10T12:42:00Z",
    )
    mocker.patch("app.api.v1.users.mastodon_service.get_user_profile", AsyncMock(return_value=dummy_profile))
    # Mock OpenAI
    dummy_content = json.dumps({
        "risk_score": 0.13,
        "recommendation": "approve",
        "summary": "Test summary",
    })
    class DummyMessage:
        def __init__(self, content):
            self.content = content
    class DummyChoice:
        def __init__(self, message):
            self.message = message
    class DummyResponse:
        def __init__(self, choices):
            self.choices = choices
    dummy_response = DummyResponse([
        DummyChoice(DummyMessage(dummy_content))
    ])
    mock_AsyncOpenAI = mocker.patch("app.services.llm.AsyncOpenAI")
    mock_client = mock_AsyncOpenAI.return_value
    mock_chat = mock_client.chat
    mock_completions = mock_chat.completions
    mock_completions.create = AsyncMock(return_value=dummy_response)
    payload = {"username": "janedoe"}
    response = client.post("/api/v1/users/evaluate/auto", json=payload)
    if response.status_code != 200:
        print("Response body:", response.text)
    assert response.status_code == 200
    data = response.json()
    assert data["risk_score"] == 0.13
    assert data["recommendation"] == "approve"
    assert data["summary"] == "Test summary"
    mock_completions.create.assert_awaited_once_with(
        model=settings.OPENAI_MODEL,
        messages=ANY,
    )

def test_evaluate_user_auto_not_found(mocker):
    # Simulate Mastodon not found
    from fastapi import HTTPException
    async def raise_not_found(username):
        raise HTTPException(status_code=404, detail="User not found")
    mocker.patch("app.api.v1.users.mastodon_service.get_user_profile", raise_not_found)
    payload = {"username": "ghostuser"}
    response = client.post("/api/v1/users/evaluate/auto", json=payload)
    assert response.status_code == 422
    assert "not found" in response.json()["detail"]