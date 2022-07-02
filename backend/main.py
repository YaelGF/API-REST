from typing import Union
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sqlite3
from typing import List
import hashlib  # importa la libreria hashlib




class Respuesta(BaseModel):
    message: str

class Mensaje(BaseModel):
    mensaje: str

class Cliente(BaseModel):
    id_cliente: int
    nombre: str
    email: str

class ClienteNew(BaseModel):
    nombre: str
    email: str

class ClienteID(BaseModel):
    id_cliente: int

class Usuarios(BaseModel):
    username: str
    level: int

app = FastAPI()

origins = [
    "http://127.0.0.1:8000",
    "http://0.0.0.0:8080",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

security = HTTPBasic()

def get_current_level(credentials: HTTPBasicCredentials = Depends(security)):
    password_b = hashlib.md5(credentials.password.encode())
    password = password_b.hexdigest()
    with sqlite3.connect('backend/sql/clientes.sqlite') as connection:
        cursor = connection.cursor()
        cursor.execute(
            "SELECT level FROM usuarios WHERE username = ? and password = ?",
            (credentials.username, password),
        )
        user = cursor.fetchone()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Basic"},
            )
    return user[0]

@app.get("/", response_model=Respuesta)
async def index():
    return {"message": "Fast API"}

@app.get("/clientes/", response_model=List[Cliente],status_code=status.HTTP_202_ACCEPTED)
async def clientes(offset:int =0,limit: int = 10,level: int = Depends(get_current_level)):
    if level == 1:
        with sqlite3.connect('backend/sql/clientes.sqlite') as connection:
            connection.row_factory = sqlite3.Row
            cursor = connection.cursor()
            cursor.execute('SELECT * FROM clientes  LIMIT {limit}  OFFSET {offset}'.format(offset=offset,limit=limit))
            response = cursor.fetchall()
            return response
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Don't have permission to access this resource",
            headers={"WWW-Authenticate": "Basic"},
        )

@app.get("/clientes/{id_cliente}", response_model=Cliente)
async def cliente_parametros(id_cliente: int,level: int = Depends(get_current_level)):
    if level == 1:    
        with sqlite3.connect("backend/sql/clientes.sqlite") as connection:
            connection.row_factory = sqlite3.Row
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM clientes where id_cliente = {}".format(id_cliente))
            response = cursor.fetchone()
            return response
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Don't have permission to access this resource",
            headers={"WWW-Authenticate": "Basic"},
        )
        
@app.post("/clientes/", response_model=Mensaje)
async def cliente_add(nombre:str,email:str,level: int = Depends(get_current_level)):
    if level == 0:    
        with sqlite3.connect("backend/sql/clientes.sqlite") as connection:
            connection.row_factory = sqlite3.Row
            cursor = connection.cursor()
            cursor.execute("insert into clientes(nombre,email) values('{nombre}', '{email}')".format(nombre=nombre, email=email))
            response = cursor.fetchone()
            data = {"mensaje":"Cliente agregado"}
            return data

    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Don't have permission to access this resource",
            headers={"WWW-Authenticate": "Basic"},
        )

@app.put("/clientes/{id_cliente}", response_model=Mensaje)
async def cliente_put(id_cliente: int, nombre:str,email:str,level: int = Depends(get_current_level)):
    if level == 0:    
        with sqlite3.connect("backend/sql/clientes.sqlite") as connection:
            connection.row_factory = sqlite3.Row
            cursor = connection.cursor()
            cursor.execute("Update clientes set nombre = '{name}', email = '{email}' where id_cliente = {id}".format(name=nombre,email=email,id=id_cliente))
            response = cursor.fetchone()
            data = {"mensaje":"Cliente actualizado"}
            return data

    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Don't have permission to access this resource",
            headers={"WWW-Authenticate": "Basic"},
        )

@app.delete("/clientes/{id_cliente}", response_model=Mensaje)
async def cliente_delete(id_cliente: int,level: int = Depends(get_current_level)):
    if level == 0:  
        with sqlite3.connect("backend/sql/clientes.sqlite") as connection:
            connection.row_factory = sqlite3.Row
            cursor = connection.cursor()
            cursor.execute("Delete from clientes where id_cliente = {}".format(id_cliente))
            response = cursor.fetchone()
            data = {"mensaje":"Cliente borrado"}
            return data
    
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Don't have permission to access this resource",
            headers={"WWW-Authenticate": "Basic"},
        )
