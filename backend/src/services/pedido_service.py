from datetime import datetime
from decimal import Decimal
from typing import Any

from fastapi import HTTPException
from sqlalchemy.orm import Session

from src.models import Avaliacao, Adicional, Cliente, Historico, Item, Pagamento, Pedido, Produto, Status
from src.services.serialization import to_dict


def criar_pedido(db: Session, payload: dict[str, Any]) -> dict:
    item_payloads = payload.get("itens") or []
    if payload.get("produto_ids"):
        item_payloads = [{"produto_id": item_id, "quantidade": 1} for item_id in payload["produto_ids"]]
    if not item_payloads:
        raise HTTPException(422, "Informe pelo menos um produto ou item")

    status_pedido = db.query(Status).filter(Status.Status == "recebido").first()
    if not status_pedido:
        status_pedido = Status(Status="recebido", DataHora=datetime.utcnow())
        db.add(status_pedido)
        db.flush()

    pedido = Pedido(
        Mesa_id=payload.get("mesa_id"), Produto_id=payload.get("produto_id"),
        Status_id=status_pedido.id, Cupom_Codigo=payload.get("cupom_codigo"),
        Tipo=payload.get("tipo", "local"), DataHora=datetime.utcnow(),
    )
    db.add(pedido)
    db.flush()

    total = Decimal("0")
    itens_resultado = []
    for item_payload in item_payloads:
        produto = db.get(Produto, int(item_payload["produto_id"]))
        if not produto:
            raise HTTPException(404, f"Produto {item_payload['produto_id']} não encontrado")
        quantidade = int(item_payload.get("quantidade", 1))
        if quantidade < 1:
            raise HTTPException(422, "Quantidade deve ser maior que zero")

        item = Item(Pedido_id=pedido.id, Produto_id=produto.id, Quantidade=quantidade)
        db.add(item)
        db.flush()
        if produto.Preco:
            total += produto.Preco * quantidade

        adicionais = []
        for adicional_payload in item_payload.get("adicionais", []):
            adicional = Adicional(
                Item_id=item.id, Nome=adicional_payload.get("nome"),
                Preco=Decimal(str(adicional_payload.get("preco", 0))),
            )
            db.add(adicional)
            adicionais.append(adicional_payload)
        itens_resultado.append({"produto_id": produto.id, "quantidade": quantidade, "adicionais": adicionais})

    pagamento = payload.get("pagamento")
    if pagamento:
        db.add(Pagamento(
            Pedido_id=pedido.id,
            Cartao=Decimal(str(pagamento["cartao"])) if pagamento.get("cartao") is not None else None,
            Dinheiro=Decimal(str(pagamento["dinheiro"])) if pagamento.get("dinheiro") is not None else None,
            Pix=Decimal(str(pagamento["pix"])) if pagamento.get("pix") is not None else None,
        ))

    if payload.get("cliente"):
        db.add(Cliente(Pedido_id=pedido.id, **payload["cliente"]))

    db.add(Historico(Pedido_id=pedido.id, DataHora=datetime.utcnow()))
    db.commit()
    db.refresh(pedido)
    return {**to_dict(pedido), "itens": itens_resultado, "total": float(total)}


def listar_pedidos(db: Session, skip: int, limit: int) -> list[dict]:
    return [to_dict(pedido) for pedido in db.query(Pedido).offset(skip).limit(limit).all()]


def buscar_pedido(db: Session, pedido_id: int) -> dict:
    pedido = db.get(Pedido, pedido_id)
    if not pedido:
        raise HTTPException(404, "Pedido não encontrado")
    data = to_dict(pedido)

    itens = []
    for item in db.query(Item).filter(Item.Pedido_id == pedido_id).all():
        item_data = to_dict(item)
        produto = db.get(Produto, item.Produto_id)
        item_data["produto"] = to_dict(produto) if produto else None
        itens.append(item_data)

    data["itens"] = itens
    data["historico"] = [to_dict(item) for item in db.query(Historico).filter(Historico.Pedido_id == pedido_id).order_by(Historico.DataHora).all()]
    data["pagamentos"] = [to_dict(item) for item in db.query(Pagamento).filter(Pagamento.Pedido_id == pedido_id).all()]
    data["avaliacoes"] = [to_dict(item) for item in db.query(Avaliacao).filter(Avaliacao.Pedido_id == pedido_id).all()]

    status_pedido = db.get(Status, pedido.Status_id) if pedido.Status_id else None
    data["status"] = status_pedido.Status if status_pedido else "recebido"

    cliente = db.query(Cliente).filter(Cliente.Pedido_id == pedido_id).first()
    data["cliente"] = {"Nome": cliente.Nome, "Contato": cliente.Contato} if cliente else None
    return data


def criar_pedido_basico(db: Session, payload: dict[str, Any]) -> dict:
    pedido = Pedido(**payload)
    db.add(pedido)
    db.commit()
    db.refresh(pedido)
    return to_dict(pedido)


def alterar_pedido(db: Session, pedido_id: int, payload: dict[str, Any]) -> dict:
    pedido = db.get(Pedido, pedido_id)
    if not pedido:
        raise HTTPException(404, "Pedido não encontrado")
    for key, value in payload.items():
        setattr(pedido, key, value)
    db.commit()
    db.refresh(pedido)
    return to_dict(pedido)


def excluir_pedido(db: Session, pedido_id: int) -> dict:
    pedido = db.get(Pedido, pedido_id)
    if not pedido:
        raise HTTPException(404, "Pedido não encontrado")
    db.delete(pedido)
    db.commit()
    return {"deleted": True}


def atualizar_status(db: Session, pedido_id: int, nome_status: str) -> dict:
    pedido = db.get(Pedido, pedido_id)
    if not pedido:
        raise HTTPException(404, "Pedido não encontrado")
    novo_status = db.query(Status).filter(Status.Status == nome_status).order_by(Status.id.desc()).first()
    if not novo_status:
        novo_status = Status(Status=nome_status, DataHora=datetime.utcnow())
        db.add(novo_status)
        db.flush()
    pedido.Status_id = novo_status.id
    db.add(Historico(Pedido_id=pedido_id, DataHora=datetime.utcnow()))
    db.commit()
    db.refresh(pedido)
    return to_dict(pedido)


def avaliar_pedido(db: Session, pedido_id: int, mensagem: str | None, nota: int | None) -> dict:
    if not db.get(Pedido, pedido_id):
        raise HTTPException(404, "Pedido não encontrado")
    avaliacao = Avaliacao(Pedido_id=pedido_id, Mensagem=mensagem, Nota=nota)
    db.add(avaliacao)
    db.commit()
    db.refresh(avaliacao)
    return to_dict(avaliacao)


def listar_pedidos_cliente(db: Session, nome: str) -> list[dict]:
    clientes = db.query(Cliente).filter(Cliente.Nome == nome).all()
    pedido_ids = [cliente.Pedido_id for cliente in clientes if cliente.Pedido_id]
    if not pedido_ids:
        return []

    resultado = []
    for pedido_id in pedido_ids:
        pedido = db.get(Pedido, pedido_id)
        if pedido:
            resultado.append(buscar_pedido(db, pedido_id))
    resultado.sort(key=lambda item: item.get("DataHora") or "", reverse=True)
    return resultado
