from sqlalchemy import Column, Integer, VARCHAR, DateTime
from sqlalchemy.orm import relationship
from src.models import Status

# from database import Base

class Status(Base):
    __tablename__ = 'Status'

    id = Column(Integer, primary_key=True)
    Status = Column(VARCHAR(30), nullable=False)
    DataHora = Column(DateTime, nullable=False)

    pedidos = relationship('Pedido', back_populates='status')

    def __init__(self, Status, DataHora):
        self.Status = Status
        self.DataHora = DataHora

__all__ = ["Status"]