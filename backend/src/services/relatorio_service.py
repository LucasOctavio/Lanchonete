from sqlalchemy import text
from sqlalchemy.orm import Session

from src.models import Item, Pedido, Produto


def vendas(db: Session) -> dict:
    itens = db.query(Item).all()
    produtos = {produto.id: produto for produto in db.query(Produto).all()}
    receita = sum(
        float(item.Quantidade or 0) * float(produtos[item.Produto_id].Preco or 0)
        for item in itens
        if item.Produto_id in produtos
    )
    return {
        "total_pedidos": db.query(Pedido).count(),
        "total_itens": len(itens),
        "receita_estimada": round(receita, 2),
    }


def health(db: Session) -> dict:
    db.execute(text("SELECT 1"))
    return {"status": "ok"}
