#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para testar upload de arquivos e conciliação
"""

import requests
import os
import sys

# URL base da aplicação
BASE_URL = "http://localhost:5000"

def test_upload_and_conciliation():
    """Testa upload de arquivos e execução da conciliação"""
    
    # Arquivos de teste
    test_files = [
        {
            'name': 'Teste Pequeno (sem divergências)',
            'extrato': 'teste_extrato_pequeno.csv',
            'lancamentos': 'teste_lancamentos_pequeno.csv'
        },
        {
            'name': 'Teste Setembro (dados completos)',
            'extrato': 'teste_extrato_setembro.csv',
            'lancamentos': 'teste_lancamentos_setembro.csv'
        },
        {
            'name': 'Teste com Divergências',
            'extrato': 'teste_extrato_com_divergencias.csv',
            'lancamentos': 'teste_lancamentos_com_divergencias.csv'
        },
        {
            'name': 'Teste Completo (dados extensos)',
            'extrato': 'teste_extrato_completo.csv',
            'lancamentos': 'teste_lancamentos_completo.csv'
        }
    ]
    
    session = requests.Session()
    
    print("🧪 TESTE DE UPLOAD E CONCILIAÇÃO")
    print("=" * 50)
    
    for test in test_files:
        print(f"\n📁 Testando: {test['name']}")
        print("-" * 30)
        
        # Verificar se os arquivos existem
        extrato_path = test['extrato']
        lancamentos_path = test['lancamentos']
        
        if not os.path.exists(extrato_path):
            print(f"❌ Arquivo não encontrado: {extrato_path}")
            continue
            
        if not os.path.exists(lancamentos_path):
            print(f"❌ Arquivo não encontrado: {lancamentos_path}")
            continue
        
        try:
            # Upload do extrato
            print(f"📤 Fazendo upload do extrato: {extrato_path}")
            with open(extrato_path, 'rb') as f:
                files = {'file': (extrato_path, f, 'text/csv')}
                data = {'tipo': 'extrato'}
                response = session.post(f"{BASE_URL}/upload", files=files, data=data)
            
            if response.status_code == 200:
                print("✅ Upload do extrato realizado com sucesso")
            else:
                print(f"❌ Erro no upload do extrato: {response.status_code}")
                print(f"Resposta: {response.text}")
                continue
            
            # Upload dos lançamentos
            print(f"📤 Fazendo upload dos lançamentos: {lancamentos_path}")
            with open(lancamentos_path, 'rb') as f:
                files = {'file': (lancamentos_path, f, 'text/csv')}
                data = {'tipo': 'lancamentos'}
                response = session.post(f"{BASE_URL}/upload", files=files, data=data)
            
            if response.status_code == 200:
                print("✅ Upload dos lançamentos realizado com sucesso")
            else:
                print(f"❌ Erro no upload dos lançamentos: {response.status_code}")
                print(f"Resposta: {response.text}")
                continue
            
            # Executar conciliação
            print("🔄 Executando conciliação...")
            response = session.post(f"{BASE_URL}/api/conciliacao/executar")
            
            if response.status_code == 200:
                result = response.json()
                print("✅ Conciliação executada com sucesso!")
                print(f"📊 Resultados:")
                print(f"   - Conciliadas: {result.get('conciliadas', 0)}")
                print(f"   - Divergências: {result.get('divergencias', 0)}")
                print(f"   - Não encontradas: {result.get('nao_encontradas', 0)}")
                
                # Buscar conciliações para verificar
                response = session.get(f"{BASE_URL}/api/conciliacao")
                if response.status_code == 200:
                    conciliacoes = response.json()
                    print(f"📋 Total de conciliações encontradas: {len(conciliacoes)}")
                    
                    # Mostrar algumas conciliações como exemplo
                    if conciliacoes:
                        print("📝 Exemplos de conciliações:")
                        for i, conc in enumerate(conciliacoes[:3]):
                            status = "✅" if conc.get('status') == 'conciliado' else "❌"
                            print(f"   {i+1}. {status} {conc.get('data', 'N/A')} - R$ {conc.get('valor', 0):.2f}")
                
            else:
                print(f"❌ Erro na conciliação: {response.status_code}")
                print(f"Resposta: {response.text}")
            
        except Exception as e:
            print(f"❌ Erro no teste: {str(e)}")
    
    print("\n🏁 Teste concluído!")

def test_filters():
    """Testa os filtros de conciliação"""
    
    print("\n🔍 TESTE DOS FILTROS")
    print("=" * 50)
    
    filters_to_test = [
        {'name': 'Sem filtros', 'params': {}},
        {'name': 'Status: conciliado', 'params': {'status': 'conciliado'}},
        {'name': 'Status: divergente', 'params': {'status': 'divergente'}},
        {'name': 'Data: 2025-09-01', 'params': {'data_inicio': '2025-09-01', 'data_fim': '2025-09-01'}},
        {'name': 'Valor mínimo: 1000', 'params': {'valor_min': '1000'}},
        {'name': 'Valor máximo: 500', 'params': {'valor_max': '500'}},
    ]
    
    for filter_test in filters_to_test:
        print(f"\n🔎 Testando filtro: {filter_test['name']}")
        print(f"Parâmetros: {filter_test['params']}")
        
        try:
            response = requests.get(f"{BASE_URL}/api/conciliacao", params=filter_test['params'])
            
            if response.status_code == 200:
                results = response.json()
                print(f"✅ Sucesso! Encontrados: {len(results)} registros")
                
                if results and len(results) <= 3:
                    for i, result in enumerate(results):
                        print(f"   {i+1}. {result.get('data', 'N/A')} - R$ {result.get('valor', 0):.2f} - {result.get('status', 'N/A')}")
                elif len(results) > 3:
                    for i in range(3):
                        result = results[i]
                        print(f"   {i+1}. {result.get('data', 'N/A')} - R$ {result.get('valor', 0):.2f} - {result.get('status', 'N/A')}")
                    print(f"   ... e mais {len(results) - 3} registros")
                    
            else:
                print(f"❌ Erro: {response.status_code}")
                print(f"Resposta: {response.text}")
                
        except Exception as e:
            print(f"❌ Erro na requisição: {str(e)}")

if __name__ == "__main__":
    try:
        print("🚀 Iniciando testes de conciliação...")
        
        # Verificar se o servidor está rodando
        try:
            response = requests.get(f"{BASE_URL}/", timeout=5)
            if response.status_code == 200:
                print("✅ Servidor está rodando!")
            else:
                print(f"⚠️ Servidor respondeu com status: {response.status_code}")
        except requests.exceptions.RequestException:
            print("❌ Servidor não está rodando ou não está acessível!")
            print("Por favor, execute: python run.py")
            sys.exit(1)
        
        # Executar testes
        test_upload_and_conciliation()
        test_filters()
        
    except KeyboardInterrupt:
        print("\n⏹️ Teste interrompido pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro geral: {str(e)}")
