#!/usr/bin/env python3
"""
Script para iniciar o Flask de forma robusta
"""
import sys
import os

# Adicionar o diretório do sistema ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'sistema concili'))

try:
    from app import app
    print("🚀 Iniciando Flask...")
    app.run(debug=True, host='0.0.0.0', port=5000)
except Exception as e:
    print(f"❌ Erro ao iniciar Flask: {e}")
    import traceback
    traceback.print_exc()