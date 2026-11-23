from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from src.models import CargoFuncionario

__all__ = ["CargoFuncionario"]

# from database import Base

class CargoFuncionario(Base):
    __tablename__ = 'Cargo_Funcionario'

    DataInicio = Column(DateTime, primary_key=True, nullable=False)
    Cargo_id = Column(Integer, ForeignKey('Cargo.id'), nullable=False)
    Funcionario_id = Column(Integer, ForeignKey('Funcionario.id'), nullable=False)
    DataFim = Column(DateTime, nullable=True)

    cargo = relationship('Cargo', back_populates='cargos_funcionarios')
    funcionario = relationship('Funcionario', back_populates='cargos_funcionarios')

    def __init__(self, DataInicio, Cargo_id, Funcionario_id, DataFim=None):
        self.DataInicio = DataInicio
        self.Cargo_id = Cargo_id
        self.Funcionario_id = Funcionario_id
        self.DataFim = DataFim