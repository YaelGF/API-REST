from .Conexion import conexion

def Create():

def Read(limit:int=10,offset:int=0):
    cursor = conexion.OpenConexion()
    cursor.execute( "SELECT * FROM clientes LIMIT = ? OFFSET = ?",
    (limit,offset),)
    query = cursor.fetchall()
    return query

def Update():


def Delete():