const API_URL = import.meta.env.VITE_API_URL || '/api'

async function request(path, options = {}) {
  const response = await fetch(`${API_URL}${path}`, {
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
    ...options,
  })

  if (!response.ok) {
    const body = await response.json().catch(() => ({}))
    throw new Error(body.detail || `Erro ${response.status}`)
  }

  if (response.status === 204) return null
  return response.json()
}

export const api = {
  health: () => request('/health'),
  categories: {
    list: () => request('/categorias'),
    create: (Nome) => request('/categorias', { method: 'POST', body: JSON.stringify({ Nome }) }),
  },
  products: {
    list: () => request('/produtos'),
    create: (data) => request('/produtos', { method: 'POST', body: JSON.stringify(data) }),
    update: (id, data) => request(`/produtos/${id}`, { method: 'PUT', body: JSON.stringify(data) }),
  },
  suppliers: {
    list: () => request('/fornecedores'),
  },
  tables: {
    list: () => request('/mesas'),
  },
  orders: {
    list: (skip = 0, limit = 100) => request(`/pedidos?skip=${skip}&limit=${limit}`),
    create: (data) => request('/pedidos/completo', { method: 'POST', body: JSON.stringify(data) }),
    get: (id) => request(`/pedidos/${id}`),
    status: (id, status, motivo) => request(`/pedidos/${id}/status`, {
      method: 'POST',
      body: JSON.stringify({ status, ...(motivo ? { motivo } : {}) }),
    }),
    myOrders: (name) => request(`/pedidos/meus?nome=${encodeURIComponent(name)}`),
  },
  ingredients: {
    list: () => request('/ingredientes'),
    create: (data) => request('/ingredientes', { method: 'POST', body: JSON.stringify(data) }),
    update: (id, data) => request(`/ingredientes/${id}`, { method: 'PUT', body: JSON.stringify(data) }),
    restock: (id, quantidade) => request(`/ingredientes/${id}/repor`, { method: 'POST', body: JSON.stringify({ quantidade }) }),
    history: (skip = 0, limit = 100) => request(`/ingredientes/historico?skip=${skip}&limit=${limit}`),
  },
  report: () => request('/relatorios/vendas'),
  clients: {
    register: (data) => request('/clientes/cadastro', { method: 'POST', body: JSON.stringify(data) }),
    login: (data) => request('/clientes/login', { method: 'POST', body: JSON.stringify(data) }),
  },
}
