from sqlalchemy import Column, Integer, VARCHAR, ForeignKey
from sqlalchemy.orm import relationship
from src.models import Cliente

# from database import Base

class Cliente(Base):
    __tablename__ = 'Cliente'

    id = Column(Integer, primary_key=True)
    Pedido_id = Column(Integer, ForeignKey('Pedido.id'), nullable=False)
    Nome = Column(VARCHAR(255), nullable=True)
    Endereco = Column(VARCHAR(255), nullable=True)
    Contato = Column(VARCHAR(20), nullable=True)

    pedido = relationship('Pedido', back_populates='clientes')
    cupons = relationship('Cupom', back_populates='cliente')

    def __init__(self, Pedido_id, Nome=None, Endereco=None, Contato=None):
        self.Pedido_id = Pedido_id
        self.Nome = Nome
        self.Endereco = Endereco
        self.Contato = Contato

__all__ = ["Cliente"]