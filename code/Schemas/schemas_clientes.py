from pydantic import BaseModel

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


