import email
from sqlite3 import Cursor
from . import conexion
import sqlite3


def Create(nombre:str,email:str):
    cursor = conexion.conectar()
    cursor.execute( 
        "INSERT INTO clientes(nombre, email) values('?','?')",
        (nombre,email)
    )

def Read(limit:int=2,offset:int=0):
    cursor = conexion.conectar()
    cursor.execute(
        "SELECT * FROM clientes LIMIT ? OFFSET ?",(limit,offset),
    )
    response = cursor.fetchall()
    return response

def Update(nombre: str, email:str, id_cliente:int):
    cursor = conexion.conectar()
    cursor.execute( 
        "UPDATE clientes set nombre = '?', email = '?' WHERE id_cliente = ?",
        (nombre,email,id_cliente),
    )

def Delete(id_cliente:int):
    cursor = conexion.conectar()
    cursor.execute( 
        "DELETE FROM clientes Where id_cliente = ?",
        (id_cliente),
    )

def Read_with_Params(id_cliente:int):
    cursor = conexion.conectar()
    cursor.execute(
                "SELECT * FROM clientes WHERE id_cliente = ?",(id_cliente,)
            )
    query = cursor.fetchone()
    return query