
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy import MetaData
from sqlalchemy import Table, Column,Integer, String
from sqlalchemy import insert, select, update, delete
Database_URL = "sqlite:///db.sqlite"

engine = create_engine(Database_URL)

metadata = MetaData()

def querys(query):
    with engine.connect() as conn:
        conn.execute(query)

users = Table(
    "users",
    metadata,
    Column("id_user",Integer, primary_key=True, autoincrement=True),
    Column("nombre",String(50), nullable=False),
    Column("email",String(50), nullable=False)
)

metadata.create_all(engine)

stmt = insert(users).values(nombre="Yael",email="yael@gmail.com")

querys(stmt)

data = [
    {"nombre":"Cliente 1","email":"cliente1@gmail.com"},
    {"nombre":"Cliente 2","email":"cliente@gmail.com"}
    ]

stmt = insert(users).values(data)

querys(stmt)

query = select(users)

with engine.connect() as conn:
    result = conn.execute(query)
    for row in result.fetchall():
        print(f"Name: {row.nombre}, email: {row.email}")




        