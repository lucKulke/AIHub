import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from fastapi.testclient import TestClient
from app.main import app

# Add the parent directory of 'app' to the Python path


client = TestClient(app)


def test_azure_available_voices():
    response = client.get("/text_to_voice/azure/available_voices")
    assert response.status_code == 200


def test_authentication():
    response = client.post("/text_to_voice/azure")
    assert response.status_code == 401
