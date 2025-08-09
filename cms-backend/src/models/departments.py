from src.models.user import db
from datetime import datetime
from decimal import Decimal

class Department(db.Model):
    """Modelo para departamentos da construtora"""
    __tablename__ = 'departments'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    code = db.Column(db.String(10), unique=True, nullable=False)
    description = db.Column(db.Text)
    parent_id = db.Column(db.Integer, db.ForeignKey('departments.id'), nullable=True)
    level = db.Column(db.Integer, default=1)  # Nível hierárquico
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relacionamentos
    parent = db.relationship('Department', remote_side=[id], backref='children')
    users = db.relationship('User', backref='department', lazy=True)
    
    def __repr__(self):
        return f'<Department {self.name}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'code': self.code,
            'description': self.description,
            'parent_id': self.parent_id,
            'level': self.level,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'children': [child.to_dict() for child in self.children] if self.children else []
        }

class Permission(db.Model):
    """Modelo para permissões do sistema"""
    __tablename__ = 'permissions'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    code = db.Column(db.String(50), nullable=False, unique=True)
    description = db.Column(db.Text)
    module = db.Column(db.String(50), nullable=False)  # Módulo do sistema
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Permission {self.name}>'

class RolePermission(db.Model):
    """Tabela de associação entre roles e permissões"""
    __tablename__ = 'role_permissions'
    
    id = db.Column(db.Integer, primary_key=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)
    permission_id = db.Column(db.Integer, db.ForeignKey('permissions.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relacionamentos
    role = db.relationship('Role', backref='role_permissions')
    permission = db.relationship('Permission', backref='role_permissions')

class DepartmentModule(db.Model):
    """Módulos ativos por departamento"""
    __tablename__ = 'department_modules'
    
    id = db.Column(db.Integer, primary_key=True)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'), nullable=False)
    module_code = db.Column(db.String(50), nullable=False)
    module_name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, default=30.00)  # R$ 30 por módulo
    is_active = db.Column(db.Boolean, default=True)
    activated_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relacionamentos
    department = db.relationship('Department', backref='modules')
    
    def __repr__(self):
        return f'<DepartmentModule {self.module_name}>'

class WorkflowStep(db.Model):
    """Etapas de workflow entre departamentos"""
    __tablename__ = 'workflow_steps'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    from_department_id = db.Column(db.Integer, db.ForeignKey('departments.id'), nullable=False)
    to_department_id = db.Column(db.Integer, db.ForeignKey('departments.id'), nullable=False)
    order = db.Column(db.Integer, default=1)
    is_required = db.Column(db.Boolean, default=True)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relacionamentos
    from_department = db.relationship('Department', foreign_keys=[from_department_id], backref='outgoing_workflows')
    to_department = db.relationship('Department', foreign_keys=[to_department_id], backref='incoming_workflows')
    
    def __repr__(self):
        return f'<WorkflowStep {self.name}>'

class DepartmentMetric(db.Model):
    """Métricas específicas por departamento"""
    __tablename__ = 'department_metrics'
    
    id = db.Column(db.Integer, primary_key=True)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'), nullable=False)
    metric_name = db.Column(db.String(100), nullable=False)
    metric_value = db.Column(db.Float)
    metric_type = db.Column(db.String(20), default='number')  # number, percentage, currency
    period = db.Column(db.String(20), default='monthly')  # daily, weekly, monthly, yearly
    date_recorded = db.Column(db.Date, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relacionamentos
    department = db.relationship('Department', backref='metrics')
    
    def __repr__(self):
        return f'<DepartmentMetric {self.metric_name}>'

