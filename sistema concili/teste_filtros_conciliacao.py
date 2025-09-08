#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste dos Filtros de Conciliação
Testa se os filtros da seção de conciliação estão funcionando corretamente
"""

import requests
import json
from datetime import datetime, timedelta

# Configuração
BASE_URL = "http://localhost:5000"
API_URL = f"{BASE_URL}/api/procedimentos"

def test_filtros_conciliacao():
    """Testa todos os filtros da seção de conciliação"""
    
    print("🧪 INICIANDO TESTES DOS FILTROS DE CONCILIAÇÃO\n")
    
    # Teste 1: Listar todos os procedimentos (sem filtros)
    print("📋 Teste 1: Listar todos os procedimentos")
    try:
        response = requests.get(API_URL)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Sucesso - Total de procedimentos: {len(data.get('procedimentos', []))}")
            print(f"📊 Paginação: {data.get('pagination', {})}")
        else:
            print(f"❌ Erro: Status {response.status_code}")
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"❌ Erro na requisição: {e}")
    
    print("\n" + "="*50 + "\n")
    
    # Teste 2: Filtro por data de início
    print("📅 Teste 2: Filtro por data de início (últimos 30 dias)")
    data_inicio = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
    try:
        params = {'data_inicio': data_inicio}
        response = requests.get(API_URL, params=params)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Sucesso - Procedimentos desde {data_inicio}: {len(data.get('procedimentos', []))}")
        else:
            print(f"❌ Erro: Status {response.status_code}")
    except Exception as e:
        print(f"❌ Erro na requisição: {e}")
    
    print("\n" + "="*50 + "\n")
    
    # Teste 3: Filtro por período (últimos 7 dias)
    print("📅 Teste 3: Filtro por período (últimos 7 dias)")
    data_inicio = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
    data_fim = datetime.now().strftime('%Y-%m-%d')
    try:
        params = {
            'data_inicio': data_inicio,
            'data_fim': data_fim
        }
        response = requests.get(API_URL, params=params)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Sucesso - Procedimentos entre {data_inicio} e {data_fim}: {len(data.get('procedimentos', []))}")
        else:
            print(f"❌ Erro: Status {response.status_code}")
    except Exception as e:
        print(f"❌ Erro na requisição: {e}")
    
    print("\n" + "="*50 + "\n")
    
    # Teste 4: Filtro por tipo
    print("🔄 Teste 4: Filtro por tipo")
    tipos_teste = ['automatico', 'manual', 'parcial']
    
    for tipo in tipos_teste:
        try:
            params = {'tipo': tipo}
            response = requests.get(API_URL, params=params)
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Tipo '{tipo}': {len(data.get('procedimentos', []))} procedimentos")
            else:
                print(f"❌ Erro para tipo '{tipo}': Status {response.status_code}")
        except Exception as e:
            print(f"❌ Erro para tipo '{tipo}': {e}")
    
    print("\n" + "="*50 + "\n")
    
    # Teste 5: Filtro por status
    print("📊 Teste 5: Filtro por status")
    status_teste = ['em_andamento', 'concluido', 'erro', 'cancelado']
    
    for status in status_teste:
        try:
            params = {'status': status}
            response = requests.get(API_URL, params=params)
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Status '{status}': {len(data.get('procedimentos', []))} procedimentos")
            else:
                print(f"❌ Erro para status '{status}': Status {response.status_code}")
        except Exception as e:
            print(f"❌ Erro para status '{status}': {e}")
    
    print("\n" + "="*50 + "\n")
    
    # Teste 6: Paginação
    print("📄 Teste 6: Paginação")
    try:
        params = {'page': 1, 'per_page': 5}
        response = requests.get(API_URL, params=params)
        if response.status_code == 200:
            data = response.json()
            pagination = data.get('pagination', {})
            print(f"✅ Página 1, 5 por página:")
            print(f"   - Registros retornados: {len(data.get('procedimentos', []))}")
            print(f"   - Total: {pagination.get('total', 0)}")
            print(f"   - Páginas: {pagination.get('pages', 0)}")
            print(f"   - Página atual: {pagination.get('page', 0)}")
        else:
            print(f"❌ Erro: Status {response.status_code}")
    except Exception as e:
        print(f"❌ Erro na requisição: {e}")
    
    print("\n" + "="*50 + "\n")
    
    # Teste 7: Filtros combinados
    print("🔗 Teste 7: Filtros combinados")
    try:
        params = {
            'data_inicio': (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d'),
            'status': 'concluido',
            'per_page': 3
        }
        response = requests.get(API_URL, params=params)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Filtros combinados (últimos 30 dias + status concluído):")
            print(f"   - Procedimentos encontrados: {len(data.get('procedimentos', []))}")
            
            # Mostrar detalhes dos procedimentos encontrados
            for proc in data.get('procedimentos', [])[:3]:
                print(f"   - ID: {proc.get('id')} | Status: {proc.get('status')} | Data: {proc.get('data_criacao')}")
        else:
            print(f"❌ Erro: Status {response.status_code}")
    except Exception as e:
        print(f"❌ Erro na requisição: {e}")
    
    print("\n🎯 TESTES DOS FILTROS CONCLUÍDOS!")

def test_frontend_filtros():
    """Testa a integração frontend dos filtros"""
    
    print("\n🖥️  TESTANDO INTEGRAÇÃO FRONTEND\n")
    
    # Verificar se a página principal carrega
    try:
        response = requests.get(BASE_URL)
        if response.status_code == 200:
            print("✅ Página principal carrega corretamente")
            
            # Verificar se tem os elementos de filtro
            content = response.text
            elementos_filtro = [
                'filtro-data-inicio',
                'filtro-data-fim', 
                'filtro-tipo',
                'filtro-status',
                'aplicarFiltros()',
                'limparFiltros()'
            ]
            
            for elemento in elementos_filtro:
                if elemento in content:
                    print(f"✅ Elemento '{elemento}' encontrado no HTML")
                else:
                    print(f"❌ Elemento '{elemento}' NÃO encontrado no HTML")
        else:
            print(f"❌ Erro ao carregar página principal: Status {response.status_code}")
    except Exception as e:
        print(f"❌ Erro ao acessar página principal: {e}")

if __name__ == "__main__":
    test_filtros_conciliacao()
    test_frontend_filtros()
