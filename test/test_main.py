from code.main import app
from fastapi.testclient import TestClient
import requests

clientes = TestClient(app)

def test_index():
    response = clientes.get("/")
    data = {"mensaje":"Fast API"}
    assert response.status_code == 200
    assert response.json() == data

def test_clientes():
    response = clientes.get("/clientes/?offset=0&limit=2")
    dataClientes = [
    {"id_cliente":2,"nombre":"Yael","email":"yael@email.com"},
    {"id_cliente":3,"nombre":"Erick","email":"erick@email.com"}
    ]
    assert response.status_code == 200
    assert response.json() == dataClientes

def test_cliente_parametros():
    response = clientes.get("/clientes/2")
    dataCliente = {"id_cliente":2,"nombre":"Yael","email":"yael@email.com"}
    assert response.status_code == 200
    assert response.json() == dataCliente

def test_cliente_add():
    parametros_add = {"nombre":"Hola","email":"new@hotmail.com"}
    response = clientes.post("/clientes/", json=parametros_add)
    dataCliente_add = {"mensaje":"Cliente agregado"}
    assert response.status_code == 200
    assert response.json() == dataCliente_add

def test_cliente_put():
    parametros = {"nombre":"Update","email":"update@hotmail.com"}
    response = clientes.put("/clientes/6", json=parametros)
    dataCliente_put = {"mensaje":"Cliente actualizado"}
    assert response.status_code == 200
    assert response.json() == dataCliente_put

def test_cliente_delete():
    response = clientes.delete("/clientes/6")
    dataCliente_delete = {"mensaje":"Cliente borrado"}
    assert response.status_code == 200
    assert response.json() == dataCliente_delete