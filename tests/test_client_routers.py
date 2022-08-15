from fastapi.testclient import TestClient

client = {
    "first_name": "Danylo",
    "last_name": "Halytskyi",
    "email": "danylo@halytskyi.com",
    "phone": "+380143256789",
    "address": "Danyla Halytskoho, 12"
}

def test_client(client_auth: TestClient):
    response = client_auth.post("/clients", json=client)
    assert response.status_code == 200
    assert response.json()["first_name"] == client["first_name"]
    assert response.json()["last_name"] == client["last_name"]
    assert response.json()["email"] == client["email"]
    assert response.json()["phone"] == client["phone"]
    assert response.json()["address"] == client["address"]

    request_data = {"last_name": "Volynskyi"}
    response = client_auth.put("/clients/1", json=request_data)
    assert response.status_code == 200
    assert response.json()["last_name"] == request_data["last_name"]

    request_data = client_auth.get("/clients/1")
    assert response.json()["first_name"] == client["first_name"]
    assert response.json()["last_name"] == "Volynskyi"
    assert response.json()["email"] == client["email"]
    assert response.json()["phone"] == client["phone"]
    assert response.json()["address"] == client["address"]


