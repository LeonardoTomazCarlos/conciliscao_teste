#!/usr/bin/env python3
"""
Script para analisar múltiplas divergências nos novos arquivos de teste
"""
import pandas as pd
import os
from datetime import datetime

def analisar_divergencias_multiplas():
    """Analisar divergências nos arquivos principais"""
    
    print("🔍 ANÁLISE DE MÚLTIPLAS DIVERGÊNCIAS")
    print("=" * 60)
    
    # Arquivos principais
    extrato_file = "sistema concili/extrato_bancario_multiplas_divergencias.csv"
    lancamentos_file = "sistema concili/lancamentos_contabeis_multiplas_divergencias.csv"
    
    try:
        # Ler arquivos
        df_extrato = pd.read_csv(extrato_file)
        df_lancamentos = pd.read_csv(lancamentos_file)
        
        print(f"📊 Extrato bancário: {len(df_extrato)} registros")
        print(f"📋 Lançamentos contábeis: {len(df_lancamentos)} registros")
        
        print("\n" + "=" * 60)
        print("🔍 DIVERGÊNCIAS DETECTADAS:")
        print("=" * 60)
        
        # 1. Órfãos no extrato
        orfaos_extrato = []
        for _, row in df_extrato.iterrows():
            if "ÓRFÃO EXTRATO" in row['Descrição']:
                orfaos_extrato.append(row)
        
        print(f"\n1️⃣ ÓRFÃOS NO EXTRATO ({len(orfaos_extrato)} casos):")
        for orfao in orfaos_extrato:
            print(f"   🔴 {orfao['Data']} - {orfao['Descrição']} - R$ {orfao['Valor']}")
        
        # 2. Órfãos nos lançamentos
        orfaos_lancamentos = []
        for _, row in df_lancamentos.iterrows():
            if "ÓRFÃO CONTÁBIL" in row['Descrição']:
                orfaos_lancamentos.append(row)
        
        print(f"\n2️⃣ ÓRFÃOS NOS LANÇAMENTOS ({len(orfaos_lancamentos)} casos):")
        for orfao in orfaos_lancamentos:
            print(f"   🔴 {orfao['Data']} - {orfao['Descrição']} - R$ {orfao['Valor']}")
        
        # 3. Divergências de valor
        divergencias_valor = []
        for _, row_ext in df_extrato.iterrows():
            if "VALOR DIVERGENTE" in row_ext['Descrição'] or "VALOR DIFERENTE" in row_ext['Descrição']:
                # Procurar correspondente nos lançamentos
                for _, row_lanc in df_lancamentos.iterrows():
                    if ("VALOR DIFERENTE" in row_lanc['Descrição'] and 
                        row_ext['Data'] == row_lanc['Data']):
                        diferenca = abs(float(row_ext['Valor']) - float(row_lanc['Valor']))
                        divergencias_valor.append({
                            'data': row_ext['Data'],
                            'extrato_desc': row_ext['Descrição'],
                            'lancamento_desc': row_lanc['Descrição'],
                            'extrato_valor': row_ext['Valor'],
                            'lancamento_valor': row_lanc['Valor'],
                            'diferenca': diferenca
                        })
        
        print(f"\n3️⃣ DIVERGÊNCIAS DE VALOR ({len(divergencias_valor)} casos):")
        for div in divergencias_valor:
            print(f"   🔴 {div['data']} - Extrato: R$ {div['extrato_valor']} vs Lançamento: R$ {div['lancamento_valor']} (Diff: R$ {div['diferenca']:.2f})")
        
        # 4. Divergências de data
        divergencias_data = []
        for _, row_ext in df_extrato.iterrows():
            if "DATA DIVERGENTE" in row_ext['Descrição']:
                for _, row_lanc in df_lancamentos.iterrows():
                    if ("DATA DIFERENTE" in row_lanc['Descrição'] and 
                        row_ext['Data'] != row_lanc['Data'] and
                        row_ext['Valor'] == row_lanc['Valor']):
                        divergencias_data.append({
                            'extrato_data': row_ext['Data'],
                            'lancamento_data': row_lanc['Data'],
                            'valor': row_ext['Valor'],
                            'descricao': row_ext['Descrição']
                        })
        
        print(f"\n4️⃣ DIVERGÊNCIAS DE DATA ({len(divergencias_data)} casos):")
        for div in divergencias_data:
            print(f"   🔴 Valor: R$ {div['valor']} - Extrato: {div['extrato_data']} vs Lançamento: {div['lancamento_data']}")
        
        # 5. Duplicatas no extrato
        duplicatas_extrato = df_extrato[df_extrato.duplicated(['Data', 'Valor'], keep=False)]
        duplicatas_manuais = []
        for _, row in df_extrato.iterrows():
            if "DUPLICATA" in row['Descrição']:
                duplicatas_manuais.append(row)
        
        print(f"\n5️⃣ DUPLICATAS NO EXTRATO ({len(duplicatas_manuais)} casos):")
        for dup in duplicatas_manuais:
            print(f"   🔴 {dup['Data']} - {dup['Descrição']} - R$ {dup['Valor']}")
        
        # Resumo final
        total_divergencias = (len(orfaos_extrato) + len(orfaos_lancamentos) + 
                            len(divergencias_valor) + len(divergencias_data) + 
                            len(duplicatas_manuais))
        
        print("\n" + "=" * 60)
        print("📊 RESUMO GERAL:")
        print(f"   • Órfãos no extrato: {len(orfaos_extrato)}")
        print(f"   • Órfãos nos lançamentos: {len(orfaos_lancamentos)}")
        print(f"   • Divergências de valor: {len(divergencias_valor)}")
        print(f"   • Divergências de data: {len(divergencias_data)}")
        print(f"   • Duplicatas: {len(duplicatas_manuais)}")
        print(f"   🎯 TOTAL DE DIVERGÊNCIAS: {total_divergencias}")
        
        return total_divergencias
        
    except Exception as e:
        print(f"❌ Erro ao analisar arquivos: {e}")
        return 0

def analisar_casos_especiais():
    """Analisar casos especiais"""
    
    print("\n" + "=" * 60)
    print("🔍 ANÁLISE DE CASOS ESPECIAIS")
    print("=" * 60)
    
    # Arquivos especiais
    extrato_especial = "sistema concili/extrato_bancario_casos_especiais.csv"
    lancamentos_especial = "sistema concili/lancamentos_contabeis_casos_especiais.csv"
    
    try:
        df_extrato_esp = pd.read_csv(extrato_especial)
        df_lancamentos_esp = pd.read_csv(lancamentos_especial)
        
        print(f"📊 Extrato especial: {len(df_extrato_esp)} registros")
        print(f"📋 Lançamentos especiais: {len(df_lancamentos_esp)} registros")
        
        # Casos de centavos diferentes
        casos_centavos = 0
        for _, row_ext in df_extrato_esp.iterrows():
            valor_ext = float(row_ext['Valor'])
            for _, row_lanc in df_lancamentos_esp.iterrows():
                valor_lanc = float(row_lanc['Valor'])
                diferenca = abs(valor_ext - valor_lanc)
                if 0 < diferenca <= 1.0 and row_ext['Data'] == row_lanc['Data']:
                    casos_centavos += 1
                    print(f"   💰 DIFERENÇA DE CENTAVOS: {row_ext['Data']} - R$ {valor_ext:.2f} vs R$ {valor_lanc:.2f}")
        
        # Casos de órfãos especiais
        orfaos_especiais = len(df_lancamentos_esp) - len([row for _, row in df_extrato_esp.iterrows() 
                                                         if any(row['Valor'] == lanc['Valor'] and row['Data'] == lanc['Data'] 
                                                               for _, lanc in df_lancamentos_esp.iterrows())])
        
        print(f"\n📊 CASOS ESPECIAIS DETECTADOS:")
        print(f"   • Diferenças de centavos: {casos_centavos}")
        print(f"   • Órfãos especiais: {orfaos_especiais}")
        
        return casos_centavos + orfaos_especiais
        
    except Exception as e:
        print(f"❌ Erro ao analisar casos especiais: {e}")
        return 0

def gerar_relatorio_completo():
    """Gerar relatório completo de todos os arquivos"""
    
    print("\n" + "=" * 60)
    print("📋 RELATÓRIO COMPLETO DOS ARQUIVOS CRIADOS")
    print("=" * 60)
    
    arquivos_criados = [
        "sistema concili/extrato_bancario_multiplas_divergencias.csv",
        "sistema concili/lancamentos_contabeis_multiplas_divergencias.csv",
        "sistema concili/extrato_bancario_casos_especiais.csv",
        "sistema concili/lancamentos_contabeis_casos_especiais.csv"
    ]
    
    print("📁 ARQUIVOS CRIADOS:")
    total_registros = 0
    
    for arquivo in arquivos_criados:
        if os.path.exists(arquivo):
            try:
                df = pd.read_csv(arquivo)
                tamanho = os.path.getsize(arquivo)
                total_registros += len(df)
                print(f"   ✅ {os.path.basename(arquivo)}")
                print(f"      📊 {len(df)} registros | {tamanho} bytes")
            except:
                print(f"   ❌ {os.path.basename(arquivo)} (erro ao ler)")
        else:
            print(f"   ❌ {os.path.basename(arquivo)} (não encontrado)")
    
    print(f"\n📊 ESTATÍSTICAS GERAIS:")
    print(f"   • Total de arquivos: {len(arquivos_criados)}")
    print(f"   • Total de registros: {total_registros}")
    
    return len(arquivos_criados)

if __name__ == '__main__':
    try:
        print("🚀 INICIANDO ANÁLISE COMPLETA DE DIVERGÊNCIAS...")
        
        # Analisar arquivos principais
        divergencias_principais = analisar_divergencias_multiplas()
        
        # Analisar casos especiais
        casos_especiais = analisar_casos_especiais()
        
        # Gerar relatório
        arquivos_criados = gerar_relatorio_completo()
        
        total_geral = divergencias_principais + casos_especiais
        
        print(f"\n🎉 ANÁLISE CONCLUÍDA!")
        print(f"   📊 {divergencias_principais} divergências principais")
        print(f"   🔍 {casos_especiais} casos especiais")
        print(f"   🎯 {total_geral} divergências totais detectadas")
        print(f"   📁 {arquivos_criados} arquivos criados")
        
        print(f"\n📋 PRÓXIMOS PASSOS:")
        print(f"   1. Acesse http://localhost:5000")
        print(f"   2. Faça upload dos arquivos na aba 'Upload de Dados'")
        print(f"   3. Execute a conciliação")
        print(f"   4. Verifique as {total_geral} divergências detectadas")
        
    except Exception as e:
        print(f"❌ Erro geral: {e}")
        import traceback
        traceback.print_exc()