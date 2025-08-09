import os
import sys
# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from datetime import timedelta

# Importar modelos
from src.models.user import db, User, Role
from src.models.content import Page, Post, Category, Media
from src.models.accounting import Company, AccountType, Account, CostCenter, JournalEntry, JournalEntryLine, FiscalPeriod
from src.models.fiscal import TaxType, TaxRate, Customer, Product, Invoice, InvoiceItem, InvoiceTax
from src.models.financial import BankAccount, BankTransaction, PaymentMethod, Supplier, Receivable, Payable, CashFlow
from src.models.departments import Department, Permission, RolePermission, DepartmentModule, WorkflowStep, DepartmentMetric

# Importar rotas
from src.routes.user import user_bp
from src.routes.auth import auth_bp
from src.routes.content import content_bp
from src.routes.accounting import accounting_bp
from src.routes.fiscal import fiscal_bp
from src.routes.financial import financial_bp
from src.routes.sales import sales_bp
from src.routes.departments import departments_bp
from src.routes.hr_advanced import hr_bp

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))

# Configurações básicas
app.config['SECRET_KEY'] = 'cms-business-production-secret-key-2025'
app.config['JWT_SECRET_KEY'] = 'jwt-production-secret-string-2025'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)

# Configuração do banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(os.path.dirname(__file__), 'database', 'production.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Configuração de upload
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__), 'static', 'uploads')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Inicializar extensões
CORS(app, origins="*")
jwt = JWTManager(app)
db.init_app(app)

# Registrar blueprints
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(user_bp, url_prefix='/api')
app.register_blueprint(content_bp, url_prefix='/api')
app.register_blueprint(accounting_bp, url_prefix='/api/accounting')
app.register_blueprint(fiscal_bp, url_prefix='/api/fiscal')
app.register_blueprint(financial_bp, url_prefix='/api/financial')
app.register_blueprint(sales_bp, url_prefix='/api/sales')
app.register_blueprint(departments_bp, url_prefix='/api/departments')
app.register_blueprint(hr_bp, url_prefix='/api/hr')

def create_production_data():
    """Criar dados iniciais para ambiente de produção"""
    from werkzeug.security import generate_password_hash
    
    # Criar roles
    roles = [
        Role(name='admin', description='Administrador do sistema'),
        Role(name='manager', description='Gestor empresarial'),
        Role(name='accountant', description='Contador'),
        Role(name='financial', description='Financeiro'),
        Role(name='sales', description='Vendas'),
        Role(name='user', description='Utilizador padrão'),
    ]
    
    for role in roles:
        db.session.add(role)
    db.session.commit()
    
    # Criar utilizador administrador
    admin_role = Role.query.filter_by(name='admin').first()
    admin_user = User(
        username='admin',
        email='admin@empresa.com.br',
        password_hash=generate_password_hash('admin123'),
        first_name='Administrador',
        last_name='Sistema',
        is_active=True,
        role_id=admin_role.id
    )
    db.session.add(admin_user)
    db.session.commit()
    
    # Criar empresa principal (dados em branco para configuração)
    company = Company(
        cnpj='',
        name='Sua Empresa LTDA',
        trade_name='Sua Empresa',
        email='contato@suaempresa.com.br',
        phone='',
        address='',
        city='',
        state='',
        zip_code='',
        tax_regime='simples_nacional'
    )
    db.session.add(company)
    db.session.commit()
    
    # Criar tipos de conta contábil (Plano de Contas Brasileiro)
    account_types = [
        AccountType(code='1', name='ATIVO', nature='debit', category='ativo'),
        AccountType(code='1.1', name='ATIVO CIRCULANTE', nature='debit', category='ativo'),
        AccountType(code='1.1.1', name='DISPONÍVEL', nature='debit', category='ativo'),
        AccountType(code='1.1.2', name='CRÉDITOS', nature='debit', category='ativo'),
        AccountType(code='1.1.3', name='ESTOQUES', nature='debit', category='ativo'),
        AccountType(code='1.1.4', name='DESPESAS ANTECIPADAS', nature='debit', category='ativo'),
        AccountType(code='1.2', name='ATIVO NÃO CIRCULANTE', nature='debit', category='ativo'),
        AccountType(code='1.2.1', name='REALIZÁVEL A LONGO PRAZO', nature='debit', category='ativo'),
        AccountType(code='1.2.2', name='INVESTIMENTOS', nature='debit', category='ativo'),
        AccountType(code='1.2.3', name='IMOBILIZADO', nature='debit', category='ativo'),
        AccountType(code='1.2.4', name='INTANGÍVEL', nature='debit', category='ativo'),
        
        AccountType(code='2', name='PASSIVO', nature='credit', category='passivo'),
        AccountType(code='2.1', name='PASSIVO CIRCULANTE', nature='credit', category='passivo'),
        AccountType(code='2.1.1', name='OBRIGAÇÕES TRABALHISTAS', nature='credit', category='passivo'),
        AccountType(code='2.1.2', name='OBRIGAÇÕES TRIBUTÁRIAS', nature='credit', category='passivo'),
        AccountType(code='2.1.3', name='EMPRÉSTIMOS E FINANCIAMENTOS', nature='credit', category='passivo'),
        AccountType(code='2.1.4', name='FORNECEDORES', nature='credit', category='passivo'),
        AccountType(code='2.2', name='PASSIVO NÃO CIRCULANTE', nature='credit', category='passivo'),
        AccountType(code='2.3', name='PATRIMÔNIO LÍQUIDO', nature='credit', category='patrimonio_liquido'),
        
        AccountType(code='3', name='RECEITAS', nature='credit', category='receita'),
        AccountType(code='3.1', name='RECEITA BRUTA', nature='credit', category='receita'),
        AccountType(code='3.2', name='DEDUÇÕES DA RECEITA BRUTA', nature='debit', category='receita'),
        AccountType(code='3.3', name='OUTRAS RECEITAS OPERACIONAIS', nature='credit', category='receita'),
        AccountType(code='3.4', name='RECEITAS NÃO OPERACIONAIS', nature='credit', category='receita'),
        
        AccountType(code='4', name='CUSTOS E DESPESAS', nature='debit', category='despesa'),
        AccountType(code='4.1', name='CUSTOS DOS PRODUTOS VENDIDOS', nature='debit', category='despesa'),
        AccountType(code='4.2', name='CUSTOS DOS SERVIÇOS PRESTADOS', nature='debit', category='despesa'),
        AccountType(code='4.3', name='DESPESAS OPERACIONAIS', nature='debit', category='despesa'),
        AccountType(code='4.4', name='DESPESAS NÃO OPERACIONAIS', nature='debit', category='despesa'),
    ]
    
    for account_type in account_types:
        db.session.add(account_type)
    db.session.commit()
    
    # Criar plano de contas básico brasileiro
    accounts = [
        # ATIVO CIRCULANTE - DISPONÍVEL
        Account(company_id=company.id, code='1.1.1.01', name='CAIXA', account_type_id=3, level=4),
        Account(company_id=company.id, code='1.1.1.02', name='BANCOS CONTA MOVIMENTO', account_type_id=3, level=4),
        Account(company_id=company.id, code='1.1.1.03', name='APLICAÇÕES FINANCEIRAS', account_type_id=3, level=4),
        
        # ATIVO CIRCULANTE - CRÉDITOS
        Account(company_id=company.id, code='1.1.2.01', name='CLIENTES', account_type_id=4, level=4),
        Account(company_id=company.id, code='1.1.2.02', name='DUPLICATAS A RECEBER', account_type_id=4, level=4),
        Account(company_id=company.id, code='1.1.2.03', name='ADIANTAMENTOS A FORNECEDORES', account_type_id=4, level=4),
        Account(company_id=company.id, code='1.1.2.04', name='IMPOSTOS A RECUPERAR', account_type_id=4, level=4),
        
        # ATIVO CIRCULANTE - ESTOQUES
        Account(company_id=company.id, code='1.1.3.01', name='ESTOQUE DE MERCADORIAS', account_type_id=5, level=4),
        Account(company_id=company.id, code='1.1.3.02', name='ESTOQUE DE PRODUTOS ACABADOS', account_type_id=5, level=4),
        Account(company_id=company.id, code='1.1.3.03', name='ESTOQUE DE MATÉRIAS-PRIMAS', account_type_id=5, level=4),
        
        # ATIVO NÃO CIRCULANTE - IMOBILIZADO
        Account(company_id=company.id, code='1.2.3.01', name='MÓVEIS E UTENSÍLIOS', account_type_id=10, level=4),
        Account(company_id=company.id, code='1.2.3.02', name='MÁQUINAS E EQUIPAMENTOS', account_type_id=10, level=4),
        Account(company_id=company.id, code='1.2.3.03', name='VEÍCULOS', account_type_id=10, level=4),
        Account(company_id=company.id, code='1.2.3.04', name='COMPUTADORES E PERIFÉRICOS', account_type_id=10, level=4),
        Account(company_id=company.id, code='1.2.3.05', name='DEPRECIAÇÃO ACUMULADA', account_type_id=10, level=4),
        
        # PASSIVO CIRCULANTE - FORNECEDORES
        Account(company_id=company.id, code='2.1.4.01', name='FORNECEDORES NACIONAIS', account_type_id=16, level=4),
        Account(company_id=company.id, code='2.1.4.02', name='FORNECEDORES ESTRANGEIROS', account_type_id=16, level=4),
        
        # PASSIVO CIRCULANTE - OBRIGAÇÕES TRABALHISTAS
        Account(company_id=company.id, code='2.1.1.01', name='SALÁRIOS A PAGAR', account_type_id=13, level=4),
        Account(company_id=company.id, code='2.1.1.02', name='FGTS A RECOLHER', account_type_id=13, level=4),
        Account(company_id=company.id, code='2.1.1.03', name='INSS A RECOLHER', account_type_id=13, level=4),
        Account(company_id=company.id, code='2.1.1.04', name='PROVISÃO PARA FÉRIAS', account_type_id=13, level=4),
        Account(company_id=company.id, code='2.1.1.05', name='PROVISÃO PARA 13º SALÁRIO', account_type_id=13, level=4),
        
        # PASSIVO CIRCULANTE - OBRIGAÇÕES TRIBUTÁRIAS
        Account(company_id=company.id, code='2.1.2.01', name='ICMS A RECOLHER', account_type_id=14, level=4),
        Account(company_id=company.id, code='2.1.2.02', name='IPI A RECOLHER', account_type_id=14, level=4),
        Account(company_id=company.id, code='2.1.2.03', name='PIS A RECOLHER', account_type_id=14, level=4),
        Account(company_id=company.id, code='2.1.2.04', name='COFINS A RECOLHER', account_type_id=14, level=4),
        Account(company_id=company.id, code='2.1.2.05', name='ISS A RECOLHER', account_type_id=14, level=4),
        Account(company_id=company.id, code='2.1.2.06', name='IRPJ A RECOLHER', account_type_id=14, level=4),
        Account(company_id=company.id, code='2.1.2.07', name='CSLL A RECOLHER', account_type_id=14, level=4),
        Account(company_id=company.id, code='2.1.2.08', name='SIMPLES NACIONAL A RECOLHER', account_type_id=14, level=4),
        
        # PATRIMÔNIO LÍQUIDO
        Account(company_id=company.id, code='2.3.01', name='CAPITAL SOCIAL', account_type_id=18, level=3),
        Account(company_id=company.id, code='2.3.02', name='RESERVAS DE CAPITAL', account_type_id=18, level=3),
        Account(company_id=company.id, code='2.3.03', name='RESERVAS DE LUCROS', account_type_id=18, level=3),
        Account(company_id=company.id, code='2.3.04', name='LUCROS OU PREJUÍZOS ACUMULADOS', account_type_id=18, level=3),
        
        # RECEITAS
        Account(company_id=company.id, code='3.1.01', name='VENDAS DE MERCADORIAS', account_type_id=20, level=3),
        Account(company_id=company.id, code='3.1.02', name='VENDAS DE PRODUTOS', account_type_id=20, level=3),
        Account(company_id=company.id, code='3.1.03', name='PRESTAÇÃO DE SERVIÇOS', account_type_id=20, level=3),
        Account(company_id=company.id, code='3.2.01', name='DEVOLUÇÕES DE VENDAS', account_type_id=21, level=3),
        Account(company_id=company.id, code='3.2.02', name='ABATIMENTOS SOBRE VENDAS', account_type_id=21, level=3),
        Account(company_id=company.id, code='3.2.03', name='IMPOSTOS SOBRE VENDAS', account_type_id=21, level=3),
        
        # CUSTOS E DESPESAS
        Account(company_id=company.id, code='4.1.01', name='CUSTO DAS MERCADORIAS VENDIDAS', account_type_id=25, level=3),
        Account(company_id=company.id, code='4.1.02', name='CUSTO DOS PRODUTOS VENDIDOS', account_type_id=25, level=3),
        Account(company_id=company.id, code='4.2.01', name='CUSTO DOS SERVIÇOS PRESTADOS', account_type_id=26, level=3),
        Account(company_id=company.id, code='4.3.01', name='DESPESAS ADMINISTRATIVAS', account_type_id=27, level=3),
        Account(company_id=company.id, code='4.3.02', name='DESPESAS COMERCIAIS', account_type_id=27, level=3),
        Account(company_id=company.id, code='4.3.03', name='DESPESAS FINANCEIRAS', account_type_id=27, level=3),
    ]
    
    for account in accounts:
        db.session.add(account)
    db.session.commit()
    
    # Criar tipos de impostos brasileiros
    tax_types = [
        TaxType(code='ICMS', name='ICMS', description='Imposto sobre Circulação de Mercadorias e Serviços', calculation_base='valor_produto', is_federal=False),
        TaxType(code='IPI', name='IPI', description='Imposto sobre Produtos Industrializados', calculation_base='valor_produto', is_federal=True),
        TaxType(code='PIS', name='PIS', description='Programa de Integração Social', calculation_base='valor_total', is_federal=True),
        TaxType(code='COFINS', name='COFINS', description='Contribuição para o Financiamento da Seguridade Social', calculation_base='valor_total', is_federal=True),
        TaxType(code='ISS', name='ISS', description='Imposto sobre Serviços', calculation_base='valor_servico', is_federal=False),
        TaxType(code='IRPJ', name='IRPJ', description='Imposto de Renda Pessoa Jurídica', calculation_base='lucro_real', is_federal=True),
        TaxType(code='CSLL', name='CSLL', description='Contribuição Social sobre o Lucro Líquido', calculation_base='lucro_real', is_federal=True),
        TaxType(code='SIMPLES', name='Simples Nacional', description='Regime Especial Unificado de Arrecadação', calculation_base='faturamento', is_federal=True),
    ]
    
    for tax_type in tax_types:
        db.session.add(tax_type)
    db.session.commit()
    
    # Criar formas de pagamento
    payment_methods = [
        PaymentMethod(code='DINHEIRO', name='Dinheiro', type='cash', requires_bank_account=False),
        PaymentMethod(code='PIX', name='PIX', type='pix', requires_bank_account=True),
        PaymentMethod(code='TED', name='Transferência Bancária', type='bank_transfer', requires_bank_account=True),
        PaymentMethod(code='DOC', name='DOC', type='bank_transfer', requires_bank_account=True),
        PaymentMethod(code='CARTAO_CREDITO', name='Cartão de Crédito', type='credit_card', requires_bank_account=False, default_installments=1),
        PaymentMethod(code='CARTAO_DEBITO', name='Cartão de Débito', type='debit_card', requires_bank_account=False),
        PaymentMethod(code='CHEQUE', name='Cheque', type='check', requires_bank_account=True),
        PaymentMethod(code='BOLETO', name='Boleto Bancário', type='bank_slip', requires_bank_account=True),
        PaymentMethod(code='DUPLICATA', name='Duplicata', type='promissory_note', requires_bank_account=False),
    ]
    
    for payment_method in payment_methods:
        db.session.add(payment_method)
    db.session.commit()
    
    # Criar departamentos da construtora
    departments = [
        # Nível 1 - Diretorias
        Department(name='Diretoria Executiva', code='DIR', description='Diretoria Executiva da empresa', level=1),
        Department(name='Área Comercial', code='COM', description='Área Comercial e Marketing', level=1),
        Department(name='Área de Engenharia e Projetos', code='ENG', description='Engenharia e Desenvolvimento de Projetos', level=1),
        Department(name='Área Operacional', code='OPE', description='Operações e Execução', level=1),
        Department(name='Área de Qualidade e Meio Ambiente', code='QMA', description='Qualidade e Sustentabilidade', level=1),
        Department(name='Departamento de Recursos Humanos', code='RH', description='Gestão de Pessoas', level=1),
        Department(name='Departamento de Tecnologia da Informação', code='TI', description='Tecnologia e Sistemas', level=1),
    ]
    
    for dept in departments:
        db.session.add(dept)
    db.session.commit()
    
    # Buscar departamentos criados para criar subdepartamentos
    dir_dept = Department.query.filter_by(code='DIR').first()
    com_dept = Department.query.filter_by(code='COM').first()
    eng_dept = Department.query.filter_by(code='ENG').first()
    ope_dept = Department.query.filter_by(code='OPE').first()
    qma_dept = Department.query.filter_by(code='QMA').first()
    
    # Nível 2 - Subdepartamentos
    subdepartments = [
        # Sob Diretoria Executiva
        Department(name='Departamento Administrativo', code='ADM', description='Administração Geral', parent_id=dir_dept.id, level=2),
        Department(name='Departamento Financeiro', code='FIN', description='Gestão Financeira', parent_id=dir_dept.id, level=2),
        Department(name='Departamento Jurídico', code='JUR', description='Assuntos Jurídicos', parent_id=dir_dept.id, level=2),
        Department(name='Departamento de Auditoria e Compliance', code='AUD', description='Auditoria e Conformidade', parent_id=dir_dept.id, level=2),
        
        # Sob Área Comercial
        Department(name='Departamento Comercial e Vendas', code='VEN', description='Vendas e Relacionamento', parent_id=com_dept.id, level=2),
        Department(name='Departamento de Marketing e Comunicação', code='MKT', description='Marketing e Comunicação', parent_id=com_dept.id, level=2),
        Department(name='Departamento de Atendimento ao Cliente', code='SAC', description='Pós-Venda e Suporte', parent_id=com_dept.id, level=2),
        
        # Sob Área de Engenharia
        Department(name='Departamento de Engenharia', code='ENG_EXEC', description='Engenharia Executiva', parent_id=eng_dept.id, level=2),
        Department(name='Departamento de Projetos e Planejamento', code='PRJ', description='Projetos e Planejamento', parent_id=eng_dept.id, level=2),
        Department(name='Departamento de Orçamentos e Custos', code='ORC', description='Orçamentos e Análise de Custos', parent_id=eng_dept.id, level=2),
        
        # Sob Área Operacional
        Department(name='Departamento de Obras (Execução)', code='OBR', description='Execução de Obras', parent_id=ope_dept.id, level=2),
        Department(name='Departamento de Compras e Suprimentos', code='CPR', description='Compras e Suprimentos', parent_id=ope_dept.id, level=2),
        Department(name='Departamento de Logística', code='LOG', description='Logística e Distribuição', parent_id=ope_dept.id, level=2),
        Department(name='Departamento de Controle de Produção', code='PCP', description='Planejamento e Controle da Produção', parent_id=ope_dept.id, level=2),
        Department(name='Departamento de Manutenção e Equipamentos', code='MAN', description='Manutenção de Equipamentos', parent_id=ope_dept.id, level=2),
        
        # Sob Área de Qualidade
        Department(name='Departamento de Qualidade e Segurança', code='QST', description='Qualidade e Segurança do Trabalho', parent_id=qma_dept.id, level=2),
        Department(name='Departamento de Meio Ambiente', code='AMB', description='Meio Ambiente e Sustentabilidade', parent_id=qma_dept.id, level=2),
    ]
    
    for subdept in subdepartments:
        db.session.add(subdept)
    db.session.commit()
    
    # Criar permissões do sistema
    permissions = [
        # Permissões gerais
        Permission(name='Visualizar Dashboard', code='dashboard_view', description='Visualizar dashboard principal', module='dashboard'),
        Permission(name='Administrar Sistema', code='system_admin', description='Administração completa do sistema', module='system'),
        
        # Permissões financeiras
        Permission(name='Visualizar Financeiro', code='financial_view', description='Visualizar dados financeiros', module='financial'),
        Permission(name='Editar Financeiro', code='financial_edit', description='Editar dados financeiros', module='financial'),
        Permission(name='Aprovar Pagamentos', code='financial_approve', description='Aprovar pagamentos', module='financial'),
        
        # Permissões de vendas
        Permission(name='Visualizar Vendas', code='sales_view', description='Visualizar dados de vendas', module='sales'),
        Permission(name='Editar Vendas', code='sales_edit', description='Editar dados de vendas', module='sales'),
        Permission(name='Aprovar Propostas', code='sales_approve', description='Aprovar propostas comerciais', module='sales'),
        
        # Permissões de RH
        Permission(name='Visualizar RH', code='hr_view', description='Visualizar dados de RH', module='hr'),
        Permission(name='Editar RH', code='hr_edit', description='Editar dados de RH', module='hr'),
        Permission(name='Processar Folha', code='hr_payroll', description='Processar folha de pagamento', module='hr'),
        
        # Permissões de obras
        Permission(name='Visualizar Obras', code='construction_view', description='Visualizar dados de obras', module='construction'),
        Permission(name='Editar Obras', code='construction_edit', description='Editar dados de obras', module='construction'),
        Permission(name='Aprovar Medições', code='construction_approve', description='Aprovar medições de obras', module='construction'),
        
        # Permissões de compras
        Permission(name='Visualizar Compras', code='purchase_view', description='Visualizar dados de compras', module='purchase'),
        Permission(name='Editar Compras', code='purchase_edit', description='Editar dados de compras', module='purchase'),
        Permission(name='Aprovar Compras', code='purchase_approve', description='Aprovar pedidos de compra', module='purchase'),
    ]
    
    for permission in permissions:
        db.session.add(permission)
    db.session.commit()
    
    # Criar centro de custo padrão
    cost_center = CostCenter(
        company_id=company.id,
        code='001',
        name='Administração Geral',
        description='Centro de custo padrão para administração'
    )
    db.session.add(cost_center)
    db.session.commit()
    
    print("Sistema CMS Business - Ambiente de Produção Configurado:")
    print("- Utilizador admin: admin / admin123")
    print("- Roles empresariais criadas")
    print("- Empresa base configurada (dados em branco)")
    print("- Plano de contas brasileiro completo")
    print("- Tipos de impostos brasileiros")
    print("- Formas de pagamento nacionais")
    print("- Centro de custo padrão")
    print("- Sistema pronto para configuração empresarial")

# Criar tabelas e dados iniciais
with app.app_context():
    db.create_all()
    
    # Criar dados iniciais se não existirem
    if not Role.query.first():
        create_production_data()

# Criar diretório de uploads se não existir
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    static_folder_path = app.static_folder
    if static_folder_path is None:
            return "Static folder not configured", 404

    if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
        return send_from_directory(static_folder_path, path)
    else:
        index_path = os.path.join(static_folder_path, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(static_folder_path, 'index.html')
        else:
            return "Frontend not found", 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)

