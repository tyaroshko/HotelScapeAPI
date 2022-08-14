from fastapi.testclient import TestClient


def test_auth(client_not_auth: TestClient):
    response = client_not_auth.get("/rooms")
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}

    response = client_not_auth.post("/rooms")
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}

    response = client_not_auth.get("/room_types")
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}

    response = client_not_auth.post("/room_types")
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}

    response = client_not_auth.get("/features")
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}

    response = client_not_auth.post("/features")
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}

    response = client_not_auth.get("/facilities")
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}

    response = client_not_auth.post("/facilities")
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}

    response = client_not_auth.get("/bookings")
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}

    response = client_not_auth.post("/bookings")
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}

    response = client_not_auth.get("/invoices")
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}

    response = client_not_auth.post("/invoices")
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}

    response = client_not_auth.get("/clients")
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}

    response = client_not_auth.post("/clients")
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}


user = {"username": "test_user", "password": "test_password"}

form_data = {
    "grant_type": None,
    "username": "test_user",
    "password": "test_password",
    "scopes": [],
    "client_id": None,
    "client_secret": None,
}


def test_auth(client_not_auth: TestClient):
    response = client_not_auth.post("/signup", json=user)
    assert response.status_code == 200
    id = response.json()["id"]
    assert isinstance(id, str)
    assert response.json()["username"] == user["username"]
