import sqlite3


def conectar():
    conexion = sqlite3.connect("code/sql/clientes.sqlite")
    return conexion.cursor()


def close(conexion):
    conexion.close()
