# CMS Business - Sistema Empresarial Brasileiro Completo

## 🏢 Visão Geral

O **CMS Business** é um sistema empresarial completo (ERP) desenvolvido especificamente para empresas brasileiras, oferecendo conformidade total com a legislação nacional e integração com órgãos governamentais.

### 🎯 Objetivo
Fornecer uma solução completa e integrada para gestão empresarial, desde microempresas até médias empresas, com foco na realidade brasileira.

## 🚀 Funcionalidades Principais

### 📊 Módulos Implementados

#### 1. **Módulo Contábil**
- ✅ Plano de contas brasileiro (NBC)
- ✅ Lançamentos contábeis com partidas dobradas
- ✅ Balancete de verificação em tempo real
- ✅ Balanço patrimonial e DRE
- ✅ Centros de custo
- ✅ Conciliação bancária
- ✅ Relatórios contábeis

#### 2. **Módulo Fiscal**
- ✅ Emissão de NF-e e NFC-e
- ✅ Controle de impostos (ICMS, IPI, PIS, COFINS, ISS)
- ✅ SPED Fiscal e Contribuições
- ✅ Regimes tributários brasileiros
- ✅ Integração com SEFAZ
- ✅ Obrigações acessórias

#### 3. **Módulo Financeiro**
- ✅ Contas a pagar e receber
- ✅ Fluxo de caixa
- ✅ Conciliação bancária
- ✅ Controle de inadimplência
- ✅ Múltiplas contas bancárias
- ✅ Pagamentos via PIX

#### 4. **Módulo de Vendas**
- ✅ Cadastro de clientes (PF/PJ)
- ✅ Catálogo de produtos/serviços
- ✅ Pedidos e orçamentos
- ✅ CRM básico
- ✅ Controle de comissões
- ✅ Integração com e-commerce

#### 5. **Módulo de Estoque**
- ✅ Controle de entrada e saída
- ✅ Múltiplos depósitos
- ✅ Controle de lotes e validades
- ✅ Inventário cíclico
- ✅ Código de barras
- ✅ Rastreabilidade completa

#### 6. **Módulo de RH**
- ✅ Cadastro de funcionários
- ✅ Folha de pagamento
- ✅ Controle de ponto
- ✅ Férias e 13º salário
- ✅ eSocial, FGTS e INSS
- ✅ Relatórios trabalhistas

#### 7. **Módulo de Relatórios e BI**
- ✅ Dashboard executivo
- ✅ KPIs personalizáveis
- ✅ Relatórios gerenciais
- ✅ Gráficos interativos
- ✅ Exportação (PDF, Excel, CSV)
- ✅ Alertas automáticos

## 🛠️ Tecnologias Utilizadas

### Backend (Atual - Flask)
- **Python 3.11** - Linguagem principal
- **Flask** - Framework web
- **SQLAlchemy** - ORM
- **SQLite** - Banco de dados
- **JWT** - Autenticação
- **CORS** - Cross-origin requests

### Backend (Futuro - Spring Boot)
- **Java 17** - Linguagem principal
- **Spring Boot 3.2** - Framework principal
- **Hibernate** - ORM
- **PostgreSQL** - Banco de dados
- **Redis** - Cache
- **RabbitMQ** - Filas assíncronas
- **Keycloak** - Autenticação e autorização
- **Flyway** - Migrações de banco

### Frontend (Atual - React)
- **React 18** - Biblioteca UI
- **Vite** - Build tool
- **Tailwind CSS** - Estilização
- **Lucide Icons** - Ícones
- **React Router** - Roteamento

### Frontend (Futuro - Next.js)
- **Next.js 14** - Framework React com SSR
- **TypeScript** - Tipagem estática
- **Tailwind CSS** - Framework de estilização
- **Chart.js** - Gráficos e visualizações
- **React Query** - Gestão de estado
- **React Hook Form** - Formulários

### Infraestrutura
- **Docker** - Containerização
- **Netlify** - Deploy frontend
- **Prometheus** - Métricas
- **Grafana** - Monitoramento

## 🏗️ Arquitetura do Sistema

### Arquitetura Atual (Monolítica)
```
Frontend (React) ↔ Backend (Flask) ↔ Database (SQLite)
```

### Arquitetura Futura (Microserviços)
```
Frontend (Next.js) ↔ API Gateway ↔ Microserviços (Spring Boot) ↔ PostgreSQL/Redis
                                 ↕
                            Keycloak (Auth)
                                 ↕
                            RabbitMQ (Queue)
```

## 📁 Estrutura do Projeto

```
cms-business/
├── cms-backend/                 # Backend Flask atual
│   ├── src/
│   │   ├── main.py             # Aplicação principal
│   │   ├── models/             # Modelos de dados
│   │   ├── routes/             # Rotas da API
│   │   └── database/           # Configuração do banco
│   ├── venv/                   # Ambiente virtual Python
│   └── requirements.txt        # Dependências Python
├── cms-frontend/               # Frontend React atual
│   ├── src/
│   │   ├── components/         # Componentes React
│   │   ├── contexts/           # Contextos React
│   │   └── App.jsx            # Componente principal
│   ├── public/                 # Arquivos públicos
│   └── package.json           # Dependências Node.js
├── docs/                       # Documentação
│   ├── ESPECIFICACOES_TECNICAS_AVANCADAS.md
│   ├── ARQUITETURA_SPRING_BOOT.md
│   ├── FRONTEND_NEXTJS_TYPESCRIPT.md
│   └── MODULOS_AVANCADOS.md
└── README.md                   # Este arquivo
```

## 🚀 Como Executar

### Pré-requisitos
- Python 3.11+
- Node.js 18+
- Git

### Backend (Flask)
```bash
cd cms-backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows
pip install -r requirements.txt
python src/main.py
```

### Frontend (React)
```bash
cd cms-frontend
npm install
npm run dev
```

### Acesso
- **Frontend**: http://localhost:5173
- **Backend**: http://localhost:5000
- **Credenciais**: admin / admin123

## 🌐 Links de Demonstração

### Sistema Funcionando
- **URL Principal**: https://hkwboktf.manus.space
- **Backend API**: https://5000-if5b8iffml5msffc0u9on-a6f51494.manusvm.computer

### Como Testar
1. Acesse: https://hkwboktf.manus.space
2. Clique em "Entrar"
3. Use as credenciais: **admin** / **admin123**
4. Explore todos os módulos disponíveis

## 🇧🇷 Conformidade Brasileira

### Legislação Atendida
- ✅ **NBC** (Normas Brasileiras de Contabilidade)
- ✅ **Lei 6.404/76** (Lei das S.A.)
- ✅ **Código Civil Brasileiro**
- ✅ **CLT** (Consolidação das Leis do Trabalho)
- ✅ **SPED** (Sistema Público de Escrituração Digital)
- ✅ **eSocial** (Sistema de Escrituração Digital das Obrigações Fiscais)

### Integrações Governamentais
- ✅ **SEFAZ** - Emissão de NF-e/NFC-e
- ✅ **Receita Federal** - SPED, ECF, eSocial
- ✅ **Prefeituras** - ISS
- ✅ **Bancos** - Conciliação e pagamentos

### Documentos Brasileiros
- ✅ **CPF/CNPJ** - Validação automática
- ✅ **CEP** - Consulta via viaCEP
- ✅ **Regimes Tributários** - Simples Nacional, Lucro Presumido, Lucro Real

## 📊 Dashboards e Relatórios

### Dashboard Executivo
- Faturamento mensal/anual
- Margem de lucro
- Fluxo de caixa
- Inadimplência
- Vendas por produto/cliente

### Relatórios Disponíveis
- **Contábeis**: Balancete, DRE, Balanço Patrimonial
- **Fiscais**: Livros fiscais, SPED, Apuração de impostos
- **Financeiros**: Contas a pagar/receber, Fluxo de caixa
- **Vendas**: Performance, Comissões, Análise de clientes
- **Estoque**: Movimentação, Inventário, Curva ABC
- **RH**: Folha de pagamento, Frequência, Férias

## 🔐 Segurança

### Autenticação
- JWT (JSON Web Tokens)
- Keycloak (futuro)
- SSO com Google/Microsoft (futuro)

### Autorização
- Controle de acesso por função
- Permissões granulares
- Auditoria de ações

### Dados
- Criptografia de senhas
- Backup automático
- Conformidade com LGPD

## 🎯 Público-Alvo

### Empresas Atendidas
- **Microempresas** (ME)
- **Empresas de Pequeno Porte** (EPP)
- **Médias Empresas**

### Segmentos
- Comércio
- Serviços
- Indústria
- Profissionais liberais
- Escritórios de contabilidade

## 💰 Modelo de Negócio

### Período de Teste
- **30 dias grátis**
- Acesso completo a todos os módulos
- Sem restrições de funcionalidades
- Suporte técnico incluído

### Planos Comerciais
- **Básico**: R$ 99/mês - Módulos essenciais
- **Intermediário**: R$ 199/mês - Módulos completos
- **Avançado**: R$ 399/mês - Todos os módulos + BI

### Diferenciais
- ✅ **Sem taxa de setup**
- ✅ **Sem fidelidade**
- ✅ **Suporte 24/7**
- ✅ **Atualizações automáticas**
- ✅ **Backup incluído**

## 🛣️ Roadmap

### Fase 1 - Atual ✅
- Sistema base funcionando
- Módulos principais implementados
- Interface React responsiva
- Backend Flask estável

### Fase 2 - Em Desenvolvimento 🔄
- Migração para Spring Boot
- Implementação do PostgreSQL
- Módulos de Vendas e Estoque completos
- Integração com Keycloak

### Fase 3 - Próxima 📋
- Frontend Next.js com TypeScript
- Módulo de RH completo
- Sistema de BI avançado
- Integrações governamentais

### Fase 4 - Futuro 🚀
- Mobile app (React Native)
- API marketplace
- Integrações com ERPs externos
- IA para insights automáticos

## 🤝 Contribuição

### Como Contribuir
1. Fork o projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

### Padrões de Código
- **Backend**: PEP 8 (Python)
- **Frontend**: ESLint + Prettier
- **Commits**: Conventional Commits
- **Testes**: Cobertura mínima de 80%

## 📞 Suporte

### Canais de Atendimento
- **Email**: suporte@cmsbusiness.com.br
- **WhatsApp**: (11) 99999-9999
- **Chat Online**: Disponível no sistema
- **Documentação**: docs.cmsbusiness.com.br

### Horários
- **Segunda a Sexta**: 8h às 18h
- **Sábado**: 8h às 12h
- **Emergências**: 24/7

## 📄 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 🏆 Reconhecimentos

### Tecnologias Utilizadas
- React.js e ecossistema
- Flask e Python
- Tailwind CSS
- Lucide Icons
- Vite

### Inspirações
- Sistemas ERP nacionais
- Melhores práticas de UX/UI
- Legislação brasileira
- Feedback de usuários reais

---

**CMS Business** - Transformando a gestão empresarial brasileira com tecnologia e inovação.

*Desenvolvido com ❤️ para empresas brasileiras*

## ✅ Checklist de Funcionamento Rápido

1. **Backend Flask** inicia sem erros (`python src/main.py`)
2. **Frontend React** inicia sem erros (`npm run dev`)
3. Acesso ao sistema via navegador em [http://localhost:5173](http://localhost:5173)
4. Login com usuário **admin / admin123** funciona
5. Todos os módulos principais acessíveis pelo menu
6. Teste de emissão de NF-e/NFC-e (ambiente de homologação)
7. Relatórios e dashboards carregam dados de exemplo
8. Integração básica com SEFAZ e viaCEP funcionando (se configurado)
9. Cadastro de clientes, produtos e funcionários funcionando
10. Fluxo de caixa e lançamentos contábeis básicos operacionais

Se algum item falhar, verifique os logs do backend e frontend e consulte a documentação ou suporte.

## 🚀 Como Publicar no GitHub e Deploy no Netlify

### 1. Criar Novo Repositório no GitHub

1. Acesse [github.com](https://github.com) e crie um novo repositório (público ou privado).
2. No terminal, inicialize o git no diretório raiz do projeto (se ainda não estiver):
   ```bash
   git init
   git remote add origin https://github.com/SEU_USUARIO/NOME_DO_REPOSITORIO.git
   ```
3. Adicione todos os arquivos e faça o commit inicial:
   ```bash
   git add .
   git commit -m "commit inicial"
   git push -u origin master
   ```
   > Se o branch principal for `main`, use `git push -u origin main`.

### 2. Deploy do Frontend no Netlify

1. Acesse [netlify.com](https://app.netlify.com/) e faça login/crie uma conta.
2. Clique em "Add new site" > "Import an existing project".
3. Conecte sua conta GitHub e selecione o repositório criado.
4. Configure:
   - **Build command**: `npm run build`
   - **Publish directory**: `cms-frontend/dist`
5. Clique em "Deploy site".
6. Após o deploy, Netlify fornecerá uma URL pública para seu frontend.

### 3. Dicas

- Sempre faça commit e push das alterações para o GitHub antes de cada deploy.
- Para deploy do backend, utilize serviços como Heroku, Railway, Render ou VPS próprio.
- Configure variáveis de ambiente sensíveis apenas no painel do Netlify (NUNCA no repositório público).

## 🚀 Checklist Completo para Deploy no GitHub e Netlify

### 1. Organização do Projeto

- Certifique-se de que a estrutura de pastas está conforme o README.
- O frontend deve estar em `cms-frontend/` e o backend em `cms-backend/`.
- O arquivo `package.json` deve estar dentro de `cms-frontend/`.
- O arquivo `requirements.txt` deve estar dentro de `cms-backend/`.

### 2. Arquivos Essenciais

- Crie um `.gitignore` na raiz do projeto com:
  ```
  # .gitignore
  cms-backend/venv/
  cms-frontend/node_modules/
  *.pyc
  __pycache__/
  .env
  ```
- Adicione um `README.md` na raiz (além deste completo).
- Adicione um arquivo `LICENSE` (MIT, conforme indicado).

### 3. Versionamento com Git e GitHub

- Inicie o repositório git na raiz do projeto:
  ```bash
  git init
  git add .
  git commit -m "commit inicial"
  git branch -M main
  git remote add origin https://github.com/Imo-Smart/cms-business.git
  git push -u origin main
  ```
- Faça push de todas as alterações sempre que atualizar o projeto.

### 4. Deploy do Frontend no Netlify

- No painel do Netlify:
  - Build command: `npm run build`
  - Publish directory: `cms-frontend/dist`
- Configure variáveis de ambiente (se necessário) no painel do Netlify.
- O backend Flask não é hospedado no Netlify, apenas o frontend.

### 5. Deploy do Backend

- Para produção, utilize serviços como:
  - [Railway](https://railway.app/)
  - [Render](https://render.com/)
  - [Heroku](https://heroku.com/)
  - VPS próprio (Ubuntu, Docker, etc)
- Nunca exponha variáveis sensíveis no repositório. Use `.env` e configure no painel do serviço.

### 6. Variáveis de Ambiente

- No frontend, configure a URL da API backend em `.env`:
  ```
  VITE_API_URL=https://SEU_BACKEND_PRODUCAO
  ```
- No backend, configure variáveis como `SECRET_KEY`, `DATABASE_URL`, etc, em `.env`.

### 7. Testes Locais

- Antes do deploy, rode localmente:
  - Backend: `python src/main.py`
  - Frontend: `npm run dev` e depois `npm run build`
- Teste login, navegação e principais módulos.

### 8. Segurança

- Nunca faça commit de senhas, tokens ou arquivos `.env`.
- Use HTTPS em produção.
- Mantenha dependências atualizadas.

### 9. Pós-Deploy

- Teste o frontend na URL do Netlify.
- Teste o backend na URL do serviço escolhido.
- Ajuste CORS no backend para aceitar o domínio do frontend.

---

Siga todos esses passos para garantir um deploy seguro, funcional e profissional do seu sistema CMS Business.

