from typing import Union
from fastapi import FastAPI
from typing import List
from .Schemas import schemas_clientes
from .Conexion import crud

app = FastAPI()

@app.get("/", response_model=schemas_clientes.Respuesta)
async def index():
    return {"message": "Fast API"}

@app.get("/clientes/",response_model=List[schemas_clientes.Cliente])
async def clientes(offset:int =0,limit: int = 10):
    return crud.Read(limit,offset)

@app.get("/clientes/{id_cliente}")
async def cliente_parametros(id_cliente: int):
    return crud.Read_with_Params(id_cliente)
        
@app.post("/clientes/", response_model=schemas_clientes.Mensaje)
async def cliente_add(nombre:str,email:str):
    crud.Create(nombre,email)
    data = {"mensaje":"Cliente agregado"}
    return data

@app.put("/clientes/{id_cliente}", response_model=schemas_clientes.Mensaje)
async def cliente_put(id_cliente: int, nombre:str,email:str):
    crud.Update(nombre,email,id_cliente)
    data = {"mensaje":"Cliente actualizado"}
    return data

@app.delete("/clientes/{id_cliente}", response_model=schemas_clientes.Mensaje)
async def cliente_delete(id_cliente: int):
    crud.Delete(id_cliente)
    data = {"mensaje":"Cliente borrado"}
    return data