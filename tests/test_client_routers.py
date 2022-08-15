from fastapi.testclient import TestClient

client = {
    "first_name": "Danylo",
    "last_name": "Halytskyi",
    "email": "danylo@halytskyi.com",
    "phone": "+380143256789",
    "address": "Danyla Halytskoho, 12",
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

    response = client_auth.get("/clients/1")
    assert response.json()["first_name"] == client["first_name"]
    assert response.json()["last_name"] == "Volynskyi"
    assert response.json()["email"] == client["email"]
    assert response.json()["phone"] == client["phone"]
    assert response.json()["address"] == client["address"]

    response = client_auth.get("/clients")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["first_name"] == client["first_name"]

    response = client_auth.get("/clients/2")
    assert response.status_code == 404
    assert response.json() == {"detail": "No client found with id 2"}

    response = client_auth.delete("/clients/1")
    assert response.status_code == 200
    assert response.json() == {"result": "Successfully deleted client with id 1"}

    response = client_auth.get("/clients")
    assert response.status_code == 200
    assert response.json() == []

    

