#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
IMPLEMENTAÇÃO DE CONTROLE DE ACESSO POR USUÁRIO
Sistema FinanceSync Pro - Controle de Conciliações por Usuário
"""

from app import db, app, Usuario, ContaBancaria, ExtratoBancario, LancamentoContabil, Conciliacao
from flask_login import current_user
from functools import wraps
from flask import jsonify

def implementar_controle_acesso():
    """Implementa controle de acesso por usuário nas tabelas"""
    
    print("🔐 IMPLEMENTANDO CONTROLE DE ACESSO POR USUÁRIO")
    print("=" * 60)
    
    # Verificar se campos de usuário já existem
    with app.app_context():
        try:
            # Testar se colunas já existem
            db.session.execute("SELECT usuario_id FROM extrato_bancario LIMIT 1")
            print("✅ Campo usuario_id já existe em extrato_bancario")
        except:
            print("➕ Adicionando campo usuario_id em extrato_bancario...")
            db.session.execute("ALTER TABLE extrato_bancario ADD COLUMN usuario_id INTEGER")
            db.session.execute("ALTER TABLE extrato_bancario ADD FOREIGN KEY (usuario_id) REFERENCES usuario(id)")
        
        try:
            db.session.execute("SELECT usuario_id FROM lancamento_contabil LIMIT 1")
            print("✅ Campo usuario_id já existe em lancamento_contabil")
        except:
            print("➕ Adicionando campo usuario_id em lancamento_contabil...")
            db.session.execute("ALTER TABLE lancamento_contabil ADD COLUMN usuario_id INTEGER")
            db.session.execute("ALTER TABLE lancamento_contabil ADD FOREIGN KEY (usuario_id) REFERENCES usuario(id)")
        
        try:
            db.session.execute("SELECT usuario_id FROM conta_bancaria LIMIT 1")
            print("✅ Campo usuario_id já existe em conta_bancaria")
        except:
            print("➕ Adicionando campo usuario_id em conta_bancaria...")
            db.session.execute("ALTER TABLE conta_bancaria ADD COLUMN usuario_id INTEGER")
            db.session.execute("ALTER TABLE conta_bancaria ADD FOREIGN KEY (usuario_id) REFERENCES usuario(id)")
        
        db.session.commit()
        print("✅ Controle de acesso implementado com sucesso!")

def requires_permission(action='read'):
    """Decorator para controlar permissões"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                return jsonify({'error': 'Usuário não autenticado'}), 401
            
            # Admins têm acesso total
            if current_user.perfil == 'admin':
                return f(*args, **kwargs)
            
            # Auditores podem ler tudo, mas não modificar
            if current_user.perfil == 'auditor' and action == 'read':
                return f(*args, **kwargs)
            elif current_user.perfil == 'auditor' and action != 'read':
                return jsonify({'error': 'Auditores não podem modificar dados'}), 403
            
            # Usuários normais só acessam seus próprios dados
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def filter_by_user_access(query, model, user=None):
    """Filtra query baseado no acesso do usuário"""
    if not user:
        user = current_user
    
    # Admin vê tudo
    if user.perfil == 'admin':
        return query
    
    # Auditor vê tudo (apenas leitura)
    if user.perfil == 'auditor':
        return query
    
    # Usuário normal vê apenas seus dados
    if model == ExtratoBancario:
        return query.filter(ExtratoBancario.usuario_id == user.id)
    elif model == LancamentoContabil:
        return query.filter(LancamentoContabil.usuario_id == user.id)
    elif model == ContaBancaria:
        return query.filter(ContaBancaria.usuario_id == user.id)
    elif model == Conciliacao:
        return query.filter(Conciliacao.usuario_id == user.id)
    
    return query

def get_user_statistics(user_id=None):
    """Retorna estatísticas específicas do usuário"""
    if not user_id:
        user_id = current_user.id
    
    user = Usuario.query.get(user_id)
    if not user:
        return None
    
    # Admin/Auditor podem ver estatísticas de qualquer usuário
    if current_user.perfil not in ['admin', 'auditor'] and user_id != current_user.id:
        return None
    
    with app.app_context():
        # Contas do usuário
        contas = ContaBancaria.query.filter_by(usuario_id=user_id).count()
        
        # Extratos do usuário
        extratos = ExtratoBancario.query.filter_by(usuario_id=user_id).count()
        extratos_conciliados = ExtratoBancario.query.filter_by(
            usuario_id=user_id, 
            conciliado=True
        ).count()
        
        # Lançamentos do usuário
        lancamentos = LancamentoContabil.query.filter_by(usuario_id=user_id).count()
        lancamentos_conciliados = LancamentoContabil.query.filter_by(
            usuario_id=user_id, 
            conciliado=True
        ).count()
        
        # Conciliações realizadas
        conciliacoes = Conciliacao.query.filter_by(usuario_id=user_id).count()
        
        return {
            'usuario': {
                'id': user.id,
                'nome': user.nome_completo,
                'username': user.username,
                'perfil': user.perfil
            },
            'estatisticas': {
                'contas_bancarias': contas,
                'extratos_total': extratos,
                'extratos_conciliados': extratos_conciliados,
                'extratos_pendentes': extratos - extratos_conciliados,
                'lancamentos_total': lancamentos,
                'lancamentos_conciliados': lancamentos_conciliados,
                'lancamentos_pendentes': lancamentos - lancamentos_conciliados,
                'conciliacoes_realizadas': conciliacoes,
                'taxa_conciliacao': round((extratos_conciliados / extratos * 100) if extratos > 0 else 0, 2)
            }
        }

def assign_data_to_user(data_type, data_id, user_id):
    """Atribui dados específicos a um usuário"""
    with app.app_context():
        if data_type == 'extrato':
            extrato = ExtratoBancario.query.get(data_id)
            if extrato:
                extrato.usuario_id = user_id
                db.session.commit()
                return True
        
        elif data_type == 'lancamento':
            lancamento = LancamentoContabil.query.get(data_id)
            if lancamento:
                lancamento.usuario_id = user_id
                db.session.commit()
                return True
        
        elif data_type == 'conta':
            conta = ContaBancaria.query.get(data_id)
            if conta:
                conta.usuario_id = user_id
                db.session.commit()
                return True
    
    return False

if __name__ == "__main__":
    implementar_controle_acesso()
    
    print("\n📋 EXEMPLO DE USO:")
    print("=" * 60)
    
    print("""
    # 1. Filtrar extratos por usuário
    from app import filter_by_user_access, ExtratoBancario
    
    query = ExtratoBancario.query
    extratos_usuario = filter_by_user_access(query, ExtratoBancario)
    
    # 2. Verificar permissões
    @requires_permission('write')
    def criar_conciliacao():
        # Código para criar conciliação
        pass
    
    # 3. Estatísticas do usuário
    stats = get_user_statistics(user_id=1)
    print(stats)
    
    # 4. Atribuir dados a usuário
    assign_data_to_user('extrato', extrato_id=1, user_id=2)
    """)
    
    print("\n🔒 NÍVEIS DE ACESSO:")
    print("=" * 60)
    print("👑 ADMIN: Acesso total a todos os dados")
    print("🔍 AUDITOR: Acesso de leitura a todos os dados")
    print("👤 USUÁRIO: Acesso apenas aos próprios dados")
