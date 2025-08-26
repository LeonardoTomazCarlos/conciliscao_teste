import requests
import os

def test_complete_upload():
    # URL base
    base_url = "http://localhost:5000"
    
    # Criar sessão para manter cookies
    session = requests.Session()
    
    # 1. Fazer login
    print("1. Fazendo login...")
    login_data = {
        'username': 'admin',
        'password': 'admin123'
    }
    
    try:
        login_response = session.post(f"{base_url}/login", json=login_data)
        print(f"Login Status: {login_response.status_code}")
        
        if login_response.status_code == 200:
            login_result = login_response.json()
            if login_result.get('success'):
                print("✅ Login realizado com sucesso!")
            else:
                print(f"❌ Erro no login: {login_result.get('error')}")
                return
        else:
            print(f"❌ Erro no login: {login_response.status_code}")
            return
            
    except Exception as e:
        print(f"❌ Erro na requisição de login: {e}")
        return
    
    # 2. Testar upload de extrato
    print("\n2. Testando upload de extrato...")
    file_path = "exemplos/extrato_exemplo.csv"
    
    if not os.path.exists(file_path):
        print(f"❌ Arquivo {file_path} não encontrado!")
        return
    
    try:
        with open(file_path, 'rb') as file:
            files = {'file': (os.path.basename(file_path), file, 'text/csv')}
            
            print(f"Enviando arquivo {file_path}...")
            upload_response = session.post(f"{base_url}/api/upload-extrato", files=files)
            
            print(f"Upload Status: {upload_response.status_code}")
            print(f"Upload Response: {upload_response.text[:500]}...")  # Primeiros 500 chars
            
            if upload_response.status_code == 200:
                try:
                    result = upload_response.json()
                    if result.get('success'):
                        print("✅ Upload realizado com sucesso!")
                        print(f"   Registros importados: {result.get('registros', 0)}")
                        print(f"   Duplicatas detectadas: {result.get('duplicatas', 0)}")
                    else:
                        print(f"❌ Erro no upload: {result.get('error')}")
                except:
                    print("⚠️ Resposta não é JSON válido")
            else:
                print("❌ Erro no upload")
                
    except Exception as e:
        print(f"❌ Erro na requisição de upload: {e}")
    
    # 3. Testar upload de lançamentos
    print("\n3. Testando upload de lançamentos...")
    file_path = "exemplos/lancamentos_exemplo.csv"
    
    if not os.path.exists(file_path):
        print(f"❌ Arquivo {file_path} não encontrado!")
        return
    
    try:
        with open(file_path, 'rb') as file:
            files = {'file': (os.path.basename(file_path), file, 'text/csv')}
            
            print(f"Enviando arquivo {file_path}...")
            upload_response = session.post(f"{base_url}/api/upload-lancamentos", files=files)
            
            print(f"Upload Status: {upload_response.status_code}")
            print(f"Upload Response: {upload_response.text[:500]}...")  # Primeiros 500 chars
            
            if upload_response.status_code == 200:
                try:
                    result = upload_response.json()
                    if result.get('success'):
                        print("✅ Upload realizado com sucesso!")
                        print(f"   Registros importados: {result.get('registros', 0)}")
                        print(f"   Duplicatas detectadas: {result.get('duplicatas', 0)}")
                    else:
                        print(f"❌ Erro no upload: {result.get('error')}")
                except:
                    print("⚠️ Resposta não é JSON válido")
            else:
                print("❌ Erro no upload")
                
    except Exception as e:
        print(f"❌ Erro na requisição de upload: {e}")

if __name__ == "__main__":
    test_complete_upload()
