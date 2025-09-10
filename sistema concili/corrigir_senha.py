#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CORREÇÃO DA SENHA DO ADMIN
Sistema ConciliaSync Pro
"""

from app import db, app, Usuario
from werkzeug.security import generate_password_hash, check_password_hash

def verificar_e_corrigir_senha_admin():
    """Verifica e corrige a senha do admin"""
    
    print("🔐 VERIFICANDO SENHA DO ADMIN")
    print("=" * 40)
    
    with app.app_context():
        # Buscar usuário admin
        admin = Usuario.query.filter_by(username='admin').first()
        
        if not admin:
            print("❌ Usuário admin não encontrado!")
            return False
        
        print(f"✅ Admin encontrado: {admin.username}")
        print(f"📧 Email: {admin.email}")
        print(f"👤 Nome: {admin.nome_completo}")
        print(f"🔑 Hash atual: {admin.password_hash[:50]}...")
        
        # Testar senha atual
        senha_teste = "admin123"
        senha_correta = check_password_hash(admin.password_hash, senha_teste)
        
        print(f"\n🧪 Testando senha '{senha_teste}':")
        print(f"Resultado: {'✅ CORRETA' if senha_correta else '❌ INCORRETA'}")
        
        if not senha_correta:
            print("\n🔧 CORRIGINDO SENHA...")
            
            # Gerar novo hash correto
            novo_hash = generate_password_hash("admin123")
            admin.password_hash = novo_hash
            
            # Salvar no banco
            db.session.commit()
            
            print("✅ Senha corrigida com sucesso!")
            
            # Testar novamente
            teste_final = check_password_hash(admin.password_hash, "admin123")
            print(f"🔍 Teste final: {'✅ SUCESSO' if teste_final else '❌ FALHA'}")
            
        else:
            print("✅ Senha já está correta!")
        
        return True

def criar_usuarios_teste():
    """Cria usuários de teste com senhas corretas"""
    
    print("\n👥 VERIFICANDO TODOS OS USUÁRIOS")
    print("=" * 40)
    
    with app.app_context():
        usuarios = Usuario.query.all()
        
        for user in usuarios:
            print(f"\n👤 {user.username} ({user.perfil})")
            
            if user.username == 'admin':
                senha_teste = 'admin123'
            elif user.username == 'auditor':
                senha_teste = 'auditor123'
            elif user.username == 'usuario1':
                senha_teste = 'senha123'
            else:
                continue
            
            # Testar senha
            senha_ok = check_password_hash(user.password_hash, senha_teste)
            print(f"   Senha '{senha_teste}': {'✅ OK' if senha_ok else '❌ ERRO'}")
            
            # Corrigir se necessário
            if not senha_ok:
                print(f"   🔧 Corrigindo senha...")
                user.password_hash = generate_password_hash(senha_teste)
                db.session.commit()
                print(f"   ✅ Senha corrigida!")

def mostrar_credenciais():
    """Mostra as credenciais corretas"""
    
    print("\n🔑 CREDENCIAIS DO SISTEMA")
    print("=" * 40)
    
    with app.app_context():
        usuarios = Usuario.query.all()
        
        for user in usuarios:
            if user.username == 'admin':
                print("👑 ADMINISTRADOR:")
                print("   Username: admin")
                print("   Senha: admin123")
                print("   Acesso: TOTAL")
                
            elif user.username == 'auditor':
                print("\n🔍 AUDITOR:")
                print("   Username: auditor")
                print("   Senha: auditor123")
                print("   Acesso: LEITURA")
                
            elif user.username == 'usuario1':
                print("\n👤 USUÁRIO:")
                print("   Username: usuario1")
                print("   Senha: senha123")
                print("   Acesso: PRÓPRIOS DADOS")

if __name__ == "__main__":
    sucesso = verificar_e_corrigir_senha_admin()
    
    if sucesso:
        criar_usuarios_teste()
        mostrar_credenciais()
        
        print("\n🚀 TESTE DE LOGIN:")
        print("=" * 40)
        print("1. Vá para: http://localhost:5000/login")
        print("2. Use: admin / admin123")
        print("3. Deve funcionar perfeitamente!")
        
    else:
        print("❌ Falha ao corrigir senha do admin")
