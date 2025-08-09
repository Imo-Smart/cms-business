from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.models.user import db, User
from src.models.departments import Department, Permission, RolePermission, DepartmentModule, WorkflowStep, DepartmentMetric
from datetime import datetime, date
import json

departments_bp = Blueprint('departments', __name__)

# ==================== DEPARTAMENTOS ====================

@departments_bp.route('/departments', methods=['GET'])
@jwt_required()
def get_departments():
    """Listar departamentos com estrutura hierárquica"""
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({'error': 'Utilizador não encontrado'}), 404
        
        # Buscar departamentos raiz (sem parent)
        root_departments = Department.query.filter_by(parent_id=None, is_active=True).all()
        
        departments_data = []
        for dept in root_departments:
            departments_data.append(dept.to_dict())
        
        return jsonify({
            'success': True,
            'data': departments_data,
            'total': len(departments_data)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@departments_bp.route('/departments/hierarchy', methods=['GET'])
@jwt_required()
def get_departments_hierarchy():
    """Obter estrutura hierárquica completa dos departamentos"""
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({'error': 'Utilizador não encontrado'}), 404
        
        # Estrutura hierárquica da construtora
        hierarchy = {
            'name': 'CMS Business - Construtora',
            'departments': [
                {
                    'name': 'Diretoria Executiva',
                    'code': 'DIR',
                    'level': 1,
                    'children': [
                        {'name': 'Departamento Administrativo', 'code': 'ADM', 'level': 2},
                        {'name': 'Departamento Financeiro', 'code': 'FIN', 'level': 2},
                        {'name': 'Departamento Jurídico', 'code': 'JUR', 'level': 2},
                        {'name': 'Departamento de Auditoria e Compliance', 'code': 'AUD', 'level': 2}
                    ]
                },
                {
                    'name': 'Departamento de Recursos Humanos',
                    'code': 'RH',
                    'level': 1,
                    'children': []
                },
                {
                    'name': 'Departamento de Tecnologia da Informação',
                    'code': 'TI',
                    'level': 1,
                    'children': []
                },
                {
                    'name': 'Área Comercial',
                    'code': 'COM',
                    'level': 1,
                    'children': [
                        {'name': 'Departamento Comercial e Vendas', 'code': 'VEN', 'level': 2},
                        {'name': 'Departamento de Marketing e Comunicação', 'code': 'MKT', 'level': 2},
                        {'name': 'Departamento de Atendimento ao Cliente', 'code': 'SAC', 'level': 2}
                    ]
                },
                {
                    'name': 'Área de Engenharia e Projetos',
                    'code': 'ENG',
                    'level': 1,
                    'children': [
                        {'name': 'Departamento de Engenharia', 'code': 'ENG', 'level': 2},
                        {'name': 'Departamento de Projetos e Planejamento', 'code': 'PRJ', 'level': 2},
                        {'name': 'Departamento de Orçamentos e Custos', 'code': 'ORC', 'level': 2}
                    ]
                },
                {
                    'name': 'Área Operacional',
                    'code': 'OPE',
                    'level': 1,
                    'children': [
                        {'name': 'Departamento de Obras (Execução)', 'code': 'OBR', 'level': 2},
                        {'name': 'Departamento de Compras e Suprimentos', 'code': 'CPR', 'level': 2},
                        {'name': 'Departamento de Logística', 'code': 'LOG', 'level': 2},
                        {'name': 'Departamento de Controle de Produção', 'code': 'PCP', 'level': 2},
                        {'name': 'Departamento de Manutenção e Equipamentos', 'code': 'MAN', 'level': 2}
                    ]
                },
                {
                    'name': 'Área de Qualidade e Meio Ambiente',
                    'code': 'QMA',
                    'level': 1,
                    'children': [
                        {'name': 'Departamento de Qualidade e Segurança', 'code': 'QST', 'level': 2},
                        {'name': 'Departamento de Meio Ambiente', 'code': 'AMB', 'level': 2}
                    ]
                }
            ]
        }
        
        return jsonify({
            'success': True,
            'data': hierarchy
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@departments_bp.route('/departments/modules', methods=['GET'])
@jwt_required()
def get_department_modules():
    """Listar módulos disponíveis por departamento"""
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({'error': 'Utilizador não encontrado'}), 404
        
        # Módulos disponíveis por departamento
        modules_by_department = {
            'DIR': [  # Diretoria Executiva
                {'code': 'dashboard_executivo', 'name': 'Dashboard Executivo', 'price': 30.00},
                {'code': 'relatorios_gerenciais', 'name': 'Relatórios Gerenciais', 'price': 30.00},
                {'code': 'indicadores_kpi', 'name': 'Indicadores e KPIs', 'price': 30.00},
                {'code': 'aprovacoes', 'name': 'Sistema de Aprovações', 'price': 30.00}
            ],
            'ADM': [  # Administrativo
                {'code': 'gestao_documentos', 'name': 'Gestão de Documentos', 'price': 30.00},
                {'code': 'protocolo', 'name': 'Sistema de Protocolo', 'price': 30.00},
                {'code': 'contratos', 'name': 'Gestão de Contratos', 'price': 30.00}
            ],
            'FIN': [  # Financeiro
                {'code': 'contas_pagar', 'name': 'Contas a Pagar', 'price': 30.00},
                {'code': 'contas_receber', 'name': 'Contas a Receber', 'price': 30.00},
                {'code': 'fluxo_caixa', 'name': 'Fluxo de Caixa', 'price': 30.00},
                {'code': 'conciliacao_bancaria', 'name': 'Conciliação Bancária', 'price': 30.00},
                {'code': 'centro_custos', 'name': 'Centro de Custos', 'price': 30.00}
            ],
            'RH': [  # Recursos Humanos
                {'code': 'folha_pagamento', 'name': 'Folha de Pagamento', 'price': 30.00},
                {'code': 'ponto_eletronico', 'name': 'Ponto Eletrônico', 'price': 30.00},
                {'code': 'ferias_13', 'name': 'Férias e 13º Salário', 'price': 30.00},
                {'code': 'admissao_demissao', 'name': 'Admissão e Demissão', 'price': 30.00},
                {'code': 'treinamentos', 'name': 'Gestão de Treinamentos', 'price': 30.00}
            ],
            'VEN': [  # Vendas
                {'code': 'crm_vendas', 'name': 'CRM de Vendas', 'price': 30.00},
                {'code': 'propostas', 'name': 'Gestão de Propostas', 'price': 30.00},
                {'code': 'comissoes', 'name': 'Controle de Comissões', 'price': 30.00},
                {'code': 'pipeline_vendas', 'name': 'Pipeline de Vendas', 'price': 30.00}
            ],
            'ENG': [  # Engenharia
                {'code': 'projetos_tecnicos', 'name': 'Projetos Técnicos', 'price': 30.00},
                {'code': 'aprovacao_projetos', 'name': 'Aprovação de Projetos', 'price': 30.00},
                {'code': 'especificacoes', 'name': 'Especificações Técnicas', 'price': 30.00}
            ],
            'OBR': [  # Obras
                {'code': 'cronograma_obras', 'name': 'Cronograma de Obras', 'price': 30.00},
                {'code': 'medicao_obras', 'name': 'Medição de Obras', 'price': 30.00},
                {'code': 'diario_obras', 'name': 'Diário de Obras', 'price': 30.00},
                {'code': 'controle_materiais', 'name': 'Controle de Materiais', 'price': 30.00}
            ],
            'CPR': [  # Compras
                {'code': 'cotacoes', 'name': 'Sistema de Cotações', 'price': 30.00},
                {'code': 'pedidos_compra', 'name': 'Pedidos de Compra', 'price': 30.00},
                {'code': 'fornecedores', 'name': 'Cadastro de Fornecedores', 'price': 30.00},
                {'code': 'estoque', 'name': 'Controle de Estoque', 'price': 30.00}
            ],
            'QST': [  # Qualidade e Segurança
                {'code': 'auditorias', 'name': 'Sistema de Auditorias', 'price': 30.00},
                {'code': 'nao_conformidades', 'name': 'Não Conformidades', 'price': 30.00},
                {'code': 'seguranca_trabalho', 'name': 'Segurança do Trabalho', 'price': 30.00},
                {'code': 'certificacoes', 'name': 'Gestão de Certificações', 'price': 30.00}
            ]
        }
        
        return jsonify({
            'success': True,
            'data': modules_by_department
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@departments_bp.route('/departments/<int:department_id>/dashboard', methods=['GET'])
@jwt_required()
def get_department_dashboard(department_id):
    """Obter dados do dashboard específico do departamento"""
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({'error': 'Utilizador não encontrado'}), 404
        
        department = Department.query.get(department_id)
        if not department:
            return jsonify({'error': 'Departamento não encontrado'}), 404
        
        # Buscar métricas do departamento
        metrics = DepartmentMetric.query.filter_by(department_id=department_id).all()
        
        # Dados específicos por departamento
        dashboard_data = {
            'department': {
                'id': department.id,
                'name': department.name,
                'code': department.code
            },
            'metrics': [],
            'quick_actions': [],
            'notifications': [],
            'recent_activities': []
        }
        
        # Métricas específicas por tipo de departamento
        if department.code == 'FIN':  # Financeiro
            dashboard_data['metrics'] = [
                {'name': 'Saldo em Caixa', 'value': 'R$ 150.000,00', 'type': 'currency', 'trend': 'up'},
                {'name': 'Contas a Pagar', 'value': 'R$ 85.000,00', 'type': 'currency', 'trend': 'down'},
                {'name': 'Contas a Receber', 'value': 'R$ 220.000,00', 'type': 'currency', 'trend': 'up'},
                {'name': 'Inadimplência', 'value': '3.2%', 'type': 'percentage', 'trend': 'down'}
            ]
            dashboard_data['quick_actions'] = [
                {'name': 'Nova Conta a Pagar', 'icon': 'plus', 'url': '/financial/payables/new'},
                {'name': 'Conciliação Bancária', 'icon': 'bank', 'url': '/financial/reconciliation'},
                {'name': 'Relatório Fluxo de Caixa', 'icon': 'chart', 'url': '/financial/reports/cashflow'}
            ]
        elif department.code == 'VEN':  # Vendas
            dashboard_data['metrics'] = [
                {'name': 'Vendas do Mês', 'value': 'R$ 450.000,00', 'type': 'currency', 'trend': 'up'},
                {'name': 'Meta Atingida', 'value': '87%', 'type': 'percentage', 'trend': 'up'},
                {'name': 'Propostas Ativas', 'value': '23', 'type': 'number', 'trend': 'stable'},
                {'name': 'Taxa de Conversão', 'value': '15.8%', 'type': 'percentage', 'trend': 'up'}
            ]
            dashboard_data['quick_actions'] = [
                {'name': 'Nova Proposta', 'icon': 'plus', 'url': '/sales/proposals/new'},
                {'name': 'Acompanhar Pipeline', 'icon': 'pipeline', 'url': '/sales/pipeline'},
                {'name': 'Relatório de Vendas', 'icon': 'chart', 'url': '/sales/reports'}
            ]
        elif department.code == 'RH':  # RH
            dashboard_data['metrics'] = [
                {'name': 'Total Funcionários', 'value': '156', 'type': 'number', 'trend': 'up'},
                {'name': 'Admissões do Mês', 'value': '8', 'type': 'number', 'trend': 'up'},
                {'name': 'Turnover', 'value': '2.1%', 'type': 'percentage', 'trend': 'down'},
                {'name': 'Folha de Pagamento', 'value': 'R$ 380.000,00', 'type': 'currency', 'trend': 'stable'}
            ]
            dashboard_data['quick_actions'] = [
                {'name': 'Nova Admissão', 'icon': 'user-plus', 'url': '/hr/employees/new'},
                {'name': 'Processar Folha', 'icon': 'calculator', 'url': '/hr/payroll'},
                {'name': 'Relatório de Ponto', 'icon': 'clock', 'url': '/hr/timesheet'}
            ]
        elif department.code == 'OBR':  # Obras
            dashboard_data['metrics'] = [
                {'name': 'Obras Ativas', 'value': '12', 'type': 'number', 'trend': 'stable'},
                {'name': 'Obras no Prazo', 'value': '83%', 'type': 'percentage', 'trend': 'up'},
                {'name': 'Custo Médio m²', 'value': 'R$ 1.850,00', 'type': 'currency', 'trend': 'down'},
                {'name': 'Produtividade', 'value': '92%', 'type': 'percentage', 'trend': 'up'}
            ]
            dashboard_data['quick_actions'] = [
                {'name': 'Nova Medição', 'icon': 'ruler', 'url': '/construction/measurement/new'},
                {'name': 'Diário de Obra', 'icon': 'book', 'url': '/construction/diary'},
                {'name': 'Cronograma', 'icon': 'calendar', 'url': '/construction/schedule'}
            ]
        
        return jsonify({
            'success': True,
            'data': dashboard_data
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@departments_bp.route('/departments/workflows', methods=['GET'])
@jwt_required()
def get_department_workflows():
    """Obter workflows entre departamentos"""
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({'error': 'Utilizador não encontrado'}), 404
        
        # Workflows típicos de uma construtora
        workflows = [
            {
                'name': 'Aprovação de Projeto',
                'steps': [
                    {'department': 'Comercial', 'action': 'Recebe solicitação do cliente'},
                    {'department': 'Engenharia', 'action': 'Desenvolve projeto técnico'},
                    {'department': 'Orçamentos', 'action': 'Calcula custos do projeto'},
                    {'department': 'Diretoria', 'action': 'Aprova projeto e orçamento'},
                    {'department': 'Comercial', 'action': 'Apresenta proposta ao cliente'}
                ]
            },
            {
                'name': 'Execução de Obra',
                'steps': [
                    {'department': 'Comercial', 'action': 'Contrato assinado'},
                    {'department': 'Projetos', 'action': 'Finaliza projetos executivos'},
                    {'department': 'Compras', 'action': 'Adquire materiais'},
                    {'department': 'Obras', 'action': 'Inicia execução'},
                    {'department': 'Qualidade', 'action': 'Controla qualidade'},
                    {'department': 'Financeiro', 'action': 'Controla custos'}
                ]
            },
            {
                'name': 'Processo de Compras',
                'steps': [
                    {'department': 'Obras', 'action': 'Solicita material'},
                    {'department': 'Compras', 'action': 'Busca fornecedores'},
                    {'department': 'Orçamentos', 'action': 'Aprova valores'},
                    {'department': 'Financeiro', 'action': 'Libera pagamento'},
                    {'department': 'Logística', 'action': 'Recebe e distribui'}
                ]
            }
        ]
        
        return jsonify({
            'success': True,
            'data': workflows
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@departments_bp.route('/departments/integration-report', methods=['GET'])
@jwt_required()
def get_integration_report():
    """Relatório de integração entre departamentos"""
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({'error': 'Utilizador não encontrado'}), 404
        
        # Relatório de integração
        integration_data = {
            'total_departments': 20,
            'active_integrations': 45,
            'pending_approvals': 12,
            'data_sync_status': 'OK',
            'last_sync': datetime.now().isoformat(),
            'department_connections': [
                {'from': 'Comercial', 'to': 'Engenharia', 'status': 'active', 'last_interaction': '2025-08-09 10:30'},
                {'from': 'Engenharia', 'to': 'Orçamentos', 'status': 'active', 'last_interaction': '2025-08-09 09:15'},
                {'from': 'Orçamentos', 'to': 'Financeiro', 'status': 'active', 'last_interaction': '2025-08-09 11:20'},
                {'from': 'Compras', 'to': 'Obras', 'status': 'active', 'last_interaction': '2025-08-09 08:45'},
                {'from': 'RH', 'to': 'Financeiro', 'status': 'active', 'last_interaction': '2025-08-09 07:30'}
            ],
            'bottlenecks': [
                {'department': 'Aprovações Diretoria', 'pending_items': 8, 'avg_time': '2.5 dias'},
                {'department': 'Liberação Financeira', 'pending_items': 5, 'avg_time': '1.2 dias'}
            ]
        }
        
        return jsonify({
            'success': True,
            'data': integration_data
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

