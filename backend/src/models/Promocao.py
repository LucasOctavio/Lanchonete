from sqlalchemy import Column, Integer, VARCHAR, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship
from src.models import Promocao, promocao_produto

__all__ = ["Promocao", "promocao_produto"]

promocao_produto = Table(
    'Promocao_Produto',
    Base.metadata,
    Column('Promocao_id', Integer, ForeignKey('Promocao.id'), primary_key=True),
    Column('Produto_id', Integer, ForeignKey('Produto.id'), primary_key=True)
)

class Promocao(Base):
    __tablename__ = 'Promocao'

    id = Column(Integer, primary_key=True)
    Nome = Column(VARCHAR(100), nullable=True)
    DataInicio = Column(DateTime, nullable=True)
    DataFim = Column(DateTime, nullable=True)

    produtos = relationship('Produto', secondary=promocao_produto, back_populates='promocoes')

    def __init__(self, Nome=None, DataInicio=None, DataFim=None):
        self.Nome = Nome
        self.DataInicio = DataInicio
        self.DataFim = DataFim