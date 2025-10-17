import React from 'react'
import { useQuery } from '@tanstack/react-query'
import axios from 'axios'

type MessageLog = {
  id: number
  customer_full_name: string
  template_name: string
  status: string
  created_at: string
}

const MessagingPage: React.FC = () => {
  const { data, isLoading } = useQuery({
    queryKey: ['messages'],
    queryFn: async () => (await axios.get('/messaging/')).data,
  })

  return (
    <div>
      <h2>Mensajería</h2>
      {isLoading ? (
        <div>Cargando...</div>
      ) : (
        <table>
          <thead>
            <tr>
              <th>Cliente</th>
              <th>Plantilla</th>
              <th>Estado</th>
              <th>Fecha</th>
            </tr>
          </thead>
          <tbody>
            {data?.results?.map((m: MessageLog) => (
              <tr key={m.id}>
                <td>{m.customer_full_name}</td>
                <td>{m.template_name}</td>
                <td>{m.status}</td>
                <td>{new Date(m.created_at).toLocaleString()}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  )
}

export default MessagingPage
