import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from main import app

@pytest.fixture
def client():
    with TestClient(app) as client:
        yield client

@patch('main.Session')
def test_get_all_users(mock_session, client):
    # Simular la consulta
    mock_query = MagicMock()
    mock_query.all.return_value = [
        {"name": "userTest", "email": "test@mail.com"},
        {"name": "userTest2", "email": "user.test@mail.com"}
    ]
    mock_session.return_value.__enter__.return_value.query.return_value = mock_query

    response = client.get("/all")
    assert response.status_code == 200
    assert isinstance(response.json(), list) and all(isinstance(item, dict) for item in response.json())

@patch('main.Session')
def test_get_user(mock_session, client):
    # Simular la consulta
    mock_query = MagicMock()
    mock_query.scalars.return_value.all.return_value = [
        {"name": "userTest", "email": "test@mail.com"}
    ]
    mock_session.return_value.__enter__.return_value.execute.return_value = mock_query

    response = client.get("/user/1")
    assert response.status_code == 200
    assert response.json() == {"name": "userTest", "email": "test@mail.com"}
