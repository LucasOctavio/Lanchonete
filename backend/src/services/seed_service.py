from sqlalchemy.orm import Session

from src.models import (
    Categoria, Fornecedor, Ingrediente, Mesa, Produto, Status,
)


def seed_database(db: Session) -> None:
    if db.query(Status).count() == 0:
        db.add_all([
            Status(Status="recebido"),
            Status(Status="em_preparo"),
            Status(Status="pronto"),
            Status(Status="entregue"),
            Status(Status="cancelado"),
        ])

    if db.query(Mesa).count() == 0:
        db.add_all([Mesa(Numero=numero) for numero in range(1, 11)])

    categorias_padrao = ["Lanches", "Bebidas", "Porções", "Sobremesas"]
    categorias = {}
    for nome in categorias_padrao:
        categoria = db.query(Categoria).filter(Categoria.Nome == nome).first()
        if not categoria:
            categoria = Categoria(Nome=nome)
            db.add(categoria)
            db.flush()
        categorias[nome] = categoria

    if db.query(Fornecedor).count() == 0:
        fornecedor = Fornecedor(Nome="Distribuidora Central", Contato="(11) 99999-0000")
        db.add(fornecedor)
        db.flush()

        db.add_all([
            Ingrediente(Fornecedor_id=fornecedor.id, Nome="Hambúrguer", QtdEstoque=50, UniMedida="un"),
            Ingrediente(Fornecedor_id=fornecedor.id, Nome="Queijo", QtdEstoque=30, UniMedida="un"),
            Ingrediente(Fornecedor_id=fornecedor.id, Nome="Batata", QtdEstoque=40, UniMedida="kg"),
            Ingrediente(Fornecedor_id=fornecedor.id, Nome="Alface", QtdEstoque=12, UniMedida="kg"),
            Ingrediente(Fornecedor_id=fornecedor.id, Nome="Refrigerante", QtdEstoque=80, UniMedida="un"),
        ])

    if db.query(Produto).count() == 0:
        db.add_all([
            Produto(Categoria_id=categorias["Lanches"].id, Nome="X-Burger", Preco=22.90, Tamanho="Único", ponto="Bem passado"),
            Produto(Categoria_id=categorias["Lanches"].id, Nome="X-Bacon", Preco=29.90, Tamanho="Único", ponto="Bem passado"),
            Produto(Categoria_id=categorias["Lanches"].id, Nome="X-Salada", Preco=24.90, Tamanho="Único", ponto="Ao ponto"),
            Produto(Categoria_id=categorias["Porções"].id, Nome="Batata Frita", Preco=18.50, Tamanho="Grande", ponto=None),
            Produto(Categoria_id=categorias["Porções"].id, Nome="Anéis de Cebola", Preco=16.90, Tamanho="Grande", ponto=None),
            Produto(Categoria_id=categorias["Bebidas"].id, Nome="Refrigerante Lata", Preco=6.50, Tamanho="350 ml", ponto=None),
            Produto(Categoria_id=categorias["Bebidas"].id, Nome="Suco Natural", Preco=9.90, Tamanho="500 ml", ponto=None),
            Produto(Categoria_id=categorias["Sobremesas"].id, Nome="Pudim", Preco=10.00, Tamanho="Único", ponto=None),
        ])

    db.commit()
