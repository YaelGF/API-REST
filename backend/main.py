
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse
from typing import Union
from typing import List
import pyrebase
import sqlite3
import hashlib

#from Models import Models
from .Schemas import Schemas
# from Conexion import Conexion

app = FastAPI()

origins = [
    "http://127.0.0.1:8000",
    "http://0.0.0.0:8080",
    "http://localhost:8080",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

firebaseConfig = {
    "apiKey": "AIzaSyCqcAsOlCtnuCEmUIUgJJvTeHg9n2xjCg4",
    "authDomain": "loginapirest-b1c29.firebaseapp.com",
    "databaseURL": "https://loginapirest-b1c29-default-rtdb.firebaseio.com/",
    "projectId": "loginapirest-b1c29",
    "storageBucket": "loginapirest-b1c29.appspot.com",
    "messagingSenderId": "364265836121",
    "appId": "1:364265836121:web:09a406b3328d87323f6b48",
    "measurementId": "G-DVS09D026Q"
  };

firebase = pyrebase.initialize_app(firebaseConfig)

auth = firebase.auth()
db = firebase.database()

securityBasic = HTTPBasic()
securityBearer = HTTPBearer()

"""
Obtener el nivel de acceso del usuario desde sqlite

def get_current_level(crendentials: HTTPBasicCredentials = Depends(securityBasic)):
    password_b = hashlib.md5(crendentials.password.encode())
    password = password_b.hexdigest()
    with sqlite3.connect('backend_Good/sql/clientes.sqlite') as connection:
        cursor = connection.cursor()
        cursor.execute(
            "SELECT level FROM usuarios WHERE username = ? and password = ?",
            (crendentials.username, password),
        )
        user = cursor.fetchone()
        if user is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Incorrect username or password")
        return user[0]
"""
def get_level(token: str):
    user = auth.get_account_info(token)
    uid = user['users'][0]['localId']
    return db.child('users').child(uid).child('level').get().val()

@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url='/docs')

@app.get(
    "/clientes",
    response_model=List[Schemas.Usuario],
    status_code = status.HTTP_202_ACCEPTED,
    summary="Obtiene todos los clientes",
    description="Obtiene todos los clientes",
    tags=["clientes"],
)
async def get_clientes(offsent: int = 0, limit: int = 10,credentials: HTTPAuthorizationCredentials = Depends(securityBearer)):
    token = credentials.credentials
    level=get_level(token)
    if level == 'User':
        with sqlite3.connect("backend/sql/clientes.sqlite") as connection:
            connection.row_factory = sqlite3.Row
            cursor = connection.cursor()
            cursor.execute(
                "SELECT id_cliente, nombre, email FROM clientes LIMIT ? OFFSET ?",
                (limit, offsent),
            )
            clientes = cursor.fetchall()
            if not clientes:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="No hay clientes",
                )
        return clientes
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para ver los clientes",
            headers={"WWW-Authenticate": "Basic"},
        )

@app.get(
    "/clientes/{id_cliente}",
    response_model=Schemas.Usuario,
    status_code = status.HTTP_202_ACCEPTED,
    summary="Obtiene un cliente",
    description="Obtiene un cliente",
    tags=["clientes"],
)
async def get_cliente(id_cliente: int, credentials: HTTPAuthorizationCredentials = Depends(securityBearer)):
    token = credentials.credentials
    level=get_level(token)
    if level == 'User':
        with sqlite3.connect("backend/sql/clientes.sqlite") as connection:
            connection.row_factory = sqlite3.Row
            cursor = connection.cursor()
            cursor.execute(
                "SELECT id_cliente, nombre, email FROM clientes WHERE id_cliente = ?",
                (id_cliente,),
            )
            cliente = cursor.fetchone()
            if not cliente:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="No hay cliente con ese id",
                )
        return cliente
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para ver el cliente",
            headers={"WWW-Authenticate": "Basic"},
        )

@app.post(
    "/clientes",
    response_model=Schemas.Mensaje,
    status_code = status.HTTP_202_ACCEPTED,
    summary="Crea un cliente",
    description="Crea un cliente",
    tags=["clientes"],
)
async def create_cliente(cliente: Schemas.UsuarioNew, credentials: HTTPAuthorizationCredentials = Depends(securityBearer)):
    token = credentials.credentials
    level=get_level(token)
    if level == "Admin":
        with sqlite3.connect("backend/sql/clientes.sqlite") as connection:
            connection.row_factory = sqlite3.Row
            cursor = connection.cursor()
            cursor.execute(
                "INSERT INTO clientes (nombre, email) VALUES (?, ?)",
                (cliente.nombre, cliente.email),
            )
            connection.commit()
        return {"mensaje": "Cliente creado"}
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para crear un cliente",
            headers={"WWW-Authenticate": "Basic"},
        )

@app.put(
    "/clientes/{id_cliente}",
    response_model=Schemas.Mensaje,
    status_code = status.HTTP_202_ACCEPTED,
    summary="Actualiza un cliente",
    description="Actualiza un cliente",
    tags=["clientes"],
)
async def update_cliente(id_cliente: int, cliente: Schemas.UsuarioUpdate, credentials: HTTPAuthorizationCredentials = Depends(securityBearer)):
    token = credentials.credentials
    level=get_level(token)
    if level == "Admin":
        with sqlite3.connect("backend/sql/clientes.sqlite") as connection:
            connection.row_factory = sqlite3.Row
            cursor = connection.cursor()
            cursor.execute(
                "UPDATE clientes SET nombre = ?, email = ? WHERE id_cliente = ?",
                (cliente.nombre, cliente.email, id_cliente),
            )
            connection.commit()
        return {"mensaje": "Cliente actualizado"}
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para actualizar el cliente",
            headers={"WWW-Authenticate": "Basic"},
        )

@app.delete(
    "/clientes/{id_cliente}",
    response_model=Schemas.Mensaje,
    status_code = status.HTTP_202_ACCEPTED,
    summary="Elimina un cliente",
    description="Elimina un cliente",
    tags=["clientes"],
)
async def delete_cliente(id_cliente: int, credentials: HTTPAuthorizationCredentials = Depends(securityBearer)):
    token = credentials.credentials
    level=get_level(token)
    if level == "Admin":
        with sqlite3.connect("backend/sql/clientes.sqlite") as connection:
            connection.row_factory = sqlite3.Row
            cursor = connection.cursor()
            cursor.execute(
                "DELETE FROM clientes WHERE id_cliente = ?",
                (id_cliente,),
            )
            connection.commit()
        return {"mensaje": "Cliente eliminado"}
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para eliminar el cliente",
            headers={"WWW-Authenticate": "Basic"},
        )

@app.get(
    "/user/validate",
    response_model=Schemas.Token,
    status_code = status.HTTP_202_ACCEPTED,
    summary="Get a token for a user",
    description="Get a Token for user",
    tags=["auth"],
)
async def get_token(credentials: HTTPBasicCredentials = Depends(securityBasic)):
    try:
      user = credentials.username
      password = credentials.password
      user = auth.sign_in_with_email_and_password(user, password)
      response = {
        "token": user['idToken'],
      }
      return response
    except Exception as e:
      print(f"Error: {e}")
      raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=e)

@app.get(
    "/user/info",
    #response_model=Schemas.Usuario,
    status_code = status.HTTP_202_ACCEPTED,
    summary="Get user info",
    description="Get user info",
    tags=["auth"],
)
async def get_user_info(credentials: HTTPAuthorizationCredentials = Depends(securityBearer)):
    try:
      user = auth.get_account_info(credentials.credentials)
      uid = user['users'][0]['localId']
      users_data = db.child("users").child(uid).get().val()
      response = {
        "user": users_data,
      }
      return response
    except Exception as e:
      print(f"Error: {e}")
      raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=e)

@app.post(
    "/user/register",
    response_model=Schemas.Mensaje,
    status_code = status.HTTP_202_ACCEPTED,
    summary="Create a user with email and password",
    description="Create a user with email and password",
    tags=["auth"],
)
async def create_user(user_new: Schemas.UsuarioNew):
  try:
    user = auth.create_user_with_email_and_password(user_new.email, user_new.password)
    user = auth.sign_in_with_email_and_password(user_new.email, user_new.password)
    uid = user['localId']
    data= {
      "nombre":user_new.name,
      "level":"User"
      }
    userData = db.child("users").child(uid).set(data)
    mensaje = "Usuario creado"
    return mensaje

  except Exception as e:
    print(f"Error: {e}")
