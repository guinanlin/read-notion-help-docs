from fastapi.testclient import TestClient

def test_read_main(client):
    response = client.get("/users/me/items")
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}

def test_read_users_me_unauthorized(client):
    response = client.get("/users/me/")
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"} 