import email
from sqlite3 import Cursor
from . import conexion
import sqlite3


def Create(nombre:str,email:str):
    cursor = conexion.OpenConexion()
    cursor.execute( "INSERT INTO clientes(nombre, email) values('?','?')",
    (nombre,email))

def Read(limit:int=0,offset:int=10):
    with sqlite3.connect('code/sql/clientes.sqlite') as connection:
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM clientes  LIMIT {limit}  OFFSET {offset}'.format(offset=offset,limit=limit))
        response = cursor.fetchall()
        return response

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