import requests
import os

def test_cnab400_upload():
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
    
    # 2. Testar upload do primeiro arquivo CNAB400
    print("\n2. Testando upload do primeiro arquivo CNAB400...")
    file_path = "cnab_arquivo1.ret"
    
    if not os.path.exists(file_path):
        print(f"❌ Arquivo {file_path} não encontrado!")
        return
    
    try:
        with open(file_path, 'rb') as file:
            files = {'file': (os.path.basename(file_path), file, 'text/plain')}
            
            print(f"Enviando arquivo {file_path}...")
            upload_response = session.post(f"{base_url}/api/upload-extrato", files=files)
            
            print(f"Upload Status: {upload_response.status_code}")
            print(f"Upload Response: {upload_response.text[:500]}...")  # Primeiros 500 chars
            
            if upload_response.status_code == 200:
                try:
                    result = upload_response.json()
                    if result.get('success'):
                        print("✅ Upload do primeiro arquivo realizado com sucesso!")
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
    
    # 3. Testar upload do segundo arquivo CNAB400 (deve detectar duplicatas)
    print("\n3. Testando upload do segundo arquivo CNAB400 (deve detectar duplicatas)...")
    file_path = "cnab_arquivo2.ret"
    
    if not os.path.exists(file_path):
        print(f"❌ Arquivo {file_path} não encontrado!")
        return
    
    try:
        with open(file_path, 'rb') as file:
            files = {'file': (os.path.basename(file_path), file, 'text/plain')}
            
            print(f"Enviando arquivo {file_path}...")
            upload_response = session.post(f"{base_url}/api/upload-extrato", files=files)
            
            print(f"Upload Status: {upload_response.status_code}")
            print(f"Upload Response: {upload_response.text[:500]}...")  # Primeiros 500 chars
            
            if upload_response.status_code == 200:
                try:
                    result = upload_response.json()
                    if result.get('success'):
                        print("✅ Upload do segundo arquivo realizado com sucesso!")
                        print(f"   Registros importados: {result.get('registros', 0)}")
                        print(f"   Duplicatas detectadas: {result.get('duplicatas', 0)}")
                        
                        # Verificar se detectou a duplicata esperada
                        if result.get('duplicatas', 0) > 0:
                            print("🎯 Duplicata detectada corretamente!")
                        else:
                            print("⚠️ Esperava detectar uma duplicata")
                    else:
                        print(f"❌ Erro no upload: {result.get('error')}")
                except:
                    print("⚠️ Resposta não é JSON válido")
            else:
                print("❌ Erro no upload")
                
    except Exception as e:
        print(f"❌ Erro na requisição de upload: {e}")
    
    # 4. Verificar estatísticas finais
    print("\n4. Verificando estatísticas finais...")
    try:
        stats_response = session.get(f"{base_url}/api/estatisticas")
        if stats_response.status_code == 200:
            stats = stats_response.json()
            print(f"   Total de extratos: {stats.get('total_extratos', 0)}")
            print(f"   Extratos conciliados: {stats.get('extratos_conciliados', 0)}")
            print(f"   Divergências pendentes: {stats.get('divergencias_pendentes', 0)}")
        else:
            print("❌ Erro ao buscar estatísticas")
    except Exception as e:
        print(f"❌ Erro ao buscar estatísticas: {e}")

if __name__ == "__main__":
    test_cnab400_upload()
