import { useState, useEffect } from 'react'
import { useAuth } from '../contexts/AuthContext'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { PenTool, Plus } from 'lucide-react'

export default function Posts() {
  const { apiRequest } = useAuth()
  const [posts, setPosts] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadPosts()
  }, [])

  const loadPosts = async () => {
    try {
      setLoading(true)
      const response = await apiRequest('/posts')
      setPosts(response)
    } catch (error) {
      console.error('Erro ao carregar posts:', error)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Posts</h1>
          <p className="text-gray-600 mt-2">Gerencie os posts do seu blog</p>
        </div>
        <Button className="flex items-center space-x-2">
          <Plus className="w-4 h-4" />
          <span>Novo Post</span>
        </Button>
      </div>

      <Card>
        <CardHeader>
          <CardTitle className="flex items-center space-x-2">
            <PenTool className="w-5 h-5" />
            <span>Lista de Posts</span>
          </CardTitle>
          <CardDescription>
            {posts.length} post(s) encontrado(s)
          </CardDescription>
        </CardHeader>
        <CardContent>
          {posts.length === 0 ? (
            <div className="text-center py-12">
              <PenTool className="w-12 h-12 text-gray-400 mx-auto mb-4" />
              <h3 className="text-lg font-medium text-gray-900 mb-2">
                Nenhum post encontrado
              </h3>
              <p className="text-gray-500 mb-4">
                Comece criando seu primeiro post
              </p>
              <Button>
                <Plus className="w-4 h-4 mr-2" />
                Criar Primeiro Post
              </Button>
            </div>
          ) : (
            <div className="text-center py-8">
              <p className="text-gray-600">
                Funcionalidade de posts em desenvolvimento...
              </p>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  )
}

