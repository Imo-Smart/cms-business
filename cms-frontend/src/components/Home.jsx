import React from 'react';
import { Link } from 'react-router-dom';
import { 
  Building2, 
  Calculator, 
  FileText, 
  DollarSign, 
  Users, 
  BarChart3,
  CheckCircle,
  ArrowRight,
  Shield,
  Zap,
  Globe
} from 'lucide-react';

const Home = () => {
  const features = [
    {
      icon: <Calculator className="w-8 h-8 text-blue-600" />,
      title: "Contabilidade Completa",
      description: "Plano de contas brasileiro, lançamentos contábeis, balancetes e relatórios obrigatórios."
    },
    {
      icon: <FileText className="w-8 h-8 text-green-600" />,
      title: "Gestão Fiscal",
      description: "Emissão de NFe, controle de impostos (ICMS, PIS, COFINS) e conformidade com SEFAZ."
    },
    {
      icon: <DollarSign className="w-8 h-8 text-purple-600" />,
      title: "Financeiro",
      description: "Contas a pagar/receber, fluxo de caixa, conciliação bancária e controle de inadimplência."
    },
    {
      icon: <Users className="w-8 h-8 text-orange-600" />,
      title: "Gestão de Clientes",
      description: "Cadastro completo de clientes PF/PJ, histórico de vendas e relacionamento."
    },
    {
      icon: <BarChart3 className="w-8 h-8 text-red-600" />,
      title: "Relatórios Gerenciais",
      description: "Dashboards inteligentes, KPIs empresariais e análises de performance."
    },
    {
      icon: <Shield className="w-8 h-8 text-indigo-600" />,
      title: "Segurança Total",
      description: "Backup automático, controle de acesso e conformidade com LGPD."
    }
  ];

  const benefits = [
    "Conformidade com legislação brasileira",
    "Interface intuitiva e moderna",
    "Suporte técnico especializado",
    "Atualizações automáticas",
    "Integração com bancos",
    "Relatórios personalizáveis"
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-4">
            <div className="flex items-center space-x-3">
              <div className="w-10 h-10 bg-blue-600 rounded-lg flex items-center justify-center">
                <Building2 className="w-6 h-6 text-white" />
              </div>
              <div>
                <h1 className="text-xl font-bold text-gray-900">CMS Business</h1>
                <p className="text-sm text-gray-500">Sistema Empresarial Brasileiro</p>
              </div>
            </div>
            <div className="flex items-center space-x-4">
              <Link 
                to="/login" 
                className="text-gray-600 hover:text-gray-900 font-medium transition-colors"
              >
                Entrar
              </Link>
              <Link 
                to="/register" 
                className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition-colors font-medium"
              >
                Começar Grátis
              </Link>
            </div>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <section className="py-20 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto text-center">
          <div className="mb-8">
            <span className="inline-flex items-center px-4 py-2 rounded-full text-sm font-medium bg-blue-100 text-blue-800 mb-6">
              <Zap className="w-4 h-4 mr-2" />
              Sistema 100% Brasileiro
            </span>
          </div>
          
          <h1 className="text-5xl md:text-6xl font-bold text-gray-900 mb-6 leading-tight">
            Gerencie sua empresa com
            <span className="text-blue-600 block">inteligência e simplicidade</span>
          </h1>
          
          <p className="text-xl text-gray-600 mb-10 max-w-3xl mx-auto leading-relaxed">
            Sistema empresarial completo com contabilidade, fiscal, financeiro e muito mais. 
            Desenvolvido especialmente para empresas brasileiras de todos os portes.
          </p>
          
          <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
            <Link 
              to="/register" 
              className="bg-blue-600 text-white px-8 py-4 rounded-lg hover:bg-blue-700 transition-all duration-300 font-semibold text-lg flex items-center group shadow-lg hover:shadow-xl"
            >
              Criar Conta Grátis
              <ArrowRight className="w-5 h-5 ml-2 group-hover:translate-x-1 transition-transform" />
            </Link>
            <Link 
              to="/demo" 
              className="border-2 border-gray-300 text-gray-700 px-8 py-4 rounded-lg hover:border-gray-400 transition-colors font-semibold text-lg"
            >
              Ver Demonstração
            </Link>
          </div>
          
          <div className="mt-12 flex items-center justify-center space-x-8 text-sm text-gray-500">
            <div className="flex items-center">
              <CheckCircle className="w-5 h-5 text-green-500 mr-2" />
              Teste grátis por 30 dias
            </div>
            <div className="flex items-center">
              <CheckCircle className="w-5 h-5 text-green-500 mr-2" />
              Sem cartão de crédito
            </div>
            <div className="flex items-center">
              <CheckCircle className="w-5 h-5 text-green-500 mr-2" />
              Suporte especializado
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-gray-900 mb-4">
              Tudo que sua empresa precisa
            </h2>
            <p className="text-xl text-gray-600 max-w-2xl mx-auto">
              Módulos integrados para gestão completa do seu negócio
            </p>
          </div>
          
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            {features.map((feature, index) => (
              <div 
                key={index} 
                className="p-8 rounded-2xl border border-gray-100 hover:border-gray-200 transition-all duration-300 hover:shadow-lg group"
              >
                <div className="mb-4 group-hover:scale-110 transition-transform duration-300">
                  {feature.icon}
                </div>
                <h3 className="text-xl font-semibold text-gray-900 mb-3">
                  {feature.title}
                </h3>
                <p className="text-gray-600 leading-relaxed">
                  {feature.description}
                </p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Benefits Section */}
      <section className="py-20 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid lg:grid-cols-2 gap-12 items-center">
            <div>
              <h2 className="text-4xl font-bold text-gray-900 mb-6">
                Por que escolher o CMS Business?
              </h2>
              <p className="text-xl text-gray-600 mb-8">
                Desenvolvido por especialistas brasileiros para atender todas as necessidades 
                das empresas nacionais, desde microempresas até grandes corporações.
              </p>
              
              <div className="grid sm:grid-cols-2 gap-4">
                {benefits.map((benefit, index) => (
                  <div key={index} className="flex items-center">
                    <CheckCircle className="w-5 h-5 text-green-500 mr-3 flex-shrink-0" />
                    <span className="text-gray-700">{benefit}</span>
                  </div>
                ))}
              </div>
            </div>
            
            <div className="relative">
              <div className="bg-gradient-to-br from-blue-500 to-purple-600 rounded-2xl p-8 text-white">
                <div className="mb-6">
                  <Globe className="w-12 h-12 mb-4" />
                  <h3 className="text-2xl font-bold mb-2">Acesso em qualquer lugar</h3>
                  <p className="text-blue-100">
                    Sistema 100% online, acesse de qualquer dispositivo com internet
                  </p>
                </div>
                
                <div className="grid grid-cols-2 gap-4 text-center">
                  <div className="bg-white/10 rounded-lg p-4">
                    <div className="text-2xl font-bold">99.9%</div>
                    <div className="text-sm text-blue-100">Uptime</div>
                  </div>
                  <div className="bg-white/10 rounded-lg p-4">
                    <div className="text-2xl font-bold">24/7</div>
                    <div className="text-sm text-blue-100">Suporte</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 bg-blue-600">
        <div className="max-w-4xl mx-auto text-center px-4 sm:px-6 lg:px-8">
          <h2 className="text-4xl font-bold text-white mb-6">
            Pronto para transformar sua gestão empresarial?
          </h2>
          <p className="text-xl text-blue-100 mb-10">
            Junte-se a milhares de empresas que já confiam no CMS Business
          </p>
          
          <Link 
            to="/register" 
            className="inline-flex items-center bg-white text-blue-600 px-8 py-4 rounded-lg hover:bg-gray-50 transition-colors font-semibold text-lg shadow-lg hover:shadow-xl group"
          >
            Começar Agora - É Grátis
            <ArrowRight className="w-5 h-5 ml-2 group-hover:translate-x-1 transition-transform" />
          </Link>
          
          <p className="text-blue-200 mt-6 text-sm">
            Teste grátis por 30 dias • Sem compromisso • Cancele quando quiser
          </p>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-900 text-white py-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid md:grid-cols-4 gap-8">
            <div>
              <div className="flex items-center space-x-3 mb-4">
                <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center">
                  <Building2 className="w-5 h-5 text-white" />
                </div>
                <span className="text-lg font-bold">CMS Business</span>
              </div>
              <p className="text-gray-400">
                Sistema empresarial brasileiro completo para gestão inteligente do seu negócio.
              </p>
            </div>
            
            <div>
              <h4 className="font-semibold mb-4">Produto</h4>
              <ul className="space-y-2 text-gray-400">
                <li><a href="#" className="hover:text-white transition-colors">Funcionalidades</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Preços</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Demonstração</a></li>
              </ul>
            </div>
            
            <div>
              <h4 className="font-semibold mb-4">Suporte</h4>
              <ul className="space-y-2 text-gray-400">
                <li><a href="#" className="hover:text-white transition-colors">Central de Ajuda</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Contato</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Treinamentos</a></li>
              </ul>
            </div>
            
            <div>
              <h4 className="font-semibold mb-4">Empresa</h4>
              <ul className="space-y-2 text-gray-400">
                <li><a href="#" className="hover:text-white transition-colors">Sobre</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Blog</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Carreiras</a></li>
              </ul>
            </div>
          </div>
          
          <div className="border-t border-gray-800 mt-8 pt-8 text-center text-gray-400">
            <p>&copy; 2024 CMS Business. Todos os direitos reservados.</p>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default Home;

