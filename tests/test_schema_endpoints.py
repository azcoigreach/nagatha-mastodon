import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_schema_functions():
    response = client.get("/schema/functions")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    # There should be at least one function for users and one for reports
    users_found = False
    reports_found = False
    for func in data:
        assert "name" in func
        assert "description" in func
        assert "parameters" in func
        assert isinstance(func["parameters"], dict)
        # Check for users/reports in function name or description
        if "user" in func["name"] or "user" in func["description"].lower():
            users_found = True
        if "report" in func["name"] or "report" in func["description"].lower():
            reports_found = True
    assert users_found, "No user-related function found in /schema/functions"
    assert reports_found, "No report-related function found in /schema/functions"

def test_schema_capabilities():
    response = client.get("/schema/capabilities")
    assert response.status_code == 200
    data = response.json()
    assert data["agent_name"] == "nagatha-mastodon-submind"
    assert data["version"] == "0.1.0"
    assert isinstance(data["capabilities"], list)
    assert len(data["capabilities"]) >= 3
    assert "description" in data 