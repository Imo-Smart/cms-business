import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Badge } from './ui/badge';
import { Tabs, TabsContent, TabsList, TabsTrigger } from './ui/tabs';
import { Switch } from './ui/switch';
import { 
  Package, 
  DollarSign, 
  CheckCircle, 
  XCircle,
  Clock,
  Users,
  Building2,
  Settings,
  ShoppingCart,
  Calculator,
  FileText,
  Truck,
  Shield,
  Zap,
  BarChart3
} from 'lucide-react';

const ModularSystem = () => {
  const [modules, setModules] = useState([]);
  const [departments, setDepartments] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchModules();
    fetchDepartments();
  }, []);

  const fetchModules = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await fetch('/api/departments/modules', {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });

      if (response.ok) {
        const result = await response.json();
        setModules(result.data);
      }
    } catch (error) {
      console.error('Erro ao carregar módulos:', error);
    }
  };

  const fetchDepartments = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await fetch('/api/departments/hierarchy', {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });

      if (response.ok) {
        const result = await response.json();
        setDepartments(result.data.departments || []);
      }
    } catch (error) {
      console.error('Erro ao carregar departamentos:', error);
    } finally {
      setLoading(false);
    }
  };

  const getModuleIcon = (moduleCode) => {
    const icons = {
      'dashboard_executivo': BarChart3,
      'relatorios_gerenciais': FileText,
      'indicadores_kpi': BarChart3,
      'aprovacoes': CheckCircle,
      'gestao_documentos': FileText,
      'protocolo': Clock,
      'contratos': FileText,
      'contas_pagar': DollarSign,
      'contas_receber': DollarSign,
      'fluxo_caixa': DollarSign,
      'conciliacao_bancaria': Building2,
      'centro_custos': Calculator,
      'folha_pagamento': Users,
      'ponto_eletronico': Clock,
      'ferias_13': Users,
      'admissao_demissao': Users,
      'treinamentos': Users,
      'crm_vendas': ShoppingCart,
      'propostas': FileText,
      'comissoes': DollarSign,
      'pipeline_vendas': BarChart3,
      'projetos_tecnicos': Settings,
      'aprovacao_projetos': CheckCircle,
      'especificacoes': FileText,
      'cronograma_obras': Clock,
      'medicao_obras': Calculator,
      'diario_obras': FileText,
      'controle_materiais': Package,
      'cotacoes': ShoppingCart,
      'pedidos_compra': ShoppingCart,
      'fornecedores': Building2,
      'estoque': Package,
      'auditorias': Shield,
      'nao_conformidades': XCircle,
      'seguranca_trabalho': Shield,
      'certificacoes': CheckCircle
    };

    return icons[moduleCode] || Package;
  };

  const getDepartmentColor = (deptCode) => {
    const colors = {
      'DIR': 'bg-purple-100 text-purple-800',
      'ADM': 'bg-blue-100 text-blue-800',
      'FIN': 'bg-green-100 text-green-800',
      'JUR': 'bg-indigo-100 text-indigo-800',
      'AUD': 'bg-gray-100 text-gray-800',
      'RH': 'bg-orange-100 text-orange-800',
      'TI': 'bg-cyan-100 text-cyan-800',
      'VEN': 'bg-blue-100 text-blue-800',
      'MKT': 'bg-pink-100 text-pink-800',
      'SAC': 'bg-teal-100 text-teal-800',
      'ENG': 'bg-indigo-100 text-indigo-800',
      'PRJ': 'bg-purple-100 text-purple-800',
      'ORC': 'bg-yellow-100 text-yellow-800',
      'OBR': 'bg-orange-100 text-orange-800',
      'CPR': 'bg-red-100 text-red-800',
      'LOG': 'bg-blue-100 text-blue-800',
      'PCP': 'bg-green-100 text-green-800',
      'MAN': 'bg-gray-100 text-gray-800',
      'QST': 'bg-teal-100 text-teal-800',
      'AMB': 'bg-green-100 text-green-800'
    };

    return colors[deptCode] || 'bg-gray-100 text-gray-800';
  };

  const calculateTotalCost = (departmentModules) => {
    return departmentModules.reduce((total, module) => total + module.price, 0);
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-center">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-2 text-gray-600">Carregando sistema modular...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Sistema Modular</h1>
          <p className="text-gray-600">Gestão de módulos por departamento - R$ 30,00 por módulo</p>
        </div>
        <div className="flex space-x-2">
          <Button variant="outline">
            <BarChart3 className="h-4 w-4 mr-2" />
            Relatório de Custos
          </Button>
          <Button>
            <Settings className="h-4 w-4 mr-2" />
            Configurar Módulos
          </Button>
        </div>
      </div>

      {/* Resumo Financeiro */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Módulos Ativos</CardTitle>
            <Package className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">47</div>
            <p className="text-xs text-muted-foreground">
              De 60 módulos disponíveis
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Custo Mensal</CardTitle>
            <DollarSign className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-green-600">R$ 1.410,00</div>
            <p className="text-xs text-muted-foreground">
              47 módulos × R$ 30,00
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Departamentos</CardTitle>
            <Building2 className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">20</div>
            <p className="text-xs text-muted-foreground">
              Departamentos ativos
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Economia</CardTitle>
            <Zap className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-blue-600">R$ 390,00</div>
            <p className="text-xs text-muted-foreground">
              Vs. sistema tradicional
            </p>
          </CardContent>
        </Card>
      </div>

      {/* Tabs de Conteúdo */}
      <Tabs defaultValue="departments" className="space-y-4">
        <TabsList>
          <TabsTrigger value="departments">Por Departamento</TabsTrigger>
          <TabsTrigger value="modules">Catálogo de Módulos</TabsTrigger>
          <TabsTrigger value="billing">Faturamento</TabsTrigger>
          <TabsTrigger value="analytics">Análises</TabsTrigger>
        </TabsList>

        {/* Por Departamento */}
        <TabsContent value="departments" className="space-y-4">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {Object.entries(modules).map(([deptCode, deptModules]) => {
              const department = departments.find(d => d.code === deptCode) || 
                                departments.flatMap(d => d.children || []).find(c => c.code === deptCode);
              
              if (!department) return null;

              const totalCost = calculateTotalCost(deptModules);
              const activeModules = deptModules.filter(m => m.is_active !== false).length;

              return (
                <Card key={deptCode}>
                  <CardHeader>
                    <div className="flex items-center justify-between">
                      <div>
                        <CardTitle className="flex items-center">
                          <Badge className={`mr-2 ${getDepartmentColor(deptCode)}`}>
                            {deptCode}
                          </Badge>
                          {department.name}
                        </CardTitle>
                        <CardDescription>
                          {activeModules} módulos ativos • R$ {totalCost.toFixed(2)}/mês
                        </CardDescription>
                      </div>
                      <Button variant="outline" size="sm">
                        Configurar
                      </Button>
                    </div>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-3">
                      {deptModules.slice(0, 4).map((module, index) => {
                        const IconComponent = getModuleIcon(module.code);
                        return (
                          <div key={index} className="flex items-center justify-between p-2 border rounded">
                            <div className="flex items-center space-x-3">
                              <IconComponent className="h-4 w-4 text-gray-600" />
                              <div>
                                <p className="text-sm font-medium">{module.name}</p>
                                <p className="text-xs text-gray-500">R$ {module.price.toFixed(2)}/mês</p>
                              </div>
                            </div>
                            <Switch defaultChecked={module.is_active !== false} />
                          </div>
                        );
                      })}
                      {deptModules.length > 4 && (
                        <p className="text-sm text-gray-500 text-center">
                          +{deptModules.length - 4} módulos adicionais
                        </p>
                      )}
                    </div>
                  </CardContent>
                </Card>
              );
            })}
          </div>
        </TabsContent>

        {/* Catálogo de Módulos */}
        <TabsContent value="modules" className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {Object.entries(modules).flatMap(([deptCode, deptModules]) => 
              deptModules.map((module, index) => {
                const IconComponent = getModuleIcon(module.code);
                return (
                  <Card key={`${deptCode}-${index}`} className="hover:shadow-md transition-shadow">
                    <CardHeader>
                      <div className="flex items-center justify-between">
                        <IconComponent className="h-8 w-8 text-blue-600" />
                        <Badge className={getDepartmentColor(deptCode)}>
                          {deptCode}
                        </Badge>
                      </div>
                      <CardTitle className="text-lg">{module.name}</CardTitle>
                      <CardDescription>
                        Módulo para {deptCode} • R$ {module.price.toFixed(2)}/mês
                      </CardDescription>
                    </CardHeader>
                    <CardContent>
                      <div className="flex items-center justify-between">
                        <div className="flex items-center space-x-2">
                          {module.is_active !== false ? (
                            <CheckCircle className="h-4 w-4 text-green-600" />
                          ) : (
                            <XCircle className="h-4 w-4 text-gray-400" />
                          )}
                          <span className="text-sm">
                            {module.is_active !== false ? 'Ativo' : 'Inativo'}
                          </span>
                        </div>
                        <Button variant="outline" size="sm">
                          {module.is_active !== false ? 'Desativar' : 'Ativar'}
                        </Button>
                      </div>
                    </CardContent>
                  </Card>
                );
              })
            )}
          </div>
        </TabsContent>

        {/* Faturamento */}
        <TabsContent value="billing" className="space-y-4">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <Card>
              <CardHeader>
                <CardTitle>Fatura Atual</CardTitle>
                <CardDescription>Período: Agosto 2025</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div className="flex justify-between items-center">
                    <span>Módulos Ativos</span>
                    <span className="font-semibold">47</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span>Valor por Módulo</span>
                    <span className="font-semibold">R$ 30,00</span>
                  </div>
                  <div className="border-t pt-4">
                    <div className="flex justify-between items-center text-lg font-bold">
                      <span>Total</span>
                      <span className="text-green-600">R$ 1.410,00</span>
                    </div>
                  </div>
                  <Button className="w-full">
                    <DollarSign className="h-4 w-4 mr-2" />
                    Pagar Fatura
                  </Button>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Histórico de Pagamentos</CardTitle>
                <CardDescription>Últimos 6 meses</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  {[
                    { month: 'Julho 2025', amount: 'R$ 1.380,00', status: 'Pago' },
                    { month: 'Junho 2025', amount: 'R$ 1.350,00', status: 'Pago' },
                    { month: 'Maio 2025', amount: 'R$ 1.320,00', status: 'Pago' },
                    { month: 'Abril 2025', amount: 'R$ 1.290,00', status: 'Pago' },
                    { month: 'Março 2025', amount: 'R$ 1.260,00', status: 'Pago' },
                  ].map((payment, index) => (
                    <div key={index} className="flex justify-between items-center p-3 border rounded">
                      <div>
                        <p className="font-medium">{payment.month}</p>
                        <p className="text-sm text-gray-600">{payment.amount}</p>
                      </div>
                      <Badge variant="default">{payment.status}</Badge>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        {/* Análises */}
        <TabsContent value="analytics" className="space-y-4">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <Card>
              <CardHeader>
                <CardTitle>Uso por Departamento</CardTitle>
                <CardDescription>Módulos mais utilizados</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {[
                    { dept: 'Financeiro', modules: 8, usage: 95 },
                    { dept: 'Vendas', modules: 6, usage: 87 },
                    { dept: 'RH', modules: 7, usage: 82 },
                    { dept: 'Obras', modules: 5, usage: 78 },
                    { dept: 'Compras', modules: 4, usage: 71 },
                  ].map((item, index) => (
                    <div key={index} className="space-y-2">
                      <div className="flex justify-between">
                        <span className="text-sm font-medium">{item.dept}</span>
                        <span className="text-sm text-gray-600">{item.modules} módulos</span>
                      </div>
                      <div className="w-full bg-gray-200 rounded-full h-2">
                        <div 
                          className="bg-blue-600 h-2 rounded-full" 
                          style={{ width: `${item.usage}%` }}
                        ></div>
                      </div>
                      <div className="text-xs text-gray-500">{item.usage}% de uso</div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>ROI por Módulo</CardTitle>
                <CardDescription>Retorno sobre investimento</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {[
                    { module: 'CRM Vendas', roi: 340, cost: 30 },
                    { module: 'Fluxo de Caixa', roi: 280, cost: 30 },
                    { module: 'Folha de Pagamento', roi: 250, cost: 30 },
                    { module: 'Controle de Estoque', roi: 220, cost: 30 },
                    { module: 'Gestão de Projetos', roi: 190, cost: 30 },
                  ].map((item, index) => (
                    <div key={index} className="flex justify-between items-center p-3 border rounded">
                      <div>
                        <p className="font-medium">{item.module}</p>
                        <p className="text-sm text-gray-600">R$ {item.cost}/mês</p>
                      </div>
                      <div className="text-right">
                        <p className="font-semibold text-green-600">{item.roi}%</p>
                        <p className="text-xs text-gray-500">ROI</p>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </div>
        </TabsContent>
      </Tabs>
    </div>
  );
};

export default ModularSystem;

