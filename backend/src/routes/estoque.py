from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.dependencias import get_db
from src.schemas.estoque import MovimentacaoEstoque
from src.services.estoque_service import consumir, repor

router = APIRouter(prefix="/ingredientes", tags=["Estoque"])


@router.post("/{ingrediente_id}/consumir")
def consumir_estoque(ingrediente_id: int, payload: MovimentacaoEstoque, db: Session = Depends(get_db)):
    return consumir(db, ingrediente_id, payload.quantidade)


@router.post("/{ingrediente_id}/repor")
def repor_estoque(ingrediente_id: int, payload: MovimentacaoEstoque, db: Session = Depends(get_db)):
    return repor(db, ingrediente_id, payload.quantidade)
