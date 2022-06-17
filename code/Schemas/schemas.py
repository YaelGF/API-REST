from pydantic import BaseModel

class Respuesta(BaseModel):
    message: str

class Cliente(BaseModel):
    id_cliente: int
    nombre: str
    email: str

class ClienteNew(BaseModel):
    nombre: str
    email: str

