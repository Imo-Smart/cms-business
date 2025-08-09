from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.models.user import db, User
from src.models.financial import BankAccount, BankTransaction, PaymentMethod, Supplier, Receivable, Payable, CashFlow
from src.models.accounting import Company
from datetime import datetime, date
import json

financial_bp = Blueprint('financial', __name__)

# ==================== CONTAS BANCÁRIAS ====================

@financial_bp.route('/bank-accounts', methods=['GET'])
@jwt_required()
def get_bank_accounts():
    """Listar contas bancárias"""
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({'error': 'Utilizador não encontrado'}), 404
        
        # Buscar empresa do utilizador (assumindo primeira empresa)
        company = Company.query.first()
        if not company:
            return jsonify({'error': 'Empresa não encontrada'}), 404
        
        accounts = BankAccount.query.filter_by(company_id=company.id).all()
        
        accounts_data = []
        for account in accounts:
            accounts_data.append({
                'id': account.id,
                'bank_code': account.bank_code,
                'bank_name': account.bank_name,
                'agency': account.agency,
                'account_number': account.account_number,
                'account_digit': account.account_digit,
                'account_type': account.account_type,
                'initial_balance': float(account.initial_balance),
                'current_balance': float(account.current_balance),
                'is_active': account.is_active,
                'created_at': account.created_at.isoformat() if account.created_at else None
            })
        
        return jsonify({
            'success': True,
            'data': accounts_data,
            'total': len(accounts_data)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@financial_bp.route('/bank-accounts', methods=['POST'])
@jwt_required()
def create_bank_account():
    """Criar nova conta bancária"""
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({'error': 'Utilizador não encontrado'}), 404
        
        company = Company.query.first()
        if not company:
            return jsonify({'error': 'Empresa não encontrada'}), 404
        
        data = request.get_json()
        
        # Validações
        required_fields = ['bank_code', 'bank_name', 'agency', 'account_number', 'account_type']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'Campo {field} é obrigatório'}), 400
        
        account = BankAccount(
            company_id=company.id,
            bank_code=data['bank_code'],
            bank_name=data['bank_name'],
            agency=data['agency'],
            account_number=data['account_number'],
            account_digit=data.get('account_digit', ''),
            account_type=data['account_type'],
            initial_balance=float(data.get('initial_balance', 0)),
            current_balance=float(data.get('initial_balance', 0)),
            is_active=data.get('is_active', True)
        )
        
        db.session.add(account)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Conta bancária criada com sucesso',
            'data': {
                'id': account.id,
                'bank_name': account.bank_name,
                'account_number': account.account_number
            }
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# ==================== FORNECEDORES ====================

@financial_bp.route('/suppliers', methods=['GET'])
@jwt_required()
def get_suppliers():
    """Listar fornecedores"""
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({'error': 'Utilizador não encontrado'}), 404
        
        company = Company.query.first()
        if not company:
            return jsonify({'error': 'Empresa não encontrada'}), 404
        
        suppliers = Supplier.query.filter_by(company_id=company.id).all()
        
        suppliers_data = []
        for supplier in suppliers:
            suppliers_data.append({
                'id': supplier.id,
                'type': supplier.type,
                'document': supplier.document,
                'name': supplier.name,
                'trade_name': supplier.trade_name,
                'email': supplier.email,
                'phone': supplier.phone,
                'address': supplier.address,
                'city': supplier.city,
                'state': supplier.state,
                'zip_code': supplier.zip_code,
                'is_active': supplier.is_active,
                'created_at': supplier.created_at.isoformat() if supplier.created_at else None
            })
        
        return jsonify({
            'success': True,
            'data': suppliers_data,
            'total': len(suppliers_data)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@financial_bp.route('/suppliers', methods=['POST'])
@jwt_required()
def create_supplier():
    """Criar novo fornecedor"""
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({'error': 'Utilizador não encontrado'}), 404
        
        company = Company.query.first()
        if not company:
            return jsonify({'error': 'Empresa não encontrada'}), 404
        
        data = request.get_json()
        
        # Validações
        required_fields = ['type', 'document', 'name']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'Campo {field} é obrigatório'}), 400
        
        # Verificar se documento já existe
        existing_supplier = Supplier.query.filter_by(
            company_id=company.id,
            document=data['document']
        ).first()
        
        if existing_supplier:
            return jsonify({'error': 'Já existe um fornecedor com este documento'}), 400
        
        supplier = Supplier(
            company_id=company.id,
            type=data['type'],
            document=data['document'],
            name=data['name'],
            trade_name=data.get('trade_name', ''),
            email=data.get('email', ''),
            phone=data.get('phone', ''),
            address=data.get('address', ''),
            city=data.get('city', ''),
            state=data.get('state', ''),
            zip_code=data.get('zip_code', ''),
            is_active=data.get('is_active', True)
        )
        
        db.session.add(supplier)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Fornecedor criado com sucesso',
            'data': {
                'id': supplier.id,
                'name': supplier.name,
                'document': supplier.document
            }
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# ==================== CONTAS A PAGAR ====================

@financial_bp.route('/payables', methods=['GET'])
@jwt_required()
def get_payables():
    """Listar contas a pagar"""
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({'error': 'Utilizador não encontrado'}), 404
        
        company = Company.query.first()
        if not company:
            return jsonify({'error': 'Empresa não encontrada'}), 404
        
        # Filtros opcionais
        status = request.args.get('status')
        supplier_id = request.args.get('supplier_id')
        
        query = Payable.query.filter_by(company_id=company.id)
        
        if status:
            query = query.filter_by(status=status)
        if supplier_id:
            query = query.filter_by(supplier_id=supplier_id)
        
        payables = query.all()
        
        payables_data = []
        for payable in payables:
            supplier = Supplier.query.get(payable.supplier_id) if payable.supplier_id else None
            
            payables_data.append({
                'id': payable.id,
                'document_number': payable.document_number,
                'description': payable.description,
                'supplier': {
                    'id': supplier.id if supplier else None,
                    'name': supplier.name if supplier else 'N/A'
                },
                'issue_date': payable.issue_date.isoformat() if payable.issue_date else None,
                'due_date': payable.due_date.isoformat() if payable.due_date else None,
                'original_amount': float(payable.original_amount),
                'paid_amount': float(payable.paid_amount),
                'remaining_amount': float(payable.remaining_amount),
                'status': payable.status,
                'payment_date': payable.payment_date.isoformat() if payable.payment_date else None,
                'created_at': payable.created_at.isoformat() if payable.created_at else None
            })
        
        return jsonify({
            'success': True,
            'data': payables_data,
            'total': len(payables_data)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@financial_bp.route('/payables', methods=['POST'])
@jwt_required()
def create_payable():
    """Criar nova conta a pagar"""
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({'error': 'Utilizador não encontrado'}), 404
        
        company = Company.query.first()
        if not company:
            return jsonify({'error': 'Empresa não encontrada'}), 404
        
        data = request.get_json()
        
        # Validações
        required_fields = ['description', 'due_date', 'original_amount']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'Campo {field} é obrigatório'}), 400
        
        # Converter datas
        issue_date = datetime.strptime(data.get('issue_date', datetime.now().strftime('%Y-%m-%d')), '%Y-%m-%d').date()
        due_date = datetime.strptime(data['due_date'], '%Y-%m-%d').date()
        
        original_amount = float(data['original_amount'])
        
        payable = Payable(
            company_id=company.id,
            supplier_id=data.get('supplier_id'),
            document_number=data.get('document_number', ''),
            description=data['description'],
            issue_date=issue_date,
            due_date=due_date,
            original_amount=original_amount,
            paid_amount=0.0,
            remaining_amount=original_amount,
            status='pending'
        )
        
        db.session.add(payable)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Conta a pagar criada com sucesso',
            'data': {
                'id': payable.id,
                'description': payable.description,
                'original_amount': float(payable.original_amount)
            }
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# ==================== CONTAS A RECEBER ====================

@financial_bp.route('/receivables', methods=['GET'])
@jwt_required()
def get_receivables():
    """Listar contas a receber"""
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({'error': 'Utilizador não encontrado'}), 404
        
        company = Company.query.first()
        if not company:
            return jsonify({'error': 'Empresa não encontrada'}), 404
        
        # Filtros opcionais
        status = request.args.get('status')
        customer_id = request.args.get('customer_id')
        
        query = Receivable.query.filter_by(company_id=company.id)
        
        if status:
            query = query.filter_by(status=status)
        if customer_id:
            query = query.filter_by(customer_id=customer_id)
        
        receivables = query.all()
        
        receivables_data = []
        for receivable in receivables:
            from src.models.fiscal import Customer
            customer = Customer.query.get(receivable.customer_id) if receivable.customer_id else None
            
            receivables_data.append({
                'id': receivable.id,
                'document_number': receivable.document_number,
                'description': receivable.description,
                'customer': {
                    'id': customer.id if customer else None,
                    'name': customer.name if customer else 'N/A'
                },
                'issue_date': receivable.issue_date.isoformat() if receivable.issue_date else None,
                'due_date': receivable.due_date.isoformat() if receivable.due_date else None,
                'original_amount': float(receivable.original_amount),
                'received_amount': float(receivable.received_amount),
                'remaining_amount': float(receivable.remaining_amount),
                'status': receivable.status,
                'payment_date': receivable.payment_date.isoformat() if receivable.payment_date else None,
                'created_at': receivable.created_at.isoformat() if receivable.created_at else None
            })
        
        return jsonify({
            'success': True,
            'data': receivables_data,
            'total': len(receivables_data)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@financial_bp.route('/receivables', methods=['POST'])
@jwt_required()
def create_receivable():
    """Criar nova conta a receber"""
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({'error': 'Utilizador não encontrado'}), 404
        
        company = Company.query.first()
        if not company:
            return jsonify({'error': 'Empresa não encontrada'}), 404
        
        data = request.get_json()
        
        # Validações
        required_fields = ['description', 'due_date', 'original_amount']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'Campo {field} é obrigatório'}), 400
        
        # Converter datas
        issue_date = datetime.strptime(data.get('issue_date', datetime.now().strftime('%Y-%m-%d')), '%Y-%m-%d').date()
        due_date = datetime.strptime(data['due_date'], '%Y-%m-%d').date()
        
        original_amount = float(data['original_amount'])
        
        receivable = Receivable(
            company_id=company.id,
            customer_id=data.get('customer_id'),
            document_number=data.get('document_number', ''),
            description=data['description'],
            issue_date=issue_date,
            due_date=due_date,
            original_amount=original_amount,
            received_amount=0.0,
            remaining_amount=original_amount,
            status='pending'
        )
        
        db.session.add(receivable)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Conta a receber criada com sucesso',
            'data': {
                'id': receivable.id,
                'description': receivable.description,
                'original_amount': float(receivable.original_amount)
            }
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# ==================== FLUXO DE CAIXA ====================

@financial_bp.route('/cash-flow', methods=['GET'])
@jwt_required()
def get_cash_flow():
    """Obter fluxo de caixa"""
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({'error': 'Utilizador não encontrado'}), 404
        
        company = Company.query.first()
        if not company:
            return jsonify({'error': 'Empresa não encontrada'}), 404
        
        # Parâmetros de data
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        if not start_date or not end_date:
            return jsonify({'error': 'Datas de início e fim são obrigatórias'}), 400
        
        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        
        # Buscar entradas (contas a receber)
        receivables = Receivable.query.filter(
            Receivable.company_id == company.id,
            Receivable.due_date >= start_date,
            Receivable.due_date <= end_date
        ).all()
        
        # Buscar saídas (contas a pagar)
        payables = Payable.query.filter(
            Payable.company_id == company.id,
            Payable.due_date >= start_date,
            Payable.due_date <= end_date
        ).all()
        
        # Organizar por data
        cash_flow_data = {}
        
        # Processar recebimentos
        for receivable in receivables:
            date_str = receivable.due_date.isoformat()
            if date_str not in cash_flow_data:
                cash_flow_data[date_str] = {'date': date_str, 'inflow': 0, 'outflow': 0, 'balance': 0}
            
            cash_flow_data[date_str]['inflow'] += float(receivable.remaining_amount)
        
        # Processar pagamentos
        for payable in payables:
            date_str = payable.due_date.isoformat()
            if date_str not in cash_flow_data:
                cash_flow_data[date_str] = {'date': date_str, 'inflow': 0, 'outflow': 0, 'balance': 0}
            
            cash_flow_data[date_str]['outflow'] += float(payable.remaining_amount)
        
        # Calcular saldos
        for date_str in cash_flow_data:
            cash_flow_data[date_str]['balance'] = cash_flow_data[date_str]['inflow'] - cash_flow_data[date_str]['outflow']
        
        # Converter para lista ordenada
        cash_flow_list = sorted(cash_flow_data.values(), key=lambda x: x['date'])
        
        # Calcular totais
        total_inflow = sum(item['inflow'] for item in cash_flow_list)
        total_outflow = sum(item['outflow'] for item in cash_flow_list)
        total_balance = total_inflow - total_outflow
        
        return jsonify({
            'success': True,
            'data': {
                'cash_flow': cash_flow_list,
                'summary': {
                    'total_inflow': total_inflow,
                    'total_outflow': total_outflow,
                    'total_balance': total_balance
                }
            }
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ==================== DASHBOARD FINANCEIRO ====================

@financial_bp.route('/dashboard', methods=['GET'])
@jwt_required()
def get_financial_dashboard():
    """Obter dados do dashboard financeiro"""
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({'error': 'Utilizador não encontrado'}), 404
        
        company = Company.query.first()
        if not company:
            return jsonify({'error': 'Empresa não encontrada'}), 404
        
        # Saldo total das contas bancárias
        total_bank_balance = db.session.query(db.func.sum(BankAccount.current_balance)).filter_by(
            company_id=company.id, is_active=True
        ).scalar() or 0
        
        # Contas a receber pendentes
        pending_receivables = db.session.query(db.func.sum(Receivable.remaining_amount)).filter_by(
            company_id=company.id, status='pending'
        ).scalar() or 0
        
        # Contas a pagar pendentes
        pending_payables = db.session.query(db.func.sum(Payable.remaining_amount)).filter_by(
            company_id=company.id, status='pending'
        ).scalar() or 0
        
        # Contas vencidas (a receber)
        today = date.today()
        overdue_receivables = db.session.query(db.func.sum(Receivable.remaining_amount)).filter(
            Receivable.company_id == company.id,
            Receivable.status == 'pending',
            Receivable.due_date < today
        ).scalar() or 0
        
        # Contas vencidas (a pagar)
        overdue_payables = db.session.query(db.func.sum(Payable.remaining_amount)).filter(
            Payable.company_id == company.id,
            Payable.status == 'pending',
            Payable.due_date < today
        ).scalar() or 0
        
        return jsonify({
            'success': True,
            'data': {
                'bank_balance': float(total_bank_balance),
                'pending_receivables': float(pending_receivables),
                'pending_payables': float(pending_payables),
                'overdue_receivables': float(overdue_receivables),
                'overdue_payables': float(overdue_payables),
                'net_balance': float(total_bank_balance + pending_receivables - pending_payables)
            }
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

