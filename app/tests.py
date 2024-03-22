import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from mainTest import app, User, Users
# Integration Tests

@pytest.fixture
def client():
    with TestClient(app) as client:
        yield client

def test_root(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Message": "Hola, este es el índice"}

def test_get_users(client):
    response = client.get("/all")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_user(client):
    response = client.get("/user/1")
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}

def test_set_user(client):
    response = client.post("/users", json={"name": "John Deere", "email": "john.deere@example.com"})
    assert response.status_code == 200
    assert response.json() == {"Message": "User was created successfully"}

def test_modify_user(client):
    response = client.put("/user/1", json={"name": "John Wick", "email": "john.wick@example.com"})
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}

def test_delete_user(client):
    response = client.delete("/user/1")
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}

# Unit Tests

def test_users_model():
    user = Users(name="John Doe", email="john.doe@example.com")
    assert user.name == "John Doe"
    assert user.email == "john.doe@example.com"

@patch("app.Session")
def test_get_users_mocked(mock_session):
    mock_session.return_value.query.return_value.all.return_value = [
        Users(name="John Doe", email="john.doe@example.com"),
        Users(name="Jane Smith", email="jane.smith@example.com")
    ]
    with TestClient(app) as client:
        response = client.get("/all")
        assert response.status_code == 200
        assert isinstance(response.json(), list)
        assert len(response.json()) == 2

@patch("app.Session")
def test_get_user_mocked(mock_session):
    mock_session.return_value.execute.return_value.scalars.return_value.all.return_value = [
        Users(name="John Doe", email="john.doe@example.com")
    ]
    with TestClient(app) as client:
        response = client.get("/user/1")
        assert response.status_code == 200
        assert response.json()["name"] == "John Doe"
        assert response.json()["email"] == "john.doe@example.com"