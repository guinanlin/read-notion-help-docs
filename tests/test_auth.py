from fastapi.testclient import TestClient

def test_login_for_access_token(client, test_user):
    response = client.post(
        "/token",
        data={
            "username": "tim",
            "password": "secret123"
        }
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"

def test_login_invalid_credentials(client):
    response = client.post(
        "/token",
        data={
            "username": "wronguser",
            "password": "wrongpass"
        }
    )
    assert response.status_code == 401
    assert response.json() == {
        "detail": "Incorrect username or password"
    } 