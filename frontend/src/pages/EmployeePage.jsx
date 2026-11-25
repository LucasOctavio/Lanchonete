import { useEffect, useRef, useState } from 'react'
import { api } from '../api'
import { Icon } from '../components/Icon'
import DashboardPage from './DashboardPage'
import HistoryPage from './HistoryPage'
import OrdersPage from './OrdersPage'
import ProductsPage from './ProductsPage'
import StockPage from './StockPage'
import '../app-layout.css'
import '../employee-panel.css'

const sections = [
  { id: 'dashboard', label: 'Visão geral', icon: 'grid', title: 'Visão geral' },
  { id: 'orders', label: 'Pedidos', icon: 'bag', title: 'Pedidos' },
  { id: 'products', label: 'Produtos', icon: 'menu', title: 'Produtos' },
  { id: 'stock', label: 'Estoque', icon: 'box', title: 'Estoque' },
  { id: 'history', label: 'Histórico', icon: 'clock', title: 'Histórico' },
]

const ORDER_POLL_INTERVAL_MS = 5_000

export default function EmployeePage({ user, onLogout }) {
  const [section, setSection] = useState('dashboard')
  const [products, setProducts] = useState([])
  const [categories, setCategories] = useState([])
  const [orders, setOrders] = useState([])
  const [ingredients, setIngredients] = useState([])
  const [suppliers, setSuppliers] = useState([])
  const [report, setReport] = useState({})
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [notice, setNotice] = useState('')
  const orderIds = useRef(null)
  const sectionRef = useRef(section)

  useEffect(() => {
    sectionRef.current = section
  }, [section])

  useEffect(() => {
    let active = true
    let initialLoadComplete = false
    let orderRequestInFlight = false

    async function loadOrders() {
      if (
        !active
        || orderRequestInFlight
        || sectionRef.current !== 'orders'
      ) return

      orderRequestInFlight = true
      try {
        const currentOrders = await api.orders.list()
        if (!active) return

        const currentIds = new Set(currentOrders.map((order) => order.id))
        if (orderIds.current) {
          const newOrder = currentOrders.find((order) => !orderIds.current.has(order.id))
          if (newOrder) {
            setNotice(`Novo pedido #${newOrder.id} recebido.`)
            api.report().then(setReport).catch((loadError) => {
              if (active) setError(loadError.message)
            })
          }
        }
        orderIds.current = currentIds
        setOrders(currentOrders)
      } finally {
        orderRequestInFlight = false
      }
    }

    async function loadPanel() {
      try {
        const [productData, categoryData, orderData, ingredientData, supplierData, reportData] = await Promise.all([
          api.products.list(),
          api.categories.list(),
          api.orders.list(),
          api.ingredients.list(),
          api.suppliers.list(),
          api.report(),
        ])
        if (!active) return
        setProducts(productData)
        setCategories(categoryData)
        setOrders(orderData)
        setIngredients(ingredientData)
        setSuppliers(supplierData)
        setReport(reportData)
        orderIds.current = new Set(orderData.map((order) => order.id))
      } catch (loadError) {
        if (active) setError(loadError.message)
      } finally {
        if (active) {
          initialLoadComplete = true
          setLoading(false)
        }
      }
    }

    loadPanel()
    const timer = window.setInterval(() => {
      if (!initialLoadComplete) return
      loadOrders().catch((loadError) => {
        if (active) setError(loadError.message)
      })
    }, ORDER_POLL_INTERVAL_MS)

    return () => {
      active = false
      window.clearInterval(timer)
    }
  }, [])

  async function updateOrderStatus(order, status, reason) {
    await api.orders.status(order.id, status, reason)
    const currentOrders = await api.orders.list()
    setOrders(currentOrders)
    orderIds.current = new Set(currentOrders.map((item) => item.id))
    setError('')
    if (status === 'cancelado') setNotice(`Pedido #${order.id} cancelado.`)
  }

  async function updateProduct(productId, data) {
    const updatedProduct = await api.products.update(productId, data)
    setProducts((current) => current.map((product) => product.id === productId ? updatedProduct : product))
    setNotice('Produto atualizado com sucesso.')
  }

  async function createProduct(data) {
    const product = await api.products.create(data)
    setProducts((current) => [...current, product])
    setNotice('Produto adicionado com sucesso.')
  }

  async function createIngredient(data) {
    const ingredient = await api.ingredients.create(data)
    setIngredients((current) => [...current, ingredient])
    setNotice('Ingrediente adicionado ao estoque.')
  }

  async function updateIngredient(ingredientId, data) {
    const updatedIngredient = await api.ingredients.update(ingredientId, data)
    setIngredients((current) => current.map((item) => item.id === ingredientId ? updatedIngredient : item))
    setNotice('Ingrediente atualizado com sucesso.')
  }

  async function restock(ingredient) {
    const answer = window.prompt(`Quantidade para adicionar ao estoque de ${ingredient.Nome}:`)
    if (answer === null) return
    const quantity = Number(answer)
    if (!Number.isFinite(quantity) || quantity <= 0) {
      setError('Informe uma quantidade maior que zero.')
      return
    }

    try {
      await api.ingredients.restock(ingredient.id, quantity)
      setIngredients(await api.ingredients.list())
      setError('')
      setNotice(`Estoque de ${ingredient.Nome} atualizado.`)
    } catch (updateError) {
      setError(updateError.message)
    }
  }

  const activeSection = sections.find((item) => item.id === section)

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand">
          <span className="brand-mark" aria-hidden="true">
            <svg viewBox="0 0 24 24" width="24" height="24" fill="none">
              <circle cx="12" cy="8" r="4" fill="currentColor" />
              <path d="M4.5 21a7.5 7.5 0 0 1 15 0H4.5Z" fill="currentColor" />
            </svg>
          </span>
          <div><strong>Sabor &amp; Cia</strong><span>Painel do funcionário</span></div>
        </div>
        <nav className="main-nav" aria-label="Navegação do painel">
          {sections.map((item) => (
            <button
              type="button"
              aria-label={item.label}
              className={`nav-item ${section === item.id ? 'active' : ''}`}
              key={item.id}
              onClick={() => setSection(item.id)}
            >
              <Icon name={item.icon} /><span>{item.label}</span>
            </button>
          ))}
          <button type="button" className="nav-item logout" aria-label="Sair" onClick={onLogout}>
            <Icon name="arrow" /><span>Sair ({user.nome})</span>
          </button>
        </nav>
      </aside>

      <main className="main-content">
        <header className="topbar">
          <div><p className="eyebrow">Área do funcionário</p><h1>{activeSection?.title}</h1></div>
          <div className="top-actions">
            {section === 'orders' && <span className="connection online"><span /> Atualização automática</span>}
            <button type="button" className="avatar" aria-label="Sair" onClick={onLogout} title="Sair">AD</button>
          </div>
        </header>

        {error && <div className="notice" role="alert">{error}<button type="button" onClick={() => setError('')}>×</button></div>}
        {notice && <div className="notice" role="status">{notice}<button type="button" onClick={() => setNotice('')}>×</button></div>}

        {loading ? (
          <div className="loading-state"><div className="spinner" /><span>Carregando painel...</span></div>
        ) : (
          <>
            {section === 'dashboard' && <DashboardPage report={report} products={products} orders={orders} ingredients={ingredients} />}
            {section === 'orders' && <OrdersPage orders={orders} onStatus={updateOrderStatus} />}
            {section === 'products' && <ProductsPage products={products} categories={categories} search="" onCreate={createProduct} onUpdate={updateProduct} />}
            {section === 'stock' && <StockPage ingredients={ingredients} suppliers={suppliers} onRestock={restock} onCreate={createIngredient} onUpdate={updateIngredient} />}
            {section === 'history' && <HistoryPage />}
          </>
        )}
      </main>
    </div>
  )
}
