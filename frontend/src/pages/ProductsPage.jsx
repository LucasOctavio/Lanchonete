import { useMemo, useState } from 'react'
import '../employee-products.css'
import { productGlyph } from '../productGlyph'

const money = (value) => new Intl.NumberFormat('pt-BR', {
  style: 'currency', currency: 'BRL',
}).format(Number(value || 0))

const emptyProduct = (categoryId = '') => ({
  Nome: '',
  Preco: '',
  Categoria_id: String(categoryId),
  Tamanho: '',
  ponto: null,
})

export default function ProductsPage({ products, categories, search, onCreate, onUpdate }) {
  const [editingId, setEditingId] = useState(null)
  const [editorOpen, setEditorOpen] = useState(false)
  const [form, setForm] = useState(emptyProduct())
  const [saving, setSaving] = useState(false)
  const [error, setError] = useState('')

  const filtered = useMemo(() => products.filter((product) =>
    (product.Nome || '').toLowerCase().includes(search.toLowerCase())
  ), [products, search])

  function openEditor(product = null) {
    setEditingId(product?.id ?? null)
    setForm(product ? {
      Nome: product.Nome || '',
      Preco: product.Preco ?? '',
      Categoria_id: String(product.Categoria_id || ''),
      Tamanho: product.Tamanho || '',
      ponto: product.ponto || null,
    } : emptyProduct(categories[0]?.id))
    setError('')
    setEditorOpen(true)
  }

  async function saveProduct(event) {
    event.preventDefault()
    setSaving(true)
    setError('')
    const data = {
      ...form,
      Nome: form.Nome.trim(),
      Preco: Number(form.Preco),
      Categoria_id: Number(form.Categoria_id),
      Tamanho: form.Tamanho.trim() || null,
    }
    try {
      if (editingId === null) {
        await onCreate(data)
      } else {
        await onUpdate(editingId, data)
      }
      setEditorOpen(false)
    } catch (saveError) {
      setError(saveError.message)
    } finally {
      setSaving(false)
    }
  }

  return (
    <section>
      <div className="section-heading">
        <div><p className="eyebrow">Gerenciamento do cardápio</p><h2>Produtos</h2></div>
        <div className="product-heading-actions">
          <span className="count-badge">{filtered.length} produtos</span>
          <button type="button" className="product-add-button" onClick={() => openEditor()} disabled={!categories.length}>
            Adicionar produto
          </button>
        </div>
      </div>

      {filtered.length ? (
        <div className="product-grid">
          {filtered.map((product) => {
            const category = categories.find((item) => item.id === product.Categoria_id)
            return (
              <article className="product-card" key={product.id}>
                <div className="product-image">
                  <span>{productGlyph(product.Nome)}</span>
                </div>
                <div className="product-info">
                  <div><h3>{product.Nome || 'Produto sem nome'}</h3><p>{category?.Nome || 'Sem categoria'}</p></div>
                  {product.Tamanho && <small>{product.Tamanho}</small>}
                </div>
                <div className="product-footer">
                  <strong>{money(product.Preco)}</strong>
                  <button type="button" className="product-edit-button" aria-label={`Editar ${product.Nome || 'produto'}`} onClick={() => openEditor(product)}>Editar</button>
                </div>
              </article>
            )
          })}
        </div>
      ) : <div className="empty-state large">Nenhum produto encontrado.</div>}

      {editorOpen && (
        <div className="employee-modal-backdrop" onMouseDown={(event) => event.target === event.currentTarget && !saving && setEditorOpen(false)}>
          <form className="employee-modal product-editor-modal" onSubmit={saveProduct} aria-labelledby="product-editor-title">
            <h2 id="product-editor-title">{editingId === null ? 'Adicionar produto' : 'Editar produto'}</h2>
            <label>Nome<input required maxLength="200" value={form.Nome} onChange={(event) => setForm((current) => ({ ...current, Nome: event.target.value }))} /></label>
            <label>Categoria
              <select required value={form.Categoria_id} onChange={(event) => setForm((current) => ({ ...current, Categoria_id: event.target.value }))}>
                <option value="" disabled>Selecione</option>
                {categories.map((item) => <option value={item.id} key={item.id}>{item.Nome}</option>)}
              </select>
            </label>
            <label>Preço (R$)<input required type="number" min="0" step="0.01" value={form.Preco} onChange={(event) => setForm((current) => ({ ...current, Preco: event.target.value }))} /></label>
            <label>Tamanho<input maxLength="45" value={form.Tamanho} onChange={(event) => setForm((current) => ({ ...current, Tamanho: event.target.value }))} /></label>
            {error && <p className="employee-form-error" role="alert">{error}</p>}
            <div className="employee-modal-actions">
              <button type="button" className="employee-cancel-button" onClick={() => setEditorOpen(false)} disabled={saving}>Cancelar</button>
              <button type="submit" className="employee-save-button" disabled={saving}>{saving ? 'Salvando...' : 'Salvar'}</button>
            </div>
          </form>
        </div>
      )}
    </section>
  )
}
