from sqlalchemy import Column, Integer, VARCHAR, DECIMAL, ForeignKey
from sqlalchemy.orm import relationship
from src.models import Ingrediente

class Ingrediente(Base):
    __tablename__ = 'Ingrediente'

    id = Column(Integer, primary_key=True)
    Fornecedor_id = Column(Integer, ForeignKey('Fornecedor.id'), nullable=False)
    Nome = Column(VARCHAR(45), nullable=True)
    QtdEstoque = Column(DECIMAL(10, 3), nullable=True)
    UniMedida = Column(VARCHAR(10), nullable=True)

    fornecedor = relationship('Fornecedor', back_populates='ingredientes')
    ingredientes_produtos = relationship('IngredienteProduto', back_populates='ingrediente')

    def __init__(self, Fornecedor_id, Nome=None, QtdEstoque=None, UniMedida=None):
        self.Fornecedor_id = Fornecedor_id
        self.Nome = Nome
        self.QtdEstoque = QtdEstoque
        self.UniMedida = UniMedida

__all__ = ["Ingrediente"]