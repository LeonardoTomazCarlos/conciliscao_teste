#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para testar todos os filtros com arquivos específicos
"""

import requests
import os
import sys
from datetime import datetime, timedelta

# URL base da aplicação
BASE_URL = "http://localhost:5000"

def upload_arquivo(session, arquivo_extrato, arquivo_lancamentos, nome_teste):
    """Upload de um par de arquivos de teste"""
    print(f"\n📁 Testando: {nome_teste}")
    print("-" * 50)
    
    # Verificar se os arquivos existem
    if not os.path.exists(arquivo_extrato):
        print(f"❌ Arquivo não encontrado: {arquivo_extrato}")
        return False
        
    if not os.path.exists(arquivo_lancamentos):
        print(f"❌ Arquivo não encontrado: {arquivo_lancamentos}")
        return False
    
    try:
        # Upload do extrato
        print(f"📤 Upload: {arquivo_extrato}")
        with open(arquivo_extrato, 'rb') as f:
            files = {'file': (arquivo_extrato, f, 'text/csv')}
            data = {'tipo': 'extrato'}
            response = session.post(f"{BASE_URL}/upload", files=files, data=data)
        
        if response.status_code != 200:
            print(f"❌ Erro no upload do extrato: {response.status_code}")
            return False
        
        # Upload dos lançamentos
        print(f"📤 Upload: {arquivo_lancamentos}")
        with open(arquivo_lancamentos, 'rb') as f:
            files = {'file': (arquivo_lancamentos, f, 'text/csv')}
            data = {'tipo': 'lancamentos'}
            response = session.post(f"{BASE_URL}/upload", files=files, data=data)
        
        if response.status_code != 200:
            print(f"❌ Erro no upload dos lançamentos: {response.status_code}")
            return False
        
        # Executar conciliação
        print("🔄 Executando conciliação...")
        response = session.post(f"{BASE_URL}/api/conciliacao/executar")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Conciliação executada!")
            print(f"   - Conciliadas: {result.get('conciliadas', 0)}")
            print(f"   - Divergências: {result.get('divergencias', 0)}")
            return True
        else:
            print(f"❌ Erro na conciliação: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Erro: {str(e)}")
        return False

def testar_filtro(nome_filtro, params):
    """Testa um filtro específico"""
    print(f"\n🔍 Testando filtro: {nome_filtro}")
    print(f"Parâmetros: {params}")
    
    try:
        response = requests.get(f"{BASE_URL}/api/conciliacao", params=params)
        
        if response.status_code == 200:
            results = response.json()
            print(f"✅ Encontrados: {len(results)} registros")
            
            # Mostrar alguns exemplos
            for i, result in enumerate(results[:3]):
                data = result.get('data', 'N/A')
                valor = result.get('valor', 0)
                status = result.get('status', 'N/A')
                print(f"   {i+1}. {data} - R$ {float(valor):8.2f} - {status}")
            
            if len(results) > 3:
                print(f"   ... e mais {len(results) - 3} registros")
                
            return len(results)
        else:
            print(f"❌ Erro: {response.status_code}")
            return 0
            
    except Exception as e:
        print(f"❌ Erro na requisição: {str(e)}")
        return 0

def main():
    print("🧪 TESTE ESPECÍFICO DE FILTROS COM ARQUIVOS SEPARADOS")
    print("=" * 60)
    
    # Verificar se o servidor está rodando
    try:
        response = requests.get(f"{BASE_URL}/", timeout=5)
        if response.status_code == 200:
            print("✅ Servidor está rodando!")
        else:
            print(f"⚠️ Servidor respondeu com status: {response.status_code}")
    except requests.exceptions.RequestException:
        print("❌ Servidor não está rodando!")
        print("Execute: python app.py")
        return
    
    session = requests.Session()
    
    # 1. TESTAR DADOS CONCILIADOS
    print("\n" + "="*60)
    print("🎯 TESTE 1: DADOS CONCILIADOS")
    print("="*60)
    
    sucesso = upload_arquivo(
        session,
        "filtro_conciliado_extrato.csv",
        "filtro_conciliado_lancamentos.csv",
        "Dados que devem ser conciliados"
    )
    
    if sucesso:
        total = testar_filtro("Status: conciliado", {"status": "conciliado"})
        print(f"📊 Resultado esperado: registros conciliados encontrados ({total})")
    
    # 2. TESTAR DADOS DIVERGENTES
    print("\n" + "="*60)
    print("⚠️ TESTE 2: DADOS DIVERGENTES")
    print("="*60)
    
    sucesso = upload_arquivo(
        session,
        "filtro_divergente_extrato.csv",
        "filtro_divergente_lancamentos.csv",
        "Dados com divergências propositais"
    )
    
    if sucesso:
        total = testar_filtro("Status: divergente", {"status": "divergente"})
        print(f"📊 Resultado esperado: registros divergentes encontrados ({total})")
    
    # 3. TESTAR FILTRO DE DATA - AGOSTO
    print("\n" + "="*60)
    print("📅 TESTE 3: FILTRO POR DATA (AGOSTO)")
    print("="*60)
    
    sucesso = upload_arquivo(
        session,
        "filtro_data_agosto_extrato.csv",
        "filtro_data_agosto_lancamentos.csv",
        "Dados de agosto para teste de filtro por data"
    )
    
    if sucesso:
        # Testar filtro de agosto
        total = testar_filtro("Data: agosto 2025", {
            "data_inicio": "2025-08-01",
            "data_fim": "2025-08-31"
        })
        print(f"📊 Resultado esperado: registros de agosto encontrados ({total})")
        
        # Testar filtro que NÃO deve retornar dados de agosto
        total = testar_filtro("Data: setembro 2025", {
            "data_inicio": "2025-09-01",
            "data_fim": "2025-09-30"
        })
        print(f"📊 Resultado esperado: poucos ou nenhum registro de setembro ({total})")
    
    # 4. TESTAR FILTRO DE VALOR ALTO
    print("\n" + "="*60)
    print("💰 TESTE 4: FILTRO POR VALOR ALTO")
    print("="*60)
    
    sucesso = upload_arquivo(
        session,
        "filtro_valor_alto_extrato.csv",
        "filtro_valor_alto_lancamentos.csv",
        "Dados com valores altos"
    )
    
    if sucesso:
        total = testar_filtro("Valor mínimo: R$ 5000", {"valor_min": "5000"})
        print(f"📊 Resultado esperado: registros acima de R$ 5000 ({total})")
        
        total = testar_filtro("Valor mínimo: R$ 12000", {"valor_min": "12000"})
        print(f"📊 Resultado esperado: apenas valores muito altos ({total})")
    
    # 5. TESTAR FILTRO DE VALOR BAIXO
    print("\n" + "="*60)
    print("🪙 TESTE 5: FILTRO POR VALOR BAIXO")
    print("="*60)
    
    sucesso = upload_arquivo(
        session,
        "filtro_valor_baixo_extrato.csv",
        "filtro_valor_baixo_lancamentos.csv",
        "Dados com valores baixos"
    )
    
    if sucesso:
        total = testar_filtro("Valor máximo: R$ 200", {"valor_max": "200"})
        print(f"📊 Resultado esperado: registros até R$ 200 ({total})")
        
        total = testar_filtro("Valor máximo: R$ 50", {"valor_max": "50"})
        print(f"📊 Resultado esperado: apenas valores muito baixos ({total})")
    
    # 6. TESTAR FILTROS COMBINADOS
    print("\n" + "="*60)
    print("🔗 TESTE 6: FILTROS COMBINADOS")
    print("="*60)
    
    # Testar múltiplos filtros juntos
    total = testar_filtro("Data setembro + Valor alto", {
        "data_inicio": "2025-09-01",
        "data_fim": "2025-09-30",
        "valor_min": "1000"
    })
    print(f"📊 Resultado: registros de setembro com valor alto ({total})")
    
    total = testar_filtro("Status conciliado + Valor baixo", {
        "status": "conciliado",
        "valor_max": "1000"
    })
    print(f"📊 Resultado: registros conciliados com valor baixo ({total})")
    
    # 7. TESTAR FILTROS SEM RESULTADOS
    print("\n" + "="*60)
    print("🚫 TESTE 7: FILTROS SEM RESULTADOS")
    print("="*60)
    
    total = testar_filtro("Data impossível", {
        "data_inicio": "2026-01-01",
        "data_fim": "2026-01-31"
    })
    print(f"📊 Resultado esperado: nenhum registro ({total})")
    
    total = testar_filtro("Valor impossível", {"valor_min": "100000"})
    print(f"📊 Resultado esperado: nenhum registro ({total})")
    
    print("\n" + "="*60)
    print("🎉 TODOS OS TESTES DE FILTROS CONCLUÍDOS!")
    print("="*60)
    
    # Resumo final
    print("\n📋 RESUMO DOS ARQUIVOS CRIADOS:")
    arquivos_teste = [
        "filtro_conciliado_extrato.csv / filtro_conciliado_lancamentos.csv",
        "filtro_divergente_extrato.csv / filtro_divergente_lancamentos.csv", 
        "filtro_data_agosto_extrato.csv / filtro_data_agosto_lancamentos.csv",
        "filtro_valor_alto_extrato.csv / filtro_valor_alto_lancamentos.csv",
        "filtro_valor_baixo_extrato.csv / filtro_valor_baixo_lancamentos.csv"
    ]
    
    for i, arquivo in enumerate(arquivos_teste, 1):
        print(f"   {i}. {arquivo}")
    
    print("\n🔍 FILTROS TESTADOS:")
    filtros_testados = [
        "Status (conciliado/divergente)",
        "Data (período específico)",
        "Valor mínimo e máximo", 
        "Combinação de filtros",
        "Filtros sem resultados"
    ]
    
    for i, filtro in enumerate(filtros_testados, 1):
        print(f"   {i}. {filtro}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n⏹️ Teste interrompido pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro geral: {str(e)}")
