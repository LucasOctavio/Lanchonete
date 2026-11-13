from sqlalchemy import Column, Integer, VARCHAR, DECIMAL, ForeignKey
from sqlalchemy.orm import relationship
# from database import Base

class Entrega(Base):
    __tablename__ = 'Entrega'

    id = Column(Integer, primary_key=True)
    Funcionario_id = Column(Integer, ForeignKey('Funcionario.id'), nullable=False)
    Pedido_id = Column(Integer, ForeignKey('Pedido.id'), nullable=False)
    Endereco = Column(VARCHAR(255), nullable=True)
    Taxa = Column(DECIMAL(10, 2), nullable=True)

    funcionario = relationship('Funcionario', back_populates='entregas')
    pedido = relationship('Pedido', back_populates='entregas')

    def __init__(self, Funcionario_id, Pedido_id, Endereco=None, Taxa=None):
        self.Funcionario_id = Funcionario_id
        self.Pedido_id = Pedido_id
        self.Endereco = Endereco
        self.Taxa = Taxa