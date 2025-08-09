from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime, date
from decimal import Decimal

from src.models.user import db, User
from src.models.accounting import (
    Company, AccountType, Account, CostCenter, 
    JournalEntry, JournalEntryLine, FiscalPeriod
)

accounting_bp = Blueprint('accounting', __name__)

# ==================== EMPRESAS ====================

@accounting_bp.route('/companies', methods=['GET'])
@jwt_required()
def get_companies():
    """Listar empresas"""
    try:
        companies = Company.query.filter_by(is_active=True).all()
        return jsonify([company.to_dict() for company in companies]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@accounting_bp.route('/companies', methods=['POST'])
@jwt_required()
def create_company():
    """Criar nova empresa"""
    try:
        data = request.get_json()
        
        # Verificar se CNPJ já existe
        existing = Company.query.filter_by(cnpj=data['cnpj']).first()
        if existing:
            return jsonify({'error': 'CNPJ já cadastrado'}), 400
        
        company = Company(
            cnpj=data['cnpj'],
            name=data['name'],
            trade_name=data.get('trade_name'),
            email=data.get('email'),
            phone=data.get('phone'),
            address=data.get('address'),
            city=data.get('city'),
            state=data.get('state'),
            zip_code=data.get('zip_code'),
            tax_regime=data.get('tax_regime', 'simples_nacional')
        )
        
        db.session.add(company)
        db.session.commit()
        
        return jsonify(company.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@accounting_bp.route('/companies/<int:company_id>', methods=['GET'])
@jwt_required()
def get_company(company_id):
    """Obter empresa por ID"""
    try:
        company = Company.query.get_or_404(company_id)
        return jsonify(company.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@accounting_bp.route('/companies/<int:company_id>', methods=['PUT'])
@jwt_required()
def update_company(company_id):
    """Atualizar empresa"""
    try:
        company = Company.query.get_or_404(company_id)
        data = request.get_json()
        
        # Atualizar campos
        for field in ['name', 'trade_name', 'email', 'phone', 'address', 'city', 'state', 'zip_code', 'tax_regime']:
            if field in data:
                setattr(company, field, data[field])
        
        db.session.commit()
        return jsonify(company.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# ==================== PLANO DE CONTAS ====================

@accounting_bp.route('/companies/<int:company_id>/accounts', methods=['GET'])
@jwt_required()
def get_accounts(company_id):
    """Listar contas da empresa"""
    try:
        accounts = Account.query.filter_by(
            company_id=company_id, 
            is_active=True
        ).order_by(Account.code).all()
        
        return jsonify([account.to_dict() for account in accounts]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@accounting_bp.route('/companies/<int:company_id>/accounts', methods=['POST'])
@jwt_required()
def create_account(company_id):
    """Criar nova conta contábil"""
    try:
        data = request.get_json()
        
        # Verificar se código já existe na empresa
        existing = Account.query.filter_by(
            company_id=company_id, 
            code=data['code']
        ).first()
        if existing:
            return jsonify({'error': 'Código de conta já existe'}), 400
        
        account = Account(
            company_id=company_id,
            code=data['code'],
            name=data['name'],
            account_type_id=data['account_type_id'],
            parent_id=data.get('parent_id'),
            level=data.get('level', 1),
            is_analytical=data.get('is_analytical', True)
        )
        
        db.session.add(account)
        db.session.commit()
        
        return jsonify(account.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@accounting_bp.route('/accounts/<int:account_id>', methods=['PUT'])
@jwt_required()
def update_account(account_id):
    """Atualizar conta contábil"""
    try:
        account = Account.query.get_or_404(account_id)
        data = request.get_json()
        
        # Atualizar campos
        for field in ['name', 'account_type_id', 'parent_id', 'level', 'is_analytical', 'is_active']:
            if field in data:
                setattr(account, field, data[field])
        
        db.session.commit()
        return jsonify(account.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@accounting_bp.route('/accounts/<int:account_id>/balance', methods=['GET'])
@jwt_required()
def get_account_balance(account_id):
    """Obter saldo da conta"""
    try:
        account = Account.query.get_or_404(account_id)
        
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        if start_date:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        if end_date:
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        
        balance = account.get_balance(start_date, end_date)
        
        return jsonify({
            'account_id': account_id,
            'account_code': account.code,
            'account_name': account.name,
            'balance': float(balance),
            'start_date': start_date.isoformat() if start_date else None,
            'end_date': end_date.isoformat() if end_date else None
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ==================== TIPOS DE CONTA ====================

@accounting_bp.route('/account-types', methods=['GET'])
@jwt_required()
def get_account_types():
    """Listar tipos de conta"""
    try:
        account_types = AccountType.query.all()
        return jsonify([at.to_dict() for at in account_types]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ==================== CENTROS DE CUSTO ====================

@accounting_bp.route('/companies/<int:company_id>/cost-centers', methods=['GET'])
@jwt_required()
def get_cost_centers(company_id):
    """Listar centros de custo"""
    try:
        cost_centers = CostCenter.query.filter_by(
            company_id=company_id,
            is_active=True
        ).order_by(CostCenter.code).all()
        
        return jsonify([cc.to_dict() for cc in cost_centers]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@accounting_bp.route('/companies/<int:company_id>/cost-centers', methods=['POST'])
@jwt_required()
def create_cost_center(company_id):
    """Criar centro de custo"""
    try:
        data = request.get_json()
        
        cost_center = CostCenter(
            company_id=company_id,
            code=data['code'],
            name=data['name'],
            description=data.get('description'),
            parent_id=data.get('parent_id')
        )
        
        db.session.add(cost_center)
        db.session.commit()
        
        return jsonify(cost_center.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# ==================== LANÇAMENTOS CONTÁBEIS ====================

@accounting_bp.route('/companies/<int:company_id>/journal-entries', methods=['GET'])
@jwt_required()
def get_journal_entries(company_id):
    """Listar lançamentos contábeis"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = JournalEntry.query.filter_by(company_id=company_id)
        
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(JournalEntry.date >= datetime.strptime(start_date, '%Y-%m-%d').date())
        if end_date:
            query = query.filter(JournalEntry.date <= datetime.strptime(end_date, '%Y-%m-%d').date())
        
        entries = query.order_by(JournalEntry.date.desc(), JournalEntry.entry_number.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return jsonify({
            'entries': [entry.to_dict() for entry in entries.items],
            'total': entries.total,
            'pages': entries.pages,
            'current_page': page
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@accounting_bp.route('/companies/<int:company_id>/journal-entries', methods=['POST'])
@jwt_required()
def create_journal_entry(company_id):
    """Criar lançamento contábil"""
    try:
        data = request.get_json()
        current_user_id = get_jwt_identity()
        
        # Gerar número do lançamento
        last_entry = JournalEntry.query.filter_by(company_id=company_id).order_by(JournalEntry.id.desc()).first()
        entry_number = f"LC{(last_entry.id + 1) if last_entry else 1:06d}"
        
        # Criar lançamento
        entry = JournalEntry(
            company_id=company_id,
            entry_number=entry_number,
            date=datetime.strptime(data['date'], '%Y-%m-%d').date(),
            description=data['description'],
            reference=data.get('reference'),
            total_amount=Decimal(str(data['total_amount'])),
            created_by=current_user_id
        )
        
        db.session.add(entry)
        db.session.flush()  # Para obter o ID
        
        # Criar linhas do lançamento
        for line_data in data['lines']:
            line = JournalEntryLine(
                journal_entry_id=entry.id,
                account_id=line_data['account_id'],
                cost_center_id=line_data.get('cost_center_id'),
                description=line_data.get('description'),
                debit_amount=Decimal(str(line_data.get('debit_amount', 0))),
                credit_amount=Decimal(str(line_data.get('credit_amount', 0)))
            )
            db.session.add(line)
        
        db.session.commit()
        
        return jsonify(entry.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@accounting_bp.route('/journal-entries/<int:entry_id>', methods=['GET'])
@jwt_required()
def get_journal_entry(entry_id):
    """Obter lançamento contábil"""
    try:
        entry = JournalEntry.query.get_or_404(entry_id)
        return jsonify(entry.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@accounting_bp.route('/journal-entries/<int:entry_id>/post', methods=['POST'])
@jwt_required()
def post_journal_entry(entry_id):
    """Efetivar lançamento contábil"""
    try:
        entry = JournalEntry.query.get_or_404(entry_id)
        
        if entry.post_entry():
            db.session.commit()
            return jsonify({'message': 'Lançamento efetivado com sucesso'}), 200
        else:
            return jsonify({'error': 'Lançamento não está balanceado ou já foi efetivado'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# ==================== RELATÓRIOS CONTÁBEIS ====================

@accounting_bp.route('/companies/<int:company_id>/trial-balance', methods=['GET'])
@jwt_required()
def get_trial_balance(company_id):
    """Balancete de verificação"""
    try:
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        if start_date:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        if end_date:
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        
        accounts = Account.query.filter_by(
            company_id=company_id,
            is_active=True,
            is_analytical=True
        ).order_by(Account.code).all()
        
        balancete = []
        total_debit = 0
        total_credit = 0
        
        for account in accounts:
            balance = account.get_balance(start_date, end_date)
            
            if balance != 0:  # Só incluir contas com movimento
                if account.account_type.nature == 'debit':
                    debit_balance = balance if balance > 0 else 0
                    credit_balance = abs(balance) if balance < 0 else 0
                else:
                    credit_balance = balance if balance > 0 else 0
                    debit_balance = abs(balance) if balance < 0 else 0
                
                balancete.append({
                    'account_code': account.code,
                    'account_name': account.name,
                    'account_type': account.account_type.name,
                    'debit_balance': float(debit_balance),
                    'credit_balance': float(credit_balance)
                })
                
                total_debit += debit_balance
                total_credit += credit_balance
        
        return jsonify({
            'company_id': company_id,
            'start_date': start_date.isoformat() if start_date else None,
            'end_date': end_date.isoformat() if end_date else None,
            'accounts': balancete,
            'total_debit': float(total_debit),
            'total_credit': float(total_credit),
            'is_balanced': abs(total_debit - total_credit) < 0.01
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@accounting_bp.route('/companies/<int:company_id>/balance-sheet', methods=['GET'])
@jwt_required()
def get_balance_sheet(company_id):
    """Balanço patrimonial"""
    try:
        end_date = request.args.get('end_date')
        if end_date:
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        
        accounts = Account.query.filter_by(
            company_id=company_id,
            is_active=True
        ).order_by(Account.code).all()
        
        balance_sheet = {
            'ativo': {'circulante': [], 'nao_circulante': [], 'total': 0},
            'passivo': {'circulante': [], 'nao_circulante': [], 'total': 0},
            'patrimonio_liquido': {'contas': [], 'total': 0}
        }
        
        for account in accounts:
            balance = account.get_balance(None, end_date)
            
            if balance != 0 and account.account_type.category in ['ativo', 'passivo', 'patrimonio_liquido']:
                account_data = {
                    'code': account.code,
                    'name': account.name,
                    'balance': float(balance)
                }
                
                if account.account_type.category == 'ativo':
                    if '1.1' in account.code:  # Ativo circulante
                        balance_sheet['ativo']['circulante'].append(account_data)
                    else:  # Ativo não circulante
                        balance_sheet['ativo']['nao_circulante'].append(account_data)
                    balance_sheet['ativo']['total'] += balance
                
                elif account.account_type.category == 'passivo':
                    if '2.1' in account.code:  # Passivo circulante
                        balance_sheet['passivo']['circulante'].append(account_data)
                    else:  # Passivo não circulante
                        balance_sheet['passivo']['nao_circulante'].append(account_data)
                    balance_sheet['passivo']['total'] += balance
                
                elif account.account_type.category == 'patrimonio_liquido':
                    balance_sheet['patrimonio_liquido']['contas'].append(account_data)
                    balance_sheet['patrimonio_liquido']['total'] += balance
        
        # Converter totais para float
        balance_sheet['ativo']['total'] = float(balance_sheet['ativo']['total'])
        balance_sheet['passivo']['total'] = float(balance_sheet['passivo']['total'])
        balance_sheet['patrimonio_liquido']['total'] = float(balance_sheet['patrimonio_liquido']['total'])
        
        total_passivo_pl = balance_sheet['passivo']['total'] + balance_sheet['patrimonio_liquido']['total']
        
        return jsonify({
            'company_id': company_id,
            'end_date': end_date.isoformat() if end_date else None,
            'balance_sheet': balance_sheet,
            'total_ativo': balance_sheet['ativo']['total'],
            'total_passivo_pl': float(total_passivo_pl),
            'is_balanced': abs(balance_sheet['ativo']['total'] - total_passivo_pl) < 0.01
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

