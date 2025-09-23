#!/usr/bin/env python3
"""
Script para testar a detecção de divergências no sistema
"""
import requests
import json
import time

# Configuração
BASE_URL = "http://localhost:5000"
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

def limpar_dados(cookies):
    """Limpar dados existentes"""
    print("🧹 Limpando dados existentes...")
    
    # Limpar extratos
    response = requests.delete(f"{BASE_URL}/api/extratos", cookies=cookies)
    print(f"   Extratos: {response.status_code}")
    
    # Limpar lançamentos
    response = requests.delete(f"{BASE_URL}/api/lancamentos", cookies=cookies)
    print(f"   Lançamentos: {response.status_code}")
    
    # Limpar divergências
    response = requests.delete(f"{BASE_URL}/api/divergencias", cookies=cookies)
    print(f"   Divergências: {response.status_code}")

def fazer_upload_arquivo(cookies, arquivo, tipo):
    """Fazer upload de um arquivo"""
    print(f"📤 Fazendo upload do arquivo {arquivo}...")
    
    try:
        with open(f"sistema concili/{arquivo}", 'rb') as f:
            files = {'file': (arquivo, f, 'text/csv')}
            data = {'tipo': tipo}
            
            response = requests.post(
                f"{BASE_URL}/api/upload",
                files=files,
                data=data,
                cookies=cookies
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"   ✅ Upload concluído: {result.get('message', 'Sucesso')}")
                return True
            else:
                print(f"   ❌ Erro no upload: {response.text}")
                return False
    except Exception as e:
        print(f"   ❌ Erro ao abrir arquivo: {e}")
        return False

def executar_conciliacao_automatica(cookies):
    """Executar conciliação automática"""
    print("🔄 Executando conciliação automática...")
    
    response = requests.post(f"{BASE_URL}/api/conciliacao-automatica", cookies=cookies)
    
    if response.status_code == 200:
        result = response.json()
        print(f"   ✅ Conciliação concluída!")
        print(f"   📊 Conciliações realizadas: {result.get('conciliados', 0)}")
        return True
    else:
        print(f"   ❌ Erro na conciliação: {response.text}")
        return False

def verificar_divergencias(cookies):
    """Verificar divergências detectadas"""
    print("🔍 Verificando divergências detectadas...")
    
    response = requests.get(f"{BASE_URL}/api/divergencias", cookies=cookies)
    
    if response.status_code == 200:
        divergencias = response.json()
        print(f"   📊 Total de divergências detectadas: {len(divergencias)}")
        
        # Agrupar por tipo
        tipos = {}
        for div in divergencias:
            tipo = div.get('tipo', 'desconhecido')
            if tipo not in tipos:
                tipos[tipo] = 0
            tipos[tipo] += 1
        
        print("   📋 Divergências por tipo:")
        for tipo, count in tipos.items():
            print(f"      • {tipo}: {count}")
        
        if len(divergencias) > 0:
            print("\n   🔍 Detalhes das divergências:")
            for i, div in enumerate(divergencias[:10], 1):  # Mostrar apenas as primeiras 10
                print(f"      {i}. {div.get('tipo', 'N/A')}: {div.get('descricao', 'N/A')}")
        
        return len(divergencias)
    else:
        print(f"   ❌ Erro ao buscar divergências: {response.text}")
        return 0

def verificar_extratos_lancamentos(cookies):
    """Verificar dados carregados"""
    print("📊 Verificando dados carregados...")
    
    # Verificar extratos
    response = requests.get(f"{BASE_URL}/api/extratos", cookies=cookies)
    if response.status_code == 200:
        extratos = response.json()
        print(f"   📋 Extratos carregados: {len(extratos)}")
    else:
        print(f"   ❌ Erro ao buscar extratos: {response.text}")
    
    # Verificar lançamentos
    response = requests.get(f"{BASE_URL}/api/lancamentos", cookies=cookies)
    if response.status_code == 200:
        lancamentos = response.json()
        print(f"   📋 Lançamentos carregados: {len(lancamentos)}")
    else:
        print(f"   ❌ Erro ao buscar lançamentos: {response.text}")

def main():
    """Função principal"""
    print("🚀 TESTE DE DETECÇÃO DE DIVERGÊNCIAS")
    print("=" * 50)
    
    # 1. Fazer login
    cookies = fazer_login()
    if not cookies:
        return
    
    # 2. Limpar dados existentes
    limpar_dados(cookies)
    
    # 3. Fazer upload dos arquivos de teste
    arquivos_teste = [
        ("extrato_bancario_multiplas_divergencias.csv", "extrato"),
        ("lancamentos_contabeis_multiplas_divergencias.csv", "lancamento")
    ]
    
    print("\n📤 FAZENDO UPLOAD DOS ARQUIVOS DE TESTE")
    for arquivo, tipo in arquivos_teste:
        if not fazer_upload_arquivo(cookies, arquivo, tipo):
            print(f"❌ Falha no upload de {arquivo}. Abortando teste.")
            return
    
    # 4. Verificar dados carregados
    print("\n")
    verificar_extratos_lancamentos(cookies)
    
    # 5. Executar conciliação automática
    print("\n")
    if not executar_conciliacao_automatica(cookies):
        return
    
    # 6. Verificar divergências
    print("\n")
    divergencias_encontradas = verificar_divergencias(cookies)
    
    # 7. Resultado final
    print("\n" + "=" * 50)
    print("🎯 RESULTADO DO TESTE")
    print("=" * 50)
    
    if divergencias_encontradas > 0:
        print(f"✅ SUCESSO! {divergencias_encontradas} divergências detectadas.")
        print("   O sistema está funcionando corretamente!")
    else:
        print("❌ FALHA! Nenhuma divergência detectada.")
        print("   Verificar implementação da detecção de divergências.")
    
    print(f"\n🌐 Acesse {BASE_URL} para ver os resultados no navegador.")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n⚠️ Teste interrompido pelo usuário.")
    except Exception as e:
        print(f"\n❌ Erro durante o teste: {e}")
        import traceback
        traceback.print_exc()