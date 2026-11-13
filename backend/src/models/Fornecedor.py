from sqlalchemy import Column, Integer, VARCHAR
from sqlalchemy.orm import relationship
# from database import Base

class Fornecedor(Base):
    __tablename__ = 'Fornecedor'

    id = Column(Integer, primary_key=True)
    Nome = Column(VARCHAR(100), nullable=True)
    Contato = Column(VARCHAR(50), nullable=True)

    ingredientes = relationship('Ingrediente', back_populates='fornecedor')

    def __init__(self, Nome=None, Contato=None):
        self.Nome = Nome
        self.Contato = Contato