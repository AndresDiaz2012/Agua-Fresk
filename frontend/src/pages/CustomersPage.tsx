import React, { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import axios from 'axios'

type Customer = {
  id: number
  full_name: string
  address: string
  phone_e164: string
  is_active: boolean
  last_dispatch_date?: string | null
}

const CustomersPage: React.FC = () => {
  const qc = useQueryClient()
  const [search, setSearch] = useState('')
  const { data, isLoading } = useQuery({
    queryKey: ['customers', search],
    queryFn: async () => {
      const { data } = await axios.get(`/customers/?search=${encodeURIComponent(search)}`)
      return data
    },
  })
  const sendReminder = useMutation({
    mutationFn: async (id: number) => {
      await axios.post(`/customers/${id}/send_reminder/`)
    },
  })

  return (
    <div>
      <h2>Clientes</h2>
      <input placeholder="Buscar" value={search} onChange={(e) => setSearch(e.target.value)} />
      {isLoading ? (
        <div>Cargando...</div>
      ) : (
        <table>
          <thead>
            <tr>
              <th>Nombre</th>
              <th>Teléfono</th>
              <th>Dirección</th>
              <th>Último despacho</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            {data?.results?.map((c: Customer) => (
              <tr key={c.id}>
                <td>{c.full_name}</td>
                <td>{c.phone_e164}</td>
                <td>{c.address}</td>
                <td>{c.last_dispatch_date ?? '-'}</td>
                <td>
                  <button onClick={() => sendReminder.mutate(c.id)} disabled={sendReminder.isPending}>
                    Recordatorio
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  )
}

export default CustomersPage
