#!/usr/bin/env python3
"""
Verificar e corrigir status dos usuários
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app import app, db, Usuario

def verificar_usuarios():
    """Verifica o status de todos os usuários"""
    with app.app_context():
        print("👥 VERIFICANDO STATUS DOS USUÁRIOS")
        print("=" * 50)
        
        usuarios = Usuario.query.all()
        
        for user in usuarios:
            print(f"👤 Usuário: {user.username}")
            print(f"📧 Email: {user.email}")
            print(f"🔒 Ativo: {'✅ SIM' if user.ativo else '❌ NÃO'}")
            print(f"🛡️ Perfil: {user.perfil}")
            print(f"📅 Último acesso: {user.ultimo_acesso}")
            print(f"📅 Criado em: {user.created_at}")
            print("-" * 30)

def ativar_usuarios():
    """Ativa todos os usuários bloqueados"""
    with app.app_context():
        print("🔓 ATIVANDO USUÁRIOS BLOQUEADOS")
        print("=" * 50)
        
        usuarios_inativos = Usuario.query.filter_by(ativo=False).all()
        
        if not usuarios_inativos:
            print("✅ Todos os usuários já estão ativos!")
            return
        
        for user in usuarios_inativos:
            print(f"🔓 Ativando usuário: {user.username}")
            user.ativo = True
        
        db.session.commit()
        print(f"✅ {len(usuarios_inativos)} usuário(s) ativado(s) com sucesso!")

def verificar_usuario_admin():
    """Verifica especificamente o usuário admin"""
    with app.app_context():
        print("🔍 VERIFICANDO USUÁRIO ADMIN")
        print("=" * 50)
        
        admin = Usuario.query.filter_by(username='admin').first()
        
        if not admin:
            print("❌ Usuário admin não encontrado!")
            return False
        
        print(f"👤 Username: {admin.username}")
        print(f"📧 Email: {admin.email}")
        print(f"🔒 Ativo: {'✅ SIM' if admin.ativo else '❌ NÃO - BLOQUEADO!'}")
        print(f"🛡️ Perfil: {admin.perfil}")
        
        if not admin.ativo:
            print("\n🔧 CORRIGINDO...")
            admin.ativo = True
            db.session.commit()
            print("✅ Usuário admin ativado com sucesso!")
            return True
        
        return admin.ativo

if __name__ == "__main__":
    print("🚀 DIAGNÓSTICO DE USUÁRIOS BLOQUEADOS")
    print("=" * 60)
    
    # Verificar todos os usuários
    verificar_usuarios()
    
    # Focar no admin
    admin_ok = verificar_usuario_admin()
    
    # Ativar todos se necessário
    ativar_usuarios()
    
    print("\n" + "=" * 60)
    print("✅ DIAGNÓSTICO CONCLUÍDO!")
    print("Agora tente fazer login novamente.")