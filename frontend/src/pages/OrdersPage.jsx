const STATUS_LABEL = {
  recebido: 'Recebido', em_preparo: 'Preparando', pronto: 'Pronto',
  entregue: 'Entregue', cancelado: 'Cancelado',
}

export default function OrdersPage({ orders, onStatus }) {
  return (
    <section className="panel full-panel">
      <div className="panel-heading">
        <div><p className="eyebrow">Operação</p><h2>Pedidos</h2></div>
        <span className="count-badge">{orders.length} pedidos</span>
      </div>

      {orders.length ? (
        <div className="table-wrap">
          <table>
            <thead><tr><th>Pedido</th><th>Tipo</th><th>Mesa</th><th>Status</th><th>Ações</th></tr></thead>
            <tbody>
              {orders.map((order) => (
                <tr key={order.id}>
                  <td><strong>#{order.id}</strong></td>
                  <td>{order.Tipo || 'Local'}</td>
                  <td>{order.Mesa_id || '-'}</td>
                  <td><span className="status pending">Em aberto</span></td>
                  <td>
                    <select defaultValue="" onChange={(event) => event.target.value && onStatus(order, event.target.value)}>
                      <option value="" disabled>Alterar status</option>
                      {Object.entries(STATUS_LABEL).map(([value, label]) => <option value={value} key={value}>{label}</option>)}
                    </select>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ) : <div className="empty-state large">Nenhum pedido registrado.</div>}
    </section>
  )
}
