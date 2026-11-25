import { useState } from 'react'
import { ORDER_STATUS_LABELS, ORDER_TYPE_LABELS, orderStatusClass } from '../orderDisplay'

export default function OrdersPage({ orders, onStatus }) {
  const [cancelOrder, setCancelOrder] = useState(null)
  const [cancelReason, setCancelReason] = useState('')
  const [savingOrderId, setSavingOrderId] = useState(null)
  const [error, setError] = useState('')
  const activeOrders = orders.filter((order) => String(order.status || '').toLowerCase() !== 'cancelado')
  const statusActions = Object.entries(ORDER_STATUS_LABELS).filter(([status]) => status !== 'recebido')

  async function changeStatus(order, status, reason) {
    setSavingOrderId(order.id)
    setError('')
    try {
      await onStatus(order, status, reason)
      if (status === 'cancelado') {
        setCancelOrder(null)
        setCancelReason('')
      }
    } catch (statusError) {
      setError(statusError.message)
    } finally {
      setSavingOrderId(null)
    }
  }

  function selectStatus(order, status) {
    if (status === 'cancelado') {
      setCancelOrder(order)
      setCancelReason('')
      setError('')
      return
    }
    changeStatus(order, status)
  }

  function confirmCancellation(event) {
    event.preventDefault()
    const reason = cancelReason.trim()
    if (!reason || !cancelOrder) return
    changeStatus(cancelOrder, 'cancelado', reason)
  }

  return (
    <section className="panel full-panel">
      <div className="panel-heading">
        <div><p className="eyebrow">Operação</p><h2>Pedidos</h2></div>
        <span className="count-badge">{activeOrders.length} pedidos</span>
      </div>

      {error && <div className="notice" role="alert">{error}<button type="button" onClick={() => setError('')}>×</button></div>}
      {activeOrders.length ? (
        <div className="table-wrap">
          <table>
            <thead><tr><th>Pedido</th><th>Cliente / contato</th><th>Itens</th><th>Tipo</th><th>Horário</th><th>Status</th><th>Ações</th></tr></thead>
            <tbody>
              {activeOrders.map((order) => (
                <tr key={order.id}>
                  <td><strong>#{order.id}</strong></td>
                  <td>
                    <strong>{order.cliente?.Nome || '-'}</strong>
                    {order.cliente?.Contato && <small className="order-client-detail">Telefone: {order.cliente.Contato}</small>}
                    {order.cliente?.Endereco && <small className="order-client-detail">Endereço: {order.cliente.Endereco}</small>}
                  </td>
                  <td>{(order.itens || []).map((item) => `${item.Quantidade || 1}x ${item.produto?.Nome || 'Produto'}`).join(', ') || '-'}</td>
                  <td>{ORDER_TYPE_LABELS[order.Tipo] || order.Tipo || '-'}</td>
                  <td>{order.DataHora ? new Date(order.DataHora).toLocaleString('pt-BR') : '-'}</td>
                  <td><span className={orderStatusClass(order.status)}>{ORDER_STATUS_LABELS[order.status] || order.status || 'Recebido'}</span></td>
                  <td>
                    <select value="" disabled={savingOrderId === order.id} onChange={(event) => event.target.value && selectStatus(order, event.target.value)}>
                      <option value="" disabled>Alterar status</option>
                      {statusActions.map(([value, label]) => <option value={value} key={value}>{label}</option>)}
                    </select>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ) : <div className="empty-state large">Nenhum pedido ativo.</div>}

      {cancelOrder && (
        <div className="employee-modal-backdrop" onMouseDown={(event) => event.target === event.currentTarget && savingOrderId === null && setCancelOrder(null)}>
          <form className="employee-modal" onSubmit={confirmCancellation} aria-labelledby="cancel-order-title">
            <h2 id="cancel-order-title">Cancelar pedido #{cancelOrder.id}</h2>
            <p className="cancel-order-instructions">Escreva o motivo. Ele será exibido ao cliente em “Meus pedidos”.</p>
            <label htmlFor="cancel-order-reason">Motivo do cancelamento</label>
            <textarea
              id="cancel-order-reason"
              required
              maxLength={500}
              rows={4}
              value={cancelReason}
              onChange={(event) => setCancelReason(event.target.value)}
            />
            {error && <p className="employee-form-error" role="alert">{error}</p>}
            <div className="employee-modal-actions">
              <button type="button" className="employee-cancel-button" onClick={() => setCancelOrder(null)} disabled={savingOrderId !== null}>Voltar</button>
              <button type="submit" className="employee-danger-button" disabled={!cancelReason.trim() || savingOrderId !== null}>
                {savingOrderId === cancelOrder.id ? 'Cancelando...' : 'Confirmar cancelamento'}
              </button>
            </div>
          </form>
        </div>
      )}
    </section>
  )
}
