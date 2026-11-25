from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, model_validator


class PedidoCreate(BaseModel):
    Mesa_id: Optional[int] = None
    Produto_id: Optional[int] = None
    Status_id: Optional[int] = None
    Cupom_Codigo: Optional[str] = None
    Tipo: Optional[str] = None
    DataHora: Optional[datetime] = None


class ClientePedidoCreate(BaseModel):
    Nome: Optional[str] = Field(default=None, max_length=255)
    Endereco: Optional[str] = Field(default=None, max_length=255)
    Contato: Optional[str] = Field(default=None, max_length=20)


class PedidoCompletoCreate(BaseModel):
    mesa_id: Optional[int] = None
    produto_id: Optional[int] = None
    produto_ids: Optional[list[int]] = None
    itens: list[dict] = Field(default_factory=list)
    cupom_codigo: Optional[str] = None
    tipo: str = "local"
    pagamento: Optional[dict] = None
    cliente: Optional[ClientePedidoCreate] = None

    @model_validator(mode="after")
    def validar_dados_cliente(self):
        tipo = self.tipo.strip().lower()
        if tipo not in {"delivery", "retirada"}:
            return self
        telefone = self.cliente.Contato if self.cliente else None
        if not telefone or len(telefone) not in {10, 11} or not telefone.isascii() or not telefone.isdigit():
            raise ValueError("Informe um telefone com DDD e 10 ou 11 números")
        if tipo == "delivery" and not (self.cliente.Endereco or "").strip():
            raise ValueError("Informe o endereço para entrega")
        return self


class StatusUpdate(BaseModel):
    status: str
    motivo: Optional[str] = Field(default=None, max_length=500)


class AvaliacaoCreate(BaseModel):
    mensagem: Optional[str] = None
    nota: Optional[int] = Field(default=None, ge=1, le=5)
