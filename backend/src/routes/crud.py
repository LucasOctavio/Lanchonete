from datetime import datetime
from decimal import Decimal
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import inspect
from sqlalchemy.orm import Session

from src.dependencias import get_db
from src.models import (
    ALL_MODELS, Adicional, Avaliacao, Cargo, CargoFuncionario, Categoria,
    Cliente, Combo, Cupom, Entrega, Fornecedor, Funcionario, Historico,
    Ingrediente, IngredienteProduto, Item, Mesa, Pagamento, Pedido, Produto,
    Promocao, Status,
)

router = APIRouter()


def serialize(value: Any) -> Any:
    if isinstance(value, (datetime,)):
        return value.isoformat()
    if isinstance(value, Decimal):
        return float(value)
    return value


def to_dict(obj: Any) -> dict[str, Any]:
    result = {}
    for column in inspect(obj).mapper.column_attrs:
        key = column.key
        result[key] = serialize(getattr(obj, key))
    return result


def convert_value(column: Any, value: Any) -> Any:
    if value is None:
        return None
    python_type = getattr(column.type, "python_type", None)
    try:
        if python_type is datetime:
            return datetime.fromisoformat(str(value).replace("Z", "+00:00"))
        if python_type is Decimal:
            return Decimal(str(value))
        if python_type is int:
            return int(value)
    except (TypeError, ValueError):
        raise HTTPException(status_code=422, detail=f"Valor inválido para {column.key}")
    return value


def model_payload(model: Any, payload: dict[str, Any]) -> dict[str, Any]:
    allowed = {column.key: column for column in inspect(model).columns}
    unknown = set(payload) - set(allowed)
    if unknown:
        raise HTTPException(status_code=422, detail=f"Campos inválidos: {', '.join(sorted(unknown))}")
    return {
        key: convert_value(column, payload[key])
        for key, column in allowed.items()
        if key in payload
    }


CRUD_MODELS = {
    "categorias": ("Categoria", Categoria),
    "fornecedores": ("Fornecedor", Fornecedor),
    "ingredientes": ("Ingrediente", Ingrediente),
    "produtos": ("Produto", Produto),
    "mesas": ("Mesa", Mesa),
    "cupoms": ("Cupom", Cupom),
    "clientes": ("Cliente", Cliente),
    "pagamentos": ("Pagamento", Pagamento),
    "avaliacoes": ("Avaliacao", Avaliacao),
    "historicos": ("Historico", Historico),
    "entregas": ("Entrega", Entrega),
    "funcionarios": ("Funcionario", Funcionario),
    "cargos": ("Cargo", Cargo),
    "cargo-funcionarios": ("CargoFuncionario", CargoFuncionario),
    "itens": ("Item", Item),
    "adicionais": ("Adicional", Adicional),
    "combos": ("Combo", Combo),
    "promocoes": ("Promocao", Promocao),
}


for path_name, (label, model) in CRUD_MODELS.items():
    def make_list(model=model):
        def list_records(db: Session = Depends(get_db), skip: int = Query(0, ge=0), limit: int = Query(100, ge=1, le=500)):
            return [to_dict(item) for item in db.query(model).offset(skip).limit(limit).all()]
        return list_records

    def make_create(model=model):
        def create_record(payload: dict[str, Any], db: Session = Depends(get_db)):
            data = model_payload(model, payload)
            item = model(**data)
            db.add(item)
            db.commit()
            db.refresh(item)
            return to_dict(item)
        return create_record

    def make_get(model=model):
        def get_record(item_id: int, db: Session = Depends(get_db)):
            item = db.get(model, item_id)
            if not item:
                raise HTTPException(status_code=404, detail="Registro não encontrado")
            return to_dict(item)
        return get_record

    def make_update(model=model):
        def update_record(item_id: int, payload: dict[str, Any], db: Session = Depends(get_db)):
            item = db.get(model, item_id)
            if not item:
                raise HTTPException(status_code=404, detail="Registro não encontrado")
            for key, value in model_payload(model, payload).items():
                setattr(item, key, value)
            db.commit()
            db.refresh(item)
            return to_dict(item)
        return update_record

    def make_delete(model=model):
        def delete_record(item_id: int, db: Session = Depends(get_db)):
            item = db.get(model, item_id)
            if not item:
                raise HTTPException(status_code=404, detail="Registro não encontrado")
            db.delete(item)
            db.commit()
            return {"deleted": True}
        return delete_record

    router.add_api_route(f"/{path_name}", make_list(), methods=["GET"], tags=[label])
    router.add_api_route(f"/{path_name}", make_create(), methods=["POST"], status_code=status.HTTP_201_CREATED, tags=[label])
    router.add_api_route(f"/{path_name}/{{item_id}}", make_get(), methods=["GET"], tags=[label])
    router.add_api_route(f"/{path_name}/{{item_id}}", make_update(), methods=["PUT", "PATCH"], tags=[label])
    router.add_api_route(f"/{path_name}/{{item_id}}", make_delete(), methods=["DELETE"], tags=[label])


@router.post("/pedidos/completo", tags=["Pedido"])
def criar_pedido_completo(payload: dict[str, Any], db: Session = Depends(get_db)):
    produto_ids = payload.get("produto_ids")
    itens = payload.get("itens") or []
    if not produto_ids and not itens:
        raise HTTPException(status_code=422, detail="Informe pelo menos um produto ou item")

    status_pedido = db.query(Status).filter(Status.Status == "recebido").first()
    if not status_pedido:
        status_pedido = Status(Status="recebido", DataHora=datetime.utcnow())
        db.add(status_pedido)
        db.flush()

    pedido = Pedido(
        Mesa_id=payload.get("mesa_id"),
        Produto_id=payload.get("produto_id"),
        Status_id=status_pedido.id,
        Cupom_Codigo=payload.get("cupom_codigo"),
        Tipo=payload.get("tipo", "local"),
        DataHora=datetime.utcnow(),
    )
    db.add(pedido)
    db.flush()

    if produto_ids:
        itens = [{"produto_id": produto_id, "quantidade": 1} for produto_id in produto_ids]

    total = Decimal("0")
    for item_payload in itens:
        produto = db.get(Produto, int(item_payload["produto_id"]))
        if not produto:
            raise HTTPException(status_code=404, detail=f"Produto {item_payload['produto_id']} não encontrado")
        quantidade = int(item_payload.get("quantidade", 1))
        if quantidade < 1:
            raise HTTPException(status_code=422, detail="Quantidade deve ser maior que zero")
        item = Item(Pedido_id=pedido.id, Produto_id=produto.id, Quantidade=quantidade)
        db.add(item)
        if produto.Preco:
            total += produto.Preco * quantidade

        for adicional_payload in item_payload.get("adicionais", []):
            adicional = Adicional(
                Item_id=None,
                Nome=adicional_payload.get("nome"),
                Preco=Decimal(str(adicional_payload.get("preco", 0))),
            )
            db.flush()
            adicional.Item_id = item.id
            db.add(adicional)

    pagamento = payload.get("pagamento")
    if pagamento:
        db.add(Pagamento(
            Pedido_id=pedido.id,
            Cartao=Decimal(str(pagamento.get("cartao", 0))) if pagamento.get("cartao") is not None else None,
            Dinheiro=Decimal(str(pagamento.get("dinheiro", 0))) if pagamento.get("dinheiro") is not None else None,
            Pix=Decimal(str(pagamento.get("pix", 0))) if pagamento.get("pix") is not None else None,
        ))

    if payload.get("cliente"):
        db.add(Cliente(Pedido_id=pedido.id, **payload["cliente"]))

    db.add(Historico(Pedido_id=pedido.id, DataHora=datetime.utcnow()))
    db.commit()
    db.refresh(pedido)
    return {**to_dict(pedido), "itens": itens, "total": float(total)}


@router.get("/pedidos", tags=["Pedido"])
def listar_pedidos(db: Session = Depends(get_db), skip: int = Query(0, ge=0), limit: int = Query(100, ge=1, le=500)):
    return [to_dict(pedido) for pedido in db.query(Pedido).offset(skip).limit(limit).all()]


@router.get("/pedidos/{pedido_id}", tags=["Pedido"])
def buscar_pedido(pedido_id: int, db: Session = Depends(get_db)):
    pedido = db.get(Pedido, pedido_id)
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    data = to_dict(pedido)
    data["itens"] = [to_dict(item) for item in db.query(Item).filter(Item.Pedido_id == pedido_id).all()]
    data["historico"] = [to_dict(item) for item in db.query(Historico).filter(Historico.Pedido_id == pedido_id).order_by(Historico.DataHora).all()]
    data["pagamentos"] = [to_dict(item) for item in db.query(Pagamento).filter(Pagamento.Pedido_id == pedido_id).all()]
    data["avaliacoes"] = [to_dict(item) for item in db.query(Avaliacao).filter(Avaliacao.Pedido_id == pedido_id).all()]
    return data


@router.post("/pedidos/{pedido_id}/status", tags=["Pedido"])
def atualizar_status_pedido(pedido_id: int, payload: dict[str, Any], db: Session = Depends(get_db)):
    pedido = db.get(Pedido, pedido_id)
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    nome_status = payload.get("status")
    if not nome_status:
        raise HTTPException(status_code=422, detail="Informe o novo status")
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


@router.post("/pedidos/{pedido_id}/avaliacao", tags=["Pedido"])
def avaliar_pedido(pedido_id: int, payload: dict[str, Any], db: Session = Depends(get_db)):
    pedido = db.get(Pedido, pedido_id)
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    nota = payload.get("nota")
    if nota is not None and not 1 <= int(nota) <= 5:
        raise HTTPException(status_code=422, detail="Nota deve estar entre 1 e 5")
    avaliacao = Avaliacao(Pedido_id=pedido_id, Mensagem=payload.get("mensagem"), Nota=nota)
    db.add(avaliacao)
    db.commit()
    db.refresh(avaliacao)
    return to_dict(avaliacao)


@router.post("/ingredientes/{ingrediente_id}/consumir", tags=["Estoque"])
def consumir_ingrediente(ingrediente_id: int, payload: dict[str, Any], db: Session = Depends(get_db)):
    ingrediente = db.get(Ingrediente, ingrediente_id)
    if not ingrediente:
        raise HTTPException(status_code=404, detail="Ingrediente não encontrado")
    quantidade = Decimal(str(payload.get("quantidade", 0)))
    atual = ingrediente.QtdEstoque or Decimal("0")
    if quantidade <= 0:
        raise HTTPException(status_code=422, detail="Quantidade deve ser maior que zero")
    if atual < quantidade:
        raise HTTPException(status_code=409, detail="Estoque insuficiente")
    ingrediente.QtdEstoque = atual - quantidade
    db.commit()
    db.refresh(ingrediente)
    return to_dict(ingrediente)


@router.post("/ingredientes/{ingrediente_id}/repor", tags=["Estoque"])
def repor_ingrediente(ingrediente_id: int, payload: dict[str, Any], db: Session = Depends(get_db)):
    ingrediente = db.get(Ingrediente, ingrediente_id)
    if not ingrediente:
        raise HTTPException(status_code=404, detail="Ingrediente não encontrado")
    quantidade = Decimal(str(payload.get("quantidade", 0)))
    if quantidade <= 0:
        raise HTTPException(status_code=422, detail="Quantidade deve ser maior que zero")
    ingrediente.QtdEstoque = (ingrediente.QtdEstoque or Decimal("0")) + quantidade
    db.commit()
    db.refresh(ingrediente)
    return to_dict(ingrediente)


@router.get("/relatorios/vendas", tags=["Relatórios"])
def relatorio_vendas(db: Session = Depends(get_db)):
    pedidos = db.query(Pedido).all()
    produtos = db.query(Produto).all()
    total_pedidos = len(pedidos)
    quantidade_itens = db.query(Item).count()
    receita = sum(
        float(item.Quantidade or 0) * float(produto.Preco or 0)
        for item in db.query(Item).all()
        for produto in produtos
        if item.Produto_id == produto.id
    )
    return {"total_pedidos": total_pedidos, "total_itens": quantidade_itens, "receita_estimada": round(receita, 2)}


@router.get("/health", tags=["Sistema"])
def health(db: Session = Depends(get_db)):
    db.execute(__import__("sqlalchemy").text("SELECT 1"))
    return {"status": "ok"}


@router.post("/pedidos", tags=["Pedido"], status_code=status.HTTP_201_CREATED)
def criar_pedido(payload: dict[str, Any], db: Session = Depends(get_db)):
    pedido = Pedido(**model_payload(Pedido, payload))
    db.add(pedido)
    db.commit()
    db.refresh(pedido)
    return to_dict(pedido)


@router.put("/pedidos/{pedido_id}", tags=["Pedido"])
def alterar_pedido(pedido_id: int, payload: dict[str, Any], db: Session = Depends(get_db)):
    pedido = db.get(Pedido, pedido_id)
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    for key, value in model_payload(Pedido, payload).items():
        setattr(pedido, key, value)
    db.commit()
    db.refresh(pedido)
    return to_dict(pedido)


@router.delete("/pedidos/{pedido_id}", tags=["Pedido"])
def excluir_pedido(pedido_id: int, db: Session = Depends(get_db)):
    pedido = db.get(Pedido, pedido_id)
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    db.delete(pedido)
    db.commit()
    return {"deleted": True}
