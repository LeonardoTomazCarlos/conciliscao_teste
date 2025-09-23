#!/usr/bin/env python3
"""
Script para verificar dados no banco de dados
"""
import sys
import os

# Adicionar o diretório do sistema ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'sistema concili'))

try:
    from app import db, ExtratoBancario, LancamentoContabil, Divergencia, app
    
    with app.app_context():
        print("🔍 VERIFICANDO DADOS NO BANCO...")
        print("=" * 50)
        
        # Verificar extratos
        extratos = ExtratoBancario.query.all()
        print(f"📋 Extratos no banco: {len(extratos)}")
        
        if extratos:
            print("   Primeiros 3 extratos:")
            for i, extrato in enumerate(extratos[:3], 1):
                print(f"   {i}. {extrato.data} - {extrato.descricao} - R$ {extrato.valor}")
        
        # Verificar lançamentos
        lancamentos = LancamentoContabil.query.all()
        print(f"\n📋 Lançamentos no banco: {len(lancamentos)}")
        
        if lancamentos:
            print("   Primeiros 3 lançamentos:")
            for i, lanc in enumerate(lancamentos[:3], 1):
                print(f"   {i}. {lanc.data} - {lanc.descricao} - R$ {lanc.valor}")
        
        # Verificar divergências
        divergencias = Divergencia.query.all()
        print(f"\n🔍 Divergências no banco: {len(divergencias)}")
        
        if divergencias:
            print("   Divergências encontradas:")
            for i, div in enumerate(divergencias, 1):
                print(f"   {i}. {div.tipo}: {div.descricao}")
        
        print("\n" + "=" * 50)
        print("🎯 RESUMO:")
        print(f"   📊 {len(extratos)} extratos")
        print(f"   📋 {len(lancamentos)} lançamentos") 
        print(f"   🔍 {len(divergencias)} divergências")
        
        if len(extratos) > 0 and len(lancamentos) > 0 and len(divergencias) == 0:
            print("\n⚠️ PROBLEMA: Existem dados mas nenhuma divergência foi detectada!")
            print("   Isso indica que a função verificar_divergencias() não está funcionando.")
        elif len(divergencias) > 0:
            print("\n✅ SUCESSO: Divergências foram detectadas corretamente!")
        else:
            print("\n📝 INFO: Não há dados suficientes para análise.")

except Exception as e:
    print(f"❌ Erro: {e}")
    import traceback
    traceback.print_exc()