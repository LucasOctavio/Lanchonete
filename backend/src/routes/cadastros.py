from typing import Any

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from src.dependencias import get_db
from src.models import (
    Adicional, Avaliacao, Cargo, CargoFuncionario, Categoria, Cliente, Combo,
    Cupom, Entrega, Fornecedor, Funcionario, Historico, Ingrediente, IngredienteProduto,
    Item, Mesa, Pagamento, Produto, Promocao,
)
from src.services.crud_service import (
    create_record, delete_record, get_record, list_records, update_record,
)

router = APIRouter()

CADASTROS = {
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
    "adicionais": ("Adicional", Adicional),
    "combos": ("Combo", Combo),
    "itens": ("Item", Item),
    "promocoes": ("Promocao", Promocao),
    "ingrediente-produtos": ("IngredienteProduto", IngredienteProduto),
}


for path_name, (tag, model) in CADASTROS.items():
    def make_list(model=model):
        def endpoint(db: Session = Depends(get_db), skip: int = Query(0, ge=0), limit: int = Query(100, ge=1, le=500)):
            return list_records(db, model, skip, limit)
        return endpoint

    def make_create(model=model):
        def endpoint(payload: dict[str, Any], db: Session = Depends(get_db)):
            return create_record(db, model, payload)
        return endpoint

    def make_get(model=model):
        def endpoint(item_id: int, db: Session = Depends(get_db)):
            return get_record(db, model, item_id)
        return endpoint

    def make_update(model=model):
        def endpoint(item_id: int, payload: dict[str, Any], db: Session = Depends(get_db)):
            return update_record(db, model, item_id, payload)
        return endpoint

    def make_delete(model=model):
        def endpoint(item_id: int, db: Session = Depends(get_db)):
            return delete_record(db, model, item_id)
        return endpoint

    router.add_api_route(f"/{path_name}", make_list(), methods=["GET"], tags=[tag])
    router.add_api_route(f"/{path_name}", make_create(), methods=["POST"], status_code=status.HTTP_201_CREATED, tags=[tag])
    router.add_api_route(f"/{path_name}/{{item_id}}", make_get(), methods=["GET"], tags=[tag])
    router.add_api_route(f"/{path_name}/{{item_id}}", make_update(), methods=["PUT", "PATCH"], tags=[tag])
    router.add_api_route(f"/{path_name}/{{item_id}}", make_delete(), methods=["DELETE"], tags=[tag])
