from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
# from database import Base

class Item(Base):
    __tablename__ = 'Item'

    id = Column(Integer, primary_key=True)
    Produto_id = Column(Integer, ForeignKey('Produto.id'), nullable=False)
    Produto_Categoria_id = Column(Integer, ForeignKey('Produto.Categoria_id'), nullable=False)
    Quantidade = Column(Integer, nullable=True)

    produto = relationship('Produto', foreign_keys=[Produto_id], back_populates='itens')
    combos = relationship('Combo', back_populates='item')
    adicionais = relationship('Adicional', back_populates='item')

    def __init__(self, Produto_id, Produto_Categoria_id, Quantidade=None):
        self.Produto_id = Produto_id
        self.Produto_Categoria_id = Produto_Categoria_id
        self.Quantidade = Quantidade