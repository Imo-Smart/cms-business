from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.models.user import db
from src.models.hr_advanced import (
    Employee, Dependent, PayrollPeriod, PayrollItem, TimeRecord,
    Benefit, EmployeeBenefit, Training, EmployeeTraining,
    PerformanceEvaluation, InternalCommunication, CommunicationConfirmation,
    ESocialEvent, PaymentBatch, Payment
)
from datetime import datetime, date, timedelta
import json
import calendar

hr_bp = Blueprint('hr_advanced', __name__)

# ==================== GESTÃO DE COLABORADORES ====================

@hr_bp.route('/employees', methods=['GET'])
@jwt_required()
def get_employees():
    """Listar todos os colaboradores"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        search = request.args.get('search', '')
        department_id = request.args.get('department_id', type=int)
        status = request.args.get('status', 'active')
        
        query = Employee.query
        
        if search:
            query = query.filter(Employee.full_name.contains(search))
        if department_id:
            query = query.filter(Employee.department_id == department_id)
        if status:
            query = query.filter(Employee.status == status)
            
        employees = query.paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return jsonify({
            'success': True,
            'employees': [emp.to_dict() for emp in employees.items],
            'total': employees.total,
            'pages': employees.pages,
            'current_page': page
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@hr_bp.route('/employees', methods=['POST'])
@jwt_required()
def create_employee():
    """Criar novo colaborador"""
    try:
        data = request.get_json()
        
        # Verificar se CPF já existe
        existing = Employee.query.filter_by(cpf=data.get('cpf')).first()
        if existing:
            return jsonify({'success': False, 'message': 'CPF já cadastrado'}), 400
        
        # Gerar código do funcionário se não fornecido
        if not data.get('employee_code'):
            last_employee = Employee.query.order_by(Employee.id.desc()).first()
            next_code = (last_employee.id + 1) if last_employee else 1
            data['employee_code'] = f"EMP{next_code:04d}"
        
        employee = Employee(
            full_name=data.get('full_name'),
            cpf=data.get('cpf'),
            rg=data.get('rg'),
            birth_date=datetime.strptime(data.get('birth_date'), '%Y-%m-%d').date() if data.get('birth_date') else None,
            gender=data.get('gender'),
            marital_status=data.get('marital_status'),
            email=data.get('email'),
            phone=data.get('phone'),
            mobile=data.get('mobile'),
            emergency_contact=data.get('emergency_contact'),
            emergency_phone=data.get('emergency_phone'),
            address=data.get('address'),
            address_number=data.get('address_number'),
            complement=data.get('complement'),
            neighborhood=data.get('neighborhood'),
            city=data.get('city'),
            state=data.get('state'),
            zip_code=data.get('zip_code'),
            employee_code=data.get('employee_code'),
            ctps_number=data.get('ctps_number'),
            ctps_series=data.get('ctps_series'),
            pis_pasep=data.get('pis_pasep'),
            admission_date=datetime.strptime(data.get('admission_date'), '%Y-%m-%d').date(),
            department_id=data.get('department_id'),
            position=data.get('position'),
            salary=float(data.get('salary', 0)),
            salary_type=data.get('salary_type', 'monthly'),
            workload=int(data.get('workload', 44)),
            contract_type=data.get('contract_type', 'clt'),
            bank_code=data.get('bank_code'),
            bank_name=data.get('bank_name'),
            agency=data.get('agency'),
            account=data.get('account'),
            account_type=data.get('account_type'),
            pix_key=data.get('pix_key'),
            pix_type=data.get('pix_type'),
            created_by=get_jwt_identity()
        )
        
        db.session.add(employee)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Colaborador criado com sucesso',
            'employee': employee.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

@hr_bp.route('/employees/<int:employee_id>', methods=['PUT'])
@jwt_required()
def update_employee(employee_id):
    """Atualizar colaborador"""
    try:
        employee = Employee.query.get_or_404(employee_id)
        data = request.get_json()
        
        # Atualizar campos
        for field in ['full_name', 'email', 'phone', 'mobile', 'position', 'salary', 'status']:
            if field in data:
                setattr(employee, field, data[field])
        
        if 'birth_date' in data and data['birth_date']:
            employee.birth_date = datetime.strptime(data['birth_date'], '%Y-%m-%d').date()
        
        employee.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Colaborador atualizado com sucesso',
            'employee': employee.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

# ==================== DEPENDENTES ====================

@hr_bp.route('/employees/<int:employee_id>/dependents', methods=['GET'])
@jwt_required()
def get_employee_dependents(employee_id):
    """Listar dependentes do colaborador"""
    try:
        dependents = Dependent.query.filter_by(employee_id=employee_id).all()
        return jsonify({
            'success': True,
            'dependents': [{
                'id': dep.id,
                'name': dep.name,
                'cpf': dep.cpf,
                'birth_date': dep.birth_date.isoformat() if dep.birth_date else None,
                'relationship': dep.relationship,
                'is_ir_dependent': dep.is_ir_dependent,
                'is_sf_dependent': dep.is_sf_dependent
            } for dep in dependents]
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@hr_bp.route('/employees/<int:employee_id>/dependents', methods=['POST'])
@jwt_required()
def add_dependent(employee_id):
    """Adicionar dependente"""
    try:
        data = request.get_json()
        
        dependent = Dependent(
            employee_id=employee_id,
            name=data.get('name'),
            cpf=data.get('cpf'),
            birth_date=datetime.strptime(data.get('birth_date'), '%Y-%m-%d').date() if data.get('birth_date') else None,
            relationship=data.get('relationship'),
            is_ir_dependent=data.get('is_ir_dependent', True),
            is_sf_dependent=data.get('is_sf_dependent', True)
        )
        
        db.session.add(dependent)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Dependente adicionado com sucesso'
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

# ==================== FOLHA DE PAGAMENTO ====================

@hr_bp.route('/payroll/periods', methods=['GET'])
@jwt_required()
def get_payroll_periods():
    """Listar períodos de folha"""
    try:
        periods = PayrollPeriod.query.order_by(PayrollPeriod.year.desc(), PayrollPeriod.month.desc()).all()
        return jsonify({
            'success': True,
            'periods': [{
                'id': period.id,
                'reference': period.reference,
                'year': period.year,
                'month': period.month,
                'start_date': period.start_date.isoformat(),
                'end_date': period.end_date.isoformat(),
                'payment_date': period.payment_date.isoformat() if period.payment_date else None,
                'status': period.status
            } for period in periods]
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@hr_bp.route('/payroll/periods', methods=['POST'])
@jwt_required()
def create_payroll_period():
    """Criar período de folha"""
    try:
        data = request.get_json()
        year = int(data.get('year'))
        month = int(data.get('month'))
        
        # Verificar se período já existe
        existing = PayrollPeriod.query.filter_by(year=year, month=month).first()
        if existing:
            return jsonify({'success': False, 'message': 'Período já existe'}), 400
        
        # Calcular datas do período
        start_date = date(year, month, 1)
        last_day = calendar.monthrange(year, month)[1]
        end_date = date(year, month, last_day)
        
        period = PayrollPeriod(
            year=year,
            month=month,
            reference=f"{year}-{month:02d}",
            start_date=start_date,
            end_date=end_date,
            payment_date=datetime.strptime(data.get('payment_date'), '%Y-%m-%d').date() if data.get('payment_date') else None
        )
        
        db.session.add(period)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Período criado com sucesso',
            'period_id': period.id
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

@hr_bp.route('/payroll/calculate/<int:period_id>', methods=['POST'])
@jwt_required()
def calculate_payroll(period_id):
    """Calcular folha de pagamento"""
    try:
        period = PayrollPeriod.query.get_or_404(period_id)
        
        if period.status != 'open':
            return jsonify({'success': False, 'message': 'Período não está aberto para cálculo'}), 400
        
        # Buscar colaboradores ativos
        employees = Employee.query.filter_by(status='active').all()
        
        calculated_count = 0
        
        for employee in employees:
            # Verificar se já existe cálculo para este funcionário no período
            existing_item = PayrollItem.query.filter_by(
                employee_id=employee.id,
                period_id=period_id
            ).first()
            
            if existing_item:
                continue  # Pular se já calculado
            
            # Buscar registros de ponto do período
            time_records = TimeRecord.query.filter(
                TimeRecord.employee_id == employee.id,
                TimeRecord.record_date >= period.start_date,
                TimeRecord.record_date <= period.end_date
            ).all()
            
            # Calcular horas trabalhadas e extras
            total_worked_hours = sum(record.worked_hours or 0 for record in time_records)
            total_overtime_hours = sum(record.overtime_hours or 0 for record in time_records)
            
            # Cálculos básicos
            base_salary = employee.salary
            overtime_value = (base_salary / 220) * 1.5 * total_overtime_hours  # 220 horas mensais, 50% adicional
            
            # Cálculo do INSS (simplificado)
            gross_salary = base_salary + overtime_value
            inss = min(gross_salary * 0.11, 713.10)  # Teto do INSS 2024
            
            # Cálculo do IRRF (simplificado)
            irrf_base = gross_salary - inss
            if irrf_base <= 1903.98:
                irrf = 0
            elif irrf_base <= 2826.65:
                irrf = (irrf_base * 0.075) - 142.80
            elif irrf_base <= 3751.05:
                irrf = (irrf_base * 0.15) - 354.80
            elif irrf_base <= 4664.68:
                irrf = (irrf_base * 0.225) - 636.13
            else:
                irrf = (irrf_base * 0.275) - 869.36
            
            irrf = max(irrf, 0)
            
            # FGTS (8% sobre o salário bruto)
            fgts = gross_salary * 0.08
            
            # Descontos de benefícios (exemplo: 6% vale transporte)
            transport_voucher = base_salary * 0.06
            
            total_deductions = inss + irrf + transport_voucher
            net_salary = gross_salary - total_deductions
            
            # Criar item da folha
            payroll_item = PayrollItem(
                employee_id=employee.id,
                period_id=period_id,
                base_salary=base_salary,
                overtime_hours=total_overtime_hours,
                overtime_value=overtime_value,
                inss=inss,
                irrf=irrf,
                fgts=fgts,
                transport_voucher=transport_voucher,
                gross_salary=gross_salary,
                total_deductions=total_deductions,
                net_salary=net_salary,
                calculated_at=datetime.utcnow()
            )
            
            db.session.add(payroll_item)
            calculated_count += 1
        
        # Atualizar status do período
        period.status = 'calculated'
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'Folha calculada para {calculated_count} colaboradores',
            'calculated_count': calculated_count
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

@hr_bp.route('/payroll/items/<int:period_id>', methods=['GET'])
@jwt_required()
def get_payroll_items(period_id):
    """Listar itens da folha de pagamento"""
    try:
        items = db.session.query(PayrollItem, Employee).join(
            Employee, PayrollItem.employee_id == Employee.id
        ).filter(PayrollItem.period_id == period_id).all()
        
        return jsonify({
            'success': True,
            'items': [{
                'employee_id': item.PayrollItem.employee_id,
                'employee_name': item.Employee.full_name,
                'employee_code': item.Employee.employee_code,
                'position': item.Employee.position,
                'base_salary': item.PayrollItem.base_salary,
                'overtime_hours': item.PayrollItem.overtime_hours,
                'overtime_value': item.PayrollItem.overtime_value,
                'gross_salary': item.PayrollItem.gross_salary,
                'inss': item.PayrollItem.inss,
                'irrf': item.PayrollItem.irrf,
                'transport_voucher': item.PayrollItem.transport_voucher,
                'total_deductions': item.PayrollItem.total_deductions,
                'net_salary': item.PayrollItem.net_salary
            } for item in items]
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

# ==================== CONTROLE DE PONTO ====================

@hr_bp.route('/timerecords', methods=['POST'])
@jwt_required()
def record_time():
    """Registrar ponto"""
    try:
        data = request.get_json()
        employee_id = data.get('employee_id')
        record_date = datetime.strptime(data.get('date'), '%Y-%m-%d').date()
        
        # Buscar ou criar registro do dia
        time_record = TimeRecord.query.filter_by(
            employee_id=employee_id,
            record_date=record_date
        ).first()
        
        if not time_record:
            time_record = TimeRecord(
                employee_id=employee_id,
                record_date=record_date
            )
            db.session.add(time_record)
        
        # Determinar qual horário registrar
        current_time = datetime.strptime(data.get('time'), '%H:%M').time()
        
        if not time_record.entry_time_1:
            time_record.entry_time_1 = current_time
        elif not time_record.exit_time_1:
            time_record.exit_time_1 = current_time
        elif not time_record.entry_time_2:
            time_record.entry_time_2 = current_time
        elif not time_record.exit_time_2:
            time_record.exit_time_2 = current_time
        else:
            return jsonify({'success': False, 'message': 'Todos os horários já foram registrados hoje'}), 400
        
        # Calcular horas trabalhadas se tiver saída final
        if time_record.exit_time_2:
            morning_hours = 0
            afternoon_hours = 0
            
            if time_record.entry_time_1 and time_record.exit_time_1:
                morning_delta = datetime.combine(date.today(), time_record.exit_time_1) - \
                               datetime.combine(date.today(), time_record.entry_time_1)
                morning_hours = morning_delta.total_seconds() / 3600
            
            if time_record.entry_time_2 and time_record.exit_time_2:
                afternoon_delta = datetime.combine(date.today(), time_record.exit_time_2) - \
                                 datetime.combine(date.today(), time_record.entry_time_2)
                afternoon_hours = afternoon_delta.total_seconds() / 3600
            
            total_hours = morning_hours + afternoon_hours
            time_record.worked_hours = total_hours
            
            # Calcular horas extras (acima de 8h/dia)
            if total_hours > 8:
                time_record.overtime_hours = total_hours - 8
        
        # Salvar localização se fornecida
        if data.get('latitude') and data.get('longitude'):
            time_record.location_lat = float(data.get('latitude'))
            time_record.location_lng = float(data.get('longitude'))
            time_record.location_address = data.get('address')
        
        time_record.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Ponto registrado com sucesso',
            'next_action': 'exit_lunch' if not time_record.exit_time_1 else 
                          'entry_afternoon' if not time_record.entry_time_2 else
                          'exit_final' if not time_record.exit_time_2 else 'complete'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

@hr_bp.route('/timerecords/<int:employee_id>', methods=['GET'])
@jwt_required()
def get_employee_timerecords(employee_id):
    """Buscar registros de ponto do colaborador"""
    try:
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = TimeRecord.query.filter_by(employee_id=employee_id)
        
        if start_date:
            query = query.filter(TimeRecord.record_date >= datetime.strptime(start_date, '%Y-%m-%d').date())
        if end_date:
            query = query.filter(TimeRecord.record_date <= datetime.strptime(end_date, '%Y-%m-%d').date())
        
        records = query.order_by(TimeRecord.record_date.desc()).all()
        
        return jsonify({
            'success': True,
            'records': [{
                'id': record.id,
                'date': record.record_date.isoformat(),
                'entry_time_1': record.entry_time_1.strftime('%H:%M') if record.entry_time_1 else None,
                'exit_time_1': record.exit_time_1.strftime('%H:%M') if record.exit_time_1 else None,
                'entry_time_2': record.entry_time_2.strftime('%H:%M') if record.entry_time_2 else None,
                'exit_time_2': record.exit_time_2.strftime('%H:%M') if record.exit_time_2 else None,
                'worked_hours': record.worked_hours,
                'overtime_hours': record.overtime_hours,
                'status': record.status,
                'observations': record.observations
            } for record in records]
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

# ==================== BENEFÍCIOS ====================

@hr_bp.route('/benefits', methods=['GET'])
@jwt_required()
def get_benefits():
    """Listar benefícios disponíveis"""
    try:
        benefits = Benefit.query.filter_by(is_active=True).all()
        return jsonify({
            'success': True,
            'benefits': [{
                'id': benefit.id,
                'name': benefit.name,
                'description': benefit.description,
                'category': benefit.category,
                'value_type': benefit.value_type,
                'default_value': benefit.default_value,
                'is_taxable': benefit.is_taxable
            } for benefit in benefits]
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@hr_bp.route('/employees/<int:employee_id>/benefits', methods=['GET'])
@jwt_required()
def get_employee_benefits(employee_id):
    """Listar benefícios do colaborador"""
    try:
        benefits = db.session.query(EmployeeBenefit, Benefit).join(
            Benefit, EmployeeBenefit.benefit_id == Benefit.id
        ).filter(
            EmployeeBenefit.employee_id == employee_id,
            EmployeeBenefit.is_active == True
        ).all()
        
        return jsonify({
            'success': True,
            'benefits': [{
                'id': item.EmployeeBenefit.id,
                'benefit_name': item.Benefit.name,
                'category': item.Benefit.category,
                'value': item.EmployeeBenefit.value,
                'start_date': item.EmployeeBenefit.start_date.isoformat(),
                'end_date': item.EmployeeBenefit.end_date.isoformat() if item.EmployeeBenefit.end_date else None
            } for item in benefits]
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

# ==================== TREINAMENTOS ====================

@hr_bp.route('/trainings', methods=['GET'])
@jwt_required()
def get_trainings():
    """Listar treinamentos disponíveis"""
    try:
        trainings = Training.query.filter_by(is_active=True).all()
        return jsonify({
            'success': True,
            'trainings': [{
                'id': training.id,
                'title': training.title,
                'description': training.description,
                'category': training.category,
                'duration_hours': training.duration_hours,
                'instructor': training.instructor,
                'is_mandatory': training.is_mandatory
            } for training in trainings]
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@hr_bp.route('/employees/<int:employee_id>/trainings', methods=['GET'])
@jwt_required()
def get_employee_trainings(employee_id):
    """Listar treinamentos do colaborador"""
    try:
        trainings = db.session.query(EmployeeTraining, Training).join(
            Training, EmployeeTraining.training_id == Training.id
        ).filter(EmployeeTraining.employee_id == employee_id).all()
        
        return jsonify({
            'success': True,
            'trainings': [{
                'id': item.EmployeeTraining.id,
                'training_title': item.Training.title,
                'start_date': item.EmployeeTraining.start_date.isoformat() if item.EmployeeTraining.start_date else None,
                'completion_date': item.EmployeeTraining.completion_date.isoformat() if item.EmployeeTraining.completion_date else None,
                'status': item.EmployeeTraining.status,
                'score': item.EmployeeTraining.score,
                'certificate_url': item.EmployeeTraining.certificate_url
            } for item in trainings]
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

# ==================== COMUNICAÇÃO INTERNA ====================

@hr_bp.route('/communications', methods=['GET'])
@jwt_required()
def get_communications():
    """Listar comunicações internas"""
    try:
        communications = InternalCommunication.query.filter_by(
            status='published'
        ).order_by(InternalCommunication.published_at.desc()).all()
        
        return jsonify({
            'success': True,
            'communications': [{
                'id': comm.id,
                'title': comm.title,
                'content': comm.content,
                'type': comm.type,
                'priority': comm.priority,
                'published_at': comm.published_at.isoformat() if comm.published_at else None,
                'expires_at': comm.expires_at.isoformat() if comm.expires_at else None,
                'requires_confirmation': comm.requires_confirmation
            } for comm in communications]
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@hr_bp.route('/communications', methods=['POST'])
@jwt_required()
def create_communication():
    """Criar comunicação interna"""
    try:
        data = request.get_json()
        
        communication = InternalCommunication(
            title=data.get('title'),
            content=data.get('content'),
            type=data.get('type', 'announcement'),
            priority=data.get('priority', 'normal'),
            target_type=data.get('target_type', 'all'),
            target_departments=json.dumps(data.get('target_departments', [])),
            target_employees=json.dumps(data.get('target_employees', [])),
            requires_confirmation=data.get('requires_confirmation', False),
            send_email=data.get('send_email', True),
            send_push=data.get('send_push', True),
            status='published',
            published_at=datetime.utcnow(),
            expires_at=datetime.strptime(data.get('expires_at'), '%Y-%m-%d %H:%M:%S') if data.get('expires_at') else None,
            created_by=get_jwt_identity()
        )
        
        db.session.add(communication)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Comunicação criada com sucesso',
            'communication_id': communication.id
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

# ==================== DASHBOARDS E RELATÓRIOS ====================

@hr_bp.route('/dashboard/stats', methods=['GET'])
@jwt_required()
def get_hr_dashboard_stats():
    """Estatísticas para o dashboard de RH"""
    try:
        # Contadores básicos
        total_employees = Employee.query.filter_by(status='active').count()
        total_departments = db.session.query(Employee.department_id).distinct().count()
        
        # Funcionários por departamento
        dept_stats = db.session.query(
            Employee.department_id,
            db.func.count(Employee.id).label('count')
        ).filter_by(status='active').group_by(Employee.department_id).all()
        
        # Aniversariantes do mês
        current_month = datetime.now().month
        birthdays = Employee.query.filter(
            db.extract('month', Employee.birth_date) == current_month,
            Employee.status == 'active'
        ).count()
        
        # Admissões recentes (últimos 30 dias)
        thirty_days_ago = datetime.now().date() - timedelta(days=30)
        recent_admissions = Employee.query.filter(
            Employee.admission_date >= thirty_days_ago,
            Employee.status == 'active'
        ).count()
        
        # Folha de pagamento do mês atual
        current_year = datetime.now().year
        current_month = datetime.now().month
        current_period = PayrollPeriod.query.filter_by(
            year=current_year,
            month=current_month
        ).first()
        
        payroll_total = 0
        if current_period:
            payroll_total = db.session.query(
                db.func.sum(PayrollItem.net_salary)
            ).filter_by(period_id=current_period.id).scalar() or 0
        
        return jsonify({
            'success': True,
            'stats': {
                'total_employees': total_employees,
                'total_departments': total_departments,
                'birthdays_this_month': birthdays,
                'recent_admissions': recent_admissions,
                'payroll_total': payroll_total,
                'employees_by_department': [
                    {'department_id': stat[0], 'count': stat[1]} 
                    for stat in dept_stats
                ]
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@hr_bp.route('/reports/turnover', methods=['GET'])
@jwt_required()
def get_turnover_report():
    """Relatório de turnover"""
    try:
        year = request.args.get('year', datetime.now().year, type=int)
        
        # Admissões por mês
        admissions = db.session.query(
            db.extract('month', Employee.admission_date).label('month'),
            db.func.count(Employee.id).label('count')
        ).filter(
            db.extract('year', Employee.admission_date) == year
        ).group_by(db.extract('month', Employee.admission_date)).all()
        
        # Demissões por mês
        dismissals = db.session.query(
            db.extract('month', Employee.dismissal_date).label('month'),
            db.func.count(Employee.id).label('count')
        ).filter(
            db.extract('year', Employee.dismissal_date) == year,
            Employee.dismissal_date.isnot(None)
        ).group_by(db.extract('month', Employee.dismissal_date)).all()
        
        return jsonify({
            'success': True,
            'year': year,
            'admissions': [{'month': int(item[0]), 'count': item[1]} for item in admissions],
            'dismissals': [{'month': int(item[0]), 'count': item[1]} for item in dismissals]
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

# ==================== ESOCIAL E INTEGRAÇÕES ====================

@hr_bp.route('/esocial/events', methods=['GET'])
@jwt_required()
def get_esocial_events():
    """Listar eventos do eSocial"""
    try:
        events = ESocialEvent.query.order_by(ESocialEvent.created_at.desc()).limit(100).all()
        return jsonify({
            'success': True,
            'events': [{
                'id': event.id,
                'employee_id': event.employee_id,
                'event_type': event.event_type,
                'status': event.status,
                'receipt_number': event.receipt_number,
                'protocol_number': event.protocol_number,
                'sent_at': event.sent_at.isoformat() if event.sent_at else None,
                'error_message': event.error_message,
                'created_at': event.created_at.isoformat()
            } for event in events]
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@hr_bp.route('/payments/batches', methods=['GET'])
@jwt_required()
def get_payment_batches():
    """Listar lotes de pagamento"""
    try:
        batches = PaymentBatch.query.order_by(PaymentBatch.created_at.desc()).all()
        return jsonify({
            'success': True,
            'batches': [{
                'id': batch.id,
                'batch_number': batch.batch_number,
                'payment_method': batch.payment_method,
                'total_amount': batch.total_amount,
                'employee_count': batch.employee_count,
                'status': batch.status,
                'created_at': batch.created_at.isoformat(),
                'processed_at': batch.processed_at.isoformat() if batch.processed_at else None
            } for batch in batches]
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

