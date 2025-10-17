import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import { createBrowserRouter, RouterProvider } from 'react-router-dom'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import LoginPage from './pages/LoginPage'
import DashboardPage from './pages/DashboardPage'
import CustomersPage from './pages/CustomersPage'
import DispatchesPage from './pages/DispatchesPage'
import MessagingPage from './pages/MessagingPage'
import AppShell from './ui/AppShell'
import { AuthProvider } from './state/auth'

const router = createBrowserRouter([
  { path: '/login', element: <LoginPage /> },
  {
    path: '/',
    element: (
      <AuthProvider>
        <AppShell />
      </AuthProvider>
    ),
    children: [
      { index: true, element: <DashboardPage /> },
      { path: 'customers', element: <CustomersPage /> },
      { path: 'dispatches', element: <DispatchesPage /> },
      { path: 'messaging', element: <MessagingPage /> },
    ],
  },
])

const queryClient = new QueryClient()

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <QueryClientProvider client={queryClient}>
      <RouterProvider router={router} />
    </QueryClientProvider>
  </StrictMode>,
)
