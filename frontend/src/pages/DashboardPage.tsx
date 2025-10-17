import React from 'react'
import { useQuery } from '@tanstack/react-query'
import axios from 'axios'

const DashboardPage: React.FC = () => {
  const { data } = useQuery({
    queryKey: ['stats'],
    queryFn: async () => {
      const [customers, dispatches, messages] = await Promise.all([
        axios.get('/customers/?limit=1'),
        axios.get('/dispatches/?limit=1'),
        axios.get('/messaging/?limit=1'),
      ])
      return {
        customers: customers.data?.count ?? 0,
        dispatches: dispatches.data?.count ?? 0,
        messages: messages.data?.count ?? 0,
      }
    },
  })

  return (
    <div>
      <h2>Panel</h2>
      <div style={{ display: 'flex', gap: 16 }}>
        <div>Clientes: {data?.customers ?? '...'}</div>
        <div>Despachos: {data?.dispatches ?? '...'}</div>
        <div>Mensajes: {data?.messages ?? '...'}</div>
      </div>
    </div>
  )
}

export default DashboardPage
