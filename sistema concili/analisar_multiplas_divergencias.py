#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Análise completa das múltiplas divergências criadas para teste
"""

import pandas as pd
from datetime import datetime

def analisar_multiplas_divergencias():
    print("🔍 ANÁLISE COMPLETA - MÚLTIPLAS DIVERGÊNCIAS")
    print("="*60)
    
    try:
        # Carregar arquivos
        extrato = pd.read_csv('extrato_multiplas_divergencias.csv')
        contabil = pd.read_csv('contabil_multiplas_divergencias.csv')
        
        print(f"\n📊 RESUMO DOS ARQUIVOS:")
        print(f"   Extrato Bancário: {len(extrato)} registros")
        print(f"   Lançamentos Contábeis: {len(contabil)} registros")
        
        # Análise por documento
        print(f"\n📋 ANÁLISE POR DOCUMENTO:")
        print("-" * 50)
        
        docs_extrato = set(extrato['Numero_Documento'].tolist())
        docs_contabil = set(contabil['Numero_Documento'].tolist())
        
        # Documentos comuns
        docs_comuns = docs_extrato & docs_contabil
        print(f"✅ Documentos em ambos os arquivos: {len(docs_comuns)}")
        
        # Documentos só no extrato
        docs_so_extrato = docs_extrato - docs_contabil
        print(f"⚠️  Só no extrato bancário: {len(docs_so_extrato)}")
        if docs_so_extrato:
        for doc in sorted(docs_so_extrato):
            row = extrato[extrato['Numero_Documento'] == doc].iloc[0]
            print(f"   • {doc}: R$ {row['Valor']:.2f} - {row['Descrição']}")        # Documentos só no contábil
        docs_so_contabil = docs_contabil - docs_extrato
        print(f"⚠️  Só nos lançamentos contábeis: {len(docs_so_contabil)}")
        if docs_so_contabil:
        for doc in sorted(docs_so_contabil):
            row = contabil[contabil['Numero_Documento'] == doc].iloc[0]
            print(f"   • {doc}: R$ {row['Valor']:.2f} - {row['Descrição']}")        # Análise de valores diferentes
        print(f"\n💰 DIVERGÊNCIAS DE VALORES:")
        print("-" * 40)
        divergencias_valor = []
        
        for doc in docs_comuns:
            valor_extrato = extrato[extrato['Numero_Documento'] == doc]['Valor'].iloc[0]
            valor_contabil = contabil[contabil['Numero_Documento'] == doc]['Valor'].iloc[0]
            
            # Ajustar sinal do extrato (débitos são negativos)
            if extrato[extrato['Numero_Documento'] == doc]['Tipo'].iloc[0] == 'Debito':
                valor_extrato_abs = abs(valor_extrato)
            else:
                valor_extrato_abs = valor_extrato
            
            if abs(valor_extrato_abs - valor_contabil) > 0.01:  # Tolerância para diferenças mínimas
                divergencias_valor.append({
                    'documento': doc,
                    'extrato': valor_extrato,
                    'contabil': valor_contabil,
                    'diferenca': abs(valor_extrato_abs - valor_contabil)
                })
                
        if divergencias_valor:
            print(f"⚠️  Encontradas {len(divergencias_valor)} divergências de valores:")
            for div in divergencias_valor:
                print(f"   • {div['documento']}: Extrato R$ {div['extrato']:.2f} vs Contábil R$ {div['contabil']:.2f} (Diff: R$ {div['diferenca']:.2f})")
        else:
            print("✅ Nenhuma divergência de valor encontrada nos documentos comuns")
        
        # Totais
        print(f"\n💰 TOTAIS:")
        print("-" * 20)
        total_extrato = extrato['Valor'].sum()
        total_contabil = contabil['Valor'].sum()
        print(f"   Extrato Bancário: R$ {total_extrato:.2f}")
        print(f"   Lançamentos Contábeis: R$ {total_contabil:.2f}")
        print(f"   Diferença Total: R$ {abs(total_extrato - total_contabil):.2f}")
        
        # Resumo das divergências
        total_divergencias = len(docs_so_extrato) + len(docs_so_contabil) + len(divergencias_valor)
        print(f"\n🎯 RESUMO DAS DIVERGÊNCIAS:")
        print("=" * 40)
        print(f"   📄 Registros só no extrato: {len(docs_so_extrato)}")
        print(f"   📝 Registros só no contábil: {len(docs_so_contabil)}")
        print(f"   💰 Divergências de valores: {len(divergencias_valor)}")
        print(f"   🔢 Total de divergências: {total_divergencias}")
        
        # Porcentagem de conciliação
        total_docs = len(docs_extrato) + len(docs_contabil)
        docs_conciliados = len(docs_comuns) - len(divergencias_valor)
        perc_conciliacao = (docs_conciliados / len(docs_comuns)) * 100 if docs_comuns else 0
        
        print(f"\n📈 INDICADORES:")
        print(f"   Taxa de Conciliação: {perc_conciliacao:.1f}%")
        print(f"   Documentos Conciliados: {docs_conciliados}/{len(docs_comuns)}")
        
    except Exception as e:
        print(f"❌ Erro na análise: {e}")

def instrucoes_teste():
    print(f"\n📋 COMO TESTAR NO SISTEMA:")
    print("=" * 50)
    print("1. Acesse: http://localhost:5000")
    print("2. Vá para a seção de Conciliação")
    print("3. Upload dos arquivos:")
    print("   • Extrato: extrato_multiplas_divergencias.csv")
    print("   • Contábil: contabil_multiplas_divergencias.csv")
    print("4. Execute a conciliação")
    print("5. Analise os resultados das divergências detectadas")
    
    print(f"\n🎯 O QUE O SISTEMA DEVE DETECTAR:")
    print("   • Diferenças de valores em TED004 e BOL008")
    print("   • Registros órfãos (TRF009, COM014, ALU015, SER016)")
    print("   • Relatório detalhado das inconsistências")

if __name__ == "__main__":
    print("🚀 ANÁLISE DE MÚLTIPLAS DIVERGÊNCIAS - TESTE AVANÇADO")
    print("=" * 70)
    
    analisar_multiplas_divergencias()
    instrucoes_teste()
    
    print(f"\n✅ Análise concluída!")
    print(f"📅 {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print("🔬 Pronto para teste avançado de detecção de divergências!")