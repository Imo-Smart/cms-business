from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from decimal import Decimal
from src.models.user import db

class BankAccount(db.Model):
    """Contas Bancárias"""
    __tablename__ = 'bank_accounts'
    
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=False)
    bank_code = db.Column(db.String(3), nullable=False)  # Código do banco
    bank_name = db.Column(db.String(100), nullable=False)
    agency = db.Column(db.String(10), nullable=False)
    account_number = db.Column(db.String(20), nullable=False)
    account_digit = db.Column(db.String(2))
    account_type = db.Column(db.String(20), default='checking')  # checking, savings, investment
    
    # Saldos
    initial_balance = db.Column(db.Numeric(15, 2), default=0)
    current_balance = db.Column(db.Numeric(15, 2), default=0)
    
    # Controle
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relacionamentos
    transactions = db.relationship('BankTransaction', backref='bank_account', lazy=True)
    receivables = db.relationship('Receivable', backref='bank_account', lazy=True)
    payables = db.relationship('Payable', backref='bank_account', lazy=True)
    
    def __repr__(self):
        return f'<BankAccount {self.bank_name} - {self.account_number}>'
    
    def update_balance(self):
        """Atualiza o saldo atual baseado nas transações"""
        total_credits = sum([t.amount for t in self.transactions if t.type == 'credit'])
        total_debits = sum([t.amount for t in self.transactions if t.type == 'debit'])
        self.current_balance = self.initial_balance + total_credits - total_debits
    
    def to_dict(self):
        return {
            'id': self.id,
            'company_id': self.company_id,
            'bank_code': self.bank_code,
            'bank_name': self.bank_name,
            'agency': self.agency,
            'account_number': self.account_number,
            'account_digit': self.account_digit,
            'account_type': self.account_type,
            'initial_balance': float(self.initial_balance) if self.initial_balance else 0,
            'current_balance': float(self.current_balance) if self.current_balance else 0,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class BankTransaction(db.Model):
    """Movimentações Bancárias"""
    __tablename__ = 'bank_transactions'
    
    id = db.Column(db.Integer, primary_key=True)
    bank_account_id = db.Column(db.Integer, db.ForeignKey('bank_accounts.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    type = db.Column(db.String(10), nullable=False)  # credit, debit
    amount = db.Column(db.Numeric(15, 2), nullable=False)
    description = db.Column(db.Text, nullable=False)
    reference = db.Column(db.String(100))  # Número do documento
    category = db.Column(db.String(50))  # Categoria da movimentação
    
    # Conciliação
    is_reconciled = db.Column(db.Boolean, default=False)
    reconciled_at = db.Column(db.DateTime)
    reconciled_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    # Controle
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<BankTransaction {self.type} - {self.amount}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'bank_account_id': self.bank_account_id,
            'date': self.date.isoformat() if self.date else None,
            'type': self.type,
            'amount': float(self.amount) if self.amount else 0,
            'description': self.description,
            'reference': self.reference,
            'category': self.category,
            'is_reconciled': self.is_reconciled,
            'reconciled_at': self.reconciled_at.isoformat() if self.reconciled_at else None,
            'reconciled_by': self.reconciled_by,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class PaymentMethod(db.Model):
    """Formas de Pagamento"""
    __tablename__ = 'payment_methods'
    
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(10), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(20), nullable=False)  # cash, bank_transfer, credit_card, debit_card, check, pix
    requires_bank_account = db.Column(db.Boolean, default=False)
    default_installments = db.Column(db.Integer, default=1)
    is_active = db.Column(db.Boolean, default=True)
    
    def __repr__(self):
        return f'<PaymentMethod {self.code} - {self.name}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'code': self.code,
            'name': self.name,
            'type': self.type,
            'requires_bank_account': self.requires_bank_account,
            'default_installments': self.default_installments,
            'is_active': self.is_active
        }

class Supplier(db.Model):
    """Fornecedores"""
    __tablename__ = 'suppliers'
    
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=False)
    type = db.Column(db.String(20), nullable=False)  # pf, pj
    document = db.Column(db.String(18), nullable=False)  # CPF ou CNPJ
    name = db.Column(db.String(200), nullable=False)
    trade_name = db.Column(db.String(200))
    email = db.Column(db.String(120))
    phone = db.Column(db.String(20))
    
    # Endereço
    address = db.Column(db.String(200))
    city = db.Column(db.String(100))
    state = db.Column(db.String(2))
    zip_code = db.Column(db.String(10))
    
    # Dados bancários
    bank_code = db.Column(db.String(3))
    agency = db.Column(db.String(10))
    account_number = db.Column(db.String(20))
    account_type = db.Column(db.String(20))
    pix_key = db.Column(db.String(100))
    
    # Controle
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relacionamentos
    payables = db.relationship('Payable', backref='supplier', lazy=True)
    
    def __repr__(self):
        return f'<Supplier {self.name}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'company_id': self.company_id,
            'type': self.type,
            'document': self.document,
            'name': self.name,
            'trade_name': self.trade_name,
            'email': self.email,
            'phone': self.phone,
            'address': self.address,
            'city': self.city,
            'state': self.state,
            'zip_code': self.zip_code,
            'bank_code': self.bank_code,
            'agency': self.agency,
            'account_number': self.account_number,
            'account_type': self.account_type,
            'pix_key': self.pix_key,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class Receivable(db.Model):
    """Contas a Receber"""
    __tablename__ = 'receivables'
    
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    invoice_id = db.Column(db.Integer, db.ForeignKey('invoices.id'))
    bank_account_id = db.Column(db.Integer, db.ForeignKey('bank_accounts.id'))
    
    # Dados da conta
    document_number = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=False)
    issue_date = db.Column(db.Date, nullable=False)
    due_date = db.Column(db.Date, nullable=False)
    original_amount = db.Column(db.Numeric(15, 2), nullable=False)
    discount_amount = db.Column(db.Numeric(15, 2), default=0)
    interest_amount = db.Column(db.Numeric(15, 2), default=0)
    fine_amount = db.Column(db.Numeric(15, 2), default=0)
    paid_amount = db.Column(db.Numeric(15, 2), default=0)
    
    # Status
    status = db.Column(db.String(20), default='open')  # open, partial, paid, cancelled, overdue
    payment_date = db.Column(db.Date)
    payment_method_id = db.Column(db.Integer, db.ForeignKey('payment_methods.id'))
    
    # Observações
    notes = db.Column(db.Text)
    
    # Controle
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    payment_method = db.relationship('PaymentMethod')
    created_by_user = db.relationship('User', foreign_keys=[created_by])
    
    def __repr__(self):
        return f'<Receivable {self.document_number}>'
    
    @property
    def balance_amount(self):
        """Saldo a receber"""
        return self.original_amount + self.interest_amount + self.fine_amount - self.discount_amount - self.paid_amount
    
    @property
    def is_overdue(self):
        """Verifica se está vencida"""
        return self.due_date < datetime.now().date() and self.status in ['open', 'partial']
    
    def to_dict(self):
        return {
            'id': self.id,
            'company_id': self.company_id,
            'customer_id': self.customer_id,
            'customer_name': self.customer.name if self.customer else None,
            'invoice_id': self.invoice_id,
            'bank_account_id': self.bank_account_id,
            'document_number': self.document_number,
            'description': self.description,
            'issue_date': self.issue_date.isoformat() if self.issue_date else None,
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'original_amount': float(self.original_amount) if self.original_amount else 0,
            'discount_amount': float(self.discount_amount) if self.discount_amount else 0,
            'interest_amount': float(self.interest_amount) if self.interest_amount else 0,
            'fine_amount': float(self.fine_amount) if self.fine_amount else 0,
            'paid_amount': float(self.paid_amount) if self.paid_amount else 0,
            'balance_amount': float(self.balance_amount),
            'status': self.status,
            'is_overdue': self.is_overdue,
            'payment_date': self.payment_date.isoformat() if self.payment_date else None,
            'payment_method_id': self.payment_method_id,
            'payment_method_name': self.payment_method.name if self.payment_method else None,
            'notes': self.notes,
            'created_by': self.created_by,
            'created_by_name': self.created_by_user.username if self.created_by_user else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class Payable(db.Model):
    """Contas a Pagar"""
    __tablename__ = 'payables'
    
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=False)
    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.id'), nullable=False)
    bank_account_id = db.Column(db.Integer, db.ForeignKey('bank_accounts.id'))
    
    # Dados da conta
    document_number = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=False)
    issue_date = db.Column(db.Date, nullable=False)
    due_date = db.Column(db.Date, nullable=False)
    original_amount = db.Column(db.Numeric(15, 2), nullable=False)
    discount_amount = db.Column(db.Numeric(15, 2), default=0)
    interest_amount = db.Column(db.Numeric(15, 2), default=0)
    fine_amount = db.Column(db.Numeric(15, 2), default=0)
    paid_amount = db.Column(db.Numeric(15, 2), default=0)
    
    # Categoria
    category = db.Column(db.String(50))  # Categoria da despesa
    
    # Status
    status = db.Column(db.String(20), default='open')  # open, partial, paid, cancelled, overdue
    payment_date = db.Column(db.Date)
    payment_method_id = db.Column(db.Integer, db.ForeignKey('payment_methods.id'))
    
    # Observações
    notes = db.Column(db.Text)
    
    # Controle
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    payment_method = db.relationship('PaymentMethod')
    created_by_user = db.relationship('User', foreign_keys=[created_by])
    
    def __repr__(self):
        return f'<Payable {self.document_number}>'
    
    @property
    def balance_amount(self):
        """Saldo a pagar"""
        return self.original_amount + self.interest_amount + self.fine_amount - self.discount_amount - self.paid_amount
    
    @property
    def is_overdue(self):
        """Verifica se está vencida"""
        return self.due_date < datetime.now().date() and self.status in ['open', 'partial']
    
    def to_dict(self):
        return {
            'id': self.id,
            'company_id': self.company_id,
            'supplier_id': self.supplier_id,
            'supplier_name': self.supplier.name if self.supplier else None,
            'bank_account_id': self.bank_account_id,
            'document_number': self.document_number,
            'description': self.description,
            'issue_date': self.issue_date.isoformat() if self.issue_date else None,
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'original_amount': float(self.original_amount) if self.original_amount else 0,
            'discount_amount': float(self.discount_amount) if self.discount_amount else 0,
            'interest_amount': float(self.interest_amount) if self.interest_amount else 0,
            'fine_amount': float(self.fine_amount) if self.fine_amount else 0,
            'paid_amount': float(self.paid_amount) if self.paid_amount else 0,
            'balance_amount': float(self.balance_amount),
            'category': self.category,
            'status': self.status,
            'is_overdue': self.is_overdue,
            'payment_date': self.payment_date.isoformat() if self.payment_date else None,
            'payment_method_id': self.payment_method_id,
            'payment_method_name': self.payment_method.name if self.payment_method else None,
            'notes': self.notes,
            'created_by': self.created_by,
            'created_by_name': self.created_by_user.username if self.created_by_user else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class CashFlow(db.Model):
    """Fluxo de Caixa"""
    __tablename__ = 'cash_flow'
    
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    type = db.Column(db.String(10), nullable=False)  # inflow, outflow
    category = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=False)
    amount = db.Column(db.Numeric(15, 2), nullable=False)
    
    # Referências
    receivable_id = db.Column(db.Integer, db.ForeignKey('receivables.id'))
    payable_id = db.Column(db.Integer, db.ForeignKey('payables.id'))
    bank_account_id = db.Column(db.Integer, db.ForeignKey('bank_accounts.id'))
    
    # Controle
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relacionamentos
    receivable = db.relationship('Receivable')
    payable = db.relationship('Payable')
    created_by_user = db.relationship('User', foreign_keys=[created_by])
    
    def __repr__(self):
        return f'<CashFlow {self.type} - {self.amount}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'company_id': self.company_id,
            'date': self.date.isoformat() if self.date else None,
            'type': self.type,
            'category': self.category,
            'description': self.description,
            'amount': float(self.amount) if self.amount else 0,
            'receivable_id': self.receivable_id,
            'payable_id': self.payable_id,
            'bank_account_id': self.bank_account_id,
            'created_by': self.created_by,
            'created_by_name': self.created_by_user.username if self.created_by_user else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

