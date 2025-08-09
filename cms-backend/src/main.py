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
from src.models.content import Category, Page, Post, Tag, Media, Setting
from src.models.accounting import Company, AccountType, Account, CostCenter, JournalEntry, JournalEntryLine, FiscalPeriod
from src.models.fiscal import TaxType, TaxRate, Customer, Product, Invoice, InvoiceItem, InvoiceTax
from src.models.financial import BankAccount, BankTransaction, PaymentMethod, Supplier, Receivable, Payable, CashFlow

# Importar rotas
from src.routes.user import user_bp
from src.routes.auth import auth_bp
from src.routes.content import content_bp
from src.routes.accounting import accounting_bp
from src.routes.fiscal import fiscal_bp

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))

# Configurações básicas
app.config['SECRET_KEY'] = 'cms-business-secret-key-change-in-production'
app.config['JWT_SECRET_KEY'] = 'jwt-secret-string-change-in-production'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)

# Configuração do banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(os.path.dirname(__file__), 'database', 'app.db')}"
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

def create_initial_data():
    """Cria dados iniciais do sistema empresarial"""
    
    # Criar roles
    admin_role = Role(
        name='admin',
        description='Administrador do sistema',
        permissions=['create', 'read', 'update', 'delete', 'manage_users', 'manage_settings']
    )
    accountant_role = Role(
        name='accountant',
        description='Contador',
        permissions=['create', 'read', 'update', 'accounting', 'fiscal']
    )
    financial_role = Role(
        name='financial',
        description='Financeiro',
        permissions=['create', 'read', 'update', 'financial']
    )
    sales_role = Role(
        name='sales',
        description='Vendas',
        permissions=['create', 'read', 'update', 'sales', 'customers']
    )
    editor_role = Role(
        name='editor',
        description='Editor de conteúdo',
        permissions=['create', 'read', 'update', 'delete']
    )
    
    db.session.add_all([admin_role, accountant_role, financial_role, sales_role, editor_role])
    db.session.commit()
    
    # Criar usuário admin padrão
    admin_user = User(
        username='admin',
        email='admin@cms-business.com',
        first_name='Admin',
        last_name='User',
        role_id=admin_role.id
    )
    admin_user.set_password('admin123')
    db.session.add(admin_user)
    
    # Criar empresa padrão
    company = Company(
        cnpj='00.000.000/0001-00',
        name='Empresa Demonstração LTDA',
        trade_name='Demo Company',
        email='contato@democompany.com.br',
        phone='(11) 99999-9999',
        address='Rua das Empresas, 123',
        city='São Paulo',
        state='SP',
        zip_code='01234-567',
        tax_regime='simples_nacional'
    )
    db.session.add(company)
    db.session.commit()
    
    # Criar tipos de conta contábil
    account_types = [
        AccountType(code='1', name='ATIVO', nature='debit', category='ativo'),
        AccountType(code='1.1', name='ATIVO CIRCULANTE', nature='debit', category='ativo'),
        AccountType(code='1.2', name='ATIVO NÃO CIRCULANTE', nature='debit', category='ativo'),
        AccountType(code='2', name='PASSIVO', nature='credit', category='passivo'),
        AccountType(code='2.1', name='PASSIVO CIRCULANTE', nature='credit', category='passivo'),
        AccountType(code='2.2', name='PASSIVO NÃO CIRCULANTE', nature='credit', category='passivo'),
        AccountType(code='2.3', name='PATRIMÔNIO LÍQUIDO', nature='credit', category='patrimonio_liquido'),
        AccountType(code='3', name='RECEITAS', nature='credit', category='receita'),
        AccountType(code='4', name='DESPESAS', nature='debit', category='despesa'),
    ]
    
    for account_type in account_types:
        db.session.add(account_type)
    db.session.commit()
    
    # Criar plano de contas básico
    accounts = [
        # ATIVO CIRCULANTE
        Account(company_id=company.id, code='1.1.01', name='CAIXA E EQUIVALENTES DE CAIXA', account_type_id=2, level=3, is_analytical=False),
        Account(company_id=company.id, code='1.1.01.01', name='Caixa', account_type_id=2, level=4),
        Account(company_id=company.id, code='1.1.01.02', name='Bancos Conta Movimento', account_type_id=2, level=4),
        Account(company_id=company.id, code='1.1.02', name='CONTAS A RECEBER', account_type_id=2, level=3, is_analytical=False),
        Account(company_id=company.id, code='1.1.02.01', name='Clientes', account_type_id=2, level=4),
        
        # PASSIVO CIRCULANTE
        Account(company_id=company.id, code='2.1.01', name='FORNECEDORES', account_type_id=5, level=3, is_analytical=False),
        Account(company_id=company.id, code='2.1.01.01', name='Fornecedores Nacionais', account_type_id=5, level=4),
        Account(company_id=company.id, code='2.1.02', name='OBRIGAÇÕES TRABALHISTAS', account_type_id=5, level=3, is_analytical=False),
        Account(company_id=company.id, code='2.1.03', name='OBRIGAÇÕES TRIBUTÁRIAS', account_type_id=5, level=3, is_analytical=False),
        
        # PATRIMÔNIO LÍQUIDO
        Account(company_id=company.id, code='2.3.01', name='CAPITAL SOCIAL', account_type_id=7, level=3, is_analytical=True),
        Account(company_id=company.id, code='2.3.02', name='LUCROS ACUMULADOS', account_type_id=7, level=3, is_analytical=True),
        
        # RECEITAS
        Account(company_id=company.id, code='3.01', name='RECEITA BRUTA', account_type_id=8, level=2, is_analytical=False),
        Account(company_id=company.id, code='3.01.01', name='Vendas de Produtos', account_type_id=8, level=3),
        Account(company_id=company.id, code='3.01.02', name='Prestação de Serviços', account_type_id=8, level=3),
        
        # DESPESAS
        Account(company_id=company.id, code='4.01', name='CUSTOS DOS PRODUTOS VENDIDOS', account_type_id=9, level=2, is_analytical=False),
        Account(company_id=company.id, code='4.02', name='DESPESAS OPERACIONAIS', account_type_id=9, level=2, is_analytical=False),
        Account(company_id=company.id, code='4.02.01', name='Despesas Administrativas', account_type_id=9, level=3),
        Account(company_id=company.id, code='4.02.02', name='Despesas Comerciais', account_type_id=9, level=3),
    ]
    
    for account in accounts:
        db.session.add(account)
    db.session.commit()
    
    # Criar tipos de impostos
    tax_types = [
        TaxType(code='ICMS', name='ICMS', description='Imposto sobre Circulação de Mercadorias e Serviços', calculation_base='valor_produto', is_federal=False),
        TaxType(code='IPI', name='IPI', description='Imposto sobre Produtos Industrializados', calculation_base='valor_produto', is_federal=True),
        TaxType(code='PIS', name='PIS', description='Programa de Integração Social', calculation_base='valor_total', is_federal=True),
        TaxType(code='COFINS', name='COFINS', description='Contribuição para o Financiamento da Seguridade Social', calculation_base='valor_total', is_federal=True),
        TaxType(code='ISS', name='ISS', description='Imposto sobre Serviços', calculation_base='valor_servico', is_federal=False),
    ]
    
    for tax_type in tax_types:
        db.session.add(tax_type)
    db.session.commit()
    
    # Criar formas de pagamento
    payment_methods = [
        PaymentMethod(code='DINHEIRO', name='Dinheiro', type='cash', requires_bank_account=False),
        PaymentMethod(code='PIX', name='PIX', type='pix', requires_bank_account=True),
        PaymentMethod(code='TED', name='Transferência Bancária', type='bank_transfer', requires_bank_account=True),
        PaymentMethod(code='CARTAO_CREDITO', name='Cartão de Crédito', type='credit_card', requires_bank_account=False, default_installments=1),
        PaymentMethod(code='CARTAO_DEBITO', name='Cartão de Débito', type='debit_card', requires_bank_account=False),
        PaymentMethod(code='CHEQUE', name='Cheque', type='check', requires_bank_account=True),
        PaymentMethod(code='BOLETO', name='Boleto Bancário', type='bank_slip', requires_bank_account=True),
    ]
    
    for payment_method in payment_methods:
        db.session.add(payment_method)
    
    # Criar conta bancária padrão
    bank_account = BankAccount(
        company_id=company.id,
        bank_code='001',
        bank_name='Banco do Brasil',
        agency='1234',
        account_number='12345-6',
        account_digit='7',
        account_type='checking',
        initial_balance=10000.00,
        current_balance=10000.00
    )
    db.session.add(bank_account)
    
    # Criar centro de custo padrão
    cost_center = CostCenter(
        company_id=company.id,
        code='001',
        name='Administração',
        description='Centro de custo administrativo'
    )
    db.session.add(cost_center)
    
    # Criar cliente exemplo
    customer = Customer(
        company_id=company.id,
        type='pj',
        document='11.222.333/0001-44',
        name='Cliente Exemplo LTDA',
        trade_name='Cliente Exemplo',
        email='cliente@exemplo.com.br',
        phone='(11) 88888-8888',
        address='Rua dos Clientes, 456',
        city='São Paulo',
        state='SP',
        zip_code='01234-567',
        tax_regime='simples_nacional'
    )
    db.session.add(customer)
    
    # Criar fornecedor exemplo
    supplier = Supplier(
        company_id=company.id,
        type='pj',
        document='22.333.444/0001-55',
        name='Fornecedor Exemplo LTDA',
        trade_name='Fornecedor Exemplo',
        email='fornecedor@exemplo.com.br',
        phone='(11) 77777-7777',
        address='Rua dos Fornecedores, 789',
        city='São Paulo',
        state='SP',
        zip_code='01234-567'
    )
    db.session.add(supplier)
    
    # Criar produto exemplo
    product = Product(
        company_id=company.id,
        code='PROD001',
        name='Produto Exemplo',
        description='Produto para demonstração do sistema',
        type='product',
        unit='UN',
        cost_price=50.00,
        sale_price=100.00,
        ncm='12345678',
        cfop_internal='5102',
        cfop_external='6102',
        current_stock=100,
        minimum_stock=10
    )
    db.session.add(product)
    
    db.session.commit()
    
    print("Sistema Empresarial Brasileiro - Dados iniciais criados:")
    print("- Usuário admin: admin / admin123")
    print("- Roles: admin, accountant, financial, sales, editor")
    print("- Empresa: Empresa Demonstração LTDA")
    print("- Plano de contas básico criado")
    print("- Tipos de impostos brasileiros")
    print("- Formas de pagamento")
    print("- Conta bancária padrão")
    print("- Cliente e fornecedor exemplo")
    print("- Produto exemplo")

# Criar tabelas e dados iniciais
with app.app_context():
    db.create_all()
    
    # Criar dados iniciais se não existirem
    if not Role.query.first():
        create_initial_data()

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
            return "index.html not found", 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

