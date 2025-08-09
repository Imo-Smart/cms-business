import { useState, useEffect } from 'react'
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import './App.css'

// Componentes
import Home from './components/Home'
import Register from './components/Register'
import Login from './components/Login'
import Dashboard from './components/Dashboard'
import Sidebar from './components/Sidebar'
import Header from './components/Header'
import Pages from './components/Pages'
import Posts from './components/Posts'
import Categories from './components/Categories'
import Media from './components/Media'
import Users from './components/Users'
import Settings from './components/Settings'
import FinancialModule from './components/FinancialModule'
import SalesModule from './components/SalesModule'
import DepartmentDashboard from './components/DepartmentDashboard'
import ModularSystem from './components/ModularSystem'
import HRModule from './components/HRModule'

// Context para autenticação
import { AuthProvider, useAuth } from './contexts/AuthContext'

// Layout principal do CMS
function CMSLayout({ children }) {
  const [sidebarOpen, setSidebarOpen] = useState(true)

  return (
    <div className="flex h-screen bg-gray-50">
      <Sidebar isOpen={sidebarOpen} />
      <div className="flex-1 flex flex-col overflow-hidden">
        <Header onMenuClick={() => setSidebarOpen(!sidebarOpen)} />
        <main className="flex-1 overflow-x-hidden overflow-y-auto bg-gray-50 p-6">
          {children}
        </main>
      </div>
    </div>
  )
}

// Componente para rotas protegidas
function ProtectedRoute({ children }) {
  const { user, loading } = useAuth()

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-600"></div>
      </div>
    )
  }

  if (!user) {
    return <Navigate to="/login" replace />
  }

  return <CMSLayout>{children}</CMSLayout>
}

// Componente principal da aplicação
function AppContent() {
  const { user } = useAuth()

  return (
    <Router>
      <Routes>
        {/* Página inicial pública */}
        <Route path="/" element={<Home />} />
        
        {/* Página de registro */}
        <Route path="/register" element={<Register />} />
        
        {/* Página de login */}
        <Route 
          path="/login" 
          element={user ? <Navigate to="/dashboard" replace /> : <Login />} 
        />
        
        {/* Dashboard - rota protegida */}
        <Route 
          path="/dashboard" 
          element={
            <ProtectedRoute>
              <Dashboard />
            </ProtectedRoute>
          } 
        />
        
        {/* Outras rotas protegidas */}
        <Route 
          path="/pages" 
          element={
            <ProtectedRoute>
              <Pages />
            </ProtectedRoute>
          } 
        />
        <Route 
          path="/posts" 
          element={
            <ProtectedRoute>
              <Posts />
            </ProtectedRoute>
          } 
        />
        <Route 
          path="/categories" 
          element={
            <ProtectedRoute>
              <Categories />
            </ProtectedRoute>
          } 
        />
        <Route 
          path="/media" 
          element={
            <ProtectedRoute>
              <Media />
            </ProtectedRoute>
          } 
        />
        <Route 
          path="/users" 
          element={
            <ProtectedRoute>
              <Users />
            </ProtectedRoute>
          } 
        />
        <Route 
          path="/settings" 
          element={
            <ProtectedRoute>
              <Settings />
            </ProtectedRoute>
          } 
        />
        <Route 
          path="/financial" 
          element={
            <ProtectedRoute>
              <FinancialModule />
            </ProtectedRoute>
          } 
        />
        <Route 
          path="/sales" 
          element={
            <ProtectedRoute>
              <SalesModule />
            </ProtectedRoute>
          } 
        />
        <Route 
          path="/departments/:code" 
          element={
            <ProtectedRoute>
              <DepartmentDashboard />
            </ProtectedRoute>
          } 
        />
        <Route 
          path="/modules" 
          element={
            <ProtectedRoute>
              <ModularSystem />
            </ProtectedRoute>
          } 
        />
        <Route 
          path="/hr" 
          element={
            <ProtectedRoute>
              <HRModule />
            </ProtectedRoute>
          } 
        />
        
        {/* Rota 404 - redireciona para home */}
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </Router>
  )
}

function App() {
  return (
    <AuthProvider>
      <AppContent />
    </AuthProvider>
  )
}

export default App

