from sqlalchemy import Column, Integer, VARCHAR
from sqlalchemy.orm import relationship
# from database import Base

class Categoria(Base):
    __tablename__ = 'Categoria'

    id = Column(Integer, primary_key=True)
    Nome = Column(VARCHAR(50), nullable=True)

    produtos = relationship('Produto', back_populates='categoria')

    def __init__(self, Nome=None):
        self.Nome = Nome