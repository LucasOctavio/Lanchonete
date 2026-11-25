import { useEffect, useMemo, useState } from 'react'
import { api } from '../api'
import ClientBrand from '../components/ClientBrand'
import { productGlyph } from '../productGlyph'
import '../client-orders.css'

const money = (value) => new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' }).format(Number(value || 0))
import { ORDER_TYPE_LABELS } from '../orderDisplay'

export default function ClientMenuPage({ products, categories, cart, onAdd, onRemove, onQuantity, onLogout, user, onCheckout }) {
  const dismissedOrdersKey = `lanchonete:dismissed-canceled-orders:${String(user?.id ?? user?.email ?? user?.nome ?? 'cliente').toLowerCase()}`
  const [category, setCategory] = useState('Todos')
  const [search, setSearch] = useState('')
  const [cartOpen, setCartOpen] = useState(false)
  const [checkoutOpen, setCheckoutOpen] = useState(false)
  const [checkoutType, setCheckoutType] = useState('delivery')
  const [checkoutPhone, setCheckoutPhone] = useState('')
  const [checkoutAddress, setCheckoutAddress] = useState('')
  const [checkoutLoading, setCheckoutLoading] = useState(false)
  const [checkoutButtonAnimating, setCheckoutButtonAnimating] = useState(false)
  const [animatingProductId, setAnimatingProductId] = useState(null)
  const [myOrders, setMyOrders] = useState([])
  const [dismissedOrderIds, setDismissedOrderIds] = useState(() => {
    try {
      const saved = JSON.parse(localStorage.getItem(dismissedOrdersKey) || '[]')
      return new Set(Array.isArray(saved) ? saved.filter((id) => Number.isInteger(id)) : [])
    } catch {
      return new Set()
    }
  })
  const [ordersLoaded, setOrdersLoaded] = useState(false)
  const [ordersRefreshing, setOrdersRefreshing] = useState(false)
  const [ordersRefreshKey, setOrdersRefreshKey] = useState(0)
  const [ordersError, setOrdersError] = useState('')
  const [dismissalError, setDismissalError] = useState('')
  const [activeView, setActiveView] = useState('cardapio')

  const filtered = useMemo(() => products.filter((product) => {
    const categoryName = categories.find((item) => item.id === product.Categoria_id)?.Nome
    const matchesCategory = category === 'Todos' || categoryName === category
    return matchesCategory && (product.Nome || '').toLowerCase().includes(search.toLowerCase())
  }), [products, categories, category, search])

  const totalItems = cart.reduce((sum, item) => sum + item.quantidade, 0)
  const total = cart.reduce((sum, item) => sum + Number(item.Preco || 0) * item.quantidade, 0)
  const visibleOrders = myOrders.filter((order) => !dismissedOrderIds.has(order.id))
  const checkoutPhoneIsValid = /^[0-9]{10,11}$/.test(checkoutPhone)

  function addProductToCart(product) {
    onAdd(product)
    setAnimatingProductId(null)
    window.requestAnimationFrame(() => setAnimatingProductId(product.id))
  }

  function openCheckout() {
    if (checkoutButtonAnimating) return
    setCheckoutButtonAnimating(true)
  }

  function refreshMyOrders() {
    if (ordersRefreshing) return
    setOrdersRefreshing(true)
    setOrdersRefreshKey((current) => current + 1)
  }

  function dismissCanceledOrder(orderId) {
    const updatedIds = new Set(dismissedOrderIds)
    updatedIds.add(orderId)
    setDismissedOrderIds(updatedIds)
    setDismissalError('')
    try {
      localStorage.setItem(dismissedOrdersKey, JSON.stringify([...updatedIds]))
    } catch {
      setDismissalError('O pedido foi removido, mas não será possível manter essa alteração após atualizar a página.')
    }
  }

  async function submitCheckout(event) {
    event.preventDefault()
    if (checkoutLoading) return

    setCheckoutLoading(true)
    try {
      const succeeded = await onCheckout({
        tipo: checkoutType,
        telefone: checkoutPhone.trim(),
        endereco: checkoutType === 'delivery' ? checkoutAddress.trim() : null,
      })
      if (succeeded) {
        setCheckoutOpen(false)
        setCartOpen(false)
        setCheckoutPhone('')
        setCheckoutAddress('')
      }
    } finally {
      setCheckoutLoading(false)
    }
  }

  useEffect(() => {
    if (activeView !== 'meus-pedidos') return

    let active = true
    let requestInFlight = false

    async function loadMyOrders() {
      if (!user?.nome || requestInFlight) return
      requestInFlight = true
      setOrdersRefreshing(true)
      try {
        const orders = await api.orders.myOrders(user.nome)
        if (active) {
          setMyOrders(orders)
          setOrdersError('')
        }
      } catch (error) {
        if (active) setOrdersError(error.message)
      } finally {
        requestInFlight = false
        if (active) {
          setOrdersLoaded(true)
          setOrdersRefreshing(false)
        }
      }
    }

    const initialLoad = window.setTimeout(loadMyOrders, 0)
    return () => {
      active = false
      window.clearTimeout(initialLoad)
    }
  }, [activeView, user?.nome, ordersRefreshKey])

  return (
    <div className="client-app">
      <header className="client-header">
        <button type="button" className="client-brand" onClick={() => window.scrollTo({ top: 0, behavior: 'smooth' })}><ClientBrand /></button>
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
            <div className="client-orders-heading">
              <div><p className="eyebrow">Acompanhamento</p><h2>Meus pedidos</h2></div>
              <button type="button" className="client-orders-refresh" onClick={refreshMyOrders} disabled={ordersRefreshing}>
                {ordersRefreshing ? 'Atualizando...' : 'Atualizar'}
              </button>
            </div>
            {!ordersLoaded && <div className="client-orders-loading">Carregando pedidos...</div>}
            {ordersError && <div className="client-orders-error" role="alert">{ordersError}</div>}
            {dismissalError && <div className="client-orders-error" role="alert">{dismissalError}</div>}
            {ordersLoaded && !ordersError && visibleOrders.length === 0 && (
              <div className="client-orders-empty">
                <span>🍽️</span>
                <h3>{myOrders.length === 0 ? 'Nenhum pedido ainda' : 'Nenhum pedido para mostrar'}</h3>
                <p>{myOrders.length === 0 ? 'Quando você finalizar um pedido, ele aparecerá aqui.' : 'Os pedidos cancelados que você removeu não aparecem nesta lista.'}</p>
              </div>
            )}
            <div className="client-orders-list">
              {visibleOrders.map((order) => {
                const status = String(order.status || 'recebido').toLowerCase()
                const isPickup = order.Tipo === 'retirada'
                const labels = isPickup
                  ? ['Pedido feito', 'Sendo feito', 'Produto pronto']
                  : ['Pedido feito', 'Sendo feito', 'Produto pronto', 'Levando à sua casa']
                const stage = status === 'entregue'
                  ? (isPickup ? 3 : 4)
                  : status === 'pronto' ? 3 : status === 'em_preparo' ? 2 : 1
                const itens = order.itens || []
                const totalPedido = itens.reduce((sum, item) => sum + Number(item.produto?.Preco || 0) * Number(item.Quantidade || 1), 0)

                return (
                  <article className="client-order-card" key={order.id}>
                    <div className="client-order-title">
                      <div><span>Pedido</span><strong>#{order.id}</strong></div>
                      <span className="client-order-date">{order.DataHora ? new Date(order.DataHora).toLocaleString('pt-BR') : ''}</span>
                      {status === 'cancelado' && (
                        <button
                          type="button"
                          className="client-order-dismiss"
                          aria-label={`Remover pedido cancelado #${order.id} desta lista`}
                          onClick={() => dismissCanceledOrder(order.id)}
                        >
                          ×
                        </button>
                      )}
                    </div>
                    {status === 'cancelado' ? (
                      <div className="client-order-cancelled">
                        <strong>Pedido cancelado</strong>
                        <p>{order.motivo_cancelamento || 'Este pedido foi cancelado.'}</p>
                      </div>
                    ) : (
                      <div className="client-order-tracker" style={{ gridTemplateColumns: `repeat(${labels.length}, 1fr)` }}>
                        {labels.map((label, index) => (
                          <div className={`tracker-step ${index + 1 <= stage ? 'active' : ''}`} key={label}>
                            <div className="tracker-dot">{index + 1 <= stage ? '✓' : index + 1}</div>
                            <strong>{label}</strong>
                          </div>
                        ))}
                      </div>
                    )}
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
                    <div className="client-order-type">
                      <span>Forma de recebimento</span>
                      <strong>{ORDER_TYPE_LABELS[order.Tipo] || order.Tipo || 'Entrega'}</strong>
                    </div>
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
                  <div className="client-product-footer">
                    <strong>{money(product.Preco)}</strong>
                    <button
                      type="button"
                      className={animatingProductId === product.id ? 'is-adding' : ''}
                      onAnimationEnd={() => setAnimatingProductId(null)}
                      onClick={() => addProductToCart(product)}
                    >
                      Adicionar
                    </button>
                  </div>
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
          {cart.length > 0 && <div className="cart-footer"><div><span>Total</span><strong>{money(total)}</strong></div><button type="button" className={checkoutButtonAnimating ? 'is-opening' : ''} disabled={checkoutButtonAnimating} onClick={openCheckout} onAnimationEnd={() => {
            if (!checkoutButtonAnimating) return
            setCheckoutButtonAnimating(false)
            setCheckoutOpen(true)
          }}>Finalizar pedido</button></div>}
        </aside>
      </div>}
      {checkoutOpen && <div className="checkout-modal-backdrop">
        <form className="checkout-modal" role="dialog" aria-modal="true" onSubmit={submitCheckout} aria-labelledby="checkout-title">
          <div className="checkout-modal-heading">
            <div><span>Quase lá</span><h2 id="checkout-title">Finalizar pedido</h2></div>
            <button type="button" aria-label="Fechar" onClick={() => setCheckoutOpen(false)} disabled={checkoutLoading}>×</button>
          </div>
          <fieldset className="checkout-type-options">
            <legend>Como deseja receber?</legend>
            <label className={checkoutType === 'delivery' ? 'selected' : ''}>
              <input type="radio" name="checkout-type" value="delivery" checked={checkoutType === 'delivery'} onChange={() => setCheckoutType('delivery')} />
              Entrega
            </label>
            <label className={checkoutType === 'retirada' ? 'selected' : ''}>
              <input type="radio" name="checkout-type" value="retirada" checked={checkoutType === 'retirada'} onChange={() => setCheckoutType('retirada')} />
              Retirada
            </label>
          </fieldset>
          <label className="checkout-field" htmlFor="checkout-phone">Telefone para contato
            <input id="checkout-phone" name="telefone" type="tel" inputMode="numeric" autoComplete="tel" pattern="[0-9]{10,11}" aria-describedby="checkout-phone-hint" required value={checkoutPhone} onChange={(event) => setCheckoutPhone(event.target.value.replace(/\D/g, '').slice(0, 11))} placeholder="11999999999" />
            <small id="checkout-phone-hint">Digite DDD + telefone: 10 ou 11 números.</small>
          </label>
          {checkoutType === 'delivery' ? (
            <label className="checkout-field" htmlFor="checkout-address">Endereço de entrega
              <input id="checkout-address" name="endereco" autoComplete="street-address" maxLength={255} required value={checkoutAddress} onChange={(event) => setCheckoutAddress(event.target.value)} placeholder="Rua, número, bairro e complemento" />
            </label>
          ) : (
            <p className="checkout-pickup-note">Você escolheu retirar o pedido no local. Não é necessário informar o endereço.</p>
          )}
          <div className="checkout-modal-actions">
            <button type="button" className="checkout-back-button" onClick={() => setCheckoutOpen(false)} disabled={checkoutLoading}>Voltar ao carrinho</button>
            <button type="submit" className="checkout-submit-button" disabled={checkoutLoading || !checkoutPhoneIsValid || (checkoutType === 'delivery' && !checkoutAddress.trim())}>
              {checkoutLoading ? 'Enviando...' : 'Confirmar pedido'}
            </button>
          </div>
        </form>
      </div>}
    </div>
  )
}
