from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from datetime import datetime
from src.models.user import User, Role, db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    """Endpoint para login de usuários"""
    try:
        data = request.get_json()
        
        if not data or not data.get('username') or not data.get('password'):
            return jsonify({'error': 'Username e password são obrigatórios'}), 400
        
        username = data.get('username')
        password = data.get('password')
        
        # Buscar usuário por username ou email
        user = User.query.filter(
            (User.username == username) | (User.email == username)
        ).first()
        
        if not user or not user.check_password(password):
            return jsonify({'error': 'Credenciais inválidas'}), 401
        
        if not user.is_active:
            return jsonify({'error': 'Usuário inativo'}), 401
        
        # Atualizar último login
        user.last_login = datetime.utcnow()
        db.session.commit()
        
        # Criar token JWT
        access_token = create_access_token(identity=user.id)
        
        return jsonify({
            'access_token': access_token,
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/register', methods=['POST'])
def register():
    """Endpoint para registro de nova empresa e usuário administrador"""
    try:
        data = request.get_json()
        
        # Importar modelos necessários
        from src.models.accounting import Company, AccountType, Account, CostCenter
        from src.models.fiscal import TaxType, Customer, Product
        from src.models.financial import BankAccount, PaymentMethod, Supplier
        import re
        
        def validate_cnpj(cnpj):
            """Validação básica de CNPJ"""
            cnpj = re.sub(r'\D', '', cnpj)
            if len(cnpj) != 14:
                return False
            if cnpj == cnpj[0] * 14:
                return False
            return True

        def validate_email(email):
            """Validação básica de email"""
            pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            return re.match(pattern, email) is not None
        
        # Validações básicas
        required_fields = [
            'companyName', 'cnpj', 'email', 'phone', 'address', 'city', 'state', 'zipCode',
            'firstName', 'lastName', 'userEmail', 'username', 'password'
        ]
        
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'Campo {field} é obrigatório'}), 400
        
        # Validar CNPJ
        if not validate_cnpj(data['cnpj']):
            return jsonify({'error': 'CNPJ inválido'}), 400
        
        # Validar emails
        if not validate_email(data['email']):
            return jsonify({'error': 'Email da empresa inválido'}), 400
        
        if not validate_email(data['userEmail']):
            return jsonify({'error': 'Email do usuário inválido'}), 400
        
        # Verificar se CNPJ já existe
        existing_company = Company.query.filter_by(cnpj=data['cnpj']).first()
        if existing_company:
            return jsonify({'error': 'CNPJ já cadastrado no sistema'}), 400
        
        # Verificar se username já existe
        existing_user = User.query.filter_by(username=data['username']).first()
        if existing_user:
            return jsonify({'error': 'Nome de usuário já existe'}), 400
        
        # Verificar se email do usuário já existe
        existing_email = User.query.filter_by(email=data['userEmail']).first()
        if existing_email:
            return jsonify({'error': 'Email do usuário já cadastrado'}), 400
        
        # Criar empresa
        company = Company(
            cnpj=data['cnpj'],
            name=data['companyName'],
            trade_name=data.get('tradeName', ''),
            email=data['email'],
            phone=data['phone'],
            address=data['address'],
            number=data.get('number', ''),
            complement=data.get('complement', ''),
            neighborhood=data.get('neighborhood', ''),
            city=data['city'],
            state=data['state'],
            zip_code=data['zipCode'],
            tax_regime=data.get('taxRegime', 'simples_nacional')
        )
        
        db.session.add(company)
        db.session.flush()  # Para obter o ID da empresa
        
        # Buscar role de admin
        admin_role = Role.query.filter_by(name='admin').first()
        if not admin_role:
            return jsonify({'error': 'Erro interno: role admin não encontrada'}), 500
        
        # Criar usuário administrador
        user = User(
            username=data['username'],
            email=data['userEmail'],
            first_name=data['firstName'],
            last_name=data['lastName'],
            role_id=admin_role.id,
            company_id=company.id
        )
        user.set_password(data['password'])
        
        db.session.add(user)
        db.session.flush()  # Para obter o ID do usuário
        
        # Criar estrutura básica para a empresa
        create_company_structure(company.id)
        
        db.session.commit()
        
        return jsonify({
            'message': 'Empresa e usuário criados com sucesso!',
            'company': {
                'id': company.id,
                'name': company.name,
                'cnpj': company.cnpj
            },
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'name': f"{user.first_name} {user.last_name}"
            }
        }), 201
        
    except Exception as e:
        db.session.rollback()
        print(f"Erro no registro: {str(e)}")
        return jsonify({'error': 'Erro interno do servidor'}), 500

def create_company_structure(company_id):
    """Cria estrutura básica para nova empresa"""
    from src.models.accounting import AccountType, Account, CostCenter
    from src.models.financial import BankAccount
    
    # Buscar tipos de conta
    account_types = AccountType.query.all()
    if not account_types:
        return  # Se não há tipos de conta, pular criação
    
    # Criar plano de contas básico
    basic_accounts = [
        # ATIVO CIRCULANTE
        {'code': '1.1.01', 'name': 'CAIXA E EQUIVALENTES DE CAIXA', 'type_code': '1.1', 'level': 3, 'analytical': False},
        {'code': '1.1.01.01', 'name': 'Caixa', 'type_code': '1.1', 'level': 4, 'analytical': True},
        {'code': '1.1.01.02', 'name': 'Bancos Conta Movimento', 'type_code': '1.1', 'level': 4, 'analytical': True},
        {'code': '1.1.02', 'name': 'CONTAS A RECEBER', 'type_code': '1.1', 'level': 3, 'analytical': False},
        {'code': '1.1.02.01', 'name': 'Clientes', 'type_code': '1.1', 'level': 4, 'analytical': True},
        
        # PASSIVO CIRCULANTE
        {'code': '2.1.01', 'name': 'FORNECEDORES', 'type_code': '2.1', 'level': 3, 'analytical': False},
        {'code': '2.1.01.01', 'name': 'Fornecedores Nacionais', 'type_code': '2.1', 'level': 4, 'analytical': True},
        {'code': '2.1.02', 'name': 'OBRIGAÇÕES TRABALHISTAS', 'type_code': '2.1', 'level': 3, 'analytical': False},
        {'code': '2.1.03', 'name': 'OBRIGAÇÕES TRIBUTÁRIAS', 'type_code': '2.1', 'level': 3, 'analytical': False},
        
        # PATRIMÔNIO LÍQUIDO
        {'code': '2.3.01', 'name': 'CAPITAL SOCIAL', 'type_code': '2.3', 'level': 3, 'analytical': True},
        {'code': '2.3.02', 'name': 'LUCROS ACUMULADOS', 'type_code': '2.3', 'level': 3, 'analytical': True},
        
        # RECEITAS
        {'code': '3.01', 'name': 'RECEITA BRUTA', 'type_code': '3', 'level': 2, 'analytical': False},
        {'code': '3.01.01', 'name': 'Vendas de Produtos', 'type_code': '3', 'level': 3, 'analytical': True},
        {'code': '3.01.02', 'name': 'Prestação de Serviços', 'type_code': '3', 'level': 3, 'analytical': True},
        
        # DESPESAS
        {'code': '4.01', 'name': 'CUSTOS DOS PRODUTOS VENDIDOS', 'type_code': '4', 'level': 2, 'analytical': False},
        {'code': '4.02', 'name': 'DESPESAS OPERACIONAIS', 'type_code': '4', 'level': 2, 'analytical': False},
        {'code': '4.02.01', 'name': 'Despesas Administrativas', 'type_code': '4', 'level': 3, 'analytical': True},
        {'code': '4.02.02', 'name': 'Despesas Comerciais', 'type_code': '4', 'level': 3, 'analytical': True},
    ]
    
    # Mapear tipos de conta por código
    type_map = {at.code: at.id for at in account_types}
    
    for acc_data in basic_accounts:
        # Encontrar o tipo de conta mais específico
        account_type_id = None
        for type_code in sorted(type_map.keys(), key=len, reverse=True):
            if acc_data['type_code'].startswith(type_code):
                account_type_id = type_map[type_code]
                break
        
        if account_type_id:
            account = Account(
                company_id=company_id,
                code=acc_data['code'],
                name=acc_data['name'],
                account_type_id=account_type_id,
                level=acc_data['level'],
                is_analytical=acc_data['analytical']
            )
            db.session.add(account)
    
    # Criar centro de custo padrão
    cost_center = CostCenter(
        company_id=company_id,
        code='001',
        name='Administração',
        description='Centro de custo administrativo'
    )
    db.session.add(cost_center)
    
    # Criar conta bancária padrão
    bank_account = BankAccount(
        company_id=company_id,
        bank_code='001',
        bank_name='Banco do Brasil',
        agency='0000',
        account_number='00000-0',
        account_digit='0',
        account_type='checking',
        initial_balance=0.00,
        current_balance=0.00
    )
    db.session.add(bank_account)

@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """Endpoint para obter dados do usuário atual"""
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({'error': 'Usuário não encontrado'}), 404
        
        return jsonify({'user': user.to_dict()}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/change-password', methods=['POST'])
@jwt_required()
def change_password():
    """Endpoint para alterar senha do usuário atual"""
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({'error': 'Usuário não encontrado'}), 404
        
        data = request.get_json()
        
        if not data.get('current_password') or not data.get('new_password'):
            return jsonify({'error': 'Senha atual e nova senha são obrigatórias'}), 400
        
        # Verificar senha atual
        if not user.check_password(data['current_password']):
            return jsonify({'error': 'Senha atual incorreta'}), 400
        
        # Atualizar senha
        user.set_password(data['new_password'])
        user.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({'message': 'Senha alterada com sucesso'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/update-profile', methods=['PUT'])
@jwt_required()
def update_profile():
    """Endpoint para atualizar perfil do usuário atual"""
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({'error': 'Usuário não encontrado'}), 404
        
        data = request.get_json()
        
        # Atualizar campos permitidos
        if 'first_name' in data:
            user.first_name = data['first_name']
        if 'last_name' in data:
            user.last_name = data['last_name']
        if 'email' in data:
            # Verificar se email já existe (exceto o próprio usuário)
            existing_user = User.query.filter(
                User.email == data['email'],
                User.id != user.id
            ).first()
            if existing_user:
                return jsonify({'error': 'Email já está em uso'}), 400
            user.email = data['email']
        
        user.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'message': 'Perfil atualizado com sucesso',
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

