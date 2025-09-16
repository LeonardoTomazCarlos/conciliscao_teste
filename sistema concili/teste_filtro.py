#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Teste do filtro de conciliação
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def main():
    try:
        from app import app, db, ProcedimentoConciliacao
        
        with app.app_context():
            print("🔍 Testando filtros...")
            
            # Verificar procedimentos existentes
            procs = ProcedimentoConciliacao.query.all()
            print(f"📊 Total de procedimentos: {len(procs)}")
            
            for p in procs:
                print(f"  - ID: {p.id} | Tipo: {p.tipo_procedimento} | Método: {p.metodo} | Status: {p.status}")
            
            # Testar filtro por método
            print("\n🔧 Testando filtro por método 'automatico'...")
            automaticos = ProcedimentoConciliacao.query.filter_by(metodo='automatico').all()
            print(f"📈 Procedimentos automáticos: {len(automaticos)}")
            
            # Testar filtro por método manual
            print("\n🔧 Testando filtro por método 'manual'...")
            manuais = ProcedimentoConciliacao.query.filter_by(metodo='manual').all()
            print(f"📈 Procedimentos manuais: {len(manuais)}")
            
            # Testar o endpoint com filtro
            print("\n🌐 Testando endpoint com filtro...")
            with app.test_client() as client:
                # Login
                response = client.post('/login', data={
                    'username': 'admin',
                    'password': 'admin123'
                }, follow_redirects=True)
                
                if response.status_code == 200:
                    # Testar sem filtro
                    response = client.get('/api/procedimentos')
                    if response.status_code == 200:
                        data = response.get_json()
                        print(f"✅ Sem filtro: {len(data.get('procedimentos', []))} procedimentos")
                    
                    # Testar com filtro automático
                    response = client.get('/api/procedimentos?tipo=automatico')
                    if response.status_code == 200:
                        data = response.get_json()
                        print(f"✅ Com filtro 'automatico': {len(data.get('procedimentos', []))} procedimentos")
                    else:
                        print(f"❌ Erro com filtro: {response.data.decode()}")
                    
                    # Testar com filtro manual
                    response = client.get('/api/procedimentos?tipo=manual')
                    if response.status_code == 200:
                        data = response.get_json()
                        print(f"✅ Com filtro 'manual': {len(data.get('procedimentos', []))} procedimentos")
                    
                else:
                    print("❌ Falha no login")
                    
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
