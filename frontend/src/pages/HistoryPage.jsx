import { useEffect, useState } from 'react'
import { api } from '../api'
import { ORDER_STATUS_LABELS, ORDER_TYPE_LABELS, orderStatusClass } from '../orderDisplay'

async function loadAllPages(fetchPage) {
  const records = []
  let skip = 0
  const limit = 500

  while (true) {
    const page = await fetchPage(skip, limit)
    records.push(...page)
    if (page.length < limit) return records
    skip += limit
  }
}

export default function HistoryPage() {
  const [orders, setOrders] = useState([])
  const [restocks, setRestocks] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [refreshKey, setRefreshKey] = useState(0)

  useEffect(() => {
    let active = true

    async function loadHistory() {
      try {
        const [orderHistory, restockHistory] = await Promise.all([
          loadAllPages(api.orders.list),
          loadAllPages(api.ingredients.history),
        ])
        if (!active) return
        setOrders(orderHistory)
        setRestocks(restockHistory)
        setError('')
      } catch (loadError) {
        if (active) setError(loadError.message)
      } finally {
        if (active) setLoading(false)
      }
    }

    loadHistory()
    return () => {
      active = false
    }
  }, [refreshKey])

  return (
    <section className="employee-history">
      <div className="section-heading">
        <div><p className="eyebrow">Registro da operação</p><h2>Histórico</h2></div>
        <button type="button" className="history-refresh-button" onClick={() => {
          setLoading(true)
          setRefreshKey((current) => current + 1)
        }} disabled={loading}>
          {loading ? 'Carregando...' : 'Atualizar'}
        </button>
      </div>

      {error && <div className="notice" role="alert">{error}</div>}
      {loading ? (
        <div className="loading-state"><div className="spinner" /><span>Carregando histórico...</span></div>
      ) : (
        <>
          <section className="panel full-panel">
            <div className="panel-heading">
              <div><p className="eyebrow">Vendas</p><h2>Todos os pedidos</h2></div>
              <span className="count-badge">{orders.length} pedidos</span>
            </div>
            {orders.length ? (
              <div className="table-wrap">
                <table>
                  <thead><tr><th>Pedido</th><th>Data</th><th>Cliente / contato</th><th>Tipo</th><th>Itens</th><th>Status</th><th>Motivo do cancelamento</th></tr></thead>
                  <tbody>
                    {orders.map((order) => (
                      <tr key={order.id}>
                        <td><strong>#{order.id}</strong></td>
                        <td>{order.DataHora ? new Date(order.DataHora).toLocaleString('pt-BR') : '-'}</td>
                        <td>
                          <strong>{order.cliente?.Nome || '-'}</strong>
                          {order.cliente?.Contato && <small className="order-client-detail">Telefone: {order.cliente.Contato}</small>}
                          {order.cliente?.Endereco && <small className="order-client-detail">Endereço: {order.cliente.Endereco}</small>}
                        </td>
                        <td>{ORDER_TYPE_LABELS[order.Tipo] || order.Tipo || '-'}</td>
                        <td>{(order.itens || []).map((item) => `${item.Quantidade || 1}x ${item.produto?.Nome || 'Produto'}`).join(', ') || '-'}</td>
                        <td><span className={orderStatusClass(order.status)}>{ORDER_STATUS_LABELS[order.status] || order.status || 'Recebido'}</span></td>
                        <td>{order.motivo_cancelamento || '-'}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            ) : <div className="empty-state">Nenhum pedido registrado.</div>}
          </section>

          <section className="panel full-panel">
            <div className="panel-heading">
              <div><p className="eyebrow">Estoque</p><h2>Ingredientes repostos</h2></div>
              <span className="count-badge">{restocks.length} reposições</span>
            </div>
            {restocks.length ? (
              <div className="table-wrap">
                <table>
                  <thead><tr><th>Data</th><th>Ingrediente</th><th>Quantidade reposta</th></tr></thead>
                  <tbody>
                    {restocks.map((restock) => (
                      <tr key={restock.id}>
                        <td>{restock.DataHora ? new Date(restock.DataHora).toLocaleString('pt-BR') : '-'}</td>
                        <td><strong>{restock.Nome}</strong></td>
                        <td>{restock.Quantidade} {restock.UniMedida || ''}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            ) : <div className="empty-state">Nenhuma reposição de ingrediente registrada.</div>}
          </section>
        </>
      )}
    </section>
  )
}
