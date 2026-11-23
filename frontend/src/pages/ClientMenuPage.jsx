import { useEffect, useMemo, useState } from 'react'
import { api } from '../api'

const money = (value) => new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' }).format(Number(value || 0))

function productGlyph(productName) {
  const name = (productName || '').toLowerCase()
  if (name.includes('batata') || name.includes('porção') || name.includes('porcao') || name.includes('cebola')) return '🍟'
  if (name.includes('suco') || name.includes('refrigerante')) return '🥤'
  if (name.includes('pudim') || name.includes('sobremesa') || name.includes('bolo')) return '🍮'
  if (name.includes('pizza')) return '🍕'
  if (name.includes('lanche') || name.includes('burger') || name.includes('bacon') || name.includes('salada')) return '🍔'
  return '🍽️'
}

export default function ClientMenuPage({ products, categories, cart, onAdd, onRemove, onQuantity, onLogout, user, onCheckout }) {
  const [category, setCategory] = useState('Todos')
  const [search, setSearch] = useState('')
  const [cartOpen, setCartOpen] = useState(false)
  const [myOrders, setMyOrders] = useState([])
  const [loadingOrders, setLoadingOrders] = useState(false)
  const [activeView, setActiveView] = useState('cardapio')

  const filtered = useMemo(() => products.filter((product) => {
    const categoryName = categories.find((item) => item.id === product.Categoria_id)?.Nome
    const matchesCategory = category === 'Todos' || categoryName === category
    return matchesCategory && (product.Nome || '').toLowerCase().includes(search.toLowerCase())
  }), [products, categories, category, search])

  const totalItems = cart.reduce((sum, item) => sum + item.quantidade, 0)
  const total = cart.reduce((sum, item) => sum + Number(item.Preco || 0) * item.quantidade, 0)

  async function loadMyOrders() {
    if (!user?.nome) return
    setLoadingOrders(true)
    try {
      const orders = await api.orders.myOrders(user.nome)
      setMyOrders(orders)
    } catch {
      setMyOrders([])
    } finally {
      setLoadingOrders(false)
    }
  }

  useEffect(() => {
    if (activeView !== 'meus-pedidos') return
    loadMyOrders()
    const timer = window.setInterval(loadMyOrders, 5000)
    return () => window.clearInterval(timer)
  }, [activeView, user?.nome])

  return (
    <div className="client-app">
      <header className="client-header">
        <button type="button" className="client-brand" onClick={() => window.scrollTo({ top: 0, behavior: 'smooth' })}><span>S</span><strong>Sabor &amp; Cia</strong></button>
        <nav className="client-nav"><button className={activeView === 'cardapio' ? 'active' : ''} type="button" onClick={() => setActiveView('cardapio')}>Cardápio</button><button className={activeView === 'meus-pedidos' ? 'active' : ''} type="button" onClick={() => setActiveView('meus-pedidos')}>Meus pedidos</button></nav>
        <div className="client-actions">
          <button type="button" className="cart-button" onClick={() => setCartOpen(true)}>🛒<span>{totalItems}</span></button>
          <div className="client-user"><strong>{user?.nome || 'Cliente'}</strong><button type="button" onClick={onLogout}>Sair</button></div>
        </div>
      </header>

      <main className="client-main">
        <section className="client-hero">
          <div><span className="hero-kicker">CARDÁPIO DE HOJE</span><h1>O sabor que você ama,<br />feito na hora.</h1><p>Escolha seus favoritos e monte seu pedido.</p></div>
          <div className="hero-food" aria-hidden="true">🍔</div>
        </section>

        {activeView === 'meus-pedidos' ? (
          <section className="client-orders-page">
            <div className="client-orders-heading"><p className="eyebrow">Acompanhamento</p><h2>Meus pedidos</h2></div>
            {loadingOrders && <div className="client-orders-loading">Atualizando pedidos...</div>}
            {!loadingOrders && myOrders.length === 0 && (
              <div className="client-orders-empty"><span>🍽️</span><h3>Nenhum pedido ainda</h3><p>Quando você finalizar um pedido, ele aparecerá aqui.</p></div>
            )}
            <div className="client-orders-list">
              {myOrders.map((order) => {
                const status = String(order.status || 'recebido').toLowerCase()
                const stage = status === 'entregue' || status === 'pronto' ? 3 : status === 'em_preparo' ? 2 : 1
                const labels = ['Pedido feito', 'Sendo feito', 'Levando à sua casa']
                const itens = order.itens || []
                const totalPedido = itens.reduce((sum, item) => sum + Number(item.produto?.Preco || 0) * Number(item.Quantidade || 1), 0)

                return (
                  <article className="client-order-card" key={order.id}>
                    <div className="client-order-title"><div><span>Pedido</span><strong>#{order.id}</strong></div><span className="client-order-date">{order.DataHora ? new Date(order.DataHora).toLocaleString('pt-BR') : ''}</span></div>
                    <div className="client-order-tracker">
                      {labels.map((label, index) => (
                        <div className={`tracker-step ${index + 1 <= stage ? 'active' : ''}`} key={label}>
                          <div className="tracker-dot">{index + 1 <= stage ? '✓' : index + 1}</div>
                          <strong>{label}</strong>
                        </div>
                      ))}
                    </div>
                    <div className="client-order-items">
                      {itens.map((item, index) => (
                        <div className="client-order-item" key={`${item.id || item.Produto_id}-${index}`}>
                          <div className="client-order-glyph"><span>{productGlyph(item.produto?.Nome)}</span></div>
                          <div><strong>{item.produto?.Nome || 'Produto'}</strong><span>Quantidade: {item.Quantidade || 1}</span></div>
                        </div>
                      ))}
                    </div>
                    {itens.length === 0 && <p className="client-order-no-items">Nenhum item detalhado.</p>}
                    <div className="client-order-total"><span>Total</span><strong>{money(totalPedido)}</strong></div>
                  </article>
                )
              })}
            </div>
          </section>
        ) : (
          <>
            <section className="menu-toolbar">
              <div className="category-list">
                {['Todos', ...categories.map((item) => item.Nome).filter(Boolean)].map((name) => (
                  <button type="button" key={name} className={category === name ? 'active' : ''} onClick={() => setCategory(name)}>{name}</button>
                ))}
              </div>
              <label className="client-search">⌕<input value={search} onChange={(event) => setSearch(event.target.value)} placeholder="Buscar no cardápio" /></label>
            </section>

            <section className="client-products">
              {filtered.map((product) => (
                <article className="client-product" key={product.id}>
                  <div className="client-product-art"><span>{productGlyph(product.Nome)}</span></div>
                  <div className="client-product-info">
                    <div><h3>{product.Nome}</h3><p>{categories.find((item) => item.id === product.Categoria_id)?.Nome || 'Especialidade'}</p></div>
                    {product.Tamanho && <small>{product.Tamanho}</small>}
                  </div>
                  <div className="client-product-footer"><strong>{money(product.Preco)}</strong><button type="button" onClick={() => onAdd(product)}>Adicionar</button></div>
                </article>
              ))}
              {!filtered.length && <div className="client-empty">Nenhum produto encontrado.</div>}
            </section>
          </>
        )}
      </main>

      {cartOpen && <div className="cart-overlay" onMouseDown={(event) => event.target === event.currentTarget && setCartOpen(false)}>
        <aside className="cart-panel">
          <div className="cart-heading"><div><span>Seu pedido</span><h2>Carrinho</h2></div><button type="button" onClick={() => setCartOpen(false)}>×</button></div>
          <div className="cart-items">
            {cart.map((item) => (
              <div className="cart-item" key={item.id}>
                <div className="cart-item-image"><span>{productGlyph(item.Nome)}</span></div>
                <div className="cart-item-info"><strong>{item.Nome}</strong><span>{money(item.Preco)}</span></div>
                <div className="cart-controls">
                  <button type="button" aria-label={`Diminuir quantidade de ${item.Nome}`} onMouseDown={(event) => event.stopPropagation()} onClick={() => onQuantity(item, item.quantidade - 1)}>−</button>
                  <strong>{item.quantidade}</strong>
                  <button type="button" aria-label={`Aumentar quantidade de ${item.Nome}`} onMouseDown={(event) => event.stopPropagation()} onClick={() => onQuantity(item, item.quantidade + 1)}>+</button>
                </div>
                <button type="button" className="cart-remove" onMouseDown={(event) => event.stopPropagation()} onClick={() => onRemove(item)}>Remover</button>
              </div>
            ))}
            {!cart.length && <div className="cart-empty"><div>🛒</div><strong>Seu carrinho está vazio</strong><p>Adicione itens deliciosos do cardápio.</p></div>}
          </div>
          {cart.length > 0 && <div className="cart-footer"><div><span>Total</span><strong>{money(total)}</strong></div><button type="button" onClick={onCheckout}>Finalizar pedido</button></div>}
        </aside>
      </div>}
    </div>
  )
}
