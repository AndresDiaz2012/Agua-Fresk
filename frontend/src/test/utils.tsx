import React from 'react'
import { render } from '@testing-library/react'
import { AuthProvider } from '../state/auth'
import { MemoryRouter } from 'react-router-dom'

export function renderWithProviders(ui: React.ReactElement) {
  return render(
    <AuthProvider>
      <MemoryRouter>{ui}</MemoryRouter>
    </AuthProvider>
  )
}
