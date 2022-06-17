from code.main import app
from fastapi.testclient import TestClient
import requests

clientes = TestClient(app)

def test_index():
    response = clientes.get("/")
    data = {"message":"Fast API"}
    assert response.status_code == 200
    assert response.json() == data

def test_clientes():
    response = clientes.get("/clientes/")
    dataClientes = [
    {"id_cliente":1,"nombre":"Nombre","email":"nombre@email.com"},
    {"id_cliente":2,"nombre":"Yael","email":"yael@email.com"},
    {"id_cliente":3,"nombre":"Erick","email":"erick@email.com"},
    {"id_cliente":4,"nombre":"Mauricio","email":"mau@email.com"}
    ]
    assert response.status_code == 200
    assert response.json() == dataClientes

def test_cliente_parametros():
    response = clientes.get("/clientes/1")
    dataCliente = {"id_cliente":1,"nombre":"Nombre","email":"nombre@email.com"}
    assert response.status_code == 200
    assert response.json() == dataCliente