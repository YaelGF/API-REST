from PaginaFastAPI.main import app
from fastapi.testclient import TestClient
from urllib import response
import requests

clientes = TestClient(app)

dataClientes = [
    {"id_cliente":1,"nombre":"Nombre","email":"nombre@email.com"},
    {"id_cliente":2,"nombre":"Yael","email":"yael@email.com"},
    {"id_cliente":3,"nombre":"Erick","email":"erick@email.com"},
    {"id_cliente":4,"nombre":"Mauricio","email":"mau@email.com"}
    ]

def test_index():
    response = clientes.get("/")
    assert response.status_code == 200
    assert response.json() == {"message":"Fast API"}
