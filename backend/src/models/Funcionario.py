from sqlalchemy import Column, Integer, VARCHAR
from sqlalchemy.orm import relationship
from src.models import Funcionario

# from database import Base

class Funcionario(Base):
    __tablename__ = 'Funcionario'

    id = Column(Integer, primary_key=True)
    Nome = Column(VARCHAR(255), nullable=True)

    entregas = relationship('Entrega', back_populates='funcionario')
    cargos_funcionarios = relationship('CargoFuncionario', back_populates='funcionario')

    def __init__(self, Nome=None):
        self.Nome = Nome

__all__ = ["Funcionario"]