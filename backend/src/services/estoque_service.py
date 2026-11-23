from decimal import Decimal

from fastapi import HTTPException
from sqlalchemy.orm import Session

from src.models import Ingrediente
from src.services.serialization import to_dict


def consumir(db: Session, ingrediente_id: int, quantidade: Decimal) -> dict:
    ingrediente = db.get(Ingrediente, ingrediente_id)
    if not ingrediente:
        raise HTTPException(404, "Ingrediente não encontrado")
    atual = ingrediente.QtdEstoque or Decimal("0")
    if atual < quantidade:
        raise HTTPException(409, "Estoque insuficiente")
    ingrediente.QtdEstoque = atual - quantidade
    db.commit()
    db.refresh(ingrediente)
    return to_dict(ingrediente)


def repor(db: Session, ingrediente_id: int, quantidade: Decimal) -> dict:
    ingrediente = db.get(Ingrediente, ingrediente_id)
    if not ingrediente:
        raise HTTPException(404, "Ingrediente não encontrado")
    ingrediente.QtdEstoque = (ingrediente.QtdEstoque or Decimal("0")) + quantidade
    db.commit()
    db.refresh(ingrediente)
    return to_dict(ingrediente)
