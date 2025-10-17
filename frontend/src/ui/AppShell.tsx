import React from 'react'
import { Link, Outlet, useNavigate } from 'react-router-dom'
import { useAuth } from '../state/auth'

const AppShell: React.FC = () => {
  const { token, logout } = useAuth()
  const navigate = useNavigate()

  React.useEffect(() => {
    if (!token) navigate('/login')
  }, [token, navigate])

  if (!token) return null

  return (
    <div className="app">
      <nav style={{ display: 'flex', gap: 12, padding: 12, borderBottom: '1px solid #ddd' }}>
        <Link to="/">Dashboard</Link>
        <Link to="/customers">Clientes</Link>
        <Link to="/dispatches">Despachos</Link>
        <Link to="/messaging">Mensajería</Link>
        <span style={{ marginLeft: 'auto' }}>
          <button onClick={logout}>Salir</button>
        </span>
      </nav>
      <main style={{ padding: 16 }}>
        <Outlet />
      </main>
    </div>
  )
}

export default AppShell
