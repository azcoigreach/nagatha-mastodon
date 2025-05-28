from fastapi.testclient import TestClient

from app.main import app
from app.core.config import settings

client = TestClient(app)

def test_health_status():
    response = client.get("/health")
    assert response.status_code == 200

def test_health_response_structure():
    response = client.get("/health")
    data = response.json()
    assert "uptime" in data
    assert "instance_id" in data
    assert isinstance(data["uptime"], float)
    assert data["uptime"] >= 0
    assert isinstance(data["instance_id"], str)
    assert data["instance_id"] == settings.INSTANCE_ID