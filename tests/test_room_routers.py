import re
from urllib import request
from fastapi.testclient import TestClient


def test_feature(client_auth: TestClient):
    """Test creation of room type, adding, getting and deleting features."""

    # Create
    request_data = {"name": "feature"}
    response = client_auth.post("/features", json=request_data)
    assert response.status_code == 200
    assert response.json()["name"] == "feature"
    assert response.json()["id"] == 1

    # Get
    response = client_auth.get("/features")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["name"] == "feature"
    assert response.json()[0]["id"] == 1

    # Update
    request_data = {"name": "feature1"}
    response = client_auth.put("/features/1", json=request_data)
    assert response.status_code == 200
    assert response.json()["name"] == "feature1"
    assert response.json()["id"] == 1

    # Get when feature does not exist
    request_data = {"name": "feature2"}
    response = client_auth.get("/features/2")
    assert response.status_code == 404
    assert response.json() == {"detail": "No feature found with id 2"}

    # Update when feature does not exist
    request_data = {"name": "feature2"}
    response = client_auth.put("/features/2", json=request_data)
    assert response.status_code == 404
    assert response.json() == {"detail": "No feature found with id 2"}

    # Delete when feature does not exist
    request_data = {"name": "feature2"}
    response = client_auth.delete("/features/2", json=request_data)
    assert response.status_code == 404
    assert response.json() == {"detail": "No feature found with id 2"}

    # Create another
    request_data = {"name": "feature2"}
    response = client_auth.post("/features", json=request_data)
    assert response.status_code == 200
    assert response.json()["name"] == "feature2"
    assert response.json()["id"] == 2

    # Get multiple
    response = client_auth.get("/features")
    assert response.status_code == 200
    assert len(response.json()) == 2
    assert response.json()[0]["name"] == "feature1"
    assert response.json()[0]["id"] == 1
    assert response.json()[1]["name"] == "feature2"
    assert response.json()[1]["id"] == 2

    # Create with empty request
    request_data = {}
    response = client_auth.post("/features", json=request_data)
    assert response.status_code == 422


def test_facility(client_auth: TestClient):
    # Create
    request_data = {"name": "facility"}
    response = client_auth.post("/facilities", json=request_data)
    assert response.status_code == 200
    assert response.json()["name"] == "facility"
    assert response.json()["id"] == 1

    # Get
    response = client_auth.get("/facilities")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["name"] == "facility"
    assert response.json()[0]["id"] == 1

    # Update
    request_data = {"name": "facility1"}
    response = client_auth.put("/facilities/1", json=request_data)
    assert response.status_code == 200
    assert response.json()["name"] == "facility1"
    assert response.json()["id"] == 1

    # Get when facility does not exist
    request_data = {"name": "facility2"}
    response = client_auth.get("/facilities/2")
    assert response.status_code == 404
    assert response.json() == {"detail": "No facility found with id 2"}

    # Update when facility does not exist
    request_data = {"name": "facility2"}
    response = client_auth.put("/facilities/2", json=request_data)
    assert response.status_code == 404
    assert response.json() == {"detail": "No facility found with id 2"}

    # Delete when feature does not exist
    request_data = {"name": "facility2"}
    response = client_auth.delete("/facilities/2", json=request_data)
    assert response.status_code == 404
    assert response.json() == {"detail": "No facility found with id 2"}

    # Create another
    request_data = {"name": "facility2"}
    response = client_auth.post("/facilities", json=request_data)
    assert response.status_code == 200
    assert response.json()["name"] == "facility2"
    assert response.json()["id"] == 2

    # Get multiple
    response = client_auth.get("/facilities")
    assert response.status_code == 200
    assert len(response.json()) == 2
    assert response.json()[0]["name"] == "facility1"
    assert response.json()[0]["id"] == 1
    assert response.json()[1]["name"] == "facility2"
    assert response.json()[1]["id"] == 2

    # Create with empty request
    request_data = {}
    response = client_auth.post("/facilities", json=request_data)
    assert response.status_code == 422


def test_room_type(client_auth: TestClient):

    request_data = {"name": "single", "capacity": "5", "price": 50}
    response = client_auth.post("/room_types", json=request_data)
    assert response.status_code == 200
    assert response.json()["id"] == 1
    assert response.json()["name"] == "single"
    assert response.json()["capacity"] == "5"
    assert response.json()["price"] == 50
    assert isinstance(response.json()["id"], int)

    request_data = {"name": "feature1"}
    response = client_auth.post("/features", json=request_data)
    assert response.status_code == 200
    assert response.json()["name"] == "feature1"
    assert response.json()["id"] == 1

    response = client_auth.post("/room_types/1/features?feature_id=1")
    assert response.status_code == 200
    assert response.json() == {
        "result": "Successfully added feature (id=1) to room_type (id=1)"
    }

    response = client_auth.post("/room_types/1/features?feature_id=3")
    assert response.status_code == 404
    assert response.json() == {"detail": "No feature found with id 3"}

    response = client_auth.post("/room_types/2/features?feature_id=1")
    assert response.status_code == 404
    assert response.json() == {"detail": "No room type found with id 2"}

    response = client_auth.get("/room_types/1/features")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["id"] == 1
    assert response.json()[0]["name"] == "feature1"

    response = client_auth.delete("/room_types/1/features?feature_id=1")
    assert response.status_code == 200
    assert response.json() == {
        "result": "Successfully deleted feature (id=1) from room_type (id=1)"
    }

    request_data = {}
    response = client_auth.post("/room_types", json=request_data)
    assert response.status_code == 422


def test_room(client_auth: TestClient):
    request_data = {"name": "facility"}
    response = client_auth.post("/facilities", json=request_data)
    assert response.status_code == 200
    assert response.json()["name"] == "facility"
    assert response.json()["id"] == 1

    request_data = {"name": "single", "capacity": "5", "price": 50}
    response = client_auth.post("/room_types", json=request_data)
    assert response.status_code == 200
    assert response.json()["id"] == 1
    assert response.json()["name"] == "single"
    assert response.json()["capacity"] == "5"
    assert response.json()["price"] == 50
    assert isinstance(response.json()["id"], int)

    request_data = {"id": 100, "room_type_id": 2, "facility_id": 2, "floor": 2, "booking_status": "occupied", "cleanliness_status": "clean"}
    response = client_auth.post("/rooms", json=request_data)
    assert response.status_code == 404
    assert response.json() == {"detail": "No room type found with id 2"}

    request_data = {"id": 100, "room_type_id": 1, "facility_id": 1, "floor": 2, "booking_status": "occupied", "cleanliness_status": "clean"}
    response = client_auth.post("/rooms", json=request_data)
    assert response.status_code == 200
    assert response.json()["id"] == request_data["id"]
    assert response.json()["room_type_id"] == request_data["room_type_id"]
    assert response.json()["facility_id"] == request_data["facility_id"]
    assert response.json()["floor"] == request_data["floor"]
    assert response.json()["booking_status"] == request_data["booking_status"]
    assert response.json()["cleanliness_status"] == request_data["cleanliness_status"]
    assert isinstance(response.json()["id"], int)

    request_data = {"id": 100, "room_type_id": 1, "facility_id": 1, "floor": 2, "booking_status": "occupied", "cleanliness_status": "clean"}
    response = client_auth.post("/rooms", json=request_data)
    assert response.status_code == 400
    assert response.json() == {"detail": "Room with id 100 already exists"}

    request_data = {"id": 150, "room_type_id": 1, "facility_id": 1, "floor": 2, "booking_status": "clean", "cleanliness_status": "clean"}
    response = client_auth.post("/rooms", json=request_data)
    assert response.status_code == 422

