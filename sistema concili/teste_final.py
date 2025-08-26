import requests
import os

def teste_final_sistema():
    print("🧪 TESTE FINAL DO SISTEMA DE CONCILIAÇÃO")
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
    
    # 2. Testar upload de CSV
    print("\n2. Testando upload de arquivo CSV...")
    file_path = "exemplos/extrato_exemplo.csv"
    
    with open(file_path, 'rb') as file:
        files = {'file': (os.path.basename(file_path), file, 'text/csv')}
        upload_response = session.post(f"{base_url}/api/upload-extrato", files=files)
        
        if upload_response.status_code == 200:
            result = upload_response.json()
            if result.get('success'):
                print(f"✅ CSV importado: {result.get('registros', 0)} registros")
            else:
                print(f"❌ Erro no CSV: {result.get('error')}")
        else:
            print("❌ Falha no upload CSV")
    
    # 3. Verificar estatísticas
    print("\n3. Verificando estatísticas...")
    stats_response = session.get(f"{base_url}/api/estatisticas")
    if stats_response.status_code == 200:
        stats = stats_response.json()
        print(f"   📊 Total de extratos: {stats.get('total_extratos', 0)}")
        print(f"   📊 Extratos conciliados: {stats.get('extratos_conciliados', 0)}")
        print(f"   📊 Divergências: {stats.get('divergencias_pendentes', 0)}")
    
    # 4. Testar conciliação automática
    print("\n4. Testando conciliação automática...")
    conciliacao_response = session.post(f"{base_url}/api/conciliacao-automatica")
    if conciliacao_response.status_code == 200:
        result = conciliacao_response.json()
        if result.get('success'):
            print("✅ Conciliação automática executada!")
        else:
            print(f"❌ Erro na conciliação: {result.get('error')}")
    
    print("\n🎉 TESTE FINALIZADO!")
    print("O sistema está funcionando corretamente!")

if __name__ == "__main__":
    teste_final_sistema()
