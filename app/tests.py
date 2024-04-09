import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from main import app, User, Users


""" PRUEBAS DE INTEGRACIÓN """
#=========================================================================================
# Añadir los siguientes usuarios para ejecutar las pruebas
# {
#    "name": "userTest",
#    "email": "test@mail.com"
# }
# {
#    "name": "userToUpdate",
#    "email": "testUpdate@mail.com"
# }
# {
#    "name": "userToDelete",
#    "email": "testDelete@mail.com"
# } 

@pytest.fixture
def client():
    with TestClient(app) as client:
        yield client


# get = 200 [índice]
def test_root(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Message": "Hola, este es el índice"}


# get = 200 [todos los usuarios]
def test_get_users(client):
    response = client.get("/all")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


# get = 200 [usuario encontrado]
def test_get_user(client):
    response = client.get("/user/1")
    assert response.status_code == 200
    assert response.json() == {"id": 1 ,"name": "userTest", "email": "test@mail.com"}


# post = 404 [usuario no encontrado]
def test_get_user(client):
    response = client.get("/user/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}


# post = 200 [usuario creado]
def test_post_user(client):
    response = client.post("/users", json={"name": "TEST USER", "email": "test.test@test.com"})
    assert response.status_code == 200
    assert response.json() == {"Message":"User was created successfully"}


# post  = 400 [correo invalido]
def test_post_emailInvalid(client):
    response = client.post("/users", json={"name": "stumble", "email": "stumble.stumble.com"})
    assert response.status_code == 400
    assert response.json() == {"detail": "The email is not valid"}


 # put = 404 [usuario no encontrado]
def test_modify_notFound(client):
        response = client.put("/user/999", json={"name": "John Wick", "email": "john.wick@test.com"})
        assert response.status_code == 404
        assert response.json() == {"detail": "User not found"}


# put = 200 [usuario modificado]
def test_modify_user(client):
    response = client.put("/user/2", json={"name": "test update", "email": "test.update@test.com"})
    assert response.status_code == 200
    assert response.json() == {"Message": "User updated"}


# delete = 200 [usuario eliminado]
def test_delete_user(client):
    response = client.delete("/user/3")
    assert response.status_code == 200
    assert response.json() == {"Message": "User deleted successfully"}


# delete = 404 [usuario no encontrado]
def test_delete_notFound(client):
    response = client.delete("/user/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}


""" {
    "name": "userTest",
    "email": "test@mail.com"
}
{
    "name": "userToUpdate",
    "email": "testUpdate@mail.com"
}
{
    "name": "userToDelete",
    "email": "testDelete@mail.com"
} """