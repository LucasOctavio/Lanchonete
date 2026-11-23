from sqlalchemy import Column, Integer, VARCHAR, DECIMAL, ForeignKey
from sqlalchemy.orm import relationship
from src.models import Produto

__all__ = ["Produto"]

# from database import Base
# from models.Promocao import promocao_produto

class Produto(Base):
    __tablename__ = 'Produto'

    id = Column(Integer, primary_key=True)
    Categoria_id = Column(Integer, ForeignKey('Categoria.id'), nullable=False)
    Nome = Column(VARCHAR(200), nullable=True)
    Preco = Column(DECIMAL(10, 2), nullable=True)
    Tamanho = Column(VARCHAR(45), nullable=True)
    ponto = Column(VARCHAR(45), nullable=True)

    categoria = relationship('Categoria', back_populates='produtos')
    pedidos = relationship('Pedido', foreign_keys='Pedido.Produto_id', back_populates='produto')
    itens = relationship('Item', foreign_keys='Item.Produto_id', back_populates='produto')
    promocoes = relationship('Promocao', secondary='Promocao_Produto', back_populates='produtos')
    ingredientes_produtos = relationship('IngredienteProduto', back_populates='produto')

    def __init__(self, Categoria_id, Nome=None, Preco=None, Tamanho=None, ponto=None):
        self.Categoria_id = Categoria_id
        self.Nome = Nome
        self.Preco = Preco
        self.Tamanho = Tamanho
        self.ponto = ponto