import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Badge } from './ui/badge';
import { Tabs, TabsContent, TabsList, TabsTrigger } from './ui/tabs';
import { 
  Users, 
  DollarSign, 
  Clock, 
  Award, 
  MessageSquare, 
  BarChart3,
  UserPlus,
  Calendar,
  TrendingUp,
  AlertCircle,
  CheckCircle,
  FileText,
  Settings,
  Bell,
  Search,
  Filter,
  Download,
  Upload,
  Eye,
  Edit,
  Trash2,
  Plus,
  RefreshCw
} from 'lucide-react';

const HRModule = () => {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [employees, setEmployees] = useState([]);
  const [hrStats, setHrStats] = useState({});
  const [loading, setLoading] = useState(false);
  const [searchTerm, setSearchTerm] = useState('');

  // Dados simulados para demonstração
  const mockStats = {
    total_employees: 156,
    total_departments: 8,
    birthdays_this_month: 12,
    recent_admissions: 5,
    payroll_total: 485000.00,
    employees_by_department: [
      { department_id: 1, count: 25, name: 'Engenharia' },
      { department_id: 2, count: 18, name: 'Obras' },
      { department_id: 3, count: 15, name: 'Comercial' },
      { department_id: 4, count: 12, name: 'Administrativo' },
      { department_id: 5, count: 20, name: 'Financeiro' },
      { department_id: 6, count: 22, name: 'RH' },
      { department_id: 7, count: 28, name: 'Compras' },
      { department_id: 8, count: 16, name: 'Qualidade' }
    ]
  };

  const mockEmployees = [
    {
      id: 1,
      full_name: 'João Silva Santos',
      employee_code: 'EMP0001',
      position: 'Engenheiro Civil',
      department: 'Engenharia',
      salary: 8500.00,
      admission_date: '2023-01-15',
      status: 'active',
      email: 'joao.silva@empresa.com',
      phone: '(11) 99999-1234'
    },
    {
      id: 2,
      full_name: 'Maria Oliveira Costa',
      employee_code: 'EMP0002',
      position: 'Analista de RH',
      department: 'RH',
      salary: 5500.00,
      admission_date: '2023-03-20',
      status: 'active',
      email: 'maria.oliveira@empresa.com',
      phone: '(11) 99999-5678'
    },
    {
      id: 3,
      full_name: 'Carlos Pereira Lima',
      employee_code: 'EMP0003',
      position: 'Mestre de Obras',
      department: 'Obras',
      salary: 7200.00,
      admission_date: '2022-11-10',
      status: 'active',
      email: 'carlos.pereira@empresa.com',
      phone: '(11) 99999-9012'
    }
  ];

  useEffect(() => {
    setHrStats(mockStats);
    setEmployees(mockEmployees);
  }, []);

  const DashboardTab = () => (
    <div className="space-y-6">
      {/* Cards de Estatísticas */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <Card className="bg-gradient-to-r from-blue-500 to-blue-600 text-white">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total de Colaboradores</CardTitle>
            <Users className="h-4 w-4" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{hrStats.total_employees}</div>
            <p className="text-xs opacity-80">
              +{hrStats.recent_admissions} novos este mês
            </p>
          </CardContent>
        </Card>

        <Card className="bg-gradient-to-r from-green-500 to-green-600 text-white">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Folha de Pagamento</CardTitle>
            <DollarSign className="h-4 w-4" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              R$ {hrStats.payroll_total?.toLocaleString('pt-BR', { minimumFractionDigits: 2 })}
            </div>
            <p className="text-xs opacity-80">
              Mês atual
            </p>
          </CardContent>
        </Card>

        <Card className="bg-gradient-to-r from-purple-500 to-purple-600 text-white">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Aniversariantes</CardTitle>
            <Calendar className="h-4 w-4" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{hrStats.birthdays_this_month}</div>
            <p className="text-xs opacity-80">
              Este mês
            </p>
          </CardContent>
        </Card>

        <Card className="bg-gradient-to-r from-orange-500 to-orange-600 text-white">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Departamentos</CardTitle>
            <BarChart3 className="h-4 w-4" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{hrStats.total_departments}</div>
            <p className="text-xs opacity-80">
              Ativos
            </p>
          </CardContent>
        </Card>
      </div>

      {/* Gráfico de Colaboradores por Departamento */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <BarChart3 className="h-5 w-5" />
            Colaboradores por Departamento
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {hrStats.employees_by_department?.map((dept, index) => (
              <div key={index} className="flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <div className="w-3 h-3 rounded-full bg-blue-500"></div>
                  <span className="font-medium">{dept.name}</span>
                </div>
                <div className="flex items-center gap-2">
                  <div className="w-32 bg-gray-200 rounded-full h-2">
                    <div 
                      className="bg-blue-500 h-2 rounded-full" 
                      style={{ width: `${(dept.count / hrStats.total_employees) * 100}%` }}
                    ></div>
                  </div>
                  <span className="text-sm font-semibold w-8">{dept.count}</span>
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Ações Rápidas */}
      <Card>
        <CardHeader>
          <CardTitle>Ações Rápidas</CardTitle>
          <CardDescription>Acesso rápido às principais funcionalidades</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <Button 
              variant="outline" 
              className="h-20 flex flex-col gap-2"
              onClick={() => setActiveTab('employees')}
            >
              <UserPlus className="h-6 w-6" />
              <span className="text-xs">Novo Colaborador</span>
            </Button>
            <Button 
              variant="outline" 
              className="h-20 flex flex-col gap-2"
              onClick={() => setActiveTab('payroll')}
            >
              <DollarSign className="h-6 w-6" />
              <span className="text-xs">Calcular Folha</span>
            </Button>
            <Button 
              variant="outline" 
              className="h-20 flex flex-col gap-2"
              onClick={() => setActiveTab('timerecords')}
            >
              <Clock className="h-6 w-6" />
              <span className="text-xs">Registrar Ponto</span>
            </Button>
            <Button 
              variant="outline" 
              className="h-20 flex flex-col gap-2"
              onClick={() => setActiveTab('reports')}
            >
              <FileText className="h-6 w-6" />
              <span className="text-xs">Relatórios</span>
            </Button>
          </div>
        </CardContent>
      </Card>
    </div>
  );

  const EmployeesTab = () => (
    <div className="space-y-6">
      {/* Cabeçalho com busca e ações */}
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
        <div>
          <h2 className="text-2xl font-bold">Gestão de Colaboradores</h2>
          <p className="text-gray-600">Gerencie todos os colaboradores da empresa</p>
        </div>
        <div className="flex gap-2">
          <Button className="bg-blue-600 hover:bg-blue-700">
            <Plus className="h-4 w-4 mr-2" />
            Novo Colaborador
          </Button>
          <Button variant="outline">
            <Upload className="h-4 w-4 mr-2" />
            Importar
          </Button>
        </div>
      </div>

      {/* Filtros e Busca */}
      <Card>
        <CardContent className="pt-6">
          <div className="flex flex-col md:flex-row gap-4">
            <div className="flex-1">
              <div className="relative">
                <Search className="absolute left-3 top-3 h-4 w-4 text-gray-400" />
                <Input
                  placeholder="Buscar por nome, código ou cargo..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="pl-10"
                />
              </div>
            </div>
            <Button variant="outline">
              <Filter className="h-4 w-4 mr-2" />
              Filtros
            </Button>
            <Button variant="outline">
              <Download className="h-4 w-4 mr-2" />
              Exportar
            </Button>
          </div>
        </CardContent>
      </Card>

      {/* Lista de Colaboradores */}
      <Card>
        <CardHeader>
          <CardTitle>Colaboradores Ativos ({employees.length})</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="border-b">
                  <th className="text-left py-3 px-4 font-medium">Colaborador</th>
                  <th className="text-left py-3 px-4 font-medium">Código</th>
                  <th className="text-left py-3 px-4 font-medium">Cargo</th>
                  <th className="text-left py-3 px-4 font-medium">Departamento</th>
                  <th className="text-left py-3 px-4 font-medium">Salário</th>
                  <th className="text-left py-3 px-4 font-medium">Status</th>
                  <th className="text-left py-3 px-4 font-medium">Ações</th>
                </tr>
              </thead>
              <tbody>
                {employees.map((employee) => (
                  <tr key={employee.id} className="border-b hover:bg-gray-50">
                    <td className="py-3 px-4">
                      <div>
                        <div className="font-medium">{employee.full_name}</div>
                        <div className="text-sm text-gray-500">{employee.email}</div>
                      </div>
                    </td>
                    <td className="py-3 px-4">
                      <Badge variant="outline">{employee.employee_code}</Badge>
                    </td>
                    <td className="py-3 px-4">{employee.position}</td>
                    <td className="py-3 px-4">{employee.department}</td>
                    <td className="py-3 px-4">
                      R$ {employee.salary.toLocaleString('pt-BR', { minimumFractionDigits: 2 })}
                    </td>
                    <td className="py-3 px-4">
                      <Badge 
                        variant={employee.status === 'active' ? 'default' : 'secondary'}
                        className={employee.status === 'active' ? 'bg-green-100 text-green-800' : ''}
                      >
                        {employee.status === 'active' ? 'Ativo' : 'Inativo'}
                      </Badge>
                    </td>
                    <td className="py-3 px-4">
                      <div className="flex gap-2">
                        <Button size="sm" variant="outline">
                          <Eye className="h-4 w-4" />
                        </Button>
                        <Button size="sm" variant="outline">
                          <Edit className="h-4 w-4" />
                        </Button>
                        <Button size="sm" variant="outline" className="text-red-600 hover:text-red-700">
                          <Trash2 className="h-4 w-4" />
                        </Button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </CardContent>
      </Card>
    </div>
  );

  const PayrollTab = () => (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h2 className="text-2xl font-bold">Folha de Pagamento</h2>
          <p className="text-gray-600">Gerencie a folha de pagamento mensal</p>
        </div>
        <Button className="bg-green-600 hover:bg-green-700">
          <Plus className="h-4 w-4 mr-2" />
          Novo Período
        </Button>
      </div>

      {/* Status da Folha Atual */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <DollarSign className="h-5 w-5" />
            Folha de Agosto/2025
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <div className="text-center p-4 bg-blue-50 rounded-lg">
              <div className="text-2xl font-bold text-blue-600">156</div>
              <div className="text-sm text-gray-600">Colaboradores</div>
            </div>
            <div className="text-center p-4 bg-green-50 rounded-lg">
              <div className="text-2xl font-bold text-green-600">R$ 485.000</div>
              <div className="text-sm text-gray-600">Salário Bruto</div>
            </div>
            <div className="text-center p-4 bg-orange-50 rounded-lg">
              <div className="text-2xl font-bold text-orange-600">R$ 125.000</div>
              <div className="text-sm text-gray-600">Descontos</div>
            </div>
            <div className="text-center p-4 bg-purple-50 rounded-lg">
              <div className="text-2xl font-bold text-purple-600">R$ 360.000</div>
              <div className="text-sm text-gray-600">Salário Líquido</div>
            </div>
          </div>
          
          <div className="mt-6 flex gap-4">
            <Button className="bg-blue-600 hover:bg-blue-700">
              <RefreshCw className="h-4 w-4 mr-2" />
              Calcular Folha
            </Button>
            <Button variant="outline">
              <FileText className="h-4 w-4 mr-2" />
              Gerar Relatório
            </Button>
            <Button variant="outline">
              <Download className="h-4 w-4 mr-2" />
              Exportar CNAB
            </Button>
          </div>
        </CardContent>
      </Card>

      {/* Histórico de Períodos */}
      <Card>
        <CardHeader>
          <CardTitle>Histórico de Períodos</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {[
              { period: 'Julho/2025', status: 'Pago', total: 'R$ 478.500', date: '05/08/2025' },
              { period: 'Junho/2025', status: 'Pago', total: 'R$ 465.200', date: '05/07/2025' },
              { period: 'Maio/2025', status: 'Pago', total: 'R$ 492.800', date: '05/06/2025' },
            ].map((item, index) => (
              <div key={index} className="flex items-center justify-between p-4 border rounded-lg">
                <div className="flex items-center gap-4">
                  <div className="w-10 h-10 bg-green-100 rounded-full flex items-center justify-center">
                    <CheckCircle className="h-5 w-5 text-green-600" />
                  </div>
                  <div>
                    <div className="font-medium">{item.period}</div>
                    <div className="text-sm text-gray-500">Pago em {item.date}</div>
                  </div>
                </div>
                <div className="text-right">
                  <div className="font-semibold">{item.total}</div>
                  <Badge className="bg-green-100 text-green-800">{item.status}</Badge>
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  );

  const TimeRecordsTab = () => (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h2 className="text-2xl font-bold">Controle de Ponto</h2>
          <p className="text-gray-600">Gerencie os registros de ponto dos colaboradores</p>
        </div>
        <Button className="bg-blue-600 hover:bg-blue-700">
          <Clock className="h-4 w-4 mr-2" />
          Registrar Ponto
        </Button>
      </div>

      {/* Resumo do Dia */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Clock className="h-5 w-5" />
            Resumo de Hoje - {new Date().toLocaleDateString('pt-BR')}
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <div className="text-center p-4 bg-green-50 rounded-lg">
              <div className="text-2xl font-bold text-green-600">142</div>
              <div className="text-sm text-gray-600">Presentes</div>
            </div>
            <div className="text-center p-4 bg-red-50 rounded-lg">
              <div className="text-2xl font-bold text-red-600">8</div>
              <div className="text-sm text-gray-600">Ausentes</div>
            </div>
            <div className="text-center p-4 bg-yellow-50 rounded-lg">
              <div className="text-2xl font-bold text-yellow-600">6</div>
              <div className="text-sm text-gray-600">Atrasados</div>
            </div>
            <div className="text-center p-4 bg-blue-50 rounded-lg">
              <div className="text-2xl font-bold text-blue-600">1.248h</div>
              <div className="text-sm text-gray-600">Horas Trabalhadas</div>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Registros Recentes */}
      <Card>
        <CardHeader>
          <CardTitle>Registros Recentes</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {[
              { name: 'João Silva Santos', time: '17:58', type: 'Saída', status: 'normal' },
              { name: 'Maria Oliveira Costa', time: '17:45', type: 'Saída', status: 'normal' },
              { name: 'Carlos Pereira Lima', time: '17:30', type: 'Saída', status: 'early' },
              { name: 'Ana Santos Ferreira', time: '13:15', type: 'Entrada', status: 'late' },
              { name: 'Pedro Costa Silva', time: '12:00', type: 'Saída Almoço', status: 'normal' },
            ].map((record, index) => (
              <div key={index} className="flex items-center justify-between p-4 border rounded-lg">
                <div className="flex items-center gap-4">
                  <div className={`w-10 h-10 rounded-full flex items-center justify-center ${
                    record.status === 'normal' ? 'bg-green-100' :
                    record.status === 'late' ? 'bg-red-100' : 'bg-yellow-100'
                  }`}>
                    <Clock className={`h-5 w-5 ${
                      record.status === 'normal' ? 'text-green-600' :
                      record.status === 'late' ? 'text-red-600' : 'text-yellow-600'
                    }`} />
                  </div>
                  <div>
                    <div className="font-medium">{record.name}</div>
                    <div className="text-sm text-gray-500">{record.type}</div>
                  </div>
                </div>
                <div className="text-right">
                  <div className="font-semibold">{record.time}</div>
                  <Badge 
                    variant={record.status === 'normal' ? 'default' : 'secondary'}
                    className={
                      record.status === 'normal' ? 'bg-green-100 text-green-800' :
                      record.status === 'late' ? 'bg-red-100 text-red-800' : 'bg-yellow-100 text-yellow-800'
                    }
                  >
                    {record.status === 'normal' ? 'Normal' :
                     record.status === 'late' ? 'Atraso' : 'Saída Antecipada'}
                  </Badge>
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  );

  const BenefitsTab = () => (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h2 className="text-2xl font-bold">Gestão de Benefícios</h2>
          <p className="text-gray-600">Gerencie os benefícios dos colaboradores</p>
        </div>
        <Button className="bg-purple-600 hover:bg-purple-700">
          <Plus className="h-4 w-4 mr-2" />
          Novo Benefício
        </Button>
      </div>

      {/* Resumo de Benefícios */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <Card>
          <CardHeader>
            <CardTitle className="text-lg">Vale Transporte</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-blue-600">R$ 18.500</div>
            <p className="text-sm text-gray-600">142 colaboradores</p>
            <div className="mt-4">
              <Button size="sm" variant="outline">Gerenciar</Button>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="text-lg">Vale Alimentação</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-green-600">R$ 28.400</div>
            <p className="text-sm text-gray-600">156 colaboradores</p>
            <div className="mt-4">
              <Button size="sm" variant="outline">Gerenciar</Button>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="text-lg">Plano de Saúde</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-purple-600">R$ 45.200</div>
            <p className="text-sm text-gray-600">128 colaboradores</p>
            <div className="mt-4">
              <Button size="sm" variant="outline">Gerenciar</Button>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Lista de Benefícios */}
      <Card>
        <CardHeader>
          <CardTitle>Catálogo de Benefícios</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {[
              { name: 'Vale Transporte', category: 'Transporte', value: 'R$ 130,00', active: true },
              { name: 'Vale Alimentação', category: 'Alimentação', value: 'R$ 182,00', active: true },
              { name: 'Plano de Saúde', category: 'Saúde', value: 'R$ 289,00', active: true },
              { name: 'Seguro de Vida', category: 'Segurança', value: 'R$ 45,00', active: true },
              { name: 'Auxílio Creche', category: 'Família', value: 'R$ 320,00', active: false },
            ].map((benefit, index) => (
              <div key={index} className="flex items-center justify-between p-4 border rounded-lg">
                <div className="flex items-center gap-4">
                  <div className="w-10 h-10 bg-purple-100 rounded-full flex items-center justify-center">
                    <Award className="h-5 w-5 text-purple-600" />
                  </div>
                  <div>
                    <div className="font-medium">{benefit.name}</div>
                    <div className="text-sm text-gray-500">{benefit.category}</div>
                  </div>
                </div>
                <div className="flex items-center gap-4">
                  <div className="text-right">
                    <div className="font-semibold">{benefit.value}</div>
                    <Badge 
                      variant={benefit.active ? 'default' : 'secondary'}
                      className={benefit.active ? 'bg-green-100 text-green-800' : ''}
                    >
                      {benefit.active ? 'Ativo' : 'Inativo'}
                    </Badge>
                  </div>
                  <div className="flex gap-2">
                    <Button size="sm" variant="outline">
                      <Edit className="h-4 w-4" />
                    </Button>
                    <Button size="sm" variant="outline">
                      <Settings className="h-4 w-4" />
                    </Button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  );

  const TrainingsTab = () => (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h2 className="text-2xl font-bold">Treinamento e Desenvolvimento</h2>
          <p className="text-gray-600">Gerencie treinamentos e capacitações</p>
        </div>
        <Button className="bg-indigo-600 hover:bg-indigo-700">
          <Plus className="h-4 w-4 mr-2" />
          Novo Treinamento
        </Button>
      </div>

      {/* Estatísticas de Treinamento */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">Treinamentos Ativos</p>
                <p className="text-2xl font-bold">24</p>
              </div>
              <Award className="h-8 w-8 text-indigo-600" />
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">Colaboradores Treinando</p>
                <p className="text-2xl font-bold">89</p>
              </div>
              <Users className="h-8 w-8 text-green-600" />
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">Certificados Emitidos</p>
                <p className="text-2xl font-bold">156</p>
              </div>
              <FileText className="h-8 w-8 text-purple-600" />
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">Taxa de Conclusão</p>
                <p className="text-2xl font-bold">87%</p>
              </div>
              <TrendingUp className="h-8 w-8 text-orange-600" />
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Lista de Treinamentos */}
      <Card>
        <CardHeader>
          <CardTitle>Treinamentos Disponíveis</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {[
              { 
                title: 'Segurança no Trabalho', 
                category: 'Obrigatório', 
                duration: '8h', 
                enrolled: 45, 
                completed: 38,
                mandatory: true 
              },
              { 
                title: 'Liderança e Gestão de Equipes', 
                category: 'Desenvolvimento', 
                duration: '16h', 
                enrolled: 12, 
                completed: 8,
                mandatory: false 
              },
              { 
                title: 'Excel Avançado', 
                category: 'Técnico', 
                duration: '12h', 
                enrolled: 28, 
                completed: 22,
                mandatory: false 
              },
              { 
                title: 'Primeiros Socorros', 
                category: 'Obrigatório', 
                duration: '4h', 
                enrolled: 156, 
                completed: 142,
                mandatory: true 
              },
            ].map((training, index) => (
              <div key={index} className="flex items-center justify-between p-4 border rounded-lg">
                <div className="flex items-center gap-4">
                  <div className={`w-10 h-10 rounded-full flex items-center justify-center ${
                    training.mandatory ? 'bg-red-100' : 'bg-indigo-100'
                  }`}>
                    <Award className={`h-5 w-5 ${
                      training.mandatory ? 'text-red-600' : 'text-indigo-600'
                    }`} />
                  </div>
                  <div>
                    <div className="font-medium">{training.title}</div>
                    <div className="text-sm text-gray-500">
                      {training.category} • {training.duration}
                    </div>
                  </div>
                </div>
                <div className="flex items-center gap-6">
                  <div className="text-center">
                    <div className="text-sm font-medium">{training.enrolled}</div>
                    <div className="text-xs text-gray-500">Inscritos</div>
                  </div>
                  <div className="text-center">
                    <div className="text-sm font-medium text-green-600">{training.completed}</div>
                    <div className="text-xs text-gray-500">Concluídos</div>
                  </div>
                  <div className="flex gap-2">
                    <Button size="sm" variant="outline">
                      <Eye className="h-4 w-4" />
                    </Button>
                    <Button size="sm" variant="outline">
                      <Edit className="h-4 w-4" />
                    </Button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  );

  const CommunicationTab = () => (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h2 className="text-2xl font-bold">Comunicação Interna</h2>
          <p className="text-gray-600">Gerencie comunicados e avisos</p>
        </div>
        <Button className="bg-blue-600 hover:bg-blue-700">
          <Plus className="h-4 w-4 mr-2" />
          Novo Comunicado
        </Button>
      </div>

      {/* Comunicados Recentes */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <MessageSquare className="h-5 w-5" />
            Comunicados Recentes
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {[
              {
                title: 'Reunião Geral - Resultados do Trimestre',
                content: 'Convocamos todos os colaboradores para a reunião geral que acontecerá na próxima sexta-feira...',
                type: 'Reunião',
                priority: 'high',
                date: '2025-08-08',
                confirmations: 142,
                total: 156
              },
              {
                title: 'Nova Política de Home Office',
                content: 'Informamos sobre as novas diretrizes para trabalho remoto que entrarão em vigor...',
                type: 'Política',
                priority: 'normal',
                date: '2025-08-06',
                confirmations: 98,
                total: 156
              },
              {
                title: 'Treinamento Obrigatório de Segurança',
                content: 'Todos os colaboradores devem participar do treinamento de segurança no trabalho...',
                type: 'Treinamento',
                priority: 'high',
                date: '2025-08-05',
                confirmations: 156,
                total: 156
              },
            ].map((comm, index) => (
              <div key={index} className="border rounded-lg p-4">
                <div className="flex items-start justify-between mb-3">
                  <div className="flex items-center gap-3">
                    <div className={`w-3 h-3 rounded-full ${
                      comm.priority === 'high' ? 'bg-red-500' : 'bg-blue-500'
                    }`}></div>
                    <div>
                      <h3 className="font-medium">{comm.title}</h3>
                      <p className="text-sm text-gray-500">{comm.type} • {comm.date}</p>
                    </div>
                  </div>
                  <Badge 
                    variant={comm.priority === 'high' ? 'destructive' : 'default'}
                  >
                    {comm.priority === 'high' ? 'Urgente' : 'Normal'}
                  </Badge>
                </div>
                
                <p className="text-gray-600 mb-4">{comm.content}</p>
                
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-4">
                    <div className="text-sm">
                      <span className="font-medium text-green-600">{comm.confirmations}</span>
                      <span className="text-gray-500"> de {comm.total} confirmaram leitura</span>
                    </div>
                    <div className="w-32 bg-gray-200 rounded-full h-2">
                      <div 
                        className="bg-green-500 h-2 rounded-full" 
                        style={{ width: `${(comm.confirmations / comm.total) * 100}%` }}
                      ></div>
                    </div>
                  </div>
                  <div className="flex gap-2">
                    <Button size="sm" variant="outline">
                      <Eye className="h-4 w-4" />
                    </Button>
                    <Button size="sm" variant="outline">
                      <Edit className="h-4 w-4" />
                    </Button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  );

  const ReportsTab = () => (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h2 className="text-2xl font-bold">Relatórios e Análises</h2>
          <p className="text-gray-600">Relatórios detalhados de RH</p>
        </div>
        <Button className="bg-green-600 hover:bg-green-700">
          <Download className="h-4 w-4 mr-2" />
          Exportar Relatórios
        </Button>
      </div>

      {/* Tipos de Relatórios */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {[
          {
            title: 'Relatório de Folha',
            description: 'Detalhamento completo da folha de pagamento',
            icon: DollarSign,
            color: 'bg-green-100 text-green-600'
          },
          {
            title: 'Relatório de Ponto',
            description: 'Análise de frequência e pontualidade',
            icon: Clock,
            color: 'bg-blue-100 text-blue-600'
          },
          {
            title: 'Relatório de Turnover',
            description: 'Análise de rotatividade de pessoal',
            icon: TrendingUp,
            color: 'bg-orange-100 text-orange-600'
          },
          {
            title: 'Relatório de Benefícios',
            description: 'Custos e utilização de benefícios',
            icon: Award,
            color: 'bg-purple-100 text-purple-600'
          },
          {
            title: 'Relatório de Treinamentos',
            description: 'Progresso e conclusão de treinamentos',
            icon: FileText,
            color: 'bg-indigo-100 text-indigo-600'
          },
          {
            title: 'Relatório Demográfico',
            description: 'Análise demográfica dos colaboradores',
            icon: Users,
            color: 'bg-pink-100 text-pink-600'
          },
        ].map((report, index) => (
          <Card key={index} className="hover:shadow-md transition-shadow cursor-pointer">
            <CardHeader>
              <div className={`w-12 h-12 rounded-lg ${report.color} flex items-center justify-center mb-4`}>
                <report.icon className="h-6 w-6" />
              </div>
              <CardTitle className="text-lg">{report.title}</CardTitle>
              <CardDescription>{report.description}</CardDescription>
            </CardHeader>
            <CardContent>
              <Button variant="outline" className="w-full">
                <Download className="h-4 w-4 mr-2" />
                Gerar Relatório
              </Button>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Relatórios Recentes */}
      <Card>
        <CardHeader>
          <CardTitle>Relatórios Gerados Recentemente</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {[
              { name: 'Folha de Pagamento - Julho 2025', type: 'PDF', size: '2.4 MB', date: '05/08/2025' },
              { name: 'Relatório de Ponto - Julho 2025', type: 'Excel', size: '1.8 MB', date: '01/08/2025' },
              { name: 'Análise de Turnover - 2º Trimestre', type: 'PDF', size: '1.2 MB', date: '30/07/2025' },
              { name: 'Relatório de Benefícios - Julho 2025', type: 'Excel', size: '956 KB', date: '28/07/2025' },
            ].map((report, index) => (
              <div key={index} className="flex items-center justify-between p-4 border rounded-lg">
                <div className="flex items-center gap-4">
                  <div className="w-10 h-10 bg-gray-100 rounded-full flex items-center justify-center">
                    <FileText className="h-5 w-5 text-gray-600" />
                  </div>
                  <div>
                    <div className="font-medium">{report.name}</div>
                    <div className="text-sm text-gray-500">{report.type} • {report.size}</div>
                  </div>
                </div>
                <div className="flex items-center gap-4">
                  <span className="text-sm text-gray-500">{report.date}</span>
                  <Button size="sm" variant="outline">
                    <Download className="h-4 w-4" />
                  </Button>
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  );

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="container mx-auto px-4 py-8">
        {/* Cabeçalho */}
        <div className="mb-8">
          <div className="flex items-center gap-3 mb-2">
            <div className="w-10 h-10 bg-blue-600 rounded-lg flex items-center justify-center">
              <Users className="h-6 w-6 text-white" />
            </div>
            <div>
              <h1 className="text-3xl font-bold text-gray-900">Módulo de Recursos Humanos</h1>
              <p className="text-gray-600">Sistema completo de gestão de pessoas</p>
            </div>
          </div>
        </div>

        {/* Navegação por Tabs */}
        <Tabs value={activeTab} onValueChange={setActiveTab} className="space-y-6">
          <TabsList className="grid w-full grid-cols-4 lg:grid-cols-8 gap-1">
            <TabsTrigger value="dashboard" className="flex items-center gap-2">
              <BarChart3 className="h-4 w-4" />
              <span className="hidden sm:inline">Dashboard</span>
            </TabsTrigger>
            <TabsTrigger value="employees" className="flex items-center gap-2">
              <Users className="h-4 w-4" />
              <span className="hidden sm:inline">Colaboradores</span>
            </TabsTrigger>
            <TabsTrigger value="payroll" className="flex items-center gap-2">
              <DollarSign className="h-4 w-4" />
              <span className="hidden sm:inline">Folha</span>
            </TabsTrigger>
            <TabsTrigger value="timerecords" className="flex items-center gap-2">
              <Clock className="h-4 w-4" />
              <span className="hidden sm:inline">Ponto</span>
            </TabsTrigger>
            <TabsTrigger value="benefits" className="flex items-center gap-2">
              <Award className="h-4 w-4" />
              <span className="hidden sm:inline">Benefícios</span>
            </TabsTrigger>
            <TabsTrigger value="trainings" className="flex items-center gap-2">
              <FileText className="h-4 w-4" />
              <span className="hidden sm:inline">Treinamentos</span>
            </TabsTrigger>
            <TabsTrigger value="communication" className="flex items-center gap-2">
              <MessageSquare className="h-4 w-4" />
              <span className="hidden sm:inline">Comunicação</span>
            </TabsTrigger>
            <TabsTrigger value="reports" className="flex items-center gap-2">
              <BarChart3 className="h-4 w-4" />
              <span className="hidden sm:inline">Relatórios</span>
            </TabsTrigger>
          </TabsList>

          <TabsContent value="dashboard">
            <DashboardTab />
          </TabsContent>

          <TabsContent value="employees">
            <EmployeesTab />
          </TabsContent>

          <TabsContent value="payroll">
            <PayrollTab />
          </TabsContent>

          <TabsContent value="timerecords">
            <TimeRecordsTab />
          </TabsContent>

          <TabsContent value="benefits">
            <BenefitsTab />
          </TabsContent>

          <TabsContent value="trainings">
            <TrainingsTab />
          </TabsContent>

          <TabsContent value="communication">
            <CommunicationTab />
          </TabsContent>

          <TabsContent value="reports">
            <ReportsTab />
          </TabsContent>
        </Tabs>
      </div>
    </div>
  );
};

export default HRModule;

