import { useState } from 'react'

export default function AuthPage({ mode, onModeChange, onSubmit, loading, error }) {
  const [form, setForm] = useState({ nome: '', email: '', telefone: '', senha: '' })

  function update(event) {
    setForm((current) => ({ ...current, [event.target.name]: event.target.value }))
  }

  return (
    <main className="auth-page">
      <section className="auth-brand">
        <div className="auth-brand-inner">
          <div className="auth-logo">S</div>
          <span className="auth-kicker">Sabor &amp; Cia</span>
          <h1>Seu lanche favorito,<br />sempre perto de você.</h1>
          <p>Monte seu pedido, acompanhe a entrega e aproveite os melhores sabores.</p>
        </div>
        <div className="auth-burger">🍔</div>
      </section>

      <section className="auth-card-wrap">
        <form className="auth-card" onSubmit={(event) => { event.preventDefault(); onSubmit(form) }}>
          <div className="auth-tabs">
            <button type="button" className={mode === 'login' ? 'active' : ''} onClick={() => onModeChange('login')}>Entrar</button>
            <button type="button" className={mode === 'register' ? 'active' : ''} onClick={() => onModeChange('register')}>Criar conta</button>
          </div>

          <div className="auth-heading">
            <p className="eyebrow">Bem-vindo</p>
            <h2>{mode === 'login' ? 'Acesse sua conta' : 'Cadastre-se agora'}</h2>
          </div>

          {mode === 'register' && (
            <label>Nome completo<input name="nome" value={form.nome} onChange={update} placeholder="Seu nome" required minLength="2" /></label>
          )}
          <label>E-mail<input name="email" value={form.email} onChange={update} type="email" placeholder="voce@email.com" required /></label>
          {mode === 'register' && (
            <label>Telefone<input name="telefone" value={form.telefone} onChange={update} type="tel" placeholder="(00) 00000-0000" /></label>
          )}
          <label>Senha<input name="senha" value={form.senha} onChange={update} type="password" placeholder="••••••••" required minLength={mode === 'register' ? 6 : 1} /></label>

          {error && <div className="auth-error">{error}</div>}

          <button className="auth-submit" type="submit" disabled={loading}>{loading ? 'Aguarde...' : mode === 'login' ? 'Entrar' : 'Criar conta'}</button>

          <p className="auth-switch">
            {mode === 'login' ? 'Ainda não tem conta?' : 'Já possui uma conta?'}{' '}
            <button type="button" onClick={() => onModeChange(mode === 'login' ? 'register' : 'login')}>
              {mode === 'login' ? 'Cadastre-se' : 'Entrar'}
            </button>
          </p>
        </form>
      </section>
    </main>
  )
}
