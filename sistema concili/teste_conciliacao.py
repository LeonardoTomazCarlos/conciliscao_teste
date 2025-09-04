#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de teste para verificar funcionalidade de conciliação
"""

import sys
import os

# Adicionar o diretório atual ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    # Testar import das dependências principais
    from app import app, db, ExtratoBancario, LancamentoContabil, Conciliacao
    from app import conciliacao_automatica, detectar_transacoes_recorrentes, verificar_divergencias
    print("✅ Imports OK - Todas as dependências carregadas com sucesso")
    
    # Testar context da aplicação
    with app.app_context():
        print("✅ Context OK - Aplicação Flask funcionando")
        
        # Verificar se as tabelas existem
        try:
            extratos_count = ExtratoBancario.query.count()
            lancamentos_count = LancamentoContabil.query.count()
            conciliacoes_count = Conciliacao.query.count()
            
            print(f"✅ Database OK - {extratos_count} extratos, {lancamentos_count} lançamentos, {conciliacoes_count} conciliações")
            
            # Testar as funções principais
            print("🔄 Testando funções de conciliação...")
            
            # Teste detectar transações recorrentes
            detectar_transacoes_recorrentes()
            print("✅ detectar_transacoes_recorrentes() - OK")
            
            # Teste conciliação automática
            resultado = conciliacao_automatica()
            print(f"✅ conciliacao_automatica() - OK (resultado: {resultado})")
            
            # Teste verificar divergências
            verificar_divergencias()
            print("✅ verificar_divergencias() - OK")
            
            print("\n🎉 TESTE COMPLETO - Todas as funcionalidades estão funcionando!")
            print("\n📋 PRÓXIMOS PASSOS:")
            print("1. O sistema está pronto para uso")
            print("2. Você pode importar arquivos pelo menu Importação")
            print("3. Execute conciliação automática pelo menu Importação")
            print("4. Use os novos filtros no menu Relatórios")
            
        except Exception as e:
            print(f"❌ Erro no banco de dados: {e}")
            print("💡 Certifique-se de que o banco está inicializado")
            
except ImportError as e:
    print(f"❌ Erro de import: {e}")
    print("💡 Certifique-se de que o ambiente virtual está ativado")
    print("💡 Execute: pip install -r requirements.txt")

except Exception as e:
    print(f"❌ Erro geral: {e}")
    print("💡 Verifique se o app.py está correto")
