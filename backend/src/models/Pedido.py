from sqlalchemy import Column, Integer, VARCHAR, DateTime, ForeignKey
from sqlalchemy.orm import relationship
# from database import Base

class Pedido(Base):
    __tablename__ = 'Pedido'

    id = Column(Integer, primary_key=True)
    Mesa_id = Column(Integer, ForeignKey('Mesa.id'), nullable=False)
    Produto_id = Column(Integer, ForeignKey('Produto.id'), nullable=False)
    Produto_Categoria_id = Column(Integer, ForeignKey('Produto.Categoria_id'), nullable=False)
    Status_id = Column(Integer, ForeignKey('Status.id'), nullable=False)
    Cupom_Codigo = Column(VARCHAR(20), ForeignKey('Cupom.Codigo'), nullable=False)
    Tipo = Column(VARCHAR(20), nullable=True)
    DataHora = Column(DateTime, nullable=True)

    mesa = relationship('Mesa', back_populates='pedidos')
    produto = relationship('Produto', foreign_keys=[Produto_id], back_populates='pedidos')
    status = relationship('Status', back_populates='pedidos')
    cupom = relationship('Cupom', back_populates='pedidos')
    clientes = relationship('Cliente', back_populates='pedido')
    pagamentos = relationship('Pagamento', back_populates='pedido')
    avaliacoes = relationship('Avaliacao', back_populates='pedido')
    historicos = relationship('Historico', back_populates='pedido')
    entregas = relationship('Entrega', back_populates='pedido')

    def __init__(self, Mesa_id, Produto_id, Produto_Categoria_id, Status_id, Cupom_Codigo, Tipo=None, DataHora=None):
        self.Mesa_id = Mesa_id
        self.Produto_id = Produto_id
        self.Produto_Categoria_id = Produto_Categoria_id
        self.Status_id = Status_id
        self.Cupom_Codigo = Cupom_Codigo
        self.Tipo = Tipo
        self.DataHora = DataHora