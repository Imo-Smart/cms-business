import { useState, useEffect } from 'react'
import { useAuth } from '../contexts/AuthContext'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import {
  FileText,
  PenTool,
  Users,
  Image,
  TrendingUp,
  Eye,
  Calendar,
  Activity
} from 'lucide-react'

export default function Dashboard() {
  const { user, apiRequest } = useAuth()
  const [stats, setStats] = useState({
    pages: 0,
    posts: 0,
    users: 0,
    media: 0
  })
  const [recentActivity, setRecentActivity] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadDashboardData()
  }, [])

  const loadDashboardData = async () => {
    try {
      setLoading(true)
      
      // Carregar estatísticas básicas
      const [pagesRes, postsRes, usersRes, mediaRes] = await Promise.all([
        apiRequest('/pages'),
        apiRequest('/posts'),
        apiRequest('/users'),
        apiRequest('/media')
      ])

      setStats({
        pages: pagesRes.length,
        posts: postsRes.length,
        users: usersRes.length,
        media: mediaRes.length
      })

      // Simular atividade recente (em um sistema real, viria da API)
      setRecentActivity([
        {
          id: 1,
          type: 'post',
          title: 'Novo post criado',
          description: 'Post "Bem-vindos ao CMS" foi criado',
          time: '2 horas atrás',
          icon: PenTool
        },
        {
          id: 2,
          type: 'page',
          title: 'Página atualizada',
          description: 'Página "Sobre" foi atualizada',
          time: '4 horas atrás',
          icon: FileText
        },
        {
          id: 3,
          type: 'user',
          title: 'Novo usuário',
          description: 'Usuário "editor" foi criado',
          time: '1 dia atrás',
          icon: Users
        },
        {
          id: 4,
          type: 'media',
          title: 'Imagem enviada',
          description: 'Nova imagem foi adicionada à biblioteca',
          time: '2 dias atrás',
          icon: Image
        }
      ])

    } catch (error) {
      console.error('Erro ao carregar dados do dashboard:', error)
    } finally {
      setLoading(false)
    }
  }

  const statCards = [
    {
      title: 'Total de Páginas',
      value: stats.pages,
      description: 'Páginas publicadas',
      icon: FileText,
      color: 'text-blue-600',
      bgColor: 'bg-blue-100'
    },
    {
      title: 'Total de Posts',
      value: stats.posts,
      description: 'Posts no blog',
      icon: PenTool,
      color: 'text-green-600',
      bgColor: 'bg-green-100'
    },
    {
      title: 'Usuários',
      value: stats.users,
      description: 'Usuários cadastrados',
      icon: Users,
      color: 'text-purple-600',
      bgColor: 'bg-purple-100'
    },
    {
      title: 'Arquivos de Mídia',
      value: stats.media,
      description: 'Imagens e documentos',
      icon: Image,
      color: 'text-orange-600',
      bgColor: 'bg-orange-100'
    }
  ]

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
        <p className="text-gray-600 mt-2">
          Bem-vindo de volta, {user?.first_name || user?.username}! Aqui está um resumo do seu CMS.
        </p>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {statCards.map((stat, index) => {
          const Icon = stat.icon
          return (
            <Card key={index} className="hover:shadow-lg transition-shadow duration-200">
              <CardContent className="p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm font-medium text-gray-600">{stat.title}</p>
                    <p className="text-3xl font-bold text-gray-900 mt-2">{stat.value}</p>
                    <p className="text-sm text-gray-500 mt-1">{stat.description}</p>
                  </div>
                  <div className={`p-3 rounded-full ${stat.bgColor}`}>
                    <Icon className={`w-6 h-6 ${stat.color}`} />
                  </div>
                </div>
              </CardContent>
            </Card>
          )
        })}
      </div>

      {/* Content Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Recent Activity */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center space-x-2">
              <Activity className="w-5 h-5" />
              <span>Atividade Recente</span>
            </CardTitle>
            <CardDescription>
              Últimas ações realizadas no sistema
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {recentActivity.map((activity) => {
                const Icon = activity.icon
                return (
                  <div key={activity.id} className="flex items-start space-x-3 p-3 rounded-lg hover:bg-gray-50 transition-colors">
                    <div className="p-2 bg-gray-100 rounded-full">
                      <Icon className="w-4 h-4 text-gray-600" />
                    </div>
                    <div className="flex-1 min-w-0">
                      <p className="text-sm font-medium text-gray-900">{activity.title}</p>
                      <p className="text-sm text-gray-500">{activity.description}</p>
                      <p className="text-xs text-gray-400 mt-1">{activity.time}</p>
                    </div>
                  </div>
                )
              })}
            </div>
          </CardContent>
        </Card>

        {/* Quick Actions */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center space-x-2">
              <TrendingUp className="w-5 h-5" />
              <span>Ações Rápidas</span>
            </CardTitle>
            <CardDescription>
              Acesso rápido às funcionalidades principais
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-2 gap-4">
              <Button className="h-20 flex flex-col space-y-2" variant="outline">
                <PenTool className="w-6 h-6" />
                <span className="text-sm">Novo Post</span>
              </Button>
              <Button className="h-20 flex flex-col space-y-2" variant="outline">
                <FileText className="w-6 h-6" />
                <span className="text-sm">Nova Página</span>
              </Button>
              <Button className="h-20 flex flex-col space-y-2" variant="outline">
                <Image className="w-6 h-6" />
                <span className="text-sm">Upload Mídia</span>
              </Button>
              <Button className="h-20 flex flex-col space-y-2" variant="outline">
                <Users className="w-6 h-6" />
                <span className="text-sm">Novo Usuário</span>
              </Button>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* System Status */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center space-x-2">
            <Calendar className="w-5 h-5" />
            <span>Status do Sistema</span>
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="text-center">
              <div className="w-12 h-12 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-2">
                <div className="w-3 h-3 bg-green-500 rounded-full"></div>
              </div>
              <p className="text-sm font-medium text-gray-900">Sistema Online</p>
              <p className="text-xs text-gray-500">Funcionando normalmente</p>
            </div>
            <div className="text-center">
              <div className="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-2">
                <Eye className="w-6 h-6 text-blue-600" />
              </div>
              <p className="text-sm font-medium text-gray-900">Última Atualização</p>
              <p className="text-xs text-gray-500">Hoje às 14:30</p>
            </div>
            <div className="text-center">
              <div className="w-12 h-12 bg-purple-100 rounded-full flex items-center justify-center mx-auto mb-2">
                <TrendingUp className="w-6 h-6 text-purple-600" />
              </div>
              <p className="text-sm font-medium text-gray-900">Performance</p>
              <p className="text-xs text-gray-500">Excelente</p>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}

