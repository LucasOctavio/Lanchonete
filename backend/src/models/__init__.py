from datetime import datetime

from sqlalchemy import (Column, DateTime, DECIMAL, ForeignKey, Integer,
                       SmallInteger, String, Table)
from sqlalchemy.orm import relationship

from src.db.db import Base


promocao_produto = Table(
    "Promocao_Produto",
    Base.metadata,
    Column("Promocao_id", Integer, ForeignKey("Promocao.id", ondelete="CASCADE"), primary_key=True),
    Column("Produto_id", Integer, ForeignKey("Produto.id", ondelete="CASCADE"), primary_key=True),
)


class Categoria(Base):
    __tablename__ = "Categoria"
    id = Column(Integer, primary_key=True, index=True)
    Nome = Column(String(50), nullable=True)
    produtos = relationship("Produto", back_populates="categoria")


class Fornecedor(Base):
    __tablename__ = "Fornecedor"
    id = Column(Integer, primary_key=True, index=True)
    Nome = Column(String(100), nullable=True)
    Contato = Column(String(50), nullable=True)
    ingredientes = relationship("Ingrediente", back_populates="fornecedor")


class Ingrediente(Base):
    __tablename__ = "Ingrediente"
    id = Column(Integer, primary_key=True, index=True)
    Fornecedor_id = Column(Integer, ForeignKey("Fornecedor.id"), nullable=False)
    Nome = Column(String(45), nullable=True)
    QtdEstoque = Column(DECIMAL(10, 3), default=0)
    UniMedida = Column(String(10), nullable=True)
    fornecedor = relationship("Fornecedor", back_populates="ingredientes")
    produtos = relationship("IngredienteProduto", back_populates="ingrediente")


class ReposicaoEstoque(Base):
    __tablename__ = "Reposicao_Estoque"
    id = Column(Integer, primary_key=True, index=True)
    Ingrediente_id = Column(Integer, ForeignKey("Ingrediente.id"), nullable=False)
    Quantidade = Column(DECIMAL(10, 3), nullable=False)
    DataHora = Column(DateTime, nullable=False, default=datetime.utcnow)


class Produto(Base):
    __tablename__ = "Produto"
    id = Column(Integer, primary_key=True, index=True)
    Categoria_id = Column(Integer, ForeignKey("Categoria.id"), nullable=False)
    Nome = Column(String(200), nullable=True)
    Preco = Column(DECIMAL(10, 2), nullable=True)
    Tamanho = Column(String(45), nullable=True)
    ponto = Column(String(45), nullable=True)
    categoria = relationship("Categoria", back_populates="produtos")
    ingredientes = relationship("IngredienteProduto", back_populates="produto")
    promocoes = relationship("Promocao", secondary=promocao_produto, back_populates="produtos")


class IngredienteProduto(Base):
    __tablename__ = "Ingrediente_Produto"
    Ingredientes_id = Column(Integer, ForeignKey("Ingrediente.id", ondelete="CASCADE"), primary_key=True)
    Produto_id = Column(Integer, ForeignKey("Produto.id", ondelete="CASCADE"), primary_key=True)
    Quantidade = Column(String(45), nullable=True)
    ingrediente = relationship("Ingrediente", back_populates="produtos")
    produto = relationship("Produto", back_populates="ingredientes")


class Mesa(Base):
    __tablename__ = "Mesa"
    id = Column(Integer, primary_key=True, index=True)
    Numero = Column(Integer, nullable=True, unique=True)


class Status(Base):
    __tablename__ = "Status"
    id = Column(Integer, primary_key=True, index=True)
    Status = Column(String(30), nullable=False)
    DataHora = Column(DateTime, nullable=False, default=datetime.utcnow)


class Cupom(Base):
    __tablename__ = "Cupom"
    Codigo = Column(String(20), primary_key=True)
    Cliente_id = Column(Integer, ForeignKey("Cliente.id"), nullable=True)
    Valor = Column(DECIMAL(10, 2), nullable=True)
    Percentual = Column(DECIMAL(5, 1), nullable=True)
    DataValidade = Column(DateTime, nullable=True)


class Pedido(Base):
    __tablename__ = "Pedido"
    id = Column(Integer, primary_key=True, index=True)
    Mesa_id = Column(Integer, ForeignKey("Mesa.id"), nullable=True)
    Produto_id = Column(Integer, ForeignKey("Produto.id"), nullable=True)
    Status_id = Column(Integer, ForeignKey("Status.id"), nullable=True)
    Cupom_Codigo = Column(String(20), ForeignKey("Cupom.Codigo"), nullable=True)
    Tipo = Column(String(20), nullable=True)
    DataHora = Column(DateTime, nullable=False, default=datetime.utcnow)


class CancelamentoPedido(Base):
    __tablename__ = "Cancelamento_Pedido"
    id = Column(Integer, primary_key=True, index=True)
    Pedido_id = Column(Integer, ForeignKey("Pedido.id", ondelete="CASCADE"), nullable=False)
    Motivo = Column(String(500), nullable=False)
    DataHora = Column(DateTime, nullable=False, default=datetime.utcnow)


class Cliente(Base):
    __tablename__ = "Cliente"
    id = Column(Integer, primary_key=True, index=True)
    Pedido_id = Column(Integer, ForeignKey("Pedido.id"), nullable=True)
    Nome = Column(String(255), nullable=True)
    Endereco = Column(String(255), nullable=True)
    Contato = Column(String(20), nullable=True)


class UsuarioCliente(Base):
    __tablename__ = "Usuario_Cliente"
    id = Column(Integer, primary_key=True, index=True)
    Nome = Column(String(255), nullable=False)
    Email = Column(String(255), unique=True, nullable=False)
    Telefone = Column(String(20), nullable=True)
    Senha = Column(String(255), nullable=False)


class Pagamento(Base):
    __tablename__ = "Pagamento"
    id = Column(Integer, primary_key=True, index=True)
    Pedido_id = Column(Integer, ForeignKey("Pedido.id", ondelete="CASCADE"), nullable=False)
    Cartao = Column(DECIMAL(10, 2), nullable=True)
    Dinheiro = Column(DECIMAL(10, 2), nullable=True)
    Pix = Column(DECIMAL(10, 2), nullable=True)


class Avaliacao(Base):
    __tablename__ = "Avaliacao"
    id = Column(Integer, primary_key=True, index=True)
    Pedido_id = Column(Integer, ForeignKey("Pedido.id", ondelete="CASCADE"), nullable=False)
    Mensagem = Column(String(255), nullable=True)
    Nota = Column(SmallInteger, nullable=True)


class Historico(Base):
    __tablename__ = "Historico"
    id = Column(Integer, primary_key=True, index=True)
    Pedido_id = Column(Integer, ForeignKey("Pedido.id", ondelete="CASCADE"), nullable=False)
    DataHora = Column(DateTime, nullable=False, default=datetime.utcnow)


class Funcionario(Base):
    __tablename__ = "Funcionario"
    id = Column(Integer, primary_key=True, index=True)
    Nome = Column(String(255), nullable=True)


class Cargo(Base):
    __tablename__ = "Cargo"
    id = Column(Integer, primary_key=True, index=True)
    Funcao = Column(String(50), nullable=True)


class CargoFuncionario(Base):
    __tablename__ = "Cargo_Funcionario"
    id = Column(Integer, primary_key=True, index=True)
    DataInicio = Column(DateTime, nullable=False, default=datetime.utcnow)
    Cargo_id = Column(Integer, ForeignKey("Cargo.id"), nullable=False)
    Funcionario_id = Column(Integer, ForeignKey("Funcionario.id"), nullable=False)
    DataFim = Column(DateTime, nullable=True)


class Entrega(Base):
    __tablename__ = "Entrega"
    id = Column(Integer, primary_key=True, index=True)
    Funcionario_id = Column(Integer, ForeignKey("Funcionario.id"), nullable=False)
    Pedido_id = Column(Integer, ForeignKey("Pedido.id", ondelete="CASCADE"), nullable=False)
    Endereco = Column(String(255), nullable=True)
    Taxa = Column(DECIMAL(10, 2), nullable=True)


class Item(Base):
    __tablename__ = "Item"
    id = Column(Integer, primary_key=True, index=True)
    Pedido_id = Column(Integer, ForeignKey("Pedido.id", ondelete="CASCADE"), nullable=True)
    Produto_id = Column(Integer, ForeignKey("Produto.id"), nullable=False)
    Quantidade = Column(Integer, default=1)


class Adicional(Base):
    __tablename__ = "Adicional"
    id = Column(Integer, primary_key=True, index=True)
    Item_id = Column(Integer, ForeignKey("Item.id", ondelete="CASCADE"), nullable=False)
    Nome = Column(String(100), nullable=True)
    Preco = Column(DECIMAL(10, 2), nullable=True)


class Combo(Base):
    __tablename__ = "Combo"
    id = Column(Integer, primary_key=True, index=True)
    Nome = Column(String(100), nullable=True)
    Promocao = Column(DECIMAL(10, 2), nullable=True)


class Promocao(Base):
    __tablename__ = "Promocao"
    id = Column(Integer, primary_key=True, index=True)
    Nome = Column(String(100), nullable=True)
    DataInicio = Column(DateTime, nullable=True)
    DataFim = Column(DateTime, nullable=True)
    produtos = relationship("Produto", secondary=promocao_produto, back_populates="promocoes")


ALL_MODELS = (
    Categoria, Fornecedor, Ingrediente, ReposicaoEstoque, Produto,
    IngredienteProduto, Mesa, Status, Cupom, Pedido, CancelamentoPedido,
    Cliente, UsuarioCliente, Pagamento, Avaliacao, Historico, Funcionario,
    Cargo, CargoFuncionario, Entrega, Item, Adicional, Combo, Promocao,
)
