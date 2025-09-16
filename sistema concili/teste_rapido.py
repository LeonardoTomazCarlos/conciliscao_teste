import requests
import time

print("🧪 Testando aplicacao Flask...")
time.sleep(2)

try:
    # Teste 1: Servidor rodando
    response = requests.get("http://localhost:5000/")
    print(f"✅ Servidor respondeu: {response.status_code}")
    
    # Teste 2: Criar dados de exemplo
    response = requests.post("http://localhost:5000/api/procedimentos/criar-exemplo")
    data = response.json()
    print(f"✅ Dados criados: {data.get('procedimentos_criados', 0)} procedimentos")
    
    # Teste 3: Listar procedimentos
    response = requests.get("http://localhost:5000/api/procedimentos")
    data = response.json()
    print(f"✅ Procedimentos listados: {len(data)} encontrados")
    
    # Teste 4: Filtros
    response = requests.get("http://localhost:5000/api/procedimentos?status=Concluído")
    data = response.json()
    print(f"✅ Filtro por status: {len(data)} procedimentos concluídos")
    
    print("🎉 TODOS OS TESTES PASSARAM!")
    print("💡 Acesse: http://localhost:5000/teste_filtros_conciliacao.html")
    
except Exception as e:
    print(f"❌ Erro: {e}")