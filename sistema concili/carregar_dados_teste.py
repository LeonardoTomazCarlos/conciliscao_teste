#!/usr/bin/env python3
"""
Script para carregar dados de teste para validação dos filtros de período.
Data de referência: 11 de setembro de 2025
"""

import os
import sys
import requests
import time
from datetime import datetime

# Configurações
BASE_URL = "http://localhost:5000"
EXEMPLOS_DIR = "exemplos"

# Arquivos de teste disponíveis
ARQUIVOS_TESTE = {
    "completo": {
        "extrato": "extrato_teste_periodos.csv",
        "lancamentos": "lancamentos_teste_periodos.csv",
        "descricao": "Dados completos com múltiplos períodos"
    },
    "hoje": {
        "extrato": "extrato_hoje_apenas.csv", 
        "lancamentos": "lancamentos_hoje_apenas.csv",
        "descricao": "Dados apenas do dia 11/09/2025"
    },
    "semana": {
        "extrato": "extrato_esta_semana.csv",
        "lancamentos": "lancamentos_esta_semana.csv", 
        "descricao": "Dados da semana de 06-11/09/2025"
    },
    "mes": {
        "extrato": "extrato_este_mes.csv",
        "lancamentos": "lancamentos_este_mes.csv",
        "descricao": "Dados do mês de setembro/2025"
    },
    "divergencias": {
        "extrato": "extrato_com_divergencias.csv",
        "lancamentos": "lancamentos_com_divergencias.csv",
        "descricao": "Dados com divergências intencionais para teste"
    }
}

def verificar_servidor():
    """Verifica se o servidor está rodando"""
    try:
        response = requests.get(f"{BASE_URL}/api/estatisticas", timeout=5)
        return response.status_code in [200, 401]  # 401 é OK se não estiver logado
    except:
        return False

def fazer_upload(arquivo_path, tipo):
    """Faz upload de um arquivo para o sistema"""
    if not os.path.exists(arquivo_path):
        print(f"❌ Arquivo não encontrado: {arquivo_path}")
        return False
    
    endpoint = "/api/upload-extrato" if tipo == "extrato" else "/api/upload-lancamentos"
    
    try:
        with open(arquivo_path, 'rb') as f:
            files = {'file': f}
            response = requests.post(f"{BASE_URL}{endpoint}", files=files, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ {tipo.title()} carregado: {data.get('registros', 0)} registros")
            return True
        else:
            print(f"❌ Erro no upload do {tipo}: {response.status_code}")
            if response.text:
                print(f"   Detalhes: {response.text[:200]}...")
            return False
    except Exception as e:
        print(f"❌ Erro no upload do {tipo}: {e}")
        return False

def limpar_dados():
    """Limpa os dados existentes"""
    try:
        response = requests.post(f"{BASE_URL}/api/limpar-dados", timeout=10)
        if response.status_code == 200:
            print("🗑️  Dados limpos com sucesso")
            return True
        else:
            print(f"❌ Erro ao limpar dados: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Erro ao limpar dados: {e}")
        return False

def carregar_conjunto(nome_conjunto, limpar_antes=True):
    """Carrega um conjunto específico de dados"""
    if nome_conjunto not in ARQUIVOS_TESTE:
        print(f"❌ Conjunto '{nome_conjunto}' não encontrado")
        print(f"   Disponíveis: {', '.join(ARQUIVOS_TESTE.keys())}")
        return False
    
    conjunto = ARQUIVOS_TESTE[nome_conjunto]
    print(f"\n📂 Carregando conjunto: {nome_conjunto}")
    print(f"   {conjunto['descricao']}")
    
    if limpar_antes:
        print("\n🗑️  Limpando dados existentes...")
        if not limpar_dados():
            return False
        time.sleep(1)
    
    # Upload do extrato
    print(f"\n📤 Fazendo upload do extrato...")
    extrato_path = os.path.join(EXEMPLOS_DIR, conjunto["extrato"])
    if not fazer_upload(extrato_path, "extrato"):
        return False
    
    time.sleep(2)
    
    # Upload dos lançamentos
    print(f"\n📤 Fazendo upload dos lançamentos...")
    lancamentos_path = os.path.join(EXEMPLOS_DIR, conjunto["lancamentos"])
    if not fazer_upload(lancamentos_path, "lancamentos"):
        return False
    
    print(f"\n✅ Conjunto '{nome_conjunto}' carregado com sucesso!")
    return True

def verificar_divergencias():
    """Força a verificação de divergências"""
    try:
        response = requests.post(f"{BASE_URL}/api/verificar-divergencias", timeout=15)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ {data['message']}")
            return True
        else:
            print(f"❌ Erro ao verificar divergências: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Erro ao verificar divergências: {e}")
        return False

def testar_filtros():
    """Testa os filtros fazendo requisições para a API"""
    filtros = ["hoje", "semana", "mes", "ano"]
    
    print("\n🧪 Testando filtros...")
    
    for filtro in filtros:
        try:
            response = requests.get(f"{BASE_URL}/api/estatisticas?periodo={filtro}", timeout=10)
            if response.status_code == 200:
                data = response.json()
                total_extratos = data.get("total_extratos", 0)
                total_lancamentos = data.get("total_lancamentos", 0)
                print(f"   {filtro.capitalize()}: {total_extratos} extratos, {total_lancamentos} lançamentos")
            else:
                print(f"   {filtro.capitalize()}: Erro {response.status_code}")
        except Exception as e:
            print(f"   {filtro.capitalize()}: Erro - {e}")
    """Testa os filtros fazendo requisições para a API"""
    filtros = ["hoje", "semana", "mes", "ano"]
    
    print("\n🧪 Testando filtros...")
    
    for filtro in filtros:
        try:
            response = requests.get(f"{BASE_URL}/api/estatisticas?periodo={filtro}", timeout=10)
            if response.status_code == 200:
                data = response.json()
                total_extratos = data.get("total_extratos", 0)
                total_lancamentos = data.get("total_lancamentos", 0)
                print(f"   {filtro.capitalize()}: {total_extratos} extratos, {total_lancamentos} lançamentos")
            else:
                print(f"   {filtro.capitalize()}: Erro {response.status_code}")
        except Exception as e:
            print(f"   {filtro.capitalize()}: Erro - {e}")

def main():
    print("🚀 Script de Teste dos Filtros de Período")
    print("=" * 50)
    
    # Verificar se o servidor está rodando
    print("🔍 Verificando servidor...")
    if not verificar_servidor():
        print("❌ Servidor não está rodando em http://localhost:5000")
        print("   Inicie o servidor com: python app.py")
        return
    
    print("✅ Servidor encontrado")
    
    # Menu interativo
    while True:
        print("\n📋 Opções disponíveis:")
        print("1. Carregar dados completos (múltiplos períodos)")
        print("2. Carregar dados apenas de hoje")
        print("3. Carregar dados desta semana")
        print("4. Carregar dados deste mês")
        print("5. Carregar dados com divergências")
        print("6. Testar filtros (sem carregar dados)")
        print("7. Verificar divergências")
        print("8. Limpar todos os dados")
        print("0. Sair")
        
        opcao = input("\n👉 Escolha uma opção (0-8): ").strip()
        
        if opcao == "0":
            print("\n👋 Encerrando...")
            break
        elif opcao == "1":
            carregar_conjunto("completo")
        elif opcao == "2":
            carregar_conjunto("hoje")
        elif opcao == "3":
            carregar_conjunto("semana")
        elif opcao == "4":
            carregar_conjunto("mes")
        elif opcao == "5":
            if carregar_conjunto("divergencias"):
                print("\n🔍 Executando verificação de divergências...")
                verificar_divergencias()
        elif opcao == "6":
            testar_filtros()
        elif opcao == "7":
            verificar_divergencias()
        elif opcao == "8":
            limpar_dados()
        else:
            print("❌ Opção inválida")
        
        input("\n⏸️  Pressione Enter para continuar...")

if __name__ == "__main__":
    # Verificar se está no diretório correto
    if not os.path.exists(EXEMPLOS_DIR):
        print("❌ Diretório 'exemplos' não encontrado")
        print("   Execute este script no diretório raiz do sistema")
        sys.exit(1)
    
    main()
