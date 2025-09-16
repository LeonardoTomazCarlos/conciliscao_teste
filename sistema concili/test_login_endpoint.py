#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script para testar login e endpoint de procedimentos
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def main():
    try:
        from app import app, db, ProcedimentoConciliacao, Usuario
        
        with app.app_context():
            print("🔍 Testando login e endpoint...")
            
            # Verificar se existe usuário admin
            admin = Usuario.query.filter_by(username='admin').first()
            if not admin:
                print("❌ Usuário admin não encontrado!")
                return
            
            print(f"✅ Usuário admin encontrado: {admin.username}")
            
            # Testar com client autenticado
            with app.test_client() as client:
                print("\n🔐 Fazendo login...")
                
                # Login via formulário (HTML)
                response = client.post('/login', data={
                    'username': 'admin',
                    'password': 'admin123'
                }, follow_redirects=True)
                
                print(f"📡 Status do login: {response.status_code}")
                
                if response.status_code == 200:
                    print("✅ Login bem-sucedido!")
                    
                    # Agora testar o endpoint de procedimentos
                    print("\n🌐 Testando endpoint /api/procedimentos...")
                    response = client.get('/api/procedimentos')
                    print(f"📡 Status: {response.status_code}")
                    
                    if response.status_code == 200:
                        data = response.get_json()
                        print(f"✅ Sucesso! Dados: {data}")
                        procedimentos = data.get('procedimentos', [])
                        print(f"📊 Total de procedimentos: {len(procedimentos)}")
                    else:
                        print(f"❌ Erro: {response.data.decode()}")
                        
                else:
                    print(f"❌ Falha no login: {response.data.decode()}")
                    
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
