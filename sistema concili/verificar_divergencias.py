#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script simples para verificar as divergências criadas
"""

import pandas as pd

def verificar_arquivos():
    print("🔍 VERIFICAÇÃO DOS ARQUIVOS DE TESTE")
    print("="*50)
    
    try:
        # Ler arquivos
        extrato = pd.read_csv('extrato_multiplas_divergencias.csv')
        contabil = pd.read_csv('contabil_multiplas_divergencias.csv')
        
        print(f"✅ Extrato: {len(extrato)} registros")
        print(f"✅ Contábil: {len(contabil)} registros")
        
        # Mostrar primeiras linhas
        print(f"\n📊 EXTRATO BANCÁRIO (primeiros 5):")
        for i in range(min(5, len(extrato))):
            row = extrato.iloc[i]
            print(f"   {row['Numero_Documento']}: R$ {row['Valor']:.2f} ({row['Tipo']}) - {row['Descrição']}")
            
        print(f"\n📋 LANÇAMENTOS CONTÁBEIS (primeiros 5):")
        for i in range(min(5, len(contabil))):
            row = contabil.iloc[i]
            print(f"   {row['Numero_Documento']}: R$ {row['Valor']:.2f} ({row['Tipo']}) - {row['Descrição']}")
        
        # Totais
        total_extrato = extrato['Valor'].sum()
        total_contabil = contabil['Valor'].sum()
        
        print(f"\n💰 TOTAIS:")
        print(f"   Extrato: R$ {total_extrato:.2f}")
        print(f"   Contábil: R$ {total_contabil:.2f}")
        print(f"   Diferença: R$ {abs(total_extrato - total_contabil):.2f}")
        
        print(f"\n🎯 DIVERGÊNCIAS PLANEJADAS:")
        print("   1. TED004: Valores diferentes (R$ 2.200 vs R$ 2.500)")
        print("   2. BOL008: Valores diferentes (R$ 180 vs R$ 160)")  
        print("   3. TRF009: Só no extrato (R$ 1.100)")
        print("   4. COM014: Só no contábil (R$ 420)")
        print("   5. ALU015: Só no contábil (R$ 1.200)")
        print("   6. SER016: Só no contábil (R$ 500)")
        
        print(f"\n✅ Arquivos prontos para teste!")
        print("📋 Use no sistema: extrato_multiplas_divergencias.csv + contabil_multiplas_divergencias.csv")
        
    except Exception as e:
        print(f"❌ Erro: {e}")

if __name__ == "__main__":
    verificar_arquivos()