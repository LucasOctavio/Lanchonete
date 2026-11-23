from sqlalchemy import Column, Integer
from sqlalchemy.orm import relationship
# from database import Base
from src.models import Mesa

__all__ = ["Mesa"]

class Mesa(Base):
    __tablename__ = 'Mesa'

    id = Column(Integer, primary_key=True)
    Numero = Column(Integer, nullable=True)

    pedidos = relationship('Pedido', back_populates='mesa')

    def __init__(self, Numero=None):
        self.Numero = Numero