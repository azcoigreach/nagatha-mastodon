import pytest
from unittest.mock import patch, MagicMock
from app.services import mastodon as mastodon_service
from app.schemas.user_eval import UserProfileIn
from app.schemas.user_activity import RecentPost
from fastapi import HTTPException
from datetime import datetime, timezone
import types
import sys
import app.utils.mastodon

@pytest.mark.asyncio
@patch("app.services.mastodon.get_mastodon_client")
@patch("app.utils.mastodon.get_local_server_domain", return_value="stranger.social")
@pytest.mark.parametrize("username_variant,expected_acct", [
    ("alice", "@alice@stranger.social"),
    ("alice@stranger.social", "@alice@stranger.social"),
    ("@alice@stranger.social", "@alice@stranger.social"),
])
async def test_get_user_profile_success(mock_domain, mock_get_client, username_variant, expected_acct):
    mock_client = MagicMock()
    mock_get_client.return_value = mock_client
    mock_client.account_search.return_value = [{
        "acct": "alice",
        "note": "Bio here",
        "followers_count": 10,
        "following_count": 5,
        "statuses_count": 3,
        "created_at": "2023-01-01T12:00:00.000000Z"
    }]
    result = await mastodon_service.get_user_profile(username_variant)
    assert isinstance(result, UserProfileIn)
    assert result.username == "alice"
    assert result.bio == "Bio here"
    assert result.follower_count == 10
    assert result.following_count == 5
    assert result.statuses_count == 3
    assert result.created_at == datetime(2023, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
    mock_client.account_search.assert_called_with(expected_acct, 1)

@pytest.mark.asyncio
@patch("app.services.mastodon.get_mastodon_client")
@patch("app.utils.mastodon.get_local_server_domain", return_value="stranger.social")
async def test_get_user_profile_not_found(mock_domain, mock_get_client):
    mock_client = MagicMock()
    mock_get_client.return_value = mock_client
    mock_client.account_search.return_value = []
    with pytest.raises(HTTPException) as exc:
        await mastodon_service.get_user_profile("bob")
    assert exc.value.status_code == 502

@pytest.mark.asyncio
@patch("app.services.mastodon.get_mastodon_client")
@patch("app.utils.mastodon.get_local_server_domain", return_value="stranger.social")
@pytest.mark.parametrize("username_variant,expected_acct", [
    ("alice", "@alice@stranger.social"),
    ("alice@stranger.social", "@alice@stranger.social"),
    ("@alice@stranger.social", "@alice@stranger.social"),
])
async def test_get_recent_posts_success(mock_domain, mock_get_client, username_variant, expected_acct):
    mock_client = MagicMock()
    mock_get_client.return_value = mock_client
    mock_client.account_search.return_value = [{"id": 123}]
    mock_client.account_statuses.return_value = [
        {
            "content": "<p>Hello</p>",
            "created_at": "2023-01-01T12:00:00.000000Z",
            "favourites_count": 2,
            "reblogs_count": 1
        },
        {
            "content": "<p>World</p>",
            "created_at": "2023-01-02T13:00:00.000000Z",
            "favourites_count": 3,
            "reblogs_count": 0
        }
    ]
    posts = await mastodon_service.get_recent_posts(username_variant, limit=2)
    assert isinstance(posts, list)
    assert all(isinstance(p, RecentPost) for p in posts)
    assert posts[0].content == "<p>Hello</p>"
    assert posts[1].favorites == 3
    assert posts[0].reblogs == 1
    assert posts[1].created_at == datetime(2023, 1, 2, 13, 0, 0, tzinfo=timezone.utc)
    mock_client.account_search.assert_called_with(expected_acct, 1)

@pytest.mark.asyncio
@patch("app.services.mastodon.get_mastodon_client")
@patch("app.utils.mastodon.get_local_server_domain", return_value="stranger.social")
async def test_get_recent_posts_user_not_found(mock_domain, mock_get_client):
    mock_client = MagicMock()
    mock_get_client.return_value = mock_client
    mock_client.account_search.return_value = []
    with pytest.raises(HTTPException) as exc:
        await mastodon_service.get_recent_posts("bob")
    assert exc.value.status_code == 502

@pytest.mark.asyncio
@patch("app.services.mastodon.get_mastodon_client")
@patch("app.utils.mastodon.get_local_server_domain", return_value="stranger.social")
async def test_get_recent_posts_api_error(mock_domain, mock_get_client):
    mock_client = MagicMock()
    mock_get_client.return_value = mock_client
    mock_client.account_search.side_effect = Exception("API error")
    with pytest.raises(HTTPException) as exc:
        await mastodon_service.get_recent_posts("alice")
    assert exc.value.status_code == 502 