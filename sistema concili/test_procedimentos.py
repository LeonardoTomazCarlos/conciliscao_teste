#!/usr/bin/env python3
"""
Script de teste para a nova implementação de procedimentos
"""

import requests
import json

BASE_URL = 'http://127.0.0.1:5000'

def test_procedimentos():
    """Testar as novas rotas de procedimentos"""
    
    print("🧪 TESTE - Nova implementação de procedimentos")
    print("=" * 50)
    
    # Teste 1: Listar procedimentos
    print("\n1️⃣ Testando GET /api/procedimentos")
    try:
        response = requests.get(f"{BASE_URL}/api/procedimentos")
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Procedimentos encontrados: {len(data.get('procedimentos', []))}")
            if data.get('procedimentos'):
                proc = data['procedimentos'][0]
                print(f"   📋 Primeiro procedimento: {proc.get('uuid')} - {proc.get('tipo_procedimento')}")
        elif response.status_code == 401:
            print("⚠️ Não autenticado - teste via navegador necessário")
        else:
            print(f"❌ Erro: {response.text}")
    except Exception as e:
        print(f"❌ Erro de conexão: {e}")
    
    # Teste 2: Verificar estrutura do banco
    print("\n2️⃣ Verificando estrutura do banco")
    try:
        import sqlite3
        conn = sqlite3.connect('instance/conciliacao.db')
        cursor = conn.cursor()
        
        # Verificar se tabela existe
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='procedimento_conciliacao'")
        if cursor.fetchone():
            print("✅ Tabela procedimento_conciliacao existe")
            
            # Contar registros
            cursor.execute("SELECT COUNT(*) FROM procedimento_conciliacao")
            count = cursor.fetchone()[0]
            print(f"📊 Total de procedimentos no banco: {count}")
            
            if count > 0:
                cursor.execute("SELECT uuid, tipo_procedimento, status FROM procedimento_conciliacao LIMIT 3")
                procs = cursor.fetchall()
                print("📋 Procedimentos encontrados:")
                for p in procs:
                    print(f"   - {p[0]} | {p[1]} | {p[2]}")
        else:
            print("❌ Tabela procedimento_conciliacao não existe")
        
        # Verificar coluna procedimento_id em conciliacao
        cursor.execute("PRAGMA table_info(conciliacao)")
        columns = [col[1] for col in cursor.fetchall()]
        if 'procedimento_id' in columns:
            print("✅ Coluna procedimento_id existe na tabela conciliacao")
        else:
            print("❌ Coluna procedimento_id não existe na tabela conciliacao")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Erro ao verificar banco: {e}")
    
    print("\n" + "=" * 50)
    print("📋 RESUMO DO TESTE")
    print("=" * 50)
    print("✅ Para testar completamente:")
    print("1. Inicie o servidor: python app.py")
    print("2. Faça login no navegador: http://127.0.0.1:5000")
    print("3. Acesse a aba 'Histórico de Procedimentos'")
    print("4. Faça upload de arquivos para criar novos procedimentos")
    print("5. Clique em 'Ver' para visualizar detalhes")
    print("6. Clique em 'CSV' para exportar")

if __name__ == "__main__":
    test_procedimentos()
