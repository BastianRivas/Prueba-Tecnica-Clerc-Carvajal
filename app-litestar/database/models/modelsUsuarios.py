from sqlalchemy import Column, Integer, String, Float
from ..session import Base, engine


class Usuario(Base):
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    rol = Column(String(50), nullable=False)
    renta_mensual = Column(Float(), nullable=False)

