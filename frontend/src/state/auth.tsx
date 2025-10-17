import React, { createContext, useContext, useEffect, useMemo, useState } from 'react'
import axios from 'axios'

const API_BASE = (import.meta as any).env.VITE_API_BASE || '/api'

type AuthContextType = {
  token: string | null
  login: (username: string, password: string) => Promise<void>
  logout: () => void
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export const AuthProvider: React.FC<{ children?: React.ReactNode }> = ({ children }) => {
  const [token, setToken] = useState<string | null>(localStorage.getItem('token'))

  useEffect(() => {
    if (token) localStorage.setItem('token', token)
    else localStorage.removeItem('token')
  }, [token])

  useEffect(() => {
    axios.defaults.baseURL = API_BASE
    axios.interceptors.request.use((config) => {
      if (token) config.headers = { ...config.headers, Authorization: `Bearer ${token}` }
      return config
    })
  }, [token])

  const login = async (username: string, password: string) => {
    const { data } = await axios.post('/auth/token/', { username, password })
    setToken(data.access)
  }

  const logout = () => setToken(null)

  const value = useMemo(() => ({ token, login, logout }), [token])
  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

export function useAuth() {
  const ctx = useContext(AuthContext)
  if (!ctx) throw new Error('useAuth must be used within AuthProvider')
  return ctx
}
