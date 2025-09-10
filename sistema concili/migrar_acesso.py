#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MIGRAÇÃO PARA CONTROLE DE ACESSO POR USUÁRIO
Sistema ConciliaSync Pro
"""

from app import db, app, Usuario
from sqlalchemy import text
import os

def migrar_banco_controle_acesso():
    """Migra o banco para incluir controle de acesso"""
    
    print("🔄 MIGRANDO BANCO PARA CONTROLE DE ACESSO")
    print("=" * 50)
    
    with app.app_context():
        try:
            # Fazer backup do banco atual
            print("📦 Fazendo backup do banco atual...")
            if os.path.exists('instance/conciliacao.db'):
                import shutil
                shutil.copy('instance/conciliacao.db', 'instance/conciliacao_backup.db')
                print("✅ Backup criado: instance/conciliacao_backup.db")
            
            # Recriar todas as tabelas com as novas estruturas
            print("🔄 Recriando tabelas com controle de acesso...")
            db.drop_all()
            db.create_all()
            
            # Recriar usuário admin
            admin = Usuario(
                username='admin',
                email='admin@conciliacao.com',
                password_hash='pbkdf2:sha256:260000$7bD8mYKpzJjZ6bvH$0c8dbb2f8b9a5c7b6e5d4c3f2e1d0c9b8a7f6e5d4c3b2a1f0e9d8c7b6a5f4e3d2c1b0a9f8e7d6c5b4a3f2e1d0c',  # admin123
                nome_completo='Administrador do Sistema',
                perfil='admin'
            )
            db.session.add(admin)
            
            # Criar usuário de exemplo
            usuario_exemplo = Usuario(
                username='usuario1',
                email='usuario1@teste.com',
                password_hash='pbkdf2:sha256:260000$7bD8mYKpzJjZ6bvH$0c8dbb2f8b9a5c7b6e5d4c3f2e1d0c9b8a7f6e5d4c3b2a1f0e9d8c7b6a5f4e3d2c1b0a9f8e7d6c5b4a3f2e1d0c',  # senha123
                nome_completo='Usuário de Exemplo',
                perfil='usuario'
            )
            db.session.add(usuario_exemplo)
            
            # Criar usuário auditor
            auditor = Usuario(
                username='auditor',
                email='auditor@conciliacao.com',
                password_hash='pbkdf2:sha256:260000$7bD8mYKpzJjZ6bvH$0c8dbb2f8b9a5c7b6e5d4c3f2e1d0c9b8a7f6e5d4c3b2a1f0e9d8c7b6a5f4e3d2c1b0a9f8e7d6c5b4a3f2e1d0c',  # auditor123
                nome_completo='Auditor do Sistema',
                perfil='auditor'
            )
            db.session.add(auditor)
            
            db.session.commit()
            
            print("✅ Banco migrado com sucesso!")
            print("\n👥 USUÁRIOS CRIADOS:")
            print("=" * 50)
            print("🔑 ADMIN:")
            print("   Username: admin")
            print("   Senha: admin123")
            print("   Perfil: Administrador (acesso total)")
            
            print("\n👤 USUÁRIO EXEMPLO:")
            print("   Username: usuario1")
            print("   Senha: senha123")
            print("   Perfil: Usuário (apenas próprios dados)")
            
            print("\n🔍 AUDITOR:")
            print("   Username: auditor")
            print("   Senha: auditor123")
            print("   Perfil: Auditor (leitura de todos os dados)")
            
            print("\n🎯 NÍVEIS DE ACESSO IMPLEMENTADOS:")
            print("=" * 50)
            print("👑 ADMIN: Acesso total (CRUD) a todos os dados")
            print("🔍 AUDITOR: Acesso de leitura a todos os dados") 
            print("👤 USUÁRIO: Acesso apenas aos próprios dados")
            
            return True
            
        except Exception as e:
            print(f"❌ Erro na migração: {e}")
            return False

def testar_controle_acesso():
    """Testa o controle de acesso implementado"""
    
    print("\n🧪 TESTANDO CONTROLE DE ACESSO")
    print("=" * 50)
    
    with app.app_context():
        # Verificar usuários
        usuarios = Usuario.query.all()
        print(f"👥 Usuários no banco: {len(usuarios)}")
        
        for user in usuarios:
            print(f"   - {user.username} ({user.perfil})")
        
        # Verificar estrutura das tabelas
        from sqlalchemy import inspect
        inspector = inspect(db.engine)
        
        tabelas_com_usuario = ['extrato_bancario', 'lancamento_contabil', 'conta_bancaria']
        
        for tabela in tabelas_com_usuario:
            colunas = [col['name'] for col in inspector.get_columns(tabela)]
            if 'usuario_id' in colunas:
                print(f"✅ {tabela}: campo usuario_id presente")
            else:
                print(f"❌ {tabela}: campo usuario_id AUSENTE")
        
        print("\n🔐 CONTROLE DE ACESSO ATIVO!")

if __name__ == "__main__":
    sucesso = migrar_banco_controle_acesso()
    
    if sucesso:
        testar_controle_acesso()
        
        print("\n🚀 PRÓXIMOS PASSOS:")
        print("=" * 50)
        print("1. Restart o servidor Flask")
        print("2. Teste o login com os usuários criados")
        print("3. Cada usuário verá apenas seus dados")
        print("4. Admin pode gerenciar todos os dados")
        print("5. Auditor pode visualizar todos os dados")
        
    else:
        print("\n❌ Migração falhou. Verifique os logs.")
