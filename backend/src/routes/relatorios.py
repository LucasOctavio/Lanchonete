from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.dependencias import get_db
from src.services.relatorio_service import health, vendas

router = APIRouter(tags=["Relatórios"])


@router.get("/relatorios/vendas")
def relatorio_vendas(db: Session = Depends(get_db)):
    return vendas(db)


@router.get("/health", tags=["Sistema"])
def health_check(db: Session = Depends(get_db)):
    return health(db)
