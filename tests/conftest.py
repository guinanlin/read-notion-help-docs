import pytest
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def test_user():
    return {
        "username": "testuser",
        "full_name": "Test User",
        "email": "test@example.com",
        "password": "testpassword123"
    } 