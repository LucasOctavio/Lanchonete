from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
# from database import Base

class Historico(Base):
    __tablename__ = 'Historico'

    id = Column(Integer, primary_key=True)
    Pedido_id = Column(Integer, ForeignKey('Pedido.id'), nullable=False)
    DataHora = Column(DateTime, nullable=True)

    pedido = relationship('Pedido', back_populates='historicos')

    def __init__(self, Pedido_id, DataHora=None):
        self.Pedido_id = Pedido_id
        self.DataHora = DataHora