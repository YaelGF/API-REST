import databases # Permite ejecutar y formatear las consultas

from typing import List

from fastapi import FastAPI
from pydantic import BaseModel

from starlette.responses import RedirectResponse

from sqlalchemy import MetaData
from sqlalchemy import create_engine
from sqlalchemy import select, insert, update, delete
from sqlalchemy import Table,Column, String, Integer


DATABASE_URL = "sqlite:///clientes.db"

database = databases.Database(DATABASE_URL)

metadata = MetaData() # DB Schema

engine = create_engine(DATABASE_URL)

clientes = Table(
    'clientes',metadata,
    Column('id_cliente', Integer, primary_key = True),
    Column('nombre', String, nullable = False),
    Column('email', String, nullable = False)
)

metadata.create_all(engine)

app = FastAPI()

class Cliente(BaseModel):
    id_cliente: int
    nombre: str
    email: str

class ClienteIN(BaseModel):
    nombre : str
    email : str

class Message(BaseModel):
    message : str

@app.get("/",)
async def root():
    return RedirectResponse(url='/docs')


@app.get("/clientes", response_model = List[Cliente])
async def get_clientes():
    query = select(clientes)
    return await database.fetch_all(query)

@app.get("/clientes/{id_cliente}", response_model = Cliente)
async def get_cliente(id_cliente : int):
    query = select(clientes).where(clientes.c.id_cliente == id_cliente)
    return await database.fetch_one(query)

@app.post("/clientes", response_model = Message)
async def create_cliente(cliente : ClienteIN):
    query = insert(clientes).values(nombre = cliente.nombre, email = cliente.email)
    await database.execute(query)
    return {"message" : "Cliente agregado"}

@app.put("/clientes/{id_cliente}", response_model = Message)
async def update_cliente(id_cliente : int, cliente : ClienteIN):
    query = update(clientes).where(clientes.c.id_cliente == id_cliente).values(nombre = cliente.nombre, email = cliente.email)
    await database.execute(query)
    return {"message" : "Cliente Actualizado"}

@app.delete("/clientes/{id_cliente}", response_model = Message)
async def delete_cliente(id_cliente : int):
    query = delete(clientes).where(clientes.c.id_cliente == id_cliente)
    await database.execute(query)
    return {"message" : "Cliente Eliminado"}