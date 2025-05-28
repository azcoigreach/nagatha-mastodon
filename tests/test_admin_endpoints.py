import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from app.main import app

client = TestClient(app)

@patch("app.services.admin_mastodon.get_federated_peers")
def test_get_peers(mock_get_peers):
    mock_get_peers.return_value = ["mastodon.social", "hachyderm.io", "fosstodon.org"]
    response = client.get("/api/v1/admin/peers")
    assert response.status_code == 200
    assert response.json() == {"peers": ["mastodon.social", "hachyderm.io", "fosstodon.org"]}

@patch("app.services.admin_mastodon.get_federated_instances")
def test_get_instances(mock_get_instances):
    mock_get_instances.return_value = [
        {
            "domain": "mastodon.social",
            "users_count": 1200000,
            "statuses_count": 9000000,
            "software": "mastodon",
            "version": "4.2.0",
            "uptime": "stable"
        }
    ]
    response = client.get("/api/v1/admin/instances")
    assert response.status_code == 200
    assert response.json()[0]["domain"] == "mastodon.social"

@patch("app.services.admin_mastodon.get_report_summary")
def test_get_reports_summary(mock_get_report_summary):
    mock_get_report_summary.return_value = {
        "open_reports": 27,
        "resolved_reports": 580,
        "spam_related": 12,
        "harassment_related": 9,
        "latest_report_ts": "2025-05-25T17:04:00Z"
    }
    response = client.get("/api/v1/admin/reports/summary")
    assert response.status_code == 200
    assert response.json()["open_reports"] == 27

@patch("app.services.admin_mastodon.get_system_measures")
def test_get_measures(mock_get_measures):
    mock_get_measures.return_value = {"some": "measure"}
    response = client.get("/api/v1/admin/measures")
    assert response.status_code == 200
    assert response.json() == {"some": "measure"} 