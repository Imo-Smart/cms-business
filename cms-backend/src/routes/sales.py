from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.models.user import db, User
from src.models.fiscal import Customer, Product, Invoice, InvoiceItem, InvoiceTax
from src.models.accounting import Company
from datetime import datetime, date
import json

sales_bp = Blueprint('sales', __name__)

# ==================== CLIENTES ====================

@sales_bp.route('/customers', methods=['GET'])
@jwt_required()
def get_customers():
    """Listar clientes"""
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({'error': 'Utilizador não encontrado'}), 404
        
        company = Company.query.first()
        if not company:
            return jsonify({'error': 'Empresa não encontrada'}), 404
        
        customers = Customer.query.filter_by(company_id=company.id).all()
        
        customers_data = []
        for customer in customers:
            customers_data.append({
                'id': customer.id,
                'type': customer.type,
                'document': customer.document,
                'name': customer.name,
                'trade_name': customer.trade_name,
                'email': customer.email,
                'phone': customer.phone,
                'address': customer.address,
                'city': customer.city,
                'state': customer.state,
                'zip_code': customer.zip_code,
                'tax_regime': customer.tax_regime,
                'is_active': customer.is_active,
                'created_at': customer.created_at.isoformat() if customer.created_at else None
            })
        
        return jsonify({
            'success': True,
            'data': customers_data,
            'total': len(customers_data)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@sales_bp.route('/customers', methods=['POST'])
@jwt_required()
def create_customer():
    """Criar novo cliente"""
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
        existing_customer = Customer.query.filter_by(
            company_id=company.id,
            document=data['document']
        ).first()
        
        if existing_customer:
            return jsonify({'error': 'Já existe um cliente com este documento'}), 400
        
        customer = Customer(
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
            tax_regime=data.get('tax_regime', 'simples_nacional'),
            is_active=data.get('is_active', True)
        )
        
        db.session.add(customer)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Cliente criado com sucesso',
            'data': {
                'id': customer.id,
                'name': customer.name,
                'document': customer.document
            }
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@sales_bp.route('/customers/<int:customer_id>', methods=['PUT'])
@jwt_required()
def update_customer(customer_id):
    """Atualizar cliente"""
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({'error': 'Utilizador não encontrado'}), 404
        
        company = Company.query.first()
        if not company:
            return jsonify({'error': 'Empresa não encontrada'}), 404
        
        customer = Customer.query.filter_by(id=customer_id, company_id=company.id).first()
        if not customer:
            return jsonify({'error': 'Cliente não encontrado'}), 404
        
        data = request.get_json()
        
        # Atualizar campos
        if 'name' in data:
            customer.name = data['name']
        if 'trade_name' in data:
            customer.trade_name = data['trade_name']
        if 'email' in data:
            customer.email = data['email']
        if 'phone' in data:
            customer.phone = data['phone']
        if 'address' in data:
            customer.address = data['address']
        if 'city' in data:
            customer.city = data['city']
        if 'state' in data:
            customer.state = data['state']
        if 'zip_code' in data:
            customer.zip_code = data['zip_code']
        if 'tax_regime' in data:
            customer.tax_regime = data['tax_regime']
        if 'is_active' in data:
            customer.is_active = data['is_active']
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Cliente atualizado com sucesso'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# ==================== PRODUTOS ====================

@sales_bp.route('/products', methods=['GET'])
@jwt_required()
def get_products():
    """Listar produtos"""
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({'error': 'Utilizador não encontrado'}), 404
        
        company = Company.query.first()
        if not company:
            return jsonify({'error': 'Empresa não encontrada'}), 404
        
        products = Product.query.filter_by(company_id=company.id).all()
        
        products_data = []
        for product in products:
            products_data.append({
                'id': product.id,
                'code': product.code,
                'name': product.name,
                'description': product.description,
                'type': product.type,
                'unit': product.unit,
                'cost_price': float(product.cost_price),
                'sale_price': float(product.sale_price),
                'ncm': product.ncm,
                'cfop_internal': product.cfop_internal,
                'cfop_external': product.cfop_external,
                'current_stock': float(product.current_stock),
                'minimum_stock': float(product.minimum_stock),
                'is_active': product.is_active,
                'created_at': product.created_at.isoformat() if product.created_at else None
            })
        
        return jsonify({
            'success': True,
            'data': products_data,
            'total': len(products_data)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@sales_bp.route('/products', methods=['POST'])
@jwt_required()
def create_product():
    """Criar novo produto"""
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
        required_fields = ['code', 'name', 'type', 'unit', 'sale_price']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'Campo {field} é obrigatório'}), 400
        
        # Verificar se código já existe
        existing_product = Product.query.filter_by(
            company_id=company.id,
            code=data['code']
        ).first()
        
        if existing_product:
            return jsonify({'error': 'Já existe um produto com este código'}), 400
        
        product = Product(
            company_id=company.id,
            code=data['code'],
            name=data['name'],
            description=data.get('description', ''),
            type=data['type'],
            unit=data['unit'],
            cost_price=float(data.get('cost_price', 0)),
            sale_price=float(data['sale_price']),
            ncm=data.get('ncm', ''),
            cfop_internal=data.get('cfop_internal', '5102'),
            cfop_external=data.get('cfop_external', '6102'),
            current_stock=float(data.get('current_stock', 0)),
            minimum_stock=float(data.get('minimum_stock', 0)),
            is_active=data.get('is_active', True)
        )
        
        db.session.add(product)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Produto criado com sucesso',
            'data': {
                'id': product.id,
                'code': product.code,
                'name': product.name
            }
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@sales_bp.route('/products/<int:product_id>', methods=['PUT'])
@jwt_required()
def update_product(product_id):
    """Atualizar produto"""
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({'error': 'Utilizador não encontrado'}), 404
        
        company = Company.query.first()
        if not company:
            return jsonify({'error': 'Empresa não encontrada'}), 404
        
        product = Product.query.filter_by(id=product_id, company_id=company.id).first()
        if not product:
            return jsonify({'error': 'Produto não encontrado'}), 404
        
        data = request.get_json()
        
        # Atualizar campos
        if 'name' in data:
            product.name = data['name']
        if 'description' in data:
            product.description = data['description']
        if 'cost_price' in data:
            product.cost_price = float(data['cost_price'])
        if 'sale_price' in data:
            product.sale_price = float(data['sale_price'])
        if 'current_stock' in data:
            product.current_stock = float(data['current_stock'])
        if 'minimum_stock' in data:
            product.minimum_stock = float(data['minimum_stock'])
        if 'is_active' in data:
            product.is_active = data['is_active']
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Produto atualizado com sucesso'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# ==================== VENDAS/FATURAS ====================

@sales_bp.route('/invoices', methods=['GET'])
@jwt_required()
def get_invoices():
    """Listar faturas/vendas"""
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
        
        query = Invoice.query.filter_by(company_id=company.id)
        
        if status:
            query = query.filter_by(status=status)
        if customer_id:
            query = query.filter_by(customer_id=customer_id)
        
        invoices = query.order_by(Invoice.created_at.desc()).all()
        
        invoices_data = []
        for invoice in invoices:
            customer = Customer.query.get(invoice.customer_id) if invoice.customer_id else None
            
            # Buscar itens da fatura
            items = InvoiceItem.query.filter_by(invoice_id=invoice.id).all()
            items_data = []
            for item in items:
                product = Product.query.get(item.product_id) if item.product_id else None
                items_data.append({
                    'id': item.id,
                    'product': {
                        'id': product.id if product else None,
                        'name': product.name if product else item.description,
                        'code': product.code if product else ''
                    },
                    'description': item.description,
                    'quantity': float(item.quantity),
                    'unit_price': float(item.unit_price),
                    'total_price': float(item.total_price)
                })
            
            invoices_data.append({
                'id': invoice.id,
                'number': invoice.number,
                'series': invoice.series,
                'customer': {
                    'id': customer.id if customer else None,
                    'name': customer.name if customer else 'Cliente não informado',
                    'document': customer.document if customer else ''
                },
                'issue_date': invoice.issue_date.isoformat() if invoice.issue_date else None,
                'due_date': invoice.due_date.isoformat() if invoice.due_date else None,
                'subtotal': float(invoice.subtotal),
                'tax_amount': float(invoice.tax_amount),
                'total_amount': float(invoice.total_amount),
                'status': invoice.status,
                'items': items_data,
                'created_at': invoice.created_at.isoformat() if invoice.created_at else None
            })
        
        return jsonify({
            'success': True,
            'data': invoices_data,
            'total': len(invoices_data)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@sales_bp.route('/invoices', methods=['POST'])
@jwt_required()
def create_invoice():
    """Criar nova fatura/venda"""
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
        required_fields = ['customer_id', 'items']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'Campo {field} é obrigatório'}), 400
        
        if not data['items'] or len(data['items']) == 0:
            return jsonify({'error': 'A fatura deve ter pelo menos um item'}), 400
        
        # Verificar se cliente existe
        customer = Customer.query.filter_by(id=data['customer_id'], company_id=company.id).first()
        if not customer:
            return jsonify({'error': 'Cliente não encontrado'}), 404
        
        # Gerar número da fatura
        last_invoice = Invoice.query.filter_by(company_id=company.id).order_by(Invoice.id.desc()).first()
        next_number = (last_invoice.number + 1) if last_invoice else 1
        
        # Converter datas
        issue_date = datetime.strptime(data.get('issue_date', datetime.now().strftime('%Y-%m-%d')), '%Y-%m-%d').date()
        due_date = datetime.strptime(data.get('due_date', issue_date.strftime('%Y-%m-%d')), '%Y-%m-%d').date()
        
        # Calcular totais
        subtotal = 0
        for item_data in data['items']:
            quantity = float(item_data['quantity'])
            unit_price = float(item_data['unit_price'])
            subtotal += quantity * unit_price
        
        tax_amount = float(data.get('tax_amount', 0))
        total_amount = subtotal + tax_amount
        
        # Criar fatura
        invoice = Invoice(
            company_id=company.id,
            customer_id=data['customer_id'],
            number=next_number,
            series=data.get('series', '1'),
            issue_date=issue_date,
            due_date=due_date,
            subtotal=subtotal,
            tax_amount=tax_amount,
            total_amount=total_amount,
            status='draft'
        )
        
        db.session.add(invoice)
        db.session.flush()  # Para obter o ID da fatura
        
        # Criar itens da fatura
        for item_data in data['items']:
            quantity = float(item_data['quantity'])
            unit_price = float(item_data['unit_price'])
            total_price = quantity * unit_price
            
            item = InvoiceItem(
                invoice_id=invoice.id,
                product_id=item_data.get('product_id'),
                description=item_data['description'],
                quantity=quantity,
                unit_price=unit_price,
                total_price=total_price
            )
            
            db.session.add(item)
            
            # Atualizar estoque se for produto
            if item_data.get('product_id'):
                product = Product.query.get(item_data['product_id'])
                if product:
                    product.current_stock -= quantity
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Fatura criada com sucesso',
            'data': {
                'id': invoice.id,
                'number': invoice.number,
                'total_amount': float(invoice.total_amount)
            }
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# ==================== RELATÓRIOS DE VENDAS ====================

@sales_bp.route('/reports/sales-summary', methods=['GET'])
@jwt_required()
def get_sales_summary():
    """Relatório resumo de vendas"""
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
        
        # Vendas no período
        invoices = Invoice.query.filter(
            Invoice.company_id == company.id,
            Invoice.issue_date >= start_date,
            Invoice.issue_date <= end_date,
            Invoice.status.in_(['confirmed', 'paid'])
        ).all()
        
        # Calcular métricas
        total_sales = sum(float(invoice.total_amount) for invoice in invoices)
        total_invoices = len(invoices)
        average_ticket = total_sales / total_invoices if total_invoices > 0 else 0
        
        # Vendas por cliente
        customer_sales = {}
        for invoice in invoices:
            customer_id = invoice.customer_id
            if customer_id not in customer_sales:
                customer = Customer.query.get(customer_id)
                customer_sales[customer_id] = {
                    'customer_name': customer.name if customer else 'N/A',
                    'total_amount': 0,
                    'invoice_count': 0
                }
            
            customer_sales[customer_id]['total_amount'] += float(invoice.total_amount)
            customer_sales[customer_id]['invoice_count'] += 1
        
        # Top 10 clientes
        top_customers = sorted(
            customer_sales.values(),
            key=lambda x: x['total_amount'],
            reverse=True
        )[:10]
        
        # Vendas por produto
        product_sales = {}
        for invoice in invoices:
            items = InvoiceItem.query.filter_by(invoice_id=invoice.id).all()
            for item in items:
                product_id = item.product_id
                if product_id:
                    if product_id not in product_sales:
                        product = Product.query.get(product_id)
                        product_sales[product_id] = {
                            'product_name': product.name if product else 'N/A',
                            'total_quantity': 0,
                            'total_amount': 0
                        }
                    
                    product_sales[product_id]['total_quantity'] += float(item.quantity)
                    product_sales[product_id]['total_amount'] += float(item.total_price)
        
        # Top 10 produtos
        top_products = sorted(
            product_sales.values(),
            key=lambda x: x['total_amount'],
            reverse=True
        )[:10]
        
        return jsonify({
            'success': True,
            'data': {
                'period': {
                    'start_date': start_date.isoformat(),
                    'end_date': end_date.isoformat()
                },
                'summary': {
                    'total_sales': total_sales,
                    'total_invoices': total_invoices,
                    'average_ticket': average_ticket
                },
                'top_customers': top_customers,
                'top_products': top_products
            }
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ==================== DASHBOARD DE VENDAS ====================

@sales_bp.route('/dashboard', methods=['GET'])
@jwt_required()
def get_sales_dashboard():
    """Obter dados do dashboard de vendas"""
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({'error': 'Utilizador não encontrado'}), 404
        
        company = Company.query.first()
        if not company:
            return jsonify({'error': 'Empresa não encontrada'}), 404
        
        today = date.today()
        
        # Vendas do mês atual
        month_start = today.replace(day=1)
        monthly_sales = db.session.query(db.func.sum(Invoice.total_amount)).filter(
            Invoice.company_id == company.id,
            Invoice.issue_date >= month_start,
            Invoice.status.in_(['confirmed', 'paid'])
        ).scalar() or 0
        
        # Vendas do dia
        daily_sales = db.session.query(db.func.sum(Invoice.total_amount)).filter(
            Invoice.company_id == company.id,
            Invoice.issue_date == today,
            Invoice.status.in_(['confirmed', 'paid'])
        ).scalar() or 0
        
        # Total de clientes
        total_customers = Customer.query.filter_by(company_id=company.id, is_active=True).count()
        
        # Total de produtos
        total_products = Product.query.filter_by(company_id=company.id, is_active=True).count()
        
        # Produtos com estoque baixo
        low_stock_products = Product.query.filter(
            Product.company_id == company.id,
            Product.is_active == True,
            Product.current_stock <= Product.minimum_stock
        ).count()
        
        # Faturas pendentes
        pending_invoices = Invoice.query.filter_by(
            company_id=company.id,
            status='draft'
        ).count()
        
        return jsonify({
            'success': True,
            'data': {
                'monthly_sales': float(monthly_sales),
                'daily_sales': float(daily_sales),
                'total_customers': total_customers,
                'total_products': total_products,
                'low_stock_products': low_stock_products,
                'pending_invoices': pending_invoices
            }
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

