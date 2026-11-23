import { useMemo } from 'react'
import { Icon } from '../components/Icon'

const money = (value) => new Intl.NumberFormat('pt-BR', {
  style: 'currency', currency: 'BRL',
}).format(Number(value || 0))

export default function ProductsPage({ products, categories, search, onCreateOrder }) {
  const filtered = useMemo(() => products.filter((product) =>
    (product.Nome || '').toLowerCase().includes(search.toLowerCase())
  ), [products, search])

  return (
    <section>
      <div className="section-heading">
        <div><p className="eyebrow">Cardápio digital</p><h2>Produtos</h2></div>
        <span className="count-badge">{filtered.length} produtos</span>
      </div>

      {filtered.length ? (
        <div className="product-grid">
          {filtered.map((product) => {
            const category = categories.find((item) => item.id === product.Categoria_id)
            return (
              <article className="product-card" key={product.id}>
                <div className="product-image">
                  <span>{(product.Nome || 'P').charAt(0).toUpperCase()}</span>
                </div>
                <div className="product-info">
                  <div><h3>{product.Nome || 'Produto sem nome'}</h3><p>{category?.Nome || 'Sem categoria'}</p></div>
                  {product.Tamanho && <small>{product.Tamanho}</small>}
                </div>
                <div className="product-footer">
                  <strong>{money(product.Preco)}</strong>
                  <button onClick={() => onCreateOrder(product)} title="Criar pedido"><Icon name="plus" /></button>
                </div>
              </article>
            )
          })}
        </div>
      ) : <div className="empty-state large">Nenhum produto encontrado.</div>}
    </section>
  )
}
