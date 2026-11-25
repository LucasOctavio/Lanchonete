export function productGlyph(productName) {
  const name = (productName || '').toLowerCase()
  if (name.includes('batata') || name.includes('porção') || name.includes('porcao') || name.includes('cebola')) return '🍟'
  if (name.includes('suco') || name.includes('refrigerante')) return '🥤'
  if (name.includes('pudim') || name.includes('sobremesa') || name.includes('bolo')) return '🍮'
  if (name.includes('pizza')) return '🍕'
  if (name.includes('lanche') || name.includes('burger') || name.includes('bacon') || name.includes('salada')) return '🍔'
  return '🍽️'
}
