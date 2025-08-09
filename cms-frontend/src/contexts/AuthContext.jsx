import { createContext, useContext, useState, useEffect } from 'react'

const AuthContext = createContext()

export function useAuth() {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useAuth deve ser usado dentro de um AuthProvider')
  }
  return context
}

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)
  const [token, setToken] = useState(localStorage.getItem('token'))

  // API base URL
  const API_BASE = 'http://localhost:5000/api'

  // Função para fazer requisições autenticadas
  const apiRequest = async (endpoint, options = {}) => {
    const url = `${API_BASE}${endpoint}`
    const config = {
      headers: {
        'Content-Type': 'application/json',
        ...(token && { Authorization: `Bearer ${token}` }),
        ...options.headers,
      },
      ...options,
    }

    try {
      const response = await fetch(url, config)
      
      if (!response.ok) {
        if (response.status === 401) {
          logout()
          throw new Error('Sessão expirada')
        }
        const errorData = await response.json()
        throw new Error(errorData.error || 'Erro na requisição')
      }

      return await response.json()
    } catch (error) {
      console.error('Erro na API:', error)
      throw error
    }
  }

  // Função de login
  const login = async (username, password) => {
    try {
      const response = await apiRequest('/auth/login', {
        method: 'POST',
        body: JSON.stringify({ username, password }),
      })

      const { access_token, user: userData } = response
      
      setToken(access_token)
      setUser(userData)
      localStorage.setItem('token', access_token)
      localStorage.setItem('user', JSON.stringify(userData))

      return { success: true }
    } catch (error) {
      return { success: false, error: error.message }
    }
  }

  // Função de logout
  const logout = () => {
    setUser(null)
    setToken(null)
    localStorage.removeItem('token')
    localStorage.removeItem('user')
  }

  // Função para obter dados do usuário atual
  const getCurrentUser = async () => {
    try {
      const response = await apiRequest('/auth/me')
      setUser(response.user)
      localStorage.setItem('user', JSON.stringify(response.user))
      return response.user
    } catch (error) {
      console.error('Erro ao obter usuário:', error)
      logout()
      return null
    }
  }

  // Função para atualizar perfil
  const updateProfile = async (profileData) => {
    try {
      const response = await apiRequest('/auth/update-profile', {
        method: 'PUT',
        body: JSON.stringify(profileData),
      })

      setUser(response.user)
      localStorage.setItem('user', JSON.stringify(response.user))
      return { success: true, user: response.user }
    } catch (error) {
      return { success: false, error: error.message }
    }
  }

  // Função para alterar senha
  const changePassword = async (currentPassword, newPassword) => {
    try {
      await apiRequest('/auth/change-password', {
        method: 'POST',
        body: JSON.stringify({
          current_password: currentPassword,
          new_password: newPassword,
        }),
      })

      return { success: true }
    } catch (error) {
      return { success: false, error: error.message }
    }
  }

  // Verificar autenticação ao carregar
  useEffect(() => {
    const initAuth = async () => {
      const storedToken = localStorage.getItem('token')
      const storedUser = localStorage.getItem('user')

      if (storedToken && storedUser) {
        setToken(storedToken)
        try {
          // Verificar se o token ainda é válido
          await getCurrentUser()
        } catch (error) {
          // Token inválido, fazer logout
          logout()
        }
      }

      setLoading(false)
    }

    initAuth()
  }, [])

  const value = {
    user,
    token,
    loading,
    login,
    logout,
    getCurrentUser,
    updateProfile,
    changePassword,
    apiRequest,
  }

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  )
}

