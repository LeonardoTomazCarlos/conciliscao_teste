#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste simples para verificar se a aplicação está funcionando.
"""

import requests
import json
import time

def testar_aplicacao():
    """Testa se a aplicação Flask está funcionando corretamente."""
    
    base_url = "http://localhost:5000"
    
    print("🧪 TESTE DO SISTEMA DE CONCILIAÇÃO")
    print("=" * 50)
    
    # Teste 1: Verificar se o servidor está rodando
    print("\n1️⃣ Testando se o servidor está rodando...")
    try:
        response = requests.get(f"{base_url}/", timeout=5)
        if response.status_code == 200:
            print("✅ Servidor está rodando na porta 5000")
        else:
            print(f"❌ Servidor retornou status {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Erro ao conectar com o servidor: {e}")
        return False
    
    # Teste 2: Criar dados de exemplo
    print("\n2️⃣ Testando criação de dados de exemplo...")
    try:
        response = requests.post(f"{base_url}/api/procedimentos/criar-exemplo", timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print(f"✅ Dados criados: {data['procedimentos_criados']} procedimentos")
            else:
                print(f"❌ Erro na criação: {data.get('error', 'Erro desconhecido')}")
        else:
            print(f"❌ Erro HTTP {response.status_code}: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Erro na requisição: {e}")
    
    # Teste 3: Listar procedimentos
    print("\n3️⃣ Testando listagem de procedimentos...")
    try:
        response = requests.get(f"{base_url}/api/procedimentos", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Encontrados {len(data)} procedimentos")
            
            # Mostrar alguns detalhes
            for i, proc in enumerate(data[:3]):  # Mostrar apenas os primeiros 3
                print(f"   📋 {i+1}. ID: {proc['id_procedimento']} | "
                      f"Status: {proc['status']} | "
                      f"Método: {proc['metodo']} | "
                      f"Conciliações: {proc['total_conciliacoes']}")
        else:
            print(f"❌ Erro HTTP {response.status_code}: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Erro na requisição: {e}")
    
    # Teste 4: Testar filtros
    print("\n4️⃣ Testando filtros...")
    filtros_teste = [
        {"status": "Concluído"},
        {"metodo": "Automática"},
        {"status": "Em Andamento", "metodo": "Manual"}
    ]
    
    for i, filtro in enumerate(filtros_teste, 1):
        try:
            params = "&".join([f"{k}={v}" for k, v in filtro.items()])
            response = requests.get(f"{base_url}/api/procedimentos?{params}", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                print(f"   🔍 Filtro {i} ({filtro}): {len(data)} resultados")
            else:
                print(f"   ❌ Filtro {i} falhou: HTTP {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"   ❌ Erro no filtro {i}: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 TESTE CONCLUÍDO!")
    print("\n💡 Para testar manualmente:")
    print(f"   🌐 Interface principal: {base_url}")
    print(f"   🧪 Página de teste: {base_url}/teste_filtros_conciliacao.html")
    
    return True

if __name__ == "__main__":
    # Aguardar um pouco para o servidor iniciar
    print("⏳ Aguardando servidor iniciar...")
    time.sleep(2)
    
    testar_aplicacao()