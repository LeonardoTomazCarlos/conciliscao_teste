#!/usr/bin/env python3
"""
Script de teste para o Sistema de Conciliação Bancária
"""

import requests
import json
import time
import os

def testar_sistema():
    """Testa as principais funcionalidades do sistema"""
    
    base_url = "http://localhost:5000"
    
    print("🧪 Iniciando testes do Sistema de Conciliação Bancária...")
    print("=" * 60)
    
    # Teste 1: Verificar se o servidor está rodando
    print("1. Testando conexão com o servidor...")
    try:
        response = requests.get(base_url, timeout=5)
        if response.status_code == 200:
            print("✅ Servidor está rodando corretamente")
        else:
            print(f"❌ Erro no servidor: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Servidor não está rodando. Execute 'python app.py' primeiro.")
        return False
    except Exception as e:
        print(f"❌ Erro ao conectar: {e}")
        return False
    
    # Teste 2: Verificar estatísticas iniciais
    print("\n2. Testando API de estatísticas...")
    try:
        response = requests.get(f"{base_url}/api/estatisticas")
        if response.status_code == 200:
            stats = response.json()
            print(f"✅ Estatísticas carregadas: {stats['total_extratos']} extratos, {stats['total_lancamentos']} lançamentos")
        else:
            print(f"❌ Erro ao carregar estatísticas: {response.status_code}")
    except Exception as e:
        print(f"❌ Erro ao testar estatísticas: {e}")
    
    # Teste 3: Verificar APIs de dados
    print("\n3. Testando APIs de dados...")
    try:
        # Testar extratos
        response = requests.get(f"{base_url}/api/extratos")
        if response.status_code == 200:
            extratos = response.json()
            print(f"✅ API de extratos: {len(extratos)} registros encontrados")
        else:
            print(f"❌ Erro na API de extratos: {response.status_code}")
        
        # Testar lançamentos
        response = requests.get(f"{base_url}/api/lancamentos")
        if response.status_code == 200:
            lancamentos = response.json()
            print(f"✅ API de lançamentos: {len(lancamentos)} registros encontrados")
        else:
            print(f"❌ Erro na API de lançamentos: {response.status_code}")
        
        # Testar conciliações
        response = requests.get(f"{base_url}/api/conciliacoes")
        if response.status_code == 200:
            conciliacoes = response.json()
            print(f"✅ API de conciliações: {len(conciliacoes)} registros encontrados")
        else:
            print(f"❌ Erro na API de conciliações: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Erro ao testar APIs: {e}")
    
    print("\n" + "=" * 60)
    print("🎉 Testes concluídos!")
    print("\n📋 Próximos passos:")
    print("1. Acesse http://localhost:5000 no seu navegador")
    print("2. Use os arquivos de exemplo na pasta 'exemplos/' para testar")
    print("3. Faça upload dos arquivos CSV de exemplo")
    print("4. Teste a funcionalidade de conciliação")
    
    return True

def criar_arquivos_teste():
    """Cria arquivos de teste se não existirem"""
    
    print("\n📁 Verificando arquivos de exemplo...")
    
    # Verificar se a pasta exemplos existe
    if not os.path.exists('exemplos'):
        os.makedirs('exemplos')
        print("✅ Pasta 'exemplos' criada")
    
    # Verificar arquivo de extrato
    extrato_file = 'exemplos/extrato_exemplo.csv'
    if not os.path.exists(extrato_file):
        print("❌ Arquivo de extrato não encontrado")
    else:
        print("✅ Arquivo de extrato encontrado")
    
    # Verificar arquivo de lançamentos
    lancamentos_file = 'exemplos/lancamentos_exemplo.csv'
    if not os.path.exists(lancamentos_file):
        print("❌ Arquivo de lançamentos não encontrado")
    else:
        print("✅ Arquivo de lançamentos encontrado")

if __name__ == "__main__":
    print("🚀 Sistema de Conciliação Bancária - Teste de Funcionamento")
    print("=" * 60)
    
    # Criar arquivos de teste
    criar_arquivos_teste()
    
    # Testar sistema
    if testar_sistema():
        print("\n✅ Sistema funcionando corretamente!")
    else:
        print("\n❌ Problemas encontrados no sistema.")
        print("Verifique se:")
        print("- O servidor está rodando (python app.py)")
        print("- As dependências estão instaladas (pip install -r requirements.txt)")
        print("- A porta 5000 está disponível") 