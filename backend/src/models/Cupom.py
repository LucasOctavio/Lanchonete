from sqlalchemy import Column, Integer, VARCHAR, DECIMAL, DateTime, ForeignKey
from sqlalchemy.orm import relationship
# from database import Base

class Cupom(Base):
    __tablename__ = 'Cupom'

    Codigo = Column(VARCHAR(20), primary_key=True)
    Cliente_id = Column(Integer, ForeignKey('Cliente.id'), nullable=False)
    Valor = Column(DECIMAL(10, 2), nullable=True)
    Percentual = Column(DECIMAL(5, 1), nullable=True)
    DataValidade = Column(DateTime, nullable=True)

    cliente = relationship('Cliente', back_populates='cupons')
    pedidos = relationship('Pedido', back_populates='cupom')

    def __init__(self, Codigo, Cliente_id, Valor=None, Percentual=None, DataValidade=None):
        self.Codigo = Codigo
        self.Cliente_id = Cliente_id
        self.Valor = Valor
        self.Percentual = Percentual
        self.DataValidade = DataValidade