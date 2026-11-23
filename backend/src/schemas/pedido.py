from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class PedidoCreate(BaseModel):
    Mesa_id: Optional[int] = None
    Produto_id: Optional[int] = None
    Status_id: Optional[int] = None
    Cupom_Codigo: Optional[str] = None
    Tipo: Optional[str] = None
    DataHora: Optional[datetime] = None


class PedidoCompletoCreate(BaseModel):
    mesa_id: Optional[int] = None
    produto_id: Optional[int] = None
    produto_ids: Optional[list[int]] = None
    itens: list[dict] = Field(default_factory=list)
    cupom_codigo: Optional[str] = None
    tipo: str = "local"
    pagamento: Optional[dict] = None
    cliente: Optional[dict] = None


class StatusUpdate(BaseModel):
    status: str


class AvaliacaoCreate(BaseModel):
    mensagem: Optional[str] = None
    nota: Optional[int] = Field(default=None, ge=1, le=5)
