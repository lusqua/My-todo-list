from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_users():
    response = client.get("/users/")

    assert response.status_code == 200
    assert type(response.json()) == list

def test_user_by_id():
    response = client.get("/users/1")
    user = response.json()

    assert response.status_code == 200
    assert user['email'] == "admin"

def test_user_by_id_not_found():
    response = client.get("/users/-1")

    assert response.status_code == 404

def test_user_already_exists():
    body = {"email": "admin", "password": "admin"}
    response = client.post("/users/", json=body)

    assert response.status_code == 400
