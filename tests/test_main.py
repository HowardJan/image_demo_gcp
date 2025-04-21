import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_form():
    response = client.get("/")
    assert response.status_code == 200
    assert "<form" in response.text
