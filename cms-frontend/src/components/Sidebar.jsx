import { Link, useLocation } from 'react-router-dom'
import { cn } from '@/lib/utils'
import {
  LayoutDashboard,
  FileText,
  PenTool,
  FolderOpen,
  Image,
  Users,
  Settings,
  LogOut,
  ChevronLeft,
  ChevronRight,
  DollarSign,
  ShoppingCart,
  Calculator,
  Receipt,
  Package,
  UserCheck
} from 'lucide-react'
import { useAuth } from '../contexts/AuthContext'
import { Button } from '@/components/ui/button'

const menuItems = [
  {
    title: 'Dashboard',
    href: '/dashboard',
    icon: LayoutDashboard,
  },
  {
    title: 'Financeiro',
    href: '/financial',
    icon: DollarSign,
  },
  {
    title: 'Vendas',
    href: '/sales',
    icon: ShoppingCart,
  },
  {
    title: 'Contabilidade',
    href: '/accounting',
    icon: Calculator,
  },
  {
    title: 'Fiscal',
    href: '/fiscal',
    icon: Receipt,
  },
  {
    title: 'Páginas',
    href: '/pages',
    icon: FileText,
  },
  {
    title: 'Posts',
    href: '/posts',
    icon: PenTool,
  },
  {
    title: 'Categorias',
    href: '/categories',
    icon: FolderOpen,
  },
  {
    title: 'Mídia',
    href: '/media',
    icon: Image,
  },
  {
    title: 'Usuários',
    href: '/users',
    icon: Users,
  },
  {
    title: 'Configurações',
    href: '/settings',
    icon: Settings,
  },
  {
    title: 'Sistema Modular',
    href: '/modules',
    icon: Package,
  },
  {
    title: 'Recursos Humanos',
    href: '/hr',
    icon: UserCheck,
  },
]

export default function Sidebar({ isOpen }) {
  const location = useLocation()
  const { user, logout } = useAuth()

  const handleLogout = () => {
    logout()
  }

  return (
    <div
      className={cn(
        'bg-white shadow-lg transition-all duration-300 ease-in-out flex flex-col',
        isOpen ? 'w-64' : 'w-16'
      )}
    >
      {/* Header */}
      <div className="p-4 border-b border-gray-200">
        <div className="flex items-center space-x-3">
          <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center">
            <span className="text-white font-bold text-sm">CMS</span>
          </div>
          {isOpen && (
            <div>
              <h1 className="font-bold text-lg text-gray-900">CMS Business</h1>
              <p className="text-xs text-gray-500">Painel Administrativo</p>
            </div>
          )}
        </div>
      </div>

      {/* User Info */}
      {isOpen && user && (
        <div className="p-4 border-b border-gray-200 bg-gray-50">
          <div className="flex items-center space-x-3">
            <div className="w-10 h-10 bg-blue-100 rounded-full flex items-center justify-center">
              <span className="text-blue-600 font-semibold text-sm">
                {user.first_name ? user.first_name[0] : user.username[0]}
              </span>
            </div>
            <div className="flex-1 min-w-0">
              <p className="text-sm font-medium text-gray-900 truncate">
                {user.first_name ? `${user.first_name} ${user.last_name}` : user.username}
              </p>
              <p className="text-xs text-gray-500 truncate">{user.role_name}</p>
            </div>
          </div>
        </div>
      )}

      {/* Navigation */}
      <nav className="flex-1 p-4 space-y-2">
        {menuItems.map((item) => {
          const Icon = item.icon
          const isActive = location.pathname === item.href

          return (
            <Link
              key={item.href}
              to={item.href}
              className={cn(
                'flex items-center space-x-3 px-3 py-2 rounded-lg transition-colors duration-200',
                isActive
                  ? 'bg-blue-100 text-blue-700 border border-blue-200'
                  : 'text-gray-600 hover:bg-gray-100 hover:text-gray-900'
              )}
              title={!isOpen ? item.title : undefined}
            >
              <Icon className="w-5 h-5 flex-shrink-0" />
              {isOpen && (
                <span className="font-medium">{item.title}</span>
              )}
            </Link>
          )
        })}
      </nav>

      {/* Logout */}
      <div className="p-4 border-t border-gray-200">
        <Button
          onClick={handleLogout}
          variant="ghost"
          className={cn(
            'w-full justify-start text-red-600 hover:text-red-700 hover:bg-red-50',
            !isOpen && 'px-3'
          )}
          title={!isOpen ? 'Sair' : undefined}
        >
          <LogOut className="w-5 h-5 flex-shrink-0" />
          {isOpen && <span className="ml-3">Sair</span>}
        </Button>
      </div>
    </div>
  )
}

