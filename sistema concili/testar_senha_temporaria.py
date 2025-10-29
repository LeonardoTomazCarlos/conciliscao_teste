#!/usr/bin/env python3
"""
Script para testar a funcionalidade de senha temporária
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app import app, db, Usuario
from werkzeug.security import generate_password_hash

def testar_senha_temporaria():
    """Testa a funcionalidade de senha temporária"""
    with app.app_context():
        print("🔐 TESTANDO FUNCIONALIDADE DE SENHA TEMPORÁRIA")
        print("=" * 60)
        
        # Buscar usuário de teste
        usuario = Usuario.query.filter_by(username='admin').first()
        if not usuario:
            print("❌ Usuário admin não encontrado")
            return False
        
        print(f"👤 Usuário: {usuario.username}")
        print(f"📧 Email: {usuario.email}")
        print(f"🔐 Senha temporária atual: {usuario.senha_temporaria}")
        
        # Simular reset de senha (marcar como temporária)
        print(f"\n🔄 SIMULANDO RESET DE SENHA...")
        
        # Salvar estado original
        senha_temp_original = usuario.senha_temporaria
        
        # Marcar como senha temporária
        usuario.senha_temporaria = True
        db.session.commit()
        
        print(f"✅ Usuário marcado com senha temporária: {usuario.senha_temporaria}")
        
        # Simular troca de senha (desmarcar temporária)
        print(f"\n🔄 SIMULANDO TROCA DE SENHA...")
        usuario.senha_temporaria = False
        db.session.commit()
        
        print(f"✅ Flag de senha temporária removida: {usuario.senha_temporaria}")
        
        # Restaurar estado original
        usuario.senha_temporaria = senha_temp_original
        db.session.commit()
        
        print(f"\n🔄 Estado original restaurado: {usuario.senha_temporaria}")
        
        return True

def verificar_estrutura_banco():
    """Verifica se o campo senha_temporaria existe no banco"""
    with app.app_context():
        print("\n🗄️ VERIFICANDO ESTRUTURA DO BANCO")
        print("=" * 40)
        
        try:
            # Tentar acessar o campo senha_temporaria
            usuario = Usuario.query.first()
            if usuario:
                tem_campo = hasattr(usuario, 'senha_temporaria')
                print(f"Campo 'senha_temporaria' existe: {'✅ SIM' if tem_campo else '❌ NÃO'}")
                
                if tem_campo:
                    print(f"Valor atual: {getattr(usuario, 'senha_temporaria', 'N/A')}")
                    return True
                else:
                    print("❌ Campo não encontrado - Execute recrear_banco.py")
                    return False
            else:
                print("❌ Nenhum usuário encontrado no banco")
                return False
                
        except Exception as e:
            print(f"❌ Erro ao verificar estrutura: {e}")
            return False

def criar_usuario_teste():
    """Cria um usuário de teste com senha temporária"""
    with app.app_context():
        print("\n👥 CRIANDO USUÁRIO DE TESTE")
        print("=" * 30)
        
        try:
            # Verificar se já existe
            usuario_teste = Usuario.query.filter_by(username='teste_temp').first()
            if usuario_teste:
                print("⚠️ Usuário de teste já existe - removendo...")
                db.session.delete(usuario_teste)
                db.session.commit()
            
            # Criar novo usuário com senha temporária
            novo_usuario = Usuario(
                username='teste_temp',
                email='teste_temp@example.com',
                password_hash=generate_password_hash('temp123'),
                nome_completo='Usuário Teste Temporário',
                perfil='usuario',
                ativo=True,
                senha_temporaria=True  # Marcar como temporária
            )
            
            db.session.add(novo_usuario)
            db.session.commit()
            
            print(f"✅ Usuário criado:")
            print(f"   Username: {novo_usuario.username}")
            print(f"   Email: {novo_usuario.email}")
            print(f"   Senha: temp123")
            print(f"   Senha temporária: {novo_usuario.senha_temporaria}")
            
            return True
            
        except Exception as e:
            print(f"❌ Erro ao criar usuário de teste: {e}")
            return False

if __name__ == "__main__":
    print("🚀 INICIANDO TESTES DE SENHA TEMPORÁRIA")
    print("=" * 70)
    
    # Verificar estrutura do banco
    estrutura_ok = verificar_estrutura_banco()
    
    if not estrutura_ok:
        print("\n❌ ESTRUTURA DO BANCO INVÁLIDA!")
        print("Execute: python recriar_banco.py")
        sys.exit(1)
    
    # Testar funcionalidade
    sucesso_teste = testar_senha_temporaria()
    
    # Criar usuário de teste
    sucesso_usuario = criar_usuario_teste()
    
    print("\n" + "=" * 70)
    if estrutura_ok and sucesso_teste and sucesso_usuario:
        print("✅ TODOS OS TESTES PASSARAM!")
        print("\n🎯 PRÓXIMOS PASSOS:")
        print("1. Execute: python app.py")
        print("2. Acesse: http://localhost:5000")
        print("3. Faça login como admin e resete a senha de um usuário")
        print("4. Teste login com usuário resetado")
        print("5. Ou teste com usuário 'teste_temp' (senha: temp123)")
    else:
        print("❌ ALGUNS TESTES FALHARAM!")
        print("Verifique os erros acima")