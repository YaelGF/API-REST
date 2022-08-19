# Base Model
from pydantic import BaseModel

class Usuario(BaseModel):
    id_cliente: int
    nombre: str
    email: str

class UsuarioNew(BaseModel):
    nombre: str
    email: str

class UsuarioID(BaseModel):
    id_usuario: int

class UsuarioUpdate(BaseModel):
    nombre: str
    email: str

class Mensaje(BaseModel):
    mensaje: str

class User(BaseModel):
    username: str
    level: int

class Token(BaseModel):
    token: str

class UserNew(BaseModel):
    email: str
    password: str
    name: str