export default function StockPage({ ingredients, onRestock }) {
  return (
    <section className="panel full-panel">
      <div className="panel-heading">
        <div><p className="eyebrow">Insumos</p><h2>Controle de estoque</h2></div>
        <span className="count-badge">{ingredients.length} ingredientes</span>
      </div>

      {ingredients.length ? (
        <div className="table-wrap">
          <table>
            <thead><tr><th>Ingrediente</th><th>Fornecedor</th><th>Quantidade</th><th>Unidade</th><th>Ação</th></tr></thead>
            <tbody>
              {ingredients.map((ingredient) => (
                <tr key={ingredient.id}>
                  <td><strong>{ingredient.Nome}</strong></td>
                  <td>{ingredient.Fornecedor_id || '-'}</td>
                  <td><span className={Number(ingredient.QtdEstoque || 0) < 10 ? 'quantity-low' : 'quantity-ok'}>{ingredient.QtdEstoque || 0}</span></td>
                  <td>{ingredient.UniMedida || 'un'}</td>
                  <td><button className="restock-button" onClick={() => onRestock(ingredient)}>Repor</button></td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ) : <div className="empty-state large">Nenhum ingrediente cadastrado.</div>}
    </section>
  )
}
