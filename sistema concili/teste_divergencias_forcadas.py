import requests
import os
import csv

def criar_divergencias_forcadas():
    """Cria divergências forçadas para testar o sistema"""
    
    # Arquivo 1: Extratos com valores específicos
    extratos = [
        {"data": "2024-02-01", "descricao": "TESTE DIVERGENCIA 1", "valor": 100.00, "tipo": "debito"},
        {"data": "2024-02-02", "descricao": "TESTE DIVERGENCIA 2", "valor": 200.00, "tipo": "credito"},
        {"data": "2024-02-03", "descricao": "TESTE DIVERGENCIA 3", "valor": 300.00, "tipo": "debito"},
    ]
    
    # Arquivo 2: Lançamentos com valores diferentes (divergências forçadas)
    lancamentos = [
        {"data": "2024-02-01", "descricao": "TESTE DIVERGENCIA 1", "valor": 100.50, "tipo": "debito"},  # Diferença de R$ 0,50
        {"data": "2024-02-02", "descricao": "TESTE DIVERGENCIA 2", "valor": 200.00, "tipo": "credito"},  # Igual
        {"data": "2024-02-03", "descricao": "TESTE DIVERGENCIA 3", "valor": 295.00, "tipo": "debito"},   # Diferença de R$ 5,00
    ]
    
    # Criar arquivos CSV
    with open('teste_extratos.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['Data', 'Descrição', 'Valor', 'Tipo'])
        writer.writeheader()
        for extrato in extratos:
            writer.writerow({
                'Data': extrato['data'],
                'Descrição': extrato['descricao'],
                'Valor': extrato['valor'],
                'Tipo': extrato['tipo']
            })
    
    with open('teste_lancamentos.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['Data', 'Descrição', 'Valor', 'Tipo'])
        writer.writeheader()
        for lancamento in lancamentos:
            writer.writerow({
                'Data': lancamento['data'],
                'Descrição': lancamento['descricao'],
                'Valor': lancamento['valor'],
                'Tipo': lancamento['tipo']
            })
    
    print("✅ Arquivos de teste criados:")
    print("   - teste_extratos.csv")
    print("   - teste_lancamentos.csv")

def testar_divergencias_forcadas():
    """Testa divergências forçadas"""
    print("\n🧪 TESTE DE DIVERGÊNCIAS FORÇADAS")
    print("=" * 50)
    
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
    
    # 2. Upload de extratos
    print("\n2. Upload de extratos de teste...")
    with open('teste_extratos.csv', 'rb') as file:
        files = {'file': ('teste_extratos.csv', file, 'text/csv')}
        upload_response = session.post(f"{base_url}/api/upload-extrato", files=files)
        
        if upload_response.status_code == 200:
            result = upload_response.json()
            if result.get('success'):
                print(f"✅ Extratos importados: {result.get('registros', 0)} registros")
            else:
                print(f"❌ Erro: {result.get('error')}")
    
    # 3. Upload de lançamentos
    print("\n3. Upload de lançamentos de teste...")
    with open('teste_lancamentos.csv', 'rb') as file:
        files = {'file': ('teste_lancamentos.csv', file, 'text/csv')}
        upload_response = session.post(f"{base_url}/api/upload-lancamentos", files=files)
        
        if upload_response.status_code == 200:
            result = upload_response.json()
            if result.get('success'):
                print(f"✅ Lançamentos importados: {result.get('registros', 0)} registros")
            else:
                print(f"❌ Erro: {result.get('error')}")
    
    # 4. Executar conciliação automática
    print("\n4. Executando conciliação automática...")
    conciliacao_response = session.post(f"{base_url}/api/conciliacao-automatica")
    if conciliacao_response.status_code == 200:
        result = conciliacao_response.json()
        if result.get('success'):
            print("✅ Conciliação automática executada!")
        else:
            print(f"❌ Erro na conciliação: {result.get('error')}")
    
    # 5. Verificar divergências
    print("\n5. Verificando divergências...")
    divergencias_response = session.get(f"{base_url}/api/divergencias")
    if divergencias_response.status_code == 200:
        divergencias = divergencias_response.json()
        print(f"   📊 Total de divergências: {len(divergencias)}")
        
        if len(divergencias) > 0:
            print("   🎯 Divergências detectadas:")
            for i, div in enumerate(divergencias, 1):
                print(f"   {i}. Tipo: {div['tipo']} - {div['descricao']}")
        else:
            print("   ⚠️ Nenhuma divergência detectada (pode ser normal)")
    else:
        print("❌ Erro ao buscar divergências")
    
    # 6. Verificar estatísticas
    print("\n6. Estatísticas finais...")
    stats_response = session.get(f"{base_url}/api/estatisticas")
    if stats_response.status_code == 200:
        stats = stats_response.json()
        print(f"   📊 Total de extratos: {stats.get('total_extratos', 0)}")
        print(f"   📊 Total de lançamentos: {stats.get('total_lancamentos', 0)}")
        print(f"   📊 Extratos conciliados: {stats.get('extratos_conciliados', 0)}")
        print(f"   📊 Lançamentos conciliados: {stats.get('lancamentos_conciliados', 0)}")
        print(f"   📊 Divergências pendentes: {stats.get('divergencias_pendentes', 0)}")
    
    # 7. Verificar conciliações realizadas
    print("\n7. Verificando conciliações...")
    conciliacoes_response = session.get(f"{base_url}/api/conciliacoes")
    if conciliacoes_response.status_code == 200:
        conciliacoes = conciliacoes_response.json()
        print(f"   📊 Total de conciliações: {len(conciliacoes)}")
        
        if len(conciliacoes) > 0:
            print("   🎯 Últimas conciliações:")
            for i, conc in enumerate(conciliacoes[:3], 1):  # Mostrar apenas as 3 primeiras
                print(f"   {i}. {conc['extrato']['descricao']} - R$ {conc['extrato']['valor']}")
                print(f"      ↔ {conc['lancamento']['descricao']} - R$ {conc['lancamento']['valor']}")
    
    print("\n🎯 TESTE DE DIVERGÊNCIAS FORÇADAS FINALIZADO!")

if __name__ == "__main__":
    # Criar arquivos de teste
    criar_divergencias_forcadas()
    
    # Executar testes
    testar_divergencias_forcadas()
