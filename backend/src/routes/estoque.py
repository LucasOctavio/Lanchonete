from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from src.dependencias import get_db
from src.schemas.estoque import MovimentacaoEstoque
from src.services.estoque_service import consumir, listar_reposicoes, repor

router = APIRouter(prefix="/ingredientes", tags=["Estoque"])


@router.get("/historico")
def historico_reposicoes(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
):
    return listar_reposicoes(db, skip, limit)


@router.post("/{ingrediente_id}/consumir")
def consumir_estoque(ingrediente_id: int, payload: MovimentacaoEstoque, db: Session = Depends(get_db)):
    return consumir(db, ingrediente_id, payload.quantidade)


@router.post("/{ingrediente_id}/repor")
def repor_estoque(ingrediente_id: int, payload: MovimentacaoEstoque, db: Session = Depends(get_db)):
    return repor(db, ingrediente_id, payload.quantidade)
