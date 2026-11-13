from sqlalchemy import Column, Integer, DECIMAL, ForeignKey
from sqlalchemy.orm import relationship
# from database import Base

class Pagamento(Base):
    __tablename__ = 'Pagamento'

    id = Column(Integer, primary_key=True)
    Pedido_id = Column(Integer, ForeignKey('Pedido.id'), nullable=False)
    Cartao = Column(DECIMAL(10, 2), nullable=True)
    Dinheiro = Column(DECIMAL(10, 2), nullable=True)
    Pix = Column(DECIMAL(10, 2), nullable=True)

    pedido = relationship('Pedido', back_populates='pagamentos')

    def __init__(self, Pedido_id, Cartao=None, Dinheiro=None, Pix=None):
        self.Pedido_id = Pedido_id
        self.Cartao = Cartao
        self.Dinheiro = Dinheiro
        self.Pix = Pix