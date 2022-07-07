from backend.main import app
from fastapi.testclient import TestClient
import requests
from requests.auth import HTTPBasicAuth
import json

clientes = TestClient(app)

def test_index():
    response = clientes.get("/")
    data = {"message":"Fast API"}
    assert response.status_code == 200
    assert response.json() == data

def test_clientes():
    auth = HTTPBasicAuth(username="user", password="user")
    response = clientes.get("/clientes/?offset=0&limit=4", auth=auth)
    dataClientes = [
    {"id_cliente":1,"nombre":"Nombre","email":"nombre@email.com"},
    {"id_cliente":2,"nombre":"Yael","email":"yael@email.com"},
    {"id_cliente":3,"nombre":"Erick","email":"erick@email.com"},
    {"id_cliente":4,"nombre":"Mauricio","email":"mau@email.com"}
    ]
    assert response.status_code == 202
    assert response.json() == dataClientes

def test_cliente_parametros():
    auth = HTTPBasicAuth(username="user", password="user")
    response = clientes.get("/clientes/2", auth=auth)
    dataCliente = {"id_cliente":2,"nombre":"Yael","email":"yael@email.com"}
    assert response.status_code == 200
    assert response.json() == dataCliente

def test_cliente_add():
    auth = HTTPBasicAuth(username="admin", password="admin")
    parametrosAdd = {"nombre":"Hola","email":"new@email.com"}
    response = clientes.post("/clientes/", params=parametrosAdd, auth=auth)
    dataCliente_add = {"mensaje":"Cliente agregado"}
    assert response.status_code == 200
    assert response.json() == dataCliente_add

def test_cliente_put():
    auth = HTTPBasicAuth(username="admin", password="admin")
    parametros = {"nombre":"Ayuda","email":"update@hotmail.com"}
    response = clientes.put("/clientes/6", params=parametros, auth=auth)
    dataCliente_put = {"mensaje":"Cliente actualizado"}
    assert response.status_code == 200
    assert response.json() == dataCliente_put

def test_cliente_delete():
    auth = HTTPBasicAuth(username="admin", password="admin")
    response = clientes.delete("/clientes/6", auth=auth)
    dataCliente_delete = {"mensaje":"Cliente borrado"}
    assert response.status_code == 200
    assert response.json() == dataCliente_delete