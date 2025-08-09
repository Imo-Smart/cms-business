from src.models.user import db
from datetime import datetime, date
from decimal import Decimal
import json

class Employee(db.Model):
    """Modelo avançado para colaboradores"""
    __tablename__ = 'employees'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Dados Pessoais
    full_name = db.Column(db.String(200), nullable=False)
    cpf = db.Column(db.String(14), unique=True, nullable=False)
    rg = db.Column(db.String(20))
    birth_date = db.Column(db.Date)
    gender = db.Column(db.String(1))  # M, F, O
    marital_status = db.Column(db.String(20))
    nationality = db.Column(db.String(50), default='Brasileira')
    
    # Contatos
    email = db.Column(db.String(120))
    phone = db.Column(db.String(20))
    mobile = db.Column(db.String(20))
    emergency_contact = db.Column(db.String(200))
    emergency_phone = db.Column(db.String(20))
    
    # Endereço
    address = db.Column(db.String(200))
    address_number = db.Column(db.String(10))
    complement = db.Column(db.String(100))
    neighborhood = db.Column(db.String(100))
    city = db.Column(db.String(100))
    state = db.Column(db.String(2))
    zip_code = db.Column(db.String(10))
    
    # Dados Trabalhistas
    employee_code = db.Column(db.String(20), unique=True)
    ctps_number = db.Column(db.String(20))
    ctps_series = db.Column(db.String(10))
    pis_pasep = db.Column(db.String(20))
    admission_date = db.Column(db.Date, nullable=False)
    dismissal_date = db.Column(db.Date)
    
    # Cargo e Departamento
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'))
    position = db.Column(db.String(100), nullable=False)
    salary = db.Column(db.Float, nullable=False)
    salary_type = db.Column(db.String(20), default='monthly')  # monthly, hourly, commission
    workload = db.Column(db.Integer, default=44)  # horas semanais
    
    # Status
    status = db.Column(db.String(20), default='active')  # active, inactive, vacation, leave
    contract_type = db.Column(db.String(30), default='clt')  # clt, pj, intern, temporary
    
    # Dados Bancários
    bank_code = db.Column(db.String(10))
    bank_name = db.Column(db.String(100))
    agency = db.Column(db.String(20))
    account = db.Column(db.String(20))
    account_type = db.Column(db.String(20))  # checking, savings, salary
    pix_key = db.Column(db.String(100))
    pix_type = db.Column(db.String(20))  # cpf, email, phone, random
    
    # Metadados
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    # Relacionamentos
    department = db.relationship('Department', backref='employees')
    dependents = db.relationship('Dependent', backref='employee', lazy=True)
    payroll_items = db.relationship('PayrollItem', backref='employee', lazy=True)
    time_records = db.relationship('TimeRecord', backref='employee', lazy=True)
    benefits = db.relationship('EmployeeBenefit', backref='employee', lazy=True)
    trainings = db.relationship('EmployeeTraining', backref='employee', lazy=True)
    evaluations = db.relationship('PerformanceEvaluation', backref='employee', lazy=True)
    
    def __repr__(self):
        return f'<Employee {self.full_name}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'full_name': self.full_name,
            'cpf': self.cpf,
            'employee_code': self.employee_code,
            'position': self.position,
            'department': self.department.name if self.department else None,
            'salary': self.salary,
            'admission_date': self.admission_date.isoformat() if self.admission_date else None,
            'status': self.status,
            'email': self.email,
            'phone': self.phone
        }

class Dependent(db.Model):
    """Dependentes dos colaboradores"""
    __tablename__ = 'dependents'
    
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    cpf = db.Column(db.String(14))
    birth_date = db.Column(db.Date)
    relationship = db.Column(db.String(50))  # filho, cônjuge, pai, mãe, etc.
    is_ir_dependent = db.Column(db.Boolean, default=True)  # dependente para IR
    is_sf_dependent = db.Column(db.Boolean, default=True)  # dependente para salário família
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class PayrollPeriod(db.Model):
    """Períodos de folha de pagamento"""
    __tablename__ = 'payroll_periods'
    
    id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.Integer, nullable=False)
    month = db.Column(db.Integer, nullable=False)
    reference = db.Column(db.String(7), nullable=False)  # YYYY-MM
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    payment_date = db.Column(db.Date)
    status = db.Column(db.String(20), default='open')  # open, calculated, paid, closed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relacionamentos
    payroll_items = db.relationship('PayrollItem', backref='period', lazy=True)

class PayrollItem(db.Model):
    """Itens da folha de pagamento"""
    __tablename__ = 'payroll_items'
    
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    period_id = db.Column(db.Integer, db.ForeignKey('payroll_periods.id'), nullable=False)
    
    # Proventos
    base_salary = db.Column(db.Float, default=0)
    overtime_hours = db.Column(db.Float, default=0)
    overtime_value = db.Column(db.Float, default=0)
    night_shift_hours = db.Column(db.Float, default=0)
    night_shift_value = db.Column(db.Float, default=0)
    commission = db.Column(db.Float, default=0)
    bonus = db.Column(db.Float, default=0)
    vacation_pay = db.Column(db.Float, default=0)
    thirteenth_salary = db.Column(db.Float, default=0)
    other_earnings = db.Column(db.Float, default=0)
    
    # Descontos
    inss = db.Column(db.Float, default=0)
    irrf = db.Column(db.Float, default=0)
    fgts = db.Column(db.Float, default=0)
    transport_voucher = db.Column(db.Float, default=0)
    meal_voucher = db.Column(db.Float, default=0)
    health_insurance = db.Column(db.Float, default=0)
    dental_insurance = db.Column(db.Float, default=0)
    life_insurance = db.Column(db.Float, default=0)
    union_fee = db.Column(db.Float, default=0)
    advance_payment = db.Column(db.Float, default=0)
    other_deductions = db.Column(db.Float, default=0)
    
    # Totais
    gross_salary = db.Column(db.Float, default=0)
    total_deductions = db.Column(db.Float, default=0)
    net_salary = db.Column(db.Float, default=0)
    
    # Metadados
    calculated_at = db.Column(db.DateTime)
    paid_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class TimeRecord(db.Model):
    """Registros de ponto"""
    __tablename__ = 'time_records'
    
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    record_date = db.Column(db.Date, nullable=False)
    
    # Horários
    entry_time_1 = db.Column(db.Time)  # Entrada manhã
    exit_time_1 = db.Column(db.Time)   # Saída almoço
    entry_time_2 = db.Column(db.Time)  # Entrada tarde
    exit_time_2 = db.Column(db.Time)   # Saída final
    
    # Cálculos
    worked_hours = db.Column(db.Float, default=0)
    overtime_hours = db.Column(db.Float, default=0)
    night_shift_hours = db.Column(db.Float, default=0)
    
    # Status e observações
    status = db.Column(db.String(20), default='normal')  # normal, absence, vacation, leave, holiday
    absence_type = db.Column(db.String(50))  # medical, personal, justified, unjustified
    observations = db.Column(db.Text)
    
    # Localização (para controle remoto)
    location_lat = db.Column(db.Float)
    location_lng = db.Column(db.Float)
    location_address = db.Column(db.String(200))
    
    # Metadados
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Benefit(db.Model):
    """Catálogo de benefícios"""
    __tablename__ = 'benefits'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String(50))  # transport, meal, health, education, etc.
    value_type = db.Column(db.String(20), default='fixed')  # fixed, percentage, variable
    default_value = db.Column(db.Float, default=0)
    is_taxable = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relacionamentos
    employee_benefits = db.relationship('EmployeeBenefit', backref='benefit', lazy=True)

class EmployeeBenefit(db.Model):
    """Benefícios dos colaboradores"""
    __tablename__ = 'employee_benefits'
    
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    benefit_id = db.Column(db.Integer, db.ForeignKey('benefits.id'), nullable=False)
    value = db.Column(db.Float, nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Training(db.Model):
    """Catálogo de treinamentos"""
    __tablename__ = 'trainings'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String(50))
    duration_hours = db.Column(db.Integer)
    instructor = db.Column(db.String(100))
    content_url = db.Column(db.String(500))  # Link para vídeos, PDFs, etc.
    certificate_template = db.Column(db.String(500))
    is_mandatory = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relacionamentos
    employee_trainings = db.relationship('EmployeeTraining', backref='training', lazy=True)

class EmployeeTraining(db.Model):
    """Treinamentos dos colaboradores"""
    __tablename__ = 'employee_trainings'
    
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    training_id = db.Column(db.Integer, db.ForeignKey('trainings.id'), nullable=False)
    start_date = db.Column(db.Date)
    completion_date = db.Column(db.Date)
    score = db.Column(db.Float)  # Nota obtida
    status = db.Column(db.String(20), default='enrolled')  # enrolled, in_progress, completed, failed
    certificate_url = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class PerformanceEvaluation(db.Model):
    """Avaliações de desempenho"""
    __tablename__ = 'performance_evaluations'
    
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    evaluator_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    period_start = db.Column(db.Date, nullable=False)
    period_end = db.Column(db.Date, nullable=False)
    
    # Critérios de avaliação (1-5)
    productivity = db.Column(db.Integer)
    quality = db.Column(db.Integer)
    teamwork = db.Column(db.Integer)
    communication = db.Column(db.Integer)
    leadership = db.Column(db.Integer)
    innovation = db.Column(db.Integer)
    punctuality = db.Column(db.Integer)
    
    # Comentários
    strengths = db.Column(db.Text)
    improvement_areas = db.Column(db.Text)
    goals = db.Column(db.Text)
    general_comments = db.Column(db.Text)
    
    # Resultado
    overall_score = db.Column(db.Float)
    status = db.Column(db.String(20), default='draft')  # draft, completed, approved
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relacionamentos
    evaluator = db.relationship('User', backref='evaluations_given')

class InternalCommunication(db.Model):
    """Comunicação interna"""
    __tablename__ = 'internal_communications'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    type = db.Column(db.String(50), default='announcement')  # announcement, policy, news, alert
    priority = db.Column(db.String(20), default='normal')  # low, normal, high, urgent
    
    # Destinatários
    target_type = db.Column(db.String(20), default='all')  # all, department, specific
    target_departments = db.Column(db.Text)  # JSON com IDs dos departamentos
    target_employees = db.Column(db.Text)    # JSON com IDs dos funcionários
    
    # Configurações
    requires_confirmation = db.Column(db.Boolean, default=False)
    send_email = db.Column(db.Boolean, default=True)
    send_push = db.Column(db.Boolean, default=True)
    
    # Status
    status = db.Column(db.String(20), default='draft')  # draft, published, archived
    published_at = db.Column(db.DateTime)
    expires_at = db.Column(db.DateTime)
    
    # Metadados
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relacionamentos
    author = db.relationship('User', backref='communications')
    confirmations = db.relationship('CommunicationConfirmation', backref='communication', lazy=True)

class CommunicationConfirmation(db.Model):
    """Confirmações de leitura de comunicados"""
    __tablename__ = 'communication_confirmations'
    
    id = db.Column(db.Integer, primary_key=True)
    communication_id = db.Column(db.Integer, db.ForeignKey('internal_communications.id'), nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    confirmed_at = db.Column(db.DateTime, default=datetime.utcnow)
    ip_address = db.Column(db.String(45))
    user_agent = db.Column(db.String(500))

class ESocialEvent(db.Model):
    """Eventos do eSocial"""
    __tablename__ = 'esocial_events'
    
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'))
    event_type = db.Column(db.String(10), nullable=False)  # S-2200, S-2300, etc.
    event_data = db.Column(db.Text, nullable=False)  # JSON com dados do evento
    receipt_number = db.Column(db.String(50))
    protocol_number = db.Column(db.String(50))
    status = db.Column(db.String(20), default='pending')  # pending, sent, accepted, rejected
    error_message = db.Column(db.Text)
    sent_at = db.Column(db.DateTime)
    processed_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relacionamentos
    employee_ref = db.relationship('Employee', backref='esocial_events')

class PaymentBatch(db.Model):
    """Lotes de pagamento"""
    __tablename__ = 'payment_batches'
    
    id = db.Column(db.Integer, primary_key=True)
    period_id = db.Column(db.Integer, db.ForeignKey('payroll_periods.id'), nullable=False)
    batch_number = db.Column(db.String(20), nullable=False)
    payment_method = db.Column(db.String(20), nullable=False)  # pix, ted, doc
    total_amount = db.Column(db.Float, nullable=False)
    employee_count = db.Column(db.Integer, nullable=False)
    
    # Dados bancários
    bank_code = db.Column(db.String(10))
    bank_name = db.Column(db.String(100))
    agency = db.Column(db.String(20))
    account = db.Column(db.String(20))
    
    # Status
    status = db.Column(db.String(20), default='created')  # created, sent, processed, completed, failed
    file_path = db.Column(db.String(500))  # Caminho do arquivo CNAB/Pix
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    processed_at = db.Column(db.DateTime)
    
    # Relacionamentos
    period = db.relationship('PayrollPeriod', backref='payment_batches')
    payments = db.relationship('Payment', backref='batch', lazy=True)

class Payment(db.Model):
    """Pagamentos individuais"""
    __tablename__ = 'payments'
    
    id = db.Column(db.Integer, primary_key=True)
    batch_id = db.Column(db.Integer, db.ForeignKey('payment_batches.id'), nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    payment_method = db.Column(db.String(20), nullable=False)
    
    # Dados do pagamento
    pix_key = db.Column(db.String(100))
    bank_code = db.Column(db.String(10))
    agency = db.Column(db.String(20))
    account = db.Column(db.String(20))
    
    # Status
    status = db.Column(db.String(20), default='pending')  # pending, sent, completed, failed
    transaction_id = db.Column(db.String(100))
    error_message = db.Column(db.Text)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    processed_at = db.Column(db.DateTime)
    
    # Relacionamentos
    employee_ref = db.relationship('Employee', backref='payments')

