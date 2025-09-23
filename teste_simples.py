#!/usr/bin/env python3
"""
Teste simples para verificar divergências
"""
import requests
import time

def testar_sistema():
    print("🔍 Testando sistema de divergências...")
    
    try:
        # Testar se o sistema está rodando
        response = requests.get("http://localhost:5000", timeout=5)
        print(f"✅ Sistema respondeu: {response.status_code}")
        
        # Tentar fazer login
        login_data = {"username": "admin", "password": "admin123"}
        response = requests.post("http://localhost:5000/api/login", json=login_data, timeout=5)
        
        if response.status_code == 200:
            print("✅ Login realizado com sucesso!")
            cookies = response.cookies
            
            # Verificar divergências existentes
            response = requests.get("http://localhost:5000/api/divergencias", cookies=cookies, timeout=5)
            if response.status_code == 200:
                divergencias = response.json()
                print(f"📊 Divergências encontradas: {len(divergencias)}")
                return len(divergencias)
            else:
                print(f"❌ Erro ao buscar divergências: {response.status_code}")
        else:
            print(f"❌ Erro no login: {response.status_code}")
    
    except requests.exceptions.ConnectionError:
        print("❌ Sistema não está rodando! Execute: python app.py")
    except Exception as e:
        print(f"❌ Erro: {e}")
    
    return 0

if __name__ == '__main__':
    resultado = testar_sistema()
    print(f"\n🎯 Resultado: {resultado} divergências")