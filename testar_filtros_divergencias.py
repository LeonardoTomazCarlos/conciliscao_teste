#!/usr/bin/env python3
"""
Script para testar os filtros de divergências
"""
import requests
import json

# Configuração
BASE_URL = "http://localhost:8080"
LOGIN_DATA = {
    "username": "admin",
    "password": "admin123"
}

def fazer_login():
    """Fazer login no sistema"""
    print("🔐 Fazendo login...")
    
    response = requests.post(f"{BASE_URL}/api/login", json=LOGIN_DATA)
    if response.status_code == 200:
        print("✅ Login realizado com sucesso!")
        return response.cookies
    else:
        print(f"❌ Erro no login: {response.text}")
        return None

def testar_filtros_divergencias(cookies):
    """Testar diferentes filtros de divergências"""
    
    print("\n🔍 TESTANDO FILTROS DE DIVERGÊNCIAS")
    print("=" * 60)
    
    # Teste 1: Todas as divergências (sem filtros)
    print("\n1️⃣ TESTE: Todas as divergências")
    response = requests.get(f"{BASE_URL}/api/divergencias", cookies=cookies)
    if response.status_code == 200:
        divergencias = response.json()
        print(f"   ✅ {len(divergencias)} divergências encontradas")
        
        # Mostrar tipos encontrados
        tipos = {}
        for div in divergencias:
            tipo = div.get('tipo', 'desconhecido')
            if tipo not in tipos:
                tipos[tipo] = 0
            tipos[tipo] += 1
        
        print("   📊 Tipos encontrados:")
        for tipo, count in tipos.items():
            print(f"      • {tipo}: {count}")
    else:
        print(f"   ❌ Erro: {response.status_code}")
    
    # Teste 2: Filtro por tipo - Órfãos no extrato
    print("\n2️⃣ TESTE: Filtro por tipo - Órfãos no extrato")
    params = {"tipo": "extrato_orfao"}
    response = requests.get(f"{BASE_URL}/api/divergencias", params=params, cookies=cookies)
    if response.status_code == 200:
        divergencias = response.json()
        print(f"   ✅ {len(divergencias)} divergências de extrato órfão encontradas")
        if len(divergencias) > 0:
            print(f"   📋 Exemplo: {divergencias[0].get('descricao', 'N/A')}")
    else:
        print(f"   ❌ Erro: {response.status_code}")
    
    # Teste 3: Filtro por tipo - Órfãos nos lançamentos
    print("\n3️⃣ TESTE: Filtro por tipo - Órfãos nos lançamentos")
    params = {"tipo": "lancamento_orfao"}
    response = requests.get(f"{BASE_URL}/api/divergencias", params=params, cookies=cookies)
    if response.status_code == 200:
        divergencias = response.json()
        print(f"   ✅ {len(divergencias)} divergências de lançamento órfão encontradas")
        if len(divergencias) > 0:
            print(f"   📋 Exemplo: {divergencias[0].get('descricao', 'N/A')}")
    else:
        print(f"   ❌ Erro: {response.status_code}")
    
    # Teste 4: Filtro por tipo - Diferença de valor
    print("\n4️⃣ TESTE: Filtro por tipo - Diferença de valor")
    params = {"tipo": "diferenca_valor"}
    response = requests.get(f"{BASE_URL}/api/divergencias", params=params, cookies=cookies)
    if response.status_code == 200:
        divergencias = response.json()
        print(f"   ✅ {len(divergencias)} divergências de valor encontradas")
        if len(divergencias) > 0:
            print(f"   📋 Exemplo: {divergencias[0].get('descricao', 'N/A')}")
    else:
        print(f"   ❌ Erro: {response.status_code}")
    
    # Teste 5: Filtro por tipo - Duplicatas
    print("\n5️⃣ TESTE: Filtro por tipo - Duplicatas")
    params = {"tipo": "duplicata"}
    response = requests.get(f"{BASE_URL}/api/divergencias", params=params, cookies=cookies)
    if response.status_code == 200:
        divergencias = response.json()
        print(f"   ✅ {len(divergencias)} duplicatas encontradas")
        if len(divergencias) > 0:
            print(f"   📋 Exemplo: {divergencias[0].get('descricao', 'N/A')}")
    else:
        print(f"   ❌ Erro: {response.status_code}")
    
    # Teste 6: Filtro por status
    print("\n6️⃣ TESTE: Filtro por status - Pendente")
    params = {"status": "pendente"}
    response = requests.get(f"{BASE_URL}/api/divergencias", params=params, cookies=cookies)
    if response.status_code == 200:
        divergencias = response.json()
        print(f"   ✅ {len(divergencias)} divergências pendentes encontradas")
    else:
        print(f"   ❌ Erro: {response.status_code}")
    
    # Teste 7: Filtro combinado
    print("\n7️⃣ TESTE: Filtro combinado - Tipo + Status")
    params = {"tipo": "duplicata", "status": "pendente"}
    response = requests.get(f"{BASE_URL}/api/divergencias", params=params, cookies=cookies)
    if response.status_code == 200:
        divergencias = response.json()
        print(f"   ✅ {len(divergencias)} duplicatas pendentes encontradas")
    else:
        print(f"   ❌ Erro: {response.status_code}")
    
    # Teste 8: Filtro por data
    print("\n8️⃣ TESTE: Filtro por data - Hoje")
    from datetime import date
    hoje = date.today().strftime('%Y-%m-%d')
    params = {"data_inicial": hoje, "data_final": hoje}
    response = requests.get(f"{BASE_URL}/api/divergencias", params=params, cookies=cookies)
    if response.status_code == 200:
        divergencias = response.json()
        print(f"   ✅ {len(divergencias)} divergências de hoje encontradas")
    else:
        print(f"   ❌ Erro: {response.status_code}")

def main():
    """Função principal"""
    print("🚀 TESTE DE FILTROS DE DIVERGÊNCIAS")
    print("=" * 50)
    
    # Fazer login
    cookies = fazer_login()
    if not cookies:
        return
    
    # Testar filtros
    testar_filtros_divergencias(cookies)
    
    print("\n" + "=" * 50)
    print("🎯 TESTE CONCLUÍDO")
    print("✅ Verifique os resultados acima")
    print("🌐 Acesse http://localhost:5000 para testar no navegador")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n⚠️ Teste interrompido pelo usuário.")
    except Exception as e:
        print(f"\n❌ Erro durante o teste: {e}")
        import traceback
        traceback.print_exc()