from typing import Union
from fastapi import FastAPI
import sqlite3
from typing import List
from .Schemas import schemas



app = FastAPI()

@app.get("/", response_model=schemas.Respuesta)
async def index():
    return {"message": "Fast API"}

@app.get("/clientes/", response_model=List[schemas.Cliente])
async def clientes(offset:int =0,limit: int = 10):
    with sqlite3.connect('code/sql/clientes.sqlite') as connection:
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM clientes  LIMIT {limit}  OFFSET {offset}'.format(offset=offset,limit=limit))
        response = cursor.fetchall()
        return response

@app.get("/clientes/{id_cliente}", response_model=schemas.Cliente)
async def cliente_parametros(id_cliente: int):
    with sqlite3.connect("code/sql/clientes.sqlite") as connection:
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM clientes where id_cliente = {}".format(id_cliente))
        response = cursor.fetchone()
        return response
        
@app.post("/clientes/", response_model=schemas.Mensaje)
async def cliente_add(nombre:str,email:str):
    with sqlite3.connect("code/sql/clientes.sqlite") as connection:
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        cursor.execute("insert into clientes(nombre,email) values('{nombre}', '{email}')".format(nombre=nombre, email=email))
        response = cursor.fetchone()
        data = {"mensaje":"Cliente agregado"}
        return data

@app.put("/clientes/{id_cliente}", response_model=schemas.Mensaje)
async def cliente_put(id_cliente: int, nombre:str,email:str):
    with sqlite3.connect("code/sql/clientes.sqlite") as connection:
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        cursor.execute("Update clientes set nombre = '{name}', email = '{email}' where id_cliente = {id}".format(name=nombre,email=email,id=id_cliente))
        response = cursor.fetchone()
        data = {"mensaje":"Cliente actualizado"}
        return data

@app.delete("/clientes/{id_cliente}", response_model=schemas.Mensaje)
async def cliente_delete(id_cliente: int):
    with sqlite3.connect("code/sql/clientes.sqlite") as connection:
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        cursor.execute("Delete from clientes where id_cliente = {}".format(id_cliente))
        response = cursor.fetchone()
        data = {"mensaje":"Cliente borrado"}
        return data