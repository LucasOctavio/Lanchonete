export const ORDER_STATUS_LABELS = {
  recebido: 'Recebido',
  em_preparo: 'Preparando',
  pronto: 'Pronto',
  entregue: 'Entregue',
  cancelado: 'Cancelado',
}

const ORDER_STATUS_CLASS_NAMES = {
  recebido: 'received',
  em_preparo: 'preparing',
  pronto: 'ready',
  entregue: 'delivered',
  cancelado: 'cancelled',
}

export const ORDER_TYPE_LABELS = {
  delivery: 'Entrega',
  retirada: 'Retirada',
  local: 'Local',
}

export function orderStatusClass(status) {
  return `status order-status-${ORDER_STATUS_CLASS_NAMES[status] || 'received'}`
}
