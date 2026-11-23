from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from src.dependencias import get_db
from src.schemas.pedido import (
    AvaliacaoCreate, PedidoCompletoCreate, PedidoCreate, StatusUpdate,
)
from src.services import pedido_service

router = APIRouter(prefix="/pedidos", tags=["Pedido"])


@router.get("",)
def listar(skip: int = Query(0, ge=0), limit: int = Query(100, ge=1, le=500), db: Session = Depends(get_db)):
    return pedido_service.listar_pedidos(db, skip, limit)


@router.post("", status_code=status.HTTP_201_CREATED)
def criar(payload: PedidoCreate, db: Session = Depends(get_db)):
    return pedido_service.criar_pedido_basico(db, payload.model_dump(exclude_unset=True))


@router.post("/completo", status_code=status.HTTP_201_CREATED)
def criar_completo(payload: PedidoCompletoCreate, db: Session = Depends(get_db)):
    return pedido_service.criar_pedido(db, payload.model_dump(exclude_unset=True))


@router.get("/meus")
def meus_pedidos(nome: str, db: Session = Depends(get_db)):
    return pedido_service.listar_pedidos_cliente(db, nome)


@router.get("/{pedido_id}")
def buscar(pedido_id: int, db: Session = Depends(get_db)):
    return pedido_service.buscar_pedido(db, pedido_id)


@router.put("/{pedido_id}")
def alterar(pedido_id: int, payload: PedidoCreate, db: Session = Depends(get_db)):
    return pedido_service.alterar_pedido(db, pedido_id, payload.model_dump(exclude_unset=True))


@router.delete("/{pedido_id}")
def excluir(pedido_id: int, db: Session = Depends(get_db)):
    return pedido_service.excluir_pedido(db, pedido_id)


@router.post("/{pedido_id}/status")
def atualizar_status(pedido_id: int, payload: StatusUpdate, db: Session = Depends(get_db)):
    return pedido_service.atualizar_status(db, pedido_id, payload.status)


@router.post("/{pedido_id}/avaliacao", status_code=status.HTTP_201_CREATED)
def avaliar(pedido_id: int, payload: AvaliacaoCreate, db: Session = Depends(get_db)):
    return pedido_service.avaliar_pedido(db, pedido_id, payload.mensagem, payload.nota)
