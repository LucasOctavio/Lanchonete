import { useEffect, useState } from 'react'
import { api } from './api'
import AuthPage from './pages/AuthPage'
import ClientMenuPage from './pages/ClientMenuPage'
import './App.css'
import './client.css'

const getSavedUser = () => {
  try { return JSON.parse(localStorage.getItem('lanchonete_user')) } catch { return null }
}

const getSavedCart = () => {
  try {
    const saved = JSON.parse(localStorage.getItem('lanchonete_cart')) || []
    return saved.map((item) => ({
      ...item,
      quantidade: Number.isInteger(Number(item.quantidade)) && Number(item.quantidade) > 0
        ? Number(item.quantidade)
        : 1,
    }))
  } catch { return [] }
}

export default function App() {
  const [user, setUser] = useState(getSavedUser)
  const [authMode, setAuthMode] = useState('login')
  const [authLoading, setAuthLoading] = useState(false)
  const [authError, setAuthError] = useState('')
  const [products, setProducts] = useState([])
  const [categories, setCategories] = useState([])
  const [cart, setCart] = useState(getSavedCart)
  const [loadingMenu, setLoadingMenu] = useState(true)
  const [checkoutMessage, setCheckoutMessage] = useState('')

  useEffect(() => {
    localStorage.setItem('lanchonete_cart', JSON.stringify(cart))
  }, [cart])

  useEffect(() => {
    if (!user) return
    Promise.all([
      api.products.list().catch(() => []),
      api.categories.list().catch(() => []),
    ]).then(([productsData, categoriesData]) => {
      setProducts(productsData)
      setCategories(categoriesData)
    }).finally(() => setLoadingMenu(false))
  }, [user])

  async function submitAuth(form) {
    setAuthLoading(true)
    setAuthError('')
    try {
      const data = authMode === 'register'
        ? await api.clients.register(form)
        : await api.clients.login({ email: form.email, senha: form.senha })
      localStorage.setItem('lanchonete_user', JSON.stringify(data))
      setUser(data)
    } catch (error) {
      setAuthError(error.message)
    } finally {
      setAuthLoading(false)
    }
  }

  function logout() {
    localStorage.removeItem('lanchonete_user')
    setUser(null)
  }

  function addToCart(product) {
    setCart((current) => {
      const existing = current.find((item) => item.id === product.id)
      if (existing) {
        return current.map((item) => item.id === product.id ? { ...item, quantidade: item.quantidade + 1 } : item)
      }
      return [...current, { ...product, quantidade: 1 }]
    })
  }

  function removeFromCart(product) {
    setCart((current) => current.filter((item) => item.id !== product.id))
  }

  function changeQuantity(product, quantity) {
    const safeQuantity = Number(quantity)
    if (!Number.isFinite(safeQuantity) || safeQuantity <= 0) {
      removeFromCart(product)
      return
    }
    setCart((current) => current.map((item) =>
      item.id === product.id ? { ...item, quantidade: Math.floor(safeQuantity) } : item
    ))
  }

  async function checkout() {
    try {
      await api.orders.create({
        tipo: 'delivery',
        itens: cart.map((item) => ({ produto_id: item.id, quantidade: item.quantidade, adicionais: [] })),
        cliente: { Nome: user.nome, Contato: user.telefone },
        pagamento: { pix: cart.reduce((sum, item) => sum + Number(item.Preco || 0) * item.quantidade, 0) },
      })
      setCart([])
      setCheckoutMessage('Pedido realizado com sucesso!')
      window.setTimeout(() => setCheckoutMessage(''), 4000)
    } catch (error) {
      setCheckoutMessage(error.message)
    }
  }

  if (!user) {
    return <AuthPage mode={authMode} onModeChange={(mode) => { setAuthMode(mode); setAuthError('') }} onSubmit={submitAuth} loading={authLoading} error={authError} />
  }

  if (loadingMenu) return <div className="client-loading"><div className="spinner" /><span>Preparando o cardápio...</span></div>

  return (
    <>
      {checkoutMessage && <div className="checkout-toast">{checkoutMessage}</div>}
      <ClientMenuPage
        products={products}
        categories={categories}
        cart={cart}
        onAdd={addToCart}
        onRemove={removeFromCart}
        onQuantity={changeQuantity}
        onLogout={logout}
        user={user}
        onCheckout={checkout}
      />
    </>
  )
}
