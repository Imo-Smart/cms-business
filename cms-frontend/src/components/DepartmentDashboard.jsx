import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Badge } from './ui/badge';
import { Tabs, TabsContent, TabsList, TabsTrigger } from './ui/tabs';
import { 
  Building2, 
  Users, 
  TrendingUp, 
  TrendingDown,
  AlertTriangle,
  CheckCircle,
  Clock,
  DollarSign,
  BarChart3,
  PieChart,
  Activity,
  Target,
  Zap,
  Settings
} from 'lucide-react';

const DepartmentDashboard = ({ departmentCode = 'FIN' }) => {
  const [dashboardData, setDashboardData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchDepartmentDashboard();
  }, [departmentCode]);

  const fetchDepartmentDashboard = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await fetch(`/api/departments/1/dashboard`, {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });

      if (response.ok) {
        const result = await response.json();
        setDashboardData(result.data);
      }
    } catch (error) {
      console.error('Erro ao carregar dashboard do departamento:', error);
    } finally {
      setLoading(false);
    }
  };

  const getDepartmentConfig = (code) => {
    const configs = {
      'DIR': {
        name: 'Diretoria Executiva',
        color: 'bg-purple-600',
        icon: Building2,
        description: 'Visão estratégica e governança corporativa'
      },
      'FIN': {
        name: 'Departamento Financeiro',
        color: 'bg-green-600',
        icon: DollarSign,
        description: 'Gestão financeira e controle de custos'
      },
      'VEN': {
        name: 'Departamento de Vendas',
        color: 'bg-blue-600',
        icon: TrendingUp,
        description: 'Gestão comercial e relacionamento com clientes'
      },
      'RH': {
        name: 'Recursos Humanos',
        color: 'bg-orange-600',
        icon: Users,
        description: 'Gestão de pessoas e desenvolvimento organizacional'
      },
      'OBR': {
        name: 'Departamento de Obras',
        color: 'bg-yellow-600',
        icon: Building2,
        description: 'Execução e controle de obras'
      },
      'ENG': {
        name: 'Departamento de Engenharia',
        color: 'bg-indigo-600',
        icon: Settings,
        description: 'Projetos técnicos e especificações'
      },
      'CPR': {
        name: 'Departamento de Compras',
        color: 'bg-red-600',
        icon: Target,
        description: 'Aquisições e gestão de fornecedores'
      },
      'QST': {
        name: 'Qualidade e Segurança',
        color: 'bg-teal-600',
        icon: CheckCircle,
        description: 'Controle de qualidade e segurança do trabalho'
      }
    };

    return configs[code] || configs['FIN'];
  };

  const config = getDepartmentConfig(departmentCode);
  const IconComponent = config.icon;

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-center">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-2 text-gray-600">Carregando dashboard do departamento...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header do Departamento */}
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-4">
          <div className={`p-3 rounded-lg ${config.color} text-white`}>
            <IconComponent className="h-8 w-8" />
          </div>
          <div>
            <h1 className="text-3xl font-bold text-gray-900">{config.name}</h1>
            <p className="text-gray-600">{config.description}</p>
          </div>
        </div>
        <div className="flex space-x-2">
          <Button variant="outline">
            <BarChart3 className="h-4 w-4 mr-2" />
            Relatórios
          </Button>
          <Button>
            <Settings className="h-4 w-4 mr-2" />
            Configurações
          </Button>
        </div>
      </div>

      {/* Métricas Principais */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {dashboardData?.metrics?.map((metric, index) => (
          <Card key={index}>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">{metric.name}</CardTitle>
              {metric.trend === 'up' && <TrendingUp className="h-4 w-4 text-green-600" />}
              {metric.trend === 'down' && <TrendingDown className="h-4 w-4 text-red-600" />}
              {metric.trend === 'stable' && <Activity className="h-4 w-4 text-gray-600" />}
            </CardHeader>
            <CardContent>
              <div className={`text-2xl font-bold ${
                metric.type === 'currency' ? 'text-green-600' : 
                metric.type === 'percentage' ? 'text-blue-600' : 
                'text-gray-900'
              }`}>
                {metric.value}
              </div>
              <p className="text-xs text-muted-foreground">
                {metric.trend === 'up' && '↗ Crescimento'}
                {metric.trend === 'down' && '↘ Redução'}
                {metric.trend === 'stable' && '→ Estável'}
              </p>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Tabs de Conteúdo */}
      <Tabs defaultValue="overview" className="space-y-4">
        <TabsList>
          <TabsTrigger value="overview">Visão Geral</TabsTrigger>
          <TabsTrigger value="activities">Atividades</TabsTrigger>
          <TabsTrigger value="reports">Relatórios</TabsTrigger>
          <TabsTrigger value="team">Equipe</TabsTrigger>
        </TabsList>

        {/* Visão Geral */}
        <TabsContent value="overview" className="space-y-4">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Ações Rápidas */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <Zap className="h-5 w-5 mr-2" />
                  Ações Rápidas
                </CardTitle>
                <CardDescription>Acesso rápido às funcionalidades principais</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-1 gap-3">
                  {dashboardData?.quick_actions?.map((action, index) => (
                    <Button key={index} variant="outline" className="justify-start">
                      <div className="flex items-center">
                        <div className="w-2 h-2 bg-blue-600 rounded-full mr-3"></div>
                        {action.name}
                      </div>
                    </Button>
                  ))}
                </div>
              </CardContent>
            </Card>

            {/* Status do Departamento */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <Activity className="h-5 w-5 mr-2" />
                  Status do Departamento
                </CardTitle>
                <CardDescription>Indicadores de performance</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div className="flex items-center justify-between">
                    <span className="text-sm font-medium">Produtividade</span>
                    <Badge variant="default">92%</Badge>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-sm font-medium">Qualidade</span>
                    <Badge variant="default">95%</Badge>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-sm font-medium">Prazo</span>
                    <Badge variant="outline">87%</Badge>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-sm font-medium">Orçamento</span>
                    <Badge variant="default">103%</Badge>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Gráficos e Análises */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <Card>
              <CardHeader>
                <CardTitle>Performance Mensal</CardTitle>
                <CardDescription>Evolução dos indicadores principais</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="h-64 flex items-center justify-center bg-gray-50 rounded-lg">
                  <div className="text-center">
                    <PieChart className="h-12 w-12 text-gray-400 mx-auto mb-2" />
                    <p className="text-gray-500">Gráfico de Performance</p>
                    <p className="text-sm text-gray-400">Dados em tempo real</p>
                  </div>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Comparativo Anual</CardTitle>
                <CardDescription>Análise comparativa com períodos anteriores</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="h-64 flex items-center justify-center bg-gray-50 rounded-lg">
                  <div className="text-center">
                    <BarChart3 className="h-12 w-12 text-gray-400 mx-auto mb-2" />
                    <p className="text-gray-500">Gráfico Comparativo</p>
                    <p className="text-sm text-gray-400">Análise anual</p>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        {/* Atividades Recentes */}
        <TabsContent value="activities" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center">
                <Clock className="h-5 w-5 mr-2" />
                Atividades Recentes
              </CardTitle>
              <CardDescription>Últimas ações realizadas no departamento</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {[
                  { action: 'Aprovação de orçamento', user: 'João Silva', time: '2 horas atrás', status: 'success' },
                  { action: 'Revisão de projeto', user: 'Maria Santos', time: '4 horas atrás', status: 'pending' },
                  { action: 'Liberação de pagamento', user: 'Carlos Oliveira', time: '6 horas atrás', status: 'success' },
                  { action: 'Análise de proposta', user: 'Ana Costa', time: '1 dia atrás', status: 'warning' },
                ].map((activity, index) => (
                  <div key={index} className="flex items-center justify-between p-3 border rounded-lg">
                    <div className="flex items-center space-x-3">
                      <div className={`w-3 h-3 rounded-full ${
                        activity.status === 'success' ? 'bg-green-500' :
                        activity.status === 'pending' ? 'bg-yellow-500' :
                        activity.status === 'warning' ? 'bg-orange-500' : 'bg-gray-500'
                      }`}></div>
                      <div>
                        <p className="font-medium">{activity.action}</p>
                        <p className="text-sm text-gray-600">por {activity.user}</p>
                      </div>
                    </div>
                    <span className="text-sm text-gray-500">{activity.time}</span>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Relatórios */}
        <TabsContent value="reports" className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {[
              { name: 'Relatório Mensal', description: 'Resumo das atividades do mês', icon: BarChart3 },
              { name: 'Análise de Performance', description: 'Indicadores de desempenho', icon: TrendingUp },
              { name: 'Relatório de Custos', description: 'Controle de gastos e orçamento', icon: DollarSign },
              { name: 'Relatório de Qualidade', description: 'Métricas de qualidade', icon: CheckCircle },
              { name: 'Relatório de Equipe', description: 'Performance da equipe', icon: Users },
              { name: 'Relatório Executivo', description: 'Resumo para diretoria', icon: Building2 },
            ].map((report, index) => (
              <Card key={index} className="cursor-pointer hover:shadow-md transition-shadow">
                <CardHeader>
                  <CardTitle className="flex items-center text-lg">
                    <report.icon className="h-5 w-5 mr-2 text-blue-600" />
                    {report.name}
                  </CardTitle>
                  <CardDescription>{report.description}</CardDescription>
                </CardHeader>
                <CardContent>
                  <Button variant="outline" className="w-full">
                    Gerar Relatório
                  </Button>
                </CardContent>
              </Card>
            ))}
          </div>
        </TabsContent>

        {/* Equipe */}
        <TabsContent value="team" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center">
                <Users className="h-5 w-5 mr-2" />
                Equipe do Departamento
              </CardTitle>
              <CardDescription>Membros e suas funções</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {[
                  { name: 'João Silva', role: 'Gerente', status: 'online', avatar: 'JS' },
                  { name: 'Maria Santos', role: 'Analista Sênior', status: 'online', avatar: 'MS' },
                  { name: 'Carlos Oliveira', role: 'Coordenador', status: 'offline', avatar: 'CO' },
                  { name: 'Ana Costa', role: 'Analista', status: 'online', avatar: 'AC' },
                ].map((member, index) => (
                  <div key={index} className="flex items-center justify-between p-3 border rounded-lg">
                    <div className="flex items-center space-x-3">
                      <div className="w-10 h-10 bg-blue-600 text-white rounded-full flex items-center justify-center font-semibold">
                        {member.avatar}
                      </div>
                      <div>
                        <p className="font-medium">{member.name}</p>
                        <p className="text-sm text-gray-600">{member.role}</p>
                      </div>
                    </div>
                    <Badge variant={member.status === 'online' ? 'default' : 'secondary'}>
                      {member.status === 'online' ? 'Online' : 'Offline'}
                    </Badge>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );
};

export default DepartmentDashboard;

