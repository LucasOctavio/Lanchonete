from decimal import Decimal

from pydantic import BaseModel, Field


class MovimentacaoEstoque(BaseModel):
    quantidade: Decimal = Field(gt=0)
