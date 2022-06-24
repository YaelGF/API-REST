import email
from sqlite3 import Cursor
from .Conexion import conexion

def Create(nombre:str,email:str):
    cursor = conexion.OpenConexion()
    cursor.execute( "INSERT INTO clientes(nombre, email) values('?','?')",
    (nombre,email),)

def Read(limit:int=10,offset:int=0):
    cursor = conexion.OpenConexion()
    cursor.execute( "SELECT * FROM clientes LIMIT = ? OFFSET = ?",
    (limit,offset),)
    query = cursor.fetchall()
    return query

def Update(nombre: str, email:str, id_cliente:int):
    cursor = conexion.OpenConexion()
    cursor.execute( 
        "UPDATE clientes set nombre = '?', email = '?' WHERE id_cliente = ?",
        (nombre,email,id_cliente),)

def Delete(id_cliente:int):
    cursor = conexion.OpenConexion()
    cursor.execute( "DELETE FROM clientes Where id_cliente = ?",
        (id_cliente),)

def Read_with_Params(id_cliente:int):
    cursor = conexion.OpenConexion()
    cursor.execute( "SELECT * FROM clientes Where id_cliente = ?",
        (id_cliente),)
    query = cursor.fetchone()
    return query