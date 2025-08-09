from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime, date
from decimal import Decimal

from src.models.user import db, User
from src.models.fiscal import (
    TaxType, TaxRate, Customer, Product, 
    Invoice, InvoiceItem, InvoiceTax
)

fiscal_bp = Blueprint('fiscal', __name__)

# ==================== CLIENTES ====================

@fiscal_bp.route('/companies/<int:company_id>/customers', methods=['GET'])
@jwt_required()
def get_customers(company_id):
    """Listar clientes"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        search = request.args.get('search', '')
        
        query = Customer.query.filter_by(company_id=company_id, is_active=True)
        
        if search:
            query = query.filter(
                (Customer.name.contains(search)) |
                (Customer.document.contains(search)) |
                (Customer.email.contains(search))
            )
        
        customers = query.order_by(Customer.name).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return jsonify({
            'customers': [customer.to_dict() for customer in customers.items],
            'total': customers.total,
            'pages': customers.pages,
            'current_page': page
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@fiscal_bp.route('/companies/<int:company_id>/customers', methods=['POST'])
@jwt_required()
def create_customer(company_id):
    """Criar cliente"""
    try:
        data = request.get_json()
        
        # Verificar se documento já existe
        existing = Customer.query.filter_by(
            company_id=company_id,
            document=data['document']
        ).first()
        if existing:
            return jsonify({'error': 'Documento já cadastrado'}), 400
        
        customer = Customer(
            company_id=company_id,
            type=data['type'],
            document=data['document'],
            name=data['name'],
            trade_name=data.get('trade_name'),
            email=data.get('email'),
            phone=data.get('phone'),
            mobile=data.get('mobile'),
            address=data.get('address'),
            number=data.get('number'),
            complement=data.get('complement'),
            neighborhood=data.get('neighborhood'),
            city=data.get('city'),
            state=data.get('state'),
            zip_code=data.get('zip_code'),
            state_registration=data.get('state_registration'),
            municipal_registration=data.get('municipal_registration'),
            tax_regime=data.get('tax_regime')
        )
        
        db.session.add(customer)
        db.session.commit()
        
        return jsonify(customer.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@fiscal_bp.route('/customers/<int:customer_id>', methods=['GET'])
@jwt_required()
def get_customer(customer_id):
    """Obter cliente por ID"""
    try:
        customer = Customer.query.get_or_404(customer_id)
        return jsonify(customer.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@fiscal_bp.route('/customers/<int:customer_id>', methods=['PUT'])
@jwt_required()
def update_customer(customer_id):
    """Atualizar cliente"""
    try:
        customer = Customer.query.get_or_404(customer_id)
        data = request.get_json()
        
        # Atualizar campos
        fields = [
            'name', 'trade_name', 'email', 'phone', 'mobile', 'address', 
            'number', 'complement', 'neighborhood', 'city', 'state', 
            'zip_code', 'state_registration', 'municipal_registration', 'tax_regime'
        ]
        
        for field in fields:
            if field in data:
                setattr(customer, field, data[field])
        
        customer.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify(customer.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# ==================== PRODUTOS ====================

@fiscal_bp.route('/companies/<int:company_id>/products', methods=['GET'])
@jwt_required()
def get_products(company_id):
    """Listar produtos"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        search = request.args.get('search', '')
        product_type = request.args.get('type')
        
        query = Product.query.filter_by(company_id=company_id, is_active=True)
        
        if search:
            query = query.filter(
                (Product.name.contains(search)) |
                (Product.code.contains(search)) |
                (Product.description.contains(search))
            )
        
        if product_type:
            query = query.filter_by(type=product_type)
        
        products = query.order_by(Product.name).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return jsonify({
            'products': [product.to_dict() for product in products.items],
            'total': products.total,
            'pages': products.pages,
            'current_page': page
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@fiscal_bp.route('/companies/<int:company_id>/products', methods=['POST'])
@jwt_required()
def create_product(company_id):
    """Criar produto"""
    try:
        data = request.get_json()
        
        # Verificar se código já existe
        existing = Product.query.filter_by(
            company_id=company_id,
            code=data['code']
        ).first()
        if existing:
            return jsonify({'error': 'Código de produto já existe'}), 400
        
        product = Product(
            company_id=company_id,
            code=data['code'],
            name=data['name'],
            description=data.get('description'),
            type=data.get('type', 'product'),
            unit=data.get('unit', 'UN'),
            cost_price=Decimal(str(data.get('cost_price', 0))),
            sale_price=Decimal(str(data.get('sale_price', 0))),
            ncm=data.get('ncm'),
            cest=data.get('cest'),
            cfop_internal=data.get('cfop_internal'),
            cfop_external=data.get('cfop_external'),
            manage_stock=data.get('manage_stock', True),
            current_stock=Decimal(str(data.get('current_stock', 0))),
            minimum_stock=Decimal(str(data.get('minimum_stock', 0)))
        )
        
        db.session.add(product)
        db.session.commit()
        
        return jsonify(product.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@fiscal_bp.route('/products/<int:product_id>', methods=['GET'])
@jwt_required()
def get_product(product_id):
    """Obter produto por ID"""
    try:
        product = Product.query.get_or_404(product_id)
        return jsonify(product.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@fiscal_bp.route('/products/<int:product_id>', methods=['PUT'])
@jwt_required()
def update_product(product_id):
    """Atualizar produto"""
    try:
        product = Product.query.get_or_404(product_id)
        data = request.get_json()
        
        # Atualizar campos
        fields = [
            'name', 'description', 'type', 'unit', 'ncm', 'cest',
            'cfop_internal', 'cfop_external', 'manage_stock', 'minimum_stock'
        ]
        
        for field in fields:
            if field in data:
                setattr(product, field, data[field])
        
        # Campos decimais
        decimal_fields = ['cost_price', 'sale_price', 'current_stock']
        for field in decimal_fields:
            if field in data:
                setattr(product, field, Decimal(str(data[field])))
        
        product.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify(product.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# ==================== NOTAS FISCAIS ====================

@fiscal_bp.route('/companies/<int:company_id>/invoices', methods=['GET'])
@jwt_required()
def get_invoices(company_id):
    """Listar notas fiscais"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = Invoice.query.filter_by(company_id=company_id)
        
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(Invoice.issue_date >= datetime.strptime(start_date, '%Y-%m-%d'))
        if end_date:
            query = query.filter(Invoice.issue_date <= datetime.strptime(end_date, '%Y-%m-%d'))
        
        invoices = query.order_by(Invoice.issue_date.desc(), Invoice.number.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return jsonify({
            'invoices': [invoice.to_dict() for invoice in invoices.items],
            'total': invoices.total,
            'pages': invoices.pages,
            'current_page': page
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@fiscal_bp.route('/companies/<int:company_id>/invoices', methods=['POST'])
@jwt_required()
def create_invoice(company_id):
    """Criar nota fiscal"""
    try:
        data = request.get_json()
        current_user_id = get_jwt_identity()
        
        # Gerar número da nota fiscal
        last_invoice = Invoice.query.filter_by(
            company_id=company_id,
            series=data.get('series', '1')
        ).order_by(Invoice.number.desc()).first()
        
        next_number = (last_invoice.number + 1) if last_invoice else 1
        
        # Criar nota fiscal
        invoice = Invoice(
            company_id=company_id,
            customer_id=data['customer_id'],
            number=next_number,
            series=data.get('series', '1'),
            type=data.get('type', 'nfe'),
            model=data.get('model', '55'),
            issue_date=datetime.strptime(data['issue_date'], '%Y-%m-%d %H:%M:%S'),
            due_date=datetime.strptime(data['due_date'], '%Y-%m-%d').date() if data.get('due_date') else None,
            discount_value=Decimal(str(data.get('discount_value', 0))),
            freight_value=Decimal(str(data.get('freight_value', 0))),
            insurance_value=Decimal(str(data.get('insurance_value', 0))),
            other_expenses=Decimal(str(data.get('other_expenses', 0))),
            additional_info=data.get('additional_info'),
            internal_notes=data.get('internal_notes'),
            created_by=current_user_id
        )
        
        db.session.add(invoice)
        db.session.flush()  # Para obter o ID
        
        # Criar itens da nota fiscal
        for item_data in data['items']:
            item = InvoiceItem(
                invoice_id=invoice.id,
                product_id=item_data['product_id'],
                sequence=item_data['sequence'],
                quantity=Decimal(str(item_data['quantity'])),
                unit_price=Decimal(str(item_data['unit_price'])),
                total_value=Decimal(str(item_data['total_value'])),
                discount_value=Decimal(str(item_data.get('discount_value', 0))),
                cfop=item_data['cfop'],
                ncm=item_data.get('ncm'),
                cest=item_data.get('cest'),
                icms_origin=item_data.get('icms_origin', '0'),
                icms_cst=item_data.get('icms_cst'),
                icms_base=Decimal(str(item_data.get('icms_base', 0))),
                icms_rate=Decimal(str(item_data.get('icms_rate', 0))),
                icms_value=Decimal(str(item_data.get('icms_value', 0))),
                ipi_cst=item_data.get('ipi_cst'),
                ipi_rate=Decimal(str(item_data.get('ipi_rate', 0))),
                ipi_value=Decimal(str(item_data.get('ipi_value', 0))),
                pis_cst=item_data.get('pis_cst'),
                pis_rate=Decimal(str(item_data.get('pis_rate', 0))),
                pis_value=Decimal(str(item_data.get('pis_value', 0))),
                cofins_cst=item_data.get('cofins_cst'),
                cofins_rate=Decimal(str(item_data.get('cofins_rate', 0))),
                cofins_value=Decimal(str(item_data.get('cofins_value', 0)))
            )
            db.session.add(item)
        
        # Calcular totais
        invoice.calculate_totals()
        
        db.session.commit()
        
        return jsonify(invoice.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@fiscal_bp.route('/invoices/<int:invoice_id>', methods=['GET'])
@jwt_required()
def get_invoice(invoice_id):
    """Obter nota fiscal"""
    try:
        invoice = Invoice.query.get_or_404(invoice_id)
        return jsonify(invoice.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@fiscal_bp.route('/invoices/<int:invoice_id>', methods=['PUT'])
@jwt_required()
def update_invoice(invoice_id):
    """Atualizar nota fiscal"""
    try:
        invoice = Invoice.query.get_or_404(invoice_id)
        
        if invoice.status != 'draft':
            return jsonify({'error': 'Apenas notas em rascunho podem ser editadas'}), 400
        
        data = request.get_json()
        
        # Atualizar campos básicos
        fields = [
            'due_date', 'discount_value', 'freight_value', 
            'insurance_value', 'other_expenses', 'additional_info', 'internal_notes'
        ]
        
        for field in fields:
            if field in data:
                if field == 'due_date' and data[field]:
                    setattr(invoice, field, datetime.strptime(data[field], '%Y-%m-%d').date())
                elif field in ['discount_value', 'freight_value', 'insurance_value', 'other_expenses']:
                    setattr(invoice, field, Decimal(str(data[field])))
                else:
                    setattr(invoice, field, data[field])
        
        # Recalcular totais
        invoice.calculate_totals()
        invoice.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify(invoice.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@fiscal_bp.route('/invoices/<int:invoice_id>/issue', methods=['POST'])
@jwt_required()
def issue_invoice(invoice_id):
    """Emitir nota fiscal"""
    try:
        invoice = Invoice.query.get_or_404(invoice_id)
        
        if invoice.status != 'draft':
            return jsonify({'error': 'Apenas notas em rascunho podem ser emitidas'}), 400
        
        # Aqui seria implementada a integração com SEFAZ
        # Por enquanto, apenas simular a emissão
        
        invoice.status = 'issued'
        invoice.access_key = f"35{datetime.now().strftime('%y%m')}{invoice.company.cnpj.replace('.', '').replace('/', '').replace('-', '')}{invoice.model}{invoice.series.zfill(3)}{invoice.number:09d}{invoice.id:08d}1"
        invoice.authorization_protocol = f"135{datetime.now().strftime('%y%m%d%H%M%S')}{invoice.id:06d}"
        
        db.session.commit()
        
        return jsonify({
            'message': 'Nota fiscal emitida com sucesso',
            'access_key': invoice.access_key,
            'authorization_protocol': invoice.authorization_protocol
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@fiscal_bp.route('/invoices/<int:invoice_id>/cancel', methods=['POST'])
@jwt_required()
def cancel_invoice(invoice_id):
    """Cancelar nota fiscal"""
    try:
        invoice = Invoice.query.get_or_404(invoice_id)
        data = request.get_json()
        
        if invoice.status not in ['issued']:
            return jsonify({'error': 'Apenas notas emitidas podem ser canceladas'}), 400
        
        # Aqui seria implementada a integração com SEFAZ para cancelamento
        # Por enquanto, apenas simular o cancelamento
        
        invoice.status = 'cancelled'
        invoice.internal_notes = f"{invoice.internal_notes or ''}\nCancelada em {datetime.now().strftime('%d/%m/%Y %H:%M')}. Motivo: {data.get('reason', 'Não informado')}"
        
        db.session.commit()
        
        return jsonify({'message': 'Nota fiscal cancelada com sucesso'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# ==================== TIPOS DE IMPOSTOS ====================

@fiscal_bp.route('/tax-types', methods=['GET'])
@jwt_required()
def get_tax_types():
    """Listar tipos de impostos"""
    try:
        tax_types = TaxType.query.filter_by(is_active=True).all()
        return jsonify([tax_type.to_dict() for tax_type in tax_types]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@fiscal_bp.route('/tax-types/<int:tax_type_id>/rates', methods=['GET'])
@jwt_required()
def get_tax_rates(tax_type_id):
    """Listar alíquotas de um imposto"""
    try:
        state = request.args.get('state')
        
        query = TaxRate.query.filter_by(tax_type_id=tax_type_id, is_active=True)
        
        if state:
            query = query.filter_by(state=state)
        
        rates = query.order_by(TaxRate.start_date.desc()).all()
        
        return jsonify([rate.to_dict() for rate in rates]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ==================== RELATÓRIOS FISCAIS ====================

@fiscal_bp.route('/companies/<int:company_id>/fiscal-summary', methods=['GET'])
@jwt_required()
def get_fiscal_summary(company_id):
    """Resumo fiscal"""
    try:
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        if not start_date or not end_date:
            return jsonify({'error': 'Período obrigatório'}), 400
        
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
        
        # Buscar notas fiscais do período
        invoices = Invoice.query.filter(
            Invoice.company_id == company_id,
            Invoice.issue_date >= start_date,
            Invoice.issue_date <= end_date,
            Invoice.status == 'issued'
        ).all()
        
        # Calcular totais
        total_invoices = len(invoices)
        total_revenue = sum([invoice.total_value for invoice in invoices])
        total_icms = sum([invoice.icms_value for invoice in invoices])
        total_ipi = sum([invoice.ipi_value for invoice in invoices])
        total_pis = sum([invoice.pis_value for invoice in invoices])
        total_cofins = sum([invoice.cofins_value for invoice in invoices])
        total_iss = sum([invoice.iss_value for invoice in invoices])
        
        # Agrupar por tipo de nota
        nfe_count = len([i for i in invoices if i.type == 'nfe'])
        nfce_count = len([i for i in invoices if i.type == 'nfce'])
        nfse_count = len([i for i in invoices if i.type == 'nfse'])
        
        return jsonify({
            'company_id': company_id,
            'period': {
                'start_date': start_date.strftime('%Y-%m-%d'),
                'end_date': end_date.strftime('%Y-%m-%d')
            },
            'summary': {
                'total_invoices': total_invoices,
                'total_revenue': float(total_revenue),
                'total_taxes': float(total_icms + total_ipi + total_pis + total_cofins + total_iss),
                'taxes_breakdown': {
                    'icms': float(total_icms),
                    'ipi': float(total_ipi),
                    'pis': float(total_pis),
                    'cofins': float(total_cofins),
                    'iss': float(total_iss)
                },
                'invoice_types': {
                    'nfe': nfe_count,
                    'nfce': nfce_count,
                    'nfse': nfse_count
                }
            }
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

