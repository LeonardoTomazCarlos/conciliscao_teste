import requests
import os
import csv
from datetime import datetime, timedelta

def criar_arquivo_com_divergencias():
    """Cria arquivos com dados que geram divergências"""
    
    # Arquivo 1: Extratos com valores diferentes dos lançamentos
    extratos_divergentes = [
        {"data": "2024-01-15", "descricao": "Pagamento Fornecedor ABC", "valor": 1500.00, "tipo": "debito"},
        {"data": "2024-01-16", "descricao": "Recebimento Cliente XYZ", "valor": 2000.00, "tipo": "credito"},
        {"data": "2024-01-17", "descricao": "Pagamento Funcionários", "valor": 3000.00, "tipo": "debito"},
        {"data": "2024-01-18", "descricao": "Venda Produto A", "valor": 3500.00, "tipo": "credito"},
        {"data": "2024-01-19", "descricao": "Pagamento Impostos", "valor": 800.00, "tipo": "debito"},
    ]
    
    # Arquivo 2: Lançamentos com valores ligeiramente diferentes (divergências)
    lancamentos_divergentes = [
        {"data": "2024-01-15", "descricao": "Pagamento Fornecedor ABC", "valor": 1500.50, "tipo": "debito"},  # Diferença de R$ 0,50
        {"data": "2024-01-16", "descricao": "Recebimento Cliente XYZ", "valor": 2000.00, "tipo": "credito"},  # Igual
        {"data": "2024-01-17", "descricao": "Pagamento Funcionários", "valor": 2995.00, "tipo": "debito"},   # Diferença de R$ 5,00
        {"data": "2024-01-18", "descricao": "Venda Produto A", "valor": 3500.00, "tipo": "credito"},        # Igual
        {"data": "2024-01-19", "descricao": "Pagamento Impostos", "valor": 800.00, "tipo": "debito"},       # Igual
    ]
    
    # Arquivo 3: Extratos com duplicatas
    extratos_duplicatas = [
        {"data": "2024-01-20", "descricao": "Depósito Cliente", "valor": 1000.00, "tipo": "credito"},
        {"data": "2024-01-20", "descricao": "Depósito Cliente", "valor": 1000.00, "tipo": "credito"},  # Duplicata
        {"data": "2024-01-21", "descricao": "Transferência", "valor": 500.00, "tipo": "credito"},
        {"data": "2024-01-22", "descricao": "Pagamento Serviços", "valor": 250.00, "tipo": "debito"},
    ]
    
    # Criar arquivos CSV
    with open('extratos_divergentes.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['Data', 'Descrição', 'Valor', 'Tipo'])
        writer.writeheader()
        for extrato in extratos_divergentes:
            writer.writerow({
                'Data': extrato['data'],
                'Descrição': extrato['descricao'],
                'Valor': extrato['valor'],
                'Tipo': extrato['tipo']
            })
    
    with open('lancamentos_divergentes.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['Data', 'Descrição', 'Valor', 'Tipo'])
        writer.writeheader()
        for lancamento in lancamentos_divergentes:
            writer.writerow({
                'Data': lancamento['data'],
                'Descrição': lancamento['descricao'],
                'Valor': lancamento['valor'],
                'Tipo': lancamento['tipo']
            })
    
    with open('extratos_duplicatas.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['Data', 'Descrição', 'Valor', 'Tipo'])
        writer.writeheader()
        for extrato in extratos_duplicatas:
            writer.writerow({
                'Data': extrato['data'],
                'Descrição': extrato['descricao'],
                'Valor': extrato['valor'],
                'Tipo': extrato['tipo']
            })
    
    print("✅ Arquivos com divergências criados:")
    print("   - extratos_divergentes.csv")
    print("   - lancamentos_divergentes.csv") 
    print("   - extratos_duplicatas.csv")

def testar_divergencias():
    """Testa o sistema de divergências"""
    print("\n🧪 TESTE DE DIVERGÊNCIAS")
    print("=" * 50)
    
    # URL base
    base_url = "http://localhost:5000"
    session = requests.Session()
    
    # 1. Login
    print("1. Fazendo login...")
    login_data = {'username': 'admin', 'password': 'admin123'}
    login_response = session.post(f"{base_url}/login", json=login_data)
    
    if login_response.status_code == 200 and login_response.json().get('success'):
        print("✅ Login realizado com sucesso!")
    else:
        print("❌ Falha no login")
        return
    
    # 2. Upload de extratos divergentes
    print("\n2. Upload de extratos divergentes...")
    with open('extratos_divergentes.csv', 'rb') as file:
        files = {'file': ('extratos_divergentes.csv', file, 'text/csv')}
        upload_response = session.post(f"{base_url}/api/upload-extrato", files=files)
        
        if upload_response.status_code == 200:
            result = upload_response.json()
            if result.get('success'):
                print(f"✅ Extratos divergentes importados: {result.get('registros', 0)} registros")
            else:
                print(f"❌ Erro: {result.get('error')}")
    
    # 3. Upload de lançamentos divergentes
    print("\n3. Upload de lançamentos divergentes...")
    with open('lancamentos_divergentes.csv', 'rb') as file:
        files = {'file': ('lancamentos_divergentes.csv', file, 'text/csv')}
        upload_response = session.post(f"{base_url}/api/upload-lancamentos", files=files)
        
        if upload_response.status_code == 200:
            result = upload_response.json()
            if result.get('success'):
                print(f"✅ Lançamentos divergentes importados: {result.get('registros', 0)} registros")
            else:
                print(f"❌ Erro: {result.get('error')}")
    
    # 4. Upload de duplicatas
    print("\n4. Upload de extratos com duplicatas...")
    with open('extratos_duplicatas.csv', 'rb') as file:
        files = {'file': ('extratos_duplicatas.csv', file, 'text/csv')}
        upload_response = session.post(f"{base_url}/api/upload-extrato", files=files)
        
        if upload_response.status_code == 200:
            result = upload_response.json()
            if result.get('success'):
                print(f"✅ Extratos com duplicatas importados: {result.get('registros', 0)} registros")
                print(f"   Duplicatas detectadas: {result.get('duplicatas', 0)}")
            else:
                print(f"❌ Erro: {result.get('error')}")
    
    # 5. Executar conciliação automática
    print("\n5. Executando conciliação automática...")
    conciliacao_response = session.post(f"{base_url}/api/conciliacao-automatica")
    if conciliacao_response.status_code == 200:
        result = conciliacao_response.json()
        if result.get('success'):
            print("✅ Conciliação automática executada!")
        else:
            print(f"❌ Erro na conciliação: {result.get('error')}")
    
    # 6. Verificar divergências
    print("\n6. Verificando divergências...")
    divergencias_response = session.get(f"{base_url}/api/divergencias")
    if divergencias_response.status_code == 200:
        divergencias = divergencias_response.json()
        print(f"   📊 Total de divergências: {len(divergencias)}")
        
        for i, div in enumerate(divergencias, 1):
            print(f"   {i}. Tipo: {div['tipo']} - {div['descricao']}")
    else:
        print("❌ Erro ao buscar divergências")
    
    # 7. Verificar estatísticas finais
    print("\n7. Estatísticas finais...")
    stats_response = session.get(f"{base_url}/api/estatisticas")
    if stats_response.status_code == 200:
        stats = stats_response.json()
        print(f"   📊 Total de extratos: {stats.get('total_extratos', 0)}")
        print(f"   📊 Total de lançamentos: {stats.get('total_lancamentos', 0)}")
        print(f"   📊 Extratos conciliados: {stats.get('extratos_conciliados', 0)}")
        print(f"   📊 Lançamentos conciliados: {stats.get('lancamentos_conciliados', 0)}")
        print(f"   📊 Divergências pendentes: {stats.get('divergencias_pendentes', 0)}")
    
    print("\n🎯 TESTE DE DIVERGÊNCIAS FINALIZADO!")

if __name__ == "__main__":
    # Criar arquivos de teste
    criar_arquivo_com_divergencias()
    
    # Executar testes
    testar_divergencias()
