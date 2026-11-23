from sqlalchemy import Column, Integer, VARCHAR, DECIMAL, ForeignKey
from sqlalchemy.orm import relationship
# from database import Base
from src.models import Adicional

class Adicional(Base):
    __tablename__ = 'Adicional'

    id = Column(Integer, primary_key=True)
    Item_id = Column(Integer, ForeignKey('Item.id'), nullable=False)
    Nome = Column(VARCHAR(100), nullable=True)
    Preco = Column(DECIMAL(10, 2), nullable=True)

    item = relationship('Item', back_populates='adicionais')

    def __init__(self, Item_id, Nome=None, Preco=None):
        self.Item_id = Item_id
        self.Nome = Nome
        self.Preco = Preco

__all__ = ["Adicional"]