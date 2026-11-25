from datetime import datetime
from decimal import Decimal

from fastapi import HTTPException
from sqlalchemy.orm import Session

from src.models import Ingrediente, ReposicaoEstoque
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
    db.add(ReposicaoEstoque(
        Ingrediente_id=ingrediente_id,
        Quantidade=quantidade,
        DataHora=datetime.utcnow(),
    ))
    db.commit()
    db.refresh(ingrediente)
    return to_dict(ingrediente)


def listar_reposicoes(db: Session, skip: int, limit: int) -> list[dict]:
    reposicoes = (
        db.query(ReposicaoEstoque)
        .order_by(ReposicaoEstoque.DataHora.desc(), ReposicaoEstoque.id.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )
    resultado = []
    for reposicao in reposicoes:
        ingrediente = db.get(Ingrediente, reposicao.Ingrediente_id)
        resultado.append({
            **to_dict(reposicao),
            "Nome": ingrediente.Nome if ingrediente else "Ingrediente removido",
            "UniMedida": ingrediente.UniMedida if ingrediente else None,
        })
    return resultado
