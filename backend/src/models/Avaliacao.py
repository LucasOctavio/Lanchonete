from sqlalchemy import *
from sqlalchemy.orm import relationship

class Avaliacao(Base):
    __tablename__ = 'Avaliacao'

    id = Column(Integer, primary_key=True)
    Pedido_id = Column(Integer, ForeignKey('Pedido.id'), nullable=False)
    Mensagem = Column(VARCHAR(100), nullable=True)  # Ajustar para 255/1000 se necessário
    Nota = Column(SmallInteger, nullable=True)

    pedido = relationship('Pedido', back_populates='avaliacoes')

    def __init__(self, Pedido_id, Mensagem=None, Nota=None):
        self.Pedido_id = Pedido_id
        self.Mensagem = Mensagem
        self.Nota = Nota