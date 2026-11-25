import { useState } from 'react'

const emptyIngredient = (supplierId = '') => ({
  Nome: '',
  Fornecedor_id: String(supplierId),
  QtdEstoque: '0',
  UniMedida: 'un',
})

export default function StockPage({ ingredients, suppliers, onRestock, onCreate, onUpdate }) {
  const [editingId, setEditingId] = useState(null)
  const [editorOpen, setEditorOpen] = useState(false)
  const [form, setForm] = useState(emptyIngredient())
  const [saving, setSaving] = useState(false)
  const [error, setError] = useState('')

  function openEditor(ingredient = null) {
    setEditingId(ingredient?.id ?? null)
    setForm(ingredient ? {
      Nome: ingredient.Nome || '',
      Fornecedor_id: String(ingredient.Fornecedor_id || ''),
      QtdEstoque: ingredient.QtdEstoque ?? '0',
      UniMedida: ingredient.UniMedida || 'un',
    } : emptyIngredient(suppliers[0]?.id))
    setError('')
    setEditorOpen(true)
  }

  async function saveIngredient(event) {
    event.preventDefault()
    setSaving(true)
    setError('')
    const data = {
      Nome: form.Nome.trim(),
      Fornecedor_id: Number(form.Fornecedor_id),
      QtdEstoque: Number(form.QtdEstoque),
      UniMedida: form.UniMedida.trim(),
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
    <section className="panel full-panel">
      <div className="panel-heading">
        <div><p className="eyebrow">Insumos</p><h2>Controle de estoque</h2></div>
        <div className="stock-heading-actions">
          <span className="count-badge">{ingredients.length} ingredientes</span>
          <button type="button" className="product-add-button" onClick={() => openEditor()} disabled={!suppliers.length}>Adicionar ingrediente</button>
        </div>
      </div>

      {editorOpen && (
        <div className="employee-modal-backdrop" onMouseDown={(event) => event.target === event.currentTarget && !saving && setEditorOpen(false)}>
          <form className="employee-modal" onSubmit={saveIngredient} aria-labelledby="ingredient-editor-title">
            <h2 id="ingredient-editor-title">{editingId === null ? 'Adicionar ingrediente' : 'Editar ingrediente'}</h2>
            <label>Nome<input required maxLength="45" value={form.Nome} onChange={(event) => setForm((current) => ({ ...current, Nome: event.target.value }))} /></label>
            <label>Fornecedor
              <select required value={form.Fornecedor_id} onChange={(event) => setForm((current) => ({ ...current, Fornecedor_id: event.target.value }))}>
                <option value="" disabled>Selecione</option>
                {suppliers.map((supplier) => <option value={supplier.id} key={supplier.id}>{supplier.Nome}</option>)}
              </select>
            </label>
            <label>Quantidade em estoque<input required type="number" min="0" step="0.001" value={form.QtdEstoque} onChange={(event) => setForm((current) => ({ ...current, QtdEstoque: event.target.value }))} /></label>
            <label>Unidade<input required maxLength="10" value={form.UniMedida} onChange={(event) => setForm((current) => ({ ...current, UniMedida: event.target.value }))} /></label>
            {error && <p className="employee-form-error" role="alert">{error}</p>}
            <div className="employee-modal-actions">
              <button type="button" className="employee-cancel-button" onClick={() => setEditorOpen(false)} disabled={saving}>Cancelar</button>
              <button type="submit" className="employee-save-button" disabled={saving}>{saving ? 'Salvando...' : 'Salvar'}</button>
            </div>
          </form>
        </div>
      )}

      {ingredients.length ? (
        <div className="table-wrap">
          <table>
            <thead><tr><th>Ingrediente</th><th>Fornecedor</th><th>Quantidade</th><th>Unidade</th><th>Ações</th></tr></thead>
            <tbody>
              {ingredients.map((ingredient) => {
                const supplier = suppliers.find((item) => item.id === ingredient.Fornecedor_id)
                return (
                  <tr key={ingredient.id}>
                    <td><strong>{ingredient.Nome}</strong></td>
                    <td>{supplier?.Nome || '-'}</td>
                    <td><span className={Number(ingredient.QtdEstoque || 0) < 10 ? 'quantity-low' : 'quantity-ok'}>{ingredient.QtdEstoque || 0}</span></td>
                    <td>{ingredient.UniMedida || 'un'}</td>
                    <td className="stock-row-actions">
                      <button type="button" className="restock-button" onClick={() => onRestock(ingredient)}>Repor</button>
                      <button type="button" className="product-edit-button" aria-label={`Editar ${ingredient.Nome}`} onClick={() => openEditor(ingredient)}>Editar</button>
                    </td>
                  </tr>
                )
              })}
            </tbody>
          </table>
        </div>
      ) : <div className="empty-state large">Nenhum ingrediente cadastrado.</div>}
    </section>
  )
}
