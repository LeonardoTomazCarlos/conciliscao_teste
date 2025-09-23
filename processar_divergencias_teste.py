#!/usr/bin/env python3
"""
Script para importar e processar divergências de teste
Criado em: Setembro 2025
"""
import sys
import os
import pandas as pd
from datetime import datetime

# Adicionar o diretório do sistema ao path
sys.path.append(os.path.join(os.path.dirname(__file__), 'sistema concili'))

def importar_divergencias_teste():
    """Importar e processar os arquivos de teste com divergências"""
    
    print("🔧 IMPORTANDO ARQUIVOS DE TESTE COM DIVERGÊNCIAS")
    print("=" * 60)
    
    # Caminhos dos arquivos
    extrato_file = "sistema concili/extrato_bancario_teste_divergencias.csv"
    lancamentos_file = "sistema concili/lancamentos_contabeis_teste_divergencias.csv"
    
    try:
        # Ler extrato bancário
        print("📊 Lendo extrato bancário...")
        df_extrato = pd.read_csv(extrato_file)
        print(f"✅ Extrato carregado: {len(df_extrato)} registros")
        
        # Ler lançamentos contábeis
        print("📋 Lendo lançamentos contábeis...")
        df_lancamentos = pd.read_csv(lancamentos_file)
        print(f"✅ Lançamentos carregados: {len(df_lancamentos)} registros")
        
        print("\n" + "=" * 60)
        print("🔍 ANÁLISE DE DIVERGÊNCIAS DETECTADAS:")
        print("=" * 60)
        
        # Análise 1: Registros órfãos no extrato
        print("\n1️⃣ ÓRFÃOS NO EXTRATO (sem correspondência contábil):")
        extrato_orfaos = []
        for _, row in df_extrato.iterrows():
            # Procurar correspondência por descrição e valor
            match = df_lancamentos[
                (df_lancamentos['Valor'] == row['Valor']) & 
                (df_lancamentos['Data'] == row['Data'])
            ]
            if match.empty:
                extrato_orfaos.append(row)
                print(f"   🔴 {row['Data']} - {row['Descrição']} - R$ {row['Valor']}")
        
        # Análise 2: Registros órfãos nos lançamentos
        print(f"\n2️⃣ ÓRFÃOS NOS LANÇAMENTOS (sem correspondência no extrato):")
        lancamentos_orfaos = []
        for _, row in df_lancamentos.iterrows():
            # Procurar correspondência por descrição e valor
            match = df_extrato[
                (df_extrato['Valor'] == row['Valor']) & 
                (df_extrato['Data'] == row['Data'])
            ]
            if match.empty:
                lancamentos_orfaos.append(row)
                print(f"   🔴 {row['Data']} - {row['Descrição']} - R$ {row['Valor']}")
        
        # Análise 3: Divergências de valor
        print(f"\n3️⃣ DIVERGÊNCIAS DE VALOR:")
        divergencias_valor = []
        for _, row_ext in df_extrato.iterrows():
            for _, row_lanc in df_lancamentos.iterrows():
                if (row_ext['Data'] == row_lanc['Data'] and 
                    'DIVERGÊNCIA' in row_ext['Descrição'] and 
                    'VALOR DIFERENTE' in row_lanc['Descrição']):
                    diferenca = abs(float(row_ext['Valor']) - float(row_lanc['Valor']))
                    divergencias_valor.append({
                        'data': row_ext['Data'],
                        'extrato_valor': row_ext['Valor'],
                        'lancamento_valor': row_lanc['Valor'],
                        'diferenca': diferenca
                    })
                    print(f"   🔴 {row_ext['Data']} - Extrato: R$ {row_ext['Valor']} vs Lançamento: R$ {row_lanc['Valor']} (Diff: R$ {diferenca})")
        
        # Análise 4: Duplicatas
        print(f"\n4️⃣ DUPLICATAS DETECTADAS:")
        
        # Duplicatas no extrato
        duplicatas_extrato = df_extrato[df_extrato.duplicated(['Data', 'Valor'], keep=False)]
        if not duplicatas_extrato.empty:
            print("   📍 No Extrato:")
            for _, row in duplicatas_extrato.iterrows():
                print(f"   🔴 {row['Data']} - {row['Descrição']} - R$ {row['Valor']}")
        
        # Duplicatas nos lançamentos (se houver)
        duplicatas_lancamentos = df_lancamentos[df_lancamentos.duplicated(['Data', 'Valor'], keep=False)]
        if not duplicatas_lancamentos.empty:
            print("   📍 Nos Lançamentos:")
            for _, row in duplicatas_lancamentos.iterrows():
                print(f"   🔴 {row['Data']} - {row['Descrição']} - R$ {row['Valor']}")
        
        # Resumo final
        print("\n" + "=" * 60)
        print("📊 RESUMO DAS DIVERGÊNCIAS:")
        print(f"   • Órfãos no extrato: {len(extrato_orfaos)}")
        print(f"   • Órfãos nos lançamentos: {len(lancamentos_orfaos)}")
        print(f"   • Divergências de valor: {len(divergencias_valor)}")
        print(f"   • Duplicatas no extrato: {len(duplicatas_extrato)}")
        print(f"   • Duplicatas nos lançamentos: {len(duplicatas_lancamentos)}")
        
        total_divergencias = len(extrato_orfaos) + len(lancamentos_orfaos) + len(divergencias_valor) + len(duplicatas_extrato) + len(duplicatas_lancamentos)
        print(f"   🎯 TOTAL DE DIVERGÊNCIAS: {total_divergencias}")
        
        print("\n✅ Análise concluída! Agora você pode:")
        print("   1. Fazer upload destes arquivos no sistema")
        print("   2. Executar a conciliação")
        print("   3. Verificar se as divergências são detectadas corretamente")
        
        return {
            'extrato_orfaos': len(extrato_orfaos),
            'lancamentos_orfaos': len(lancamentos_orfaos),
            'divergencias_valor': len(divergencias_valor),
            'duplicatas_extrato': len(duplicatas_extrato),
            'duplicatas_lancamentos': len(duplicatas_lancamentos),
            'total': total_divergencias
        }
        
    except Exception as e:
        print(f"❌ Erro ao processar arquivos: {e}")
        import traceback
        traceback.print_exc()
        return None

def criar_arquivo_divergencias_complexas():
    """Criar arquivo adicional com divergências mais complexas"""
    print("\n🔧 CRIANDO ARQUIVO DE DIVERGÊNCIAS COMPLEXAS...")
    
    # Extrato com casos específicos
    extrato_complexo = [
        ["2025-09-27", "Transferência PIX - Valor aproximado", "1000.01", "credito"],
        ["2025-09-27", "Pagamento fornecedor - Data incorreta", "500.00", "debito"],
        ["2025-09-28", "Venda com desconto aplicado", "950.00", "credito"],
        ["2025-09-28", "Estorno parcial de compra", "75.50", "credito"],
        ["2025-09-29", "Taxa bancária não prevista", "15.00", "debito"],
        ["2025-09-29", "Juros sobre aplicação", "25.75", "credito"],
        ["2025-09-30", "Transferência internacional", "2500.00", "debito"],
    ]
    
    # Lançamentos com divergências correspondentes
    lancamentos_complexo = [
        ["2025-09-27", "Recebimento PIX - Valor arredondado", "1000.00", "credito", "Receitas", "Cliente PIX", "Vendas"],
        ["2025-09-26", "Pagamento fornecedor - Data correta", "500.00", "debito", "Fornecedores", "Fornecedor ABC", "Operacional"],
        ["2025-09-28", "Venda sem desconto", "1000.00", "credito", "Receitas", "Cliente Desconto", "Vendas"],
        ["2025-09-28", "Estorno total de compra", "100.00", "credito", "Estornos", "Cliente Estorno", "Vendas"],
        ["2025-09-29", "Aplicação financeira", "25.75", "credito", "Receitas Financeiras", "Banco Investimento", "Financeiro"],
        ["2025-09-30", "Pagamento internacional", "2400.00", "debito", "Fornecedores", "Fornecedor Internacional", "Operacional"],
    ]
    
    # Salvar extrato complexo
    with open("sistema concili/extrato_bancario_divergencias_complexas.csv", "w", encoding="utf-8") as f:
        f.write("Data,Descrição,Valor,Tipo\n")
        for linha in extrato_complexo:
            f.write(",".join(linha) + "\n")
    
    # Salvar lançamentos complexos
    with open("sistema concili/lancamentos_contabeis_divergencias_complexas.csv", "w", encoding="utf-8") as f:
        f.write("Data,Descrição,Valor,Tipo,Categoria,Fornecedor/Cliente,Centro de Custo\n")
        for linha in lancamentos_complexo:
            f.write(",".join(linha) + "\n")
    
    print("✅ Arquivos de divergências complexas criados:")
    print("   • extrato_bancario_divergencias_complexas.csv")
    print("   • lancamentos_contabeis_divergencias_complexas.csv")

if __name__ == '__main__':
    try:
        resultado = importar_divergencias_teste()
        criar_arquivo_divergencias_complexas()
        
        if resultado:
            print(f"\n🎉 SUCESSO! {resultado['total']} divergências detectadas nos arquivos de teste.")
            print("\n📋 Próximos passos:")
            print("   1. Acesse o sistema web em http://localhost:5000")
            print("   2. Vá para a aba 'Upload de Dados'")
            print("   3. Faça upload dos arquivos:")
            print("      • extrato_bancario_teste_divergencias.csv")
            print("      • lancamentos_contabeis_teste_divergencias.csv")
            print("   4. Execute a conciliação")
            print("   5. Verifique as divergências na aba 'Divergências'")
        
    except Exception as e:
        print(f"❌ Erro geral: {e}")
        import traceback
        traceback.print_exc()