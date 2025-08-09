from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from decimal import Decimal
from src.models.user import db

class TaxType(db.Model):
    """Tipos de Impostos"""
    __tablename__ = 'tax_types'
    
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(10), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    calculation_base = db.Column(db.String(50))  # valor_produto, valor_total, etc
    is_federal = db.Column(db.Boolean, default=True)
    is_active = db.Column(db.Boolean, default=True)
    
    # Relacionamentos
    tax_rates = db.relationship('TaxRate', backref='tax_type', lazy=True)
    
    def __repr__(self):
        return f'<TaxType {self.code} - {self.name}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'code': self.code,
            'name': self.name,
            'description': self.description,
            'calculation_base': self.calculation_base,
            'is_federal': self.is_federal,
            'is_active': self.is_active
        }

class TaxRate(db.Model):
    """Alíquotas de Impostos"""
    __tablename__ = 'tax_rates'
    
    id = db.Column(db.Integer, primary_key=True)
    tax_type_id = db.Column(db.Integer, db.ForeignKey('tax_types.id'), nullable=False)
    state = db.Column(db.String(2))  # Para ICMS estadual
    rate = db.Column(db.Numeric(5, 2), nullable=False)  # Alíquota em %
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date)
    is_active = db.Column(db.Boolean, default=True)
    
    def __repr__(self):
        return f'<TaxRate {self.tax_type.code} - {self.rate}%>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'tax_type_id': self.tax_type_id,
            'tax_type_code': self.tax_type.code if self.tax_type else None,
            'state': self.state,
            'rate': float(self.rate) if self.rate else 0,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'is_active': self.is_active
        }

class Customer(db.Model):
    """Clientes"""
    __tablename__ = 'customers'
    
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=False)
    type = db.Column(db.String(20), nullable=False)  # pf, pj
    document = db.Column(db.String(18), nullable=False)  # CPF ou CNPJ
    name = db.Column(db.String(200), nullable=False)
    trade_name = db.Column(db.String(200))
    email = db.Column(db.String(120))
    phone = db.Column(db.String(20))
    mobile = db.Column(db.String(20))
    
    # Endereço
    address = db.Column(db.String(200))
    number = db.Column(db.String(20))
    complement = db.Column(db.String(100))
    neighborhood = db.Column(db.String(100))
    city = db.Column(db.String(100))
    state = db.Column(db.String(2))
    zip_code = db.Column(db.String(10))
    
    # Dados fiscais
    state_registration = db.Column(db.String(20))
    municipal_registration = db.Column(db.String(20))
    tax_regime = db.Column(db.String(20))
    
    # Controle
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    invoices = db.relationship('Invoice', backref='customer', lazy=True)
    
    def __repr__(self):
        return f'<Customer {self.name}>'
    
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
            'mobile': self.mobile,
            'address': self.address,
            'number': self.number,
            'complement': self.complement,
            'neighborhood': self.neighborhood,
            'city': self.city,
            'state': self.state,
            'zip_code': self.zip_code,
            'state_registration': self.state_registration,
            'municipal_registration': self.municipal_registration,
            'tax_regime': self.tax_regime,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class Product(db.Model):
    """Produtos/Serviços"""
    __tablename__ = 'products'
    
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=False)
    code = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    type = db.Column(db.String(20), default='product')  # product, service
    unit = db.Column(db.String(10), default='UN')
    
    # Preços
    cost_price = db.Column(db.Numeric(15, 2))
    sale_price = db.Column(db.Numeric(15, 2))
    
    # Dados fiscais
    ncm = db.Column(db.String(10))  # Nomenclatura Comum do Mercosul
    cest = db.Column(db.String(10))  # Código Especificador da Substituição Tributária
    cfop_internal = db.Column(db.String(4))  # CFOP para vendas internas
    cfop_external = db.Column(db.String(4))  # CFOP para vendas externas
    
    # Controle de estoque
    manage_stock = db.Column(db.Boolean, default=True)
    current_stock = db.Column(db.Numeric(15, 3), default=0)
    minimum_stock = db.Column(db.Numeric(15, 3), default=0)
    
    # Controle
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    invoice_items = db.relationship('InvoiceItem', backref='product', lazy=True)
    
    def __repr__(self):
        return f'<Product {self.code} - {self.name}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'company_id': self.company_id,
            'code': self.code,
            'name': self.name,
            'description': self.description,
            'type': self.type,
            'unit': self.unit,
            'cost_price': float(self.cost_price) if self.cost_price else 0,
            'sale_price': float(self.sale_price) if self.sale_price else 0,
            'ncm': self.ncm,
            'cest': self.cest,
            'cfop_internal': self.cfop_internal,
            'cfop_external': self.cfop_external,
            'manage_stock': self.manage_stock,
            'current_stock': float(self.current_stock) if self.current_stock else 0,
            'minimum_stock': float(self.minimum_stock) if self.minimum_stock else 0,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class Invoice(db.Model):
    """Notas Fiscais"""
    __tablename__ = 'invoices'
    
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    
    # Identificação da NF
    number = db.Column(db.Integer, nullable=False)
    series = db.Column(db.String(3), default='1')
    type = db.Column(db.String(10), default='nfe')  # nfe, nfce, nfse
    model = db.Column(db.String(2), default='55')  # 55=NFe, 65=NFCe
    
    # Datas
    issue_date = db.Column(db.DateTime, nullable=False)
    due_date = db.Column(db.Date)
    
    # Valores
    products_value = db.Column(db.Numeric(15, 2), default=0)
    services_value = db.Column(db.Numeric(15, 2), default=0)
    discount_value = db.Column(db.Numeric(15, 2), default=0)
    freight_value = db.Column(db.Numeric(15, 2), default=0)
    insurance_value = db.Column(db.Numeric(15, 2), default=0)
    other_expenses = db.Column(db.Numeric(15, 2), default=0)
    total_value = db.Column(db.Numeric(15, 2), nullable=False)
    
    # Impostos
    icms_base = db.Column(db.Numeric(15, 2), default=0)
    icms_value = db.Column(db.Numeric(15, 2), default=0)
    ipi_value = db.Column(db.Numeric(15, 2), default=0)
    pis_value = db.Column(db.Numeric(15, 2), default=0)
    cofins_value = db.Column(db.Numeric(15, 2), default=0)
    iss_value = db.Column(db.Numeric(15, 2), default=0)
    
    # Status e controle
    status = db.Column(db.String(20), default='draft')  # draft, issued, cancelled, denied
    xml_file = db.Column(db.String(255))
    pdf_file = db.Column(db.String(255))
    access_key = db.Column(db.String(44))  # Chave de acesso da NFe
    authorization_protocol = db.Column(db.String(20))
    
    # Observações
    additional_info = db.Column(db.Text)
    internal_notes = db.Column(db.Text)
    
    # Controle
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    items = db.relationship('InvoiceItem', backref='invoice', lazy=True, cascade='all, delete-orphan')
    tax_calculations = db.relationship('InvoiceTax', backref='invoice', lazy=True, cascade='all, delete-orphan')
    created_by_user = db.relationship('User', foreign_keys=[created_by])
    
    def __repr__(self):
        return f'<Invoice {self.number}/{self.series}>'
    
    def calculate_totals(self):
        """Calcula os totais da nota fiscal"""
        self.products_value = sum([item.total_value for item in self.items if item.product.type == 'product'])
        self.services_value = sum([item.total_value for item in self.items if item.product.type == 'service'])
        self.total_value = self.products_value + self.services_value + self.freight_value + self.insurance_value + self.other_expenses - self.discount_value
    
    def to_dict(self):
        return {
            'id': self.id,
            'company_id': self.company_id,
            'customer_id': self.customer_id,
            'customer_name': self.customer.name if self.customer else None,
            'number': self.number,
            'series': self.series,
            'type': self.type,
            'model': self.model,
            'issue_date': self.issue_date.isoformat() if self.issue_date else None,
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'products_value': float(self.products_value) if self.products_value else 0,
            'services_value': float(self.services_value) if self.services_value else 0,
            'discount_value': float(self.discount_value) if self.discount_value else 0,
            'freight_value': float(self.freight_value) if self.freight_value else 0,
            'insurance_value': float(self.insurance_value) if self.insurance_value else 0,
            'other_expenses': float(self.other_expenses) if self.other_expenses else 0,
            'total_value': float(self.total_value) if self.total_value else 0,
            'icms_base': float(self.icms_base) if self.icms_base else 0,
            'icms_value': float(self.icms_value) if self.icms_value else 0,
            'ipi_value': float(self.ipi_value) if self.ipi_value else 0,
            'pis_value': float(self.pis_value) if self.pis_value else 0,
            'cofins_value': float(self.cofins_value) if self.cofins_value else 0,
            'iss_value': float(self.iss_value) if self.iss_value else 0,
            'status': self.status,
            'access_key': self.access_key,
            'authorization_protocol': self.authorization_protocol,
            'additional_info': self.additional_info,
            'internal_notes': self.internal_notes,
            'created_by': self.created_by,
            'created_by_name': self.created_by_user.username if self.created_by_user else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'items': [item.to_dict() for item in self.items]
        }

class InvoiceItem(db.Model):
    """Itens da Nota Fiscal"""
    __tablename__ = 'invoice_items'
    
    id = db.Column(db.Integer, primary_key=True)
    invoice_id = db.Column(db.Integer, db.ForeignKey('invoices.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    
    # Dados do item
    sequence = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Numeric(15, 3), nullable=False)
    unit_price = db.Column(db.Numeric(15, 2), nullable=False)
    total_value = db.Column(db.Numeric(15, 2), nullable=False)
    discount_value = db.Column(db.Numeric(15, 2), default=0)
    
    # Dados fiscais
    cfop = db.Column(db.String(4), nullable=False)
    ncm = db.Column(db.String(10))
    cest = db.Column(db.String(10))
    
    # Impostos do item
    icms_origin = db.Column(db.String(1), default='0')
    icms_cst = db.Column(db.String(3))
    icms_base = db.Column(db.Numeric(15, 2), default=0)
    icms_rate = db.Column(db.Numeric(5, 2), default=0)
    icms_value = db.Column(db.Numeric(15, 2), default=0)
    
    ipi_cst = db.Column(db.String(2))
    ipi_rate = db.Column(db.Numeric(5, 2), default=0)
    ipi_value = db.Column(db.Numeric(15, 2), default=0)
    
    pis_cst = db.Column(db.String(2))
    pis_rate = db.Column(db.Numeric(5, 2), default=0)
    pis_value = db.Column(db.Numeric(15, 2), default=0)
    
    cofins_cst = db.Column(db.String(2))
    cofins_rate = db.Column(db.Numeric(5, 2), default=0)
    cofins_value = db.Column(db.Numeric(15, 2), default=0)
    
    def __repr__(self):
        return f'<InvoiceItem {self.sequence} - {self.product.name}>'
    
    def calculate_taxes(self):
        """Calcula os impostos do item"""
        # Aqui seria implementada a lógica de cálculo de impostos
        # baseada no regime tributário, CFOP, etc.
        pass
    
    def to_dict(self):
        return {
            'id': self.id,
            'invoice_id': self.invoice_id,
            'product_id': self.product_id,
            'product_code': self.product.code if self.product else None,
            'product_name': self.product.name if self.product else None,
            'sequence': self.sequence,
            'quantity': float(self.quantity) if self.quantity else 0,
            'unit_price': float(self.unit_price) if self.unit_price else 0,
            'total_value': float(self.total_value) if self.total_value else 0,
            'discount_value': float(self.discount_value) if self.discount_value else 0,
            'cfop': self.cfop,
            'ncm': self.ncm,
            'cest': self.cest,
            'icms_origin': self.icms_origin,
            'icms_cst': self.icms_cst,
            'icms_base': float(self.icms_base) if self.icms_base else 0,
            'icms_rate': float(self.icms_rate) if self.icms_rate else 0,
            'icms_value': float(self.icms_value) if self.icms_value else 0,
            'ipi_cst': self.ipi_cst,
            'ipi_rate': float(self.ipi_rate) if self.ipi_rate else 0,
            'ipi_value': float(self.ipi_value) if self.ipi_value else 0,
            'pis_cst': self.pis_cst,
            'pis_rate': float(self.pis_rate) if self.pis_rate else 0,
            'pis_value': float(self.pis_value) if self.pis_value else 0,
            'cofins_cst': self.cofins_cst,
            'cofins_rate': float(self.cofins_rate) if self.cofins_rate else 0,
            'cofins_value': float(self.cofins_value) if self.cofins_value else 0
        }

class InvoiceTax(db.Model):
    """Impostos Calculados da Nota Fiscal"""
    __tablename__ = 'invoice_taxes'
    
    id = db.Column(db.Integer, primary_key=True)
    invoice_id = db.Column(db.Integer, db.ForeignKey('invoices.id'), nullable=False)
    tax_type_id = db.Column(db.Integer, db.ForeignKey('tax_types.id'), nullable=False)
    base_amount = db.Column(db.Numeric(15, 2), nullable=False)
    rate = db.Column(db.Numeric(5, 2), nullable=False)
    tax_amount = db.Column(db.Numeric(15, 2), nullable=False)
    
    def __repr__(self):
        return f'<InvoiceTax {self.tax_type.code} - {self.tax_amount}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'invoice_id': self.invoice_id,
            'tax_type_id': self.tax_type_id,
            'tax_type_code': self.tax_type.code if self.tax_type else None,
            'base_amount': float(self.base_amount) if self.base_amount else 0,
            'rate': float(self.rate) if self.rate else 0,
            'tax_amount': float(self.tax_amount) if self.tax_amount else 0
        }

