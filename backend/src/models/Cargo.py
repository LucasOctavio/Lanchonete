from sqlalchemy import Column, Integer, VARCHAR
from sqlalchemy.orm import relationship
from src.models import Cargo

__all__ = ["Cargo"]

# from database import Base

class Cargo(Base):
    __tablename__ = 'Cargo'

    id = Column(Integer, primary_key=True)
    Funcao = Column(VARCHAR(50), nullable=True)

    cargos_funcionarios = relationship('CargoFuncionario', back_populates='cargo')

    def __init__(self, Funcao=None):
        self.Funcao = Funcao