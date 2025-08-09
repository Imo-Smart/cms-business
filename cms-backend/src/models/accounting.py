from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from decimal import Decimal
from src.models.user import db

class Company(db.Model):
    """Modelo para empresas/filiais"""
    __tablename__ = 'companies'
    
    id = db.Column(db.Integer, primary_key=True)
    cnpj = db.Column(db.String(18), unique=True, nullable=False)
    name = db.Column(db.String(200), nullable=False)
    trade_name = db.Column(db.String(200))
    email = db.Column(db.String(120))
    phone = db.Column(db.String(20))
    address = db.Column(db.Text)
    city = db.Column(db.String(100))
    state = db.Column(db.String(2))
    zip_code = db.Column(db.String(10))
    tax_regime = db.Column(db.String(20))  # simples_nacional, lucro_presumido, lucro_real
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relacionamentos
    accounts = db.relationship('Account', backref='company', lazy=True)
    journal_entries = db.relationship('JournalEntry', backref='company', lazy=True)
    
    def __repr__(self):
        return f'<Company {self.name}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'cnpj': self.cnpj,
            'name': self.name,
            'trade_name': self.trade_name,
            'email': self.email,
            'phone': self.phone,
            'address': self.address,
            'city': self.city,
            'state': self.state,
            'zip_code': self.zip_code,
            'tax_regime': self.tax_regime,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class AccountType(db.Model):
    """Tipos de conta contábil"""
    __tablename__ = 'account_types'
    
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(10), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    nature = db.Column(db.String(20), nullable=False)  # debit, credit
    category = db.Column(db.String(50), nullable=False)  # ativo, passivo, patrimonio_liquido, receita, despesa
    
    # Relacionamentos
    accounts = db.relationship('Account', backref='account_type', lazy=True)
    
    def __repr__(self):
        return f'<AccountType {self.code} - {self.name}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'code': self.code,
            'name': self.name,
            'nature': self.nature,
            'category': self.category
        }

class Account(db.Model):
    """Plano de Contas"""
    __tablename__ = 'accounts'
    
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=False)
    code = db.Column(db.String(20), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    account_type_id = db.Column(db.Integer, db.ForeignKey('account_types.id'), nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('accounts.id'))
    level = db.Column(db.Integer, default=1)
    is_analytical = db.Column(db.Boolean, default=True)  # True = analítica, False = sintética
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relacionamentos
    children = db.relationship('Account', backref=db.backref('parent', remote_side=[id]))
    journal_entry_lines = db.relationship('JournalEntryLine', backref='account', lazy=True)
    
    def __repr__(self):
        return f'<Account {self.code} - {self.name}>'
    
    @property
    def full_code(self):
        """Retorna o código completo da conta"""
        if self.parent:
            return f"{self.parent.full_code}.{self.code}"
        return self.code
    
    def get_balance(self, start_date=None, end_date=None):
        """Calcula o saldo da conta"""
        query = self.journal_entry_lines
        
        if start_date:
            query = query.join(JournalEntry).filter(JournalEntry.date >= start_date)
        if end_date:
            query = query.join(JournalEntry).filter(JournalEntry.date <= end_date)
        
        debit_total = sum([line.debit_amount for line in query if line.debit_amount])
        credit_total = sum([line.credit_amount for line in query if line.credit_amount])
        
        # Natureza da conta determina o saldo
        if self.account_type.nature == 'debit':
            return debit_total - credit_total
        else:
            return credit_total - debit_total
    
    def to_dict(self):
        return {
            'id': self.id,
            'company_id': self.company_id,
            'code': self.code,
            'name': self.name,
            'full_code': self.full_code,
            'account_type_id': self.account_type_id,
            'account_type_name': self.account_type.name if self.account_type else None,
            'parent_id': self.parent_id,
            'level': self.level,
            'is_analytical': self.is_analytical,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class CostCenter(db.Model):
    """Centros de Custo"""
    __tablename__ = 'cost_centers'
    
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=False)
    code = db.Column(db.String(20), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    parent_id = db.Column(db.Integer, db.ForeignKey('cost_centers.id'))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relacionamentos
    children = db.relationship('CostCenter', backref=db.backref('parent', remote_side=[id]))
    journal_entry_lines = db.relationship('JournalEntryLine', backref='cost_center', lazy=True)
    
    def __repr__(self):
        return f'<CostCenter {self.code} - {self.name}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'company_id': self.company_id,
            'code': self.code,
            'name': self.name,
            'description': self.description,
            'parent_id': self.parent_id,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class JournalEntry(db.Model):
    """Lançamentos Contábeis"""
    __tablename__ = 'journal_entries'
    
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=False)
    entry_number = db.Column(db.String(20), nullable=False)
    date = db.Column(db.Date, nullable=False)
    description = db.Column(db.Text, nullable=False)
    reference = db.Column(db.String(100))  # Documento de origem
    total_amount = db.Column(db.Numeric(15, 2), nullable=False)
    status = db.Column(db.String(20), default='draft')  # draft, posted, cancelled
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    posted_at = db.Column(db.DateTime)
    
    # Relacionamentos
    lines = db.relationship('JournalEntryLine', backref='journal_entry', lazy=True, cascade='all, delete-orphan')
    created_by_user = db.relationship('User', foreign_keys=[created_by])
    
    def __repr__(self):
        return f'<JournalEntry {self.entry_number}>'
    
    def validate_entry(self):
        """Valida se o lançamento está balanceado"""
        total_debit = sum([line.debit_amount or 0 for line in self.lines])
        total_credit = sum([line.credit_amount or 0 for line in self.lines])
        return total_debit == total_credit
    
    def post_entry(self):
        """Efetiva o lançamento"""
        if self.validate_entry() and self.status == 'draft':
            self.status = 'posted'
            self.posted_at = datetime.utcnow()
            return True
        return False
    
    def to_dict(self):
        return {
            'id': self.id,
            'company_id': self.company_id,
            'entry_number': self.entry_number,
            'date': self.date.isoformat() if self.date else None,
            'description': self.description,
            'reference': self.reference,
            'total_amount': float(self.total_amount) if self.total_amount else 0,
            'status': self.status,
            'created_by': self.created_by,
            'created_by_name': self.created_by_user.username if self.created_by_user else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'posted_at': self.posted_at.isoformat() if self.posted_at else None,
            'lines': [line.to_dict() for line in self.lines]
        }

class JournalEntryLine(db.Model):
    """Linhas dos Lançamentos Contábeis"""
    __tablename__ = 'journal_entry_lines'
    
    id = db.Column(db.Integer, primary_key=True)
    journal_entry_id = db.Column(db.Integer, db.ForeignKey('journal_entries.id'), nullable=False)
    account_id = db.Column(db.Integer, db.ForeignKey('accounts.id'), nullable=False)
    cost_center_id = db.Column(db.Integer, db.ForeignKey('cost_centers.id'))
    description = db.Column(db.Text)
    debit_amount = db.Column(db.Numeric(15, 2))
    credit_amount = db.Column(db.Numeric(15, 2))
    
    def __repr__(self):
        return f'<JournalEntryLine {self.id}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'journal_entry_id': self.journal_entry_id,
            'account_id': self.account_id,
            'account_code': self.account.code if self.account else None,
            'account_name': self.account.name if self.account else None,
            'cost_center_id': self.cost_center_id,
            'cost_center_name': self.cost_center.name if self.cost_center else None,
            'description': self.description,
            'debit_amount': float(self.debit_amount) if self.debit_amount else 0,
            'credit_amount': float(self.credit_amount) if self.credit_amount else 0
        }

class FiscalPeriod(db.Model):
    """Períodos Fiscais"""
    __tablename__ = 'fiscal_periods'
    
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    month = db.Column(db.Integer, nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    is_closed = db.Column(db.Boolean, default=False)
    closed_at = db.Column(db.DateTime)
    closed_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    def __repr__(self):
        return f'<FiscalPeriod {self.year}/{self.month:02d}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'company_id': self.company_id,
            'year': self.year,
            'month': self.month,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'is_closed': self.is_closed,
            'closed_at': self.closed_at.isoformat() if self.closed_at else None,
            'closed_by': self.closed_by
        }

