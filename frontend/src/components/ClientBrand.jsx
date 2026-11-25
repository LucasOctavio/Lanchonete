export default function ClientBrand({ className = '' }) {
  return (
    <span className={`client-brand-lockup ${className}`.trim()}>
      <span className="client-brand-icon" aria-hidden="true">C</span>
      <strong>Charllote</strong>
    </span>
  )
}
