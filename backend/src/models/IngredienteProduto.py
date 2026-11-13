from sqlalchemy import Column, Integer, VARCHAR, ForeignKey
from sqlalchemy.orm import relationship
# from database import Base

class IngredienteProduto(Base):
    __tablename__ = 'Ingrediente_Produto'

    Ingredientes_id = Column(Integer, ForeignKey('Ingrediente.id'), primary_key=True, nullable=False)
    Produto_id = Column(Integer, ForeignKey('Produto.id'), primary_key=True, nullable=False)
    Quantidade = Column(VARCHAR(45), nullable=True)

    ingrediente = relationship('Ingrediente', back_populates='ingredientes_produtos')
    produto = relationship('Produto', back_populates='ingredientes_produtos')

    def __init__(self, Ingredientes_id, Produto_id, Quantidade=None):
        self.Ingredientes_id = Ingredientes_id
        self.Produto_id = Produto_id
        self.Quantidade = Quantidade