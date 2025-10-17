import React from 'react'
import { useQuery } from '@tanstack/react-query'
import axios from 'axios'

type Dispatch = {
  id: number
  customer_full_name: string
  scheduled_at: string
  delivered_at?: string | null
  quantity_liters: number
}

const DispatchesPage: React.FC = () => {
  const { data, isLoading } = useQuery({
    queryKey: ['dispatches'],
    queryFn: async () => (await axios.get('/dispatches/')).data,
  })

  return (
    <div>
      <h2>Despachos</h2>
      {isLoading ? (
        <div>Cargando...</div>
      ) : (
        <ul>
          {data?.results?.map((d: Dispatch) => (
            <li key={d.id}>
              {d.customer_full_name} - {new Date(d.scheduled_at).toLocaleString()} - {d.quantity_liters}L
            </li>
          ))}
        </ul>
      )}
    </div>
  )
}

export default DispatchesPage
