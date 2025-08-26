import requests
import os

def test_upload():
    # URL do servidor
    url = "http://localhost:5000/api/upload-extrato"
    
    # Arquivo de teste
    file_path = "exemplos/extrato_exemplo.csv"
    
    # Verificar se o arquivo existe
    if not os.path.exists(file_path):
        print(f"Arquivo {file_path} não encontrado!")
        return
    
    # Preparar o upload
    with open(file_path, 'rb') as file:
        files = {'file': (os.path.basename(file_path), file, 'text/csv')}
        
        try:
            print(f"Enviando arquivo {file_path}...")
            response = requests.post(url, files=files)
            
            print(f"Status Code: {response.status_code}")
            print(f"Response: {response.text}")
            
            if response.status_code == 200:
                print("✅ Upload realizado com sucesso!")
            else:
                print("❌ Erro no upload")
                
        except Exception as e:
            print(f"❌ Erro na requisição: {e}")

if __name__ == "__main__":
    test_upload()
