from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, Boolean, Text, LargeBinary, Date, Time, DateTime
from sqlalchemy.orm import relationship
from .Conexion import Conexion

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False)