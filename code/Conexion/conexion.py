from requests import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

engine = create_engine('sqlite:///clientes.sqlite', echo=True)

Base = declarative_base()

Session = sessionmaker(bind=engine)
session = Session()

class Customers(Base):
   __tablename__ = 'clientes'
   id_customer = Column(Integer, primary_key=True)
   name = Column(String)
   email = Column(String)

   def __repr__(self):
      return "<Customers(name='%s', email='%s')>" % (self.name, self.email)

class User(Base):
   __tablename__ = 'user'
   id_user = Column(Integer, primary_key=True)
   user = Column(String)
   password = Column(String(32))
   level = Column(String)

   def __repr__(self) -> str:
      return "<User(user='%s', password='%s', level='%s')>" % (self.user, self.password, self.level)


Base.metadata.create_all(engine)

nueva_fila = Customers(name='Juan', email='juan@correo')
session.add(nueva_fila)
session.commit()

print(session.query(Customers).all())

