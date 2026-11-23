const icons = {
  grid: '▦', menu: '☰', bag: '▣', box: '◆', users: '♟', chart: '◫',
  settings: '⚙', search: '⌕', plus: '+', arrow: '→', clock: '◷', check: '✓',
  refresh: '↻', plate: '◉',
}

export function Icon({ name, size = 18 }) {
  return <span className="icon" aria-hidden="true" style={{ fontSize: size }}>{icons[name] || '•'}</span>
}
