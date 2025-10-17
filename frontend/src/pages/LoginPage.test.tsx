import { describe, it, expect } from 'vitest'
import { screen } from '@testing-library/react'
import LoginPage from './LoginPage'
import { renderWithProviders } from '../test/utils'

describe('LoginPage', () => {
  it('renders login form', () => {
    renderWithProviders(<LoginPage />)
    expect(screen.getByText('Ingresar')).toBeInTheDocument()
    expect(screen.getByText('Usuario')).toBeInTheDocument()
  })
})
