from sqlalchemy import Column, Integer, VARCHAR, DECIMAL, ForeignKey
from sqlalchemy.orm import relationship
# from database import Base

class Combo(Base):
    __tablename__ = 'combo'

    id = Column(Integer, primary_key=True)
    Item_id = Column(Integer, ForeignKey('Item.id'), nullable=False)
    Nome = Column(VARCHAR(100), nullable=True)
    Promocao = Column(DECIMAL(10, 2), nullable=True)

    item = relationship('Item', back_populates='combos')

    def __init__(self, Item_id, Nome=None, Promocao=None):
        self.Item_id = Item_id
        self.Nome = Nome
        self.Promocao = Promocao