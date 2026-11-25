import { Icon } from '../components/Icon'
import { ORDER_STATUS_LABELS, ORDER_TYPE_LABELS, orderStatusClass } from '../orderDisplay'

const money = (value) => new Intl.NumberFormat('pt-BR', {
  style: 'currency', currency: 'BRL',
}).format(Number(value || 0))

export default function DashboardPage({ report, products, orders, ingredients }) {
  const recent = orders.filter((order) => String(order.status || '').toLowerCase() !== 'cancelado').slice(0, 5)
  const cards = [
    { label: 'Pedidos', value: report.total_pedidos || orders.length, icon: 'bag', color: 'orange' },
    { label: 'Receita estimada', value: money(report.receita_estimada), icon: 'chart', color: 'green' },
    { label: 'Produtos', value: products.length, icon: 'grid', color: 'blue' },
    { label: 'Itens vendidos', value: report.total_itens || 0, icon: 'box', color: 'purple' },
  ]

  return (
    <>
      <section className="welcome-card">
        <div>
          <span className="welcome-tag">Operação de hoje</span>
          <h2>Bom trabalho, equipe!</h2>
          <p>Acompanhe pedidos, vendas e estoque em tempo real.</p>
        </div>
        <div className="welcome-illustration" aria-hidden="true">🍔</div>
      </section>

      <section className="stat-grid">
        {cards.map((card) => (
          <article className="stat-card" key={card.label}>
            <div className={`stat-icon ${card.color}`}><Icon name={card.icon} /></div>
            <div><span>{card.label}</span><strong>{card.value}</strong></div>
          </article>
        ))}
      </section>

      <div className="dashboard-grid">
        <section className="panel">
          <div className="panel-heading">
            <div><p className="eyebrow">Atividade recente</p><h2>Últimos pedidos</h2></div>
          </div>
          <div className="order-list">
            {recent.length ? recent.map((order) => (
              <div className="order-row" key={order.id}>
                <div className="order-number">#{order.id}</div>
                <div className="order-description">
                  <strong>{order.cliente?.Nome || `Pedido #${order.id}`}</strong>
                  <span>{ORDER_TYPE_LABELS[order.Tipo] || order.Tipo || 'Local'} · {order.itens?.length || 0} itens</span>
                </div>
                <span className={orderStatusClass(order.status)}>{ORDER_STATUS_LABELS[order.status] || order.status || 'Recebido'}</span>
              </div>
            )) : <div className="empty-state">Nenhum pedido registrado.</div>}
          </div>
        </section>

        <section className="panel">
          <div className="panel-heading">
            <div><p className="eyebrow">Resumo rápido</p><h2>Estoque crítico</h2></div>
          </div>
          <div className="stock-preview">
            {ingredients.slice(0, 5).map((ingredient) => {
              const quantity = Number(ingredient.QtdEstoque || 0)
              return (
                <div className="stock-row" key={ingredient.id}>
                  <div className="stock-name">
                    <span>{(ingredient.Nome || 'I').charAt(0)}</span>
                    <div><strong>{ingredient.Nome}</strong><small>{quantity} {ingredient.UniMedida || 'un'}</small></div>
                  </div>
                  <div className="stock-bar"><span className={quantity < 10 ? 'low' : ''} style={{ width: `${Math.min(100, quantity * 5)}%` }} /></div>
                </div>
              )
            })}
            {!ingredients.length && <div className="empty-state">Nenhum ingrediente cadastrado.</div>}
          </div>
        </section>
      </div>
    </>
  )
}
