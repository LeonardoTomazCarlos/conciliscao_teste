#!/usr/bin/env python3
"""
Script para testar a detecção completa de divergências
"""

import os
import sys
import sqlite3
from datetime import datetime

# Adicionar o diretório do app ao path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def testar_divergencias():
    """Testa a detecção de divergências"""
    
    print("🔍 TESTE DE DETECÇÃO DE DIVERGÊNCIAS")
    print("="*50)
    
    # Conectar ao banco
    db_path = os.path.join('instance', 'conciliacao.db')
    if not os.path.exists(db_path):
        print("❌ Banco de dados não encontrado!")
        return
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # 1. Verificar dados no banco
        print("\n📊 DADOS NO BANCO:")
        
        cursor.execute("SELECT COUNT(*) FROM extrato_bancario")
        extratos_count = cursor.fetchone()[0]
        print(f"   Extratos bancários: {extratos_count}")
        
        cursor.execute("SELECT COUNT(*) FROM lancamento_contabil")
        lancamentos_count = cursor.fetchone()[0]
        print(f"   Lançamentos contábeis: {lancamentos_count}")
        
        cursor.execute("SELECT COUNT(*) FROM conciliacao")
        conciliacoes_count = cursor.fetchone()[0]
        print(f"   Conciliações: {conciliacoes_count}")
        
        cursor.execute("SELECT COUNT(*) FROM divergencia")
        divergencias_count = cursor.fetchone()[0]
        print(f"   Divergências: {divergencias_count}")
        
        # 2. Listar divergências existentes
        if divergencias_count > 0:
            print("\n🚨 DIVERGÊNCIAS DETECTADAS:")
            cursor.execute("""
                SELECT id, tipo, descricao, status, created_at
                FROM divergencia 
                ORDER BY created_at DESC
            """)
            
            divergencias = cursor.fetchall()
            for div in divergencias:
                id_div, tipo, descricao, status, created_at = div
                print(f"   ID {id_div}: [{tipo}] {descricao}")
                print(f"      Status: {status} | Criado: {created_at}")
                print()
        else:
            print("\n⚠️  Nenhuma divergência detectada!")
        
        # 3. Analisar possíveis divergências manualmente
        print("\n🔍 ANÁLISE MANUAL:")
        
        # Extratos sem conciliação
        cursor.execute("""
            SELECT e.id, e.data, e.descricao, e.valor, e.tipo
            FROM extrato_bancario e
            LEFT JOIN conciliacao c ON e.id = c.extrato_id
            WHERE c.id IS NULL
            ORDER BY e.data DESC
            LIMIT 10
        """)
        
        extratos_orfaos = cursor.fetchall()
        if extratos_orfaos:
            print(f"   Extratos órfãos encontrados: {len(extratos_orfaos)}")
            for extrato in extratos_orfaos[:5]:
                id_e, data, desc, valor, tipo = extrato
                print(f"      ID {id_e}: {data} | {desc} | R$ {valor} | {tipo}")
        
        # Lançamentos sem conciliação  
        cursor.execute("""
            SELECT l.id, l.data, l.descricao, l.valor, l.tipo
            FROM lancamento_contabil l
            LEFT JOIN conciliacao c ON l.id = c.lancamento_id
            WHERE c.id IS NULL
            ORDER BY l.data DESC
            LIMIT 10
        """)
        
        lancamentos_orfaos = cursor.fetchall()
        if lancamentos_orfaos:
            print(f"   Lançamentos órfãos encontrados: {len(lancamentos_orfaos)}")
            for lancamento in lancamentos_orfaos[:5]:
                id_l, data, desc, valor, tipo = lancamento
                print(f"      ID {id_l}: {data} | {desc} | R$ {valor} | {tipo}")
        
        # Verificar diferenças de valor
        cursor.execute("""
            SELECT c.id, e.valor as valor_extrato, l.valor as valor_lancamento,
                   ABS(e.valor - l.valor) as diferenca,
                   e.descricao, e.data
            FROM conciliacao c
            JOIN extrato_bancario e ON c.extrato_id = e.id
            JOIN lancamento_contabil l ON c.lancamento_id = l.id
            WHERE ABS(e.valor - l.valor) > 0.01
            ORDER BY diferenca DESC
            LIMIT 10
        """)
        
        diferencas_valor = cursor.fetchall()
        if diferencas_valor:
            print(f"   Diferenças de valor encontradas: {len(diferencas_valor)}")
            for diff in diferencas_valor:
                id_c, val_e, val_l, diferenca, desc, data = diff
                print(f"      Conciliação {id_c}: {data} | {desc}")
                print(f"         Extrato: R$ {val_e} | Lançamento: R$ {val_l} | Diff: R$ {diferenca}")
        
        # 4. Verificar duplicatas
        cursor.execute("""
            SELECT descricao, valor, data, COUNT(*) as total
            FROM extrato_bancario
            GROUP BY descricao, valor, data
            HAVING COUNT(*) > 1
            ORDER BY total DESC
        """)
        
        duplicatas_extrato = cursor.fetchall()
        if duplicatas_extrato:
            print(f"   Duplicatas no extrato: {len(duplicatas_extrato)}")
            for dup in duplicatas_extrato:
                desc, valor, data, total = dup
                print(f"      {total}x: {data} | {desc} | R$ {valor}")
        
        # 5. Estatísticas finais
        print("\n📈 ESTATÍSTICAS:")
        total_registros = extratos_count + lancamentos_count
        conciliacao_rate = (conciliacoes_count / max(extratos_count, lancamentos_count) * 100) if max(extratos_count, lancamentos_count) > 0 else 0
        divergencia_rate = (divergencias_count / total_registros * 100) if total_registros > 0 else 0
        
        print(f"   Total de registros: {total_registros}")
        print(f"   Taxa de conciliação: {conciliacao_rate:.1f}%")
        print(f"   Taxa de divergências: {divergencia_rate:.1f}%")
        print(f"   Extratos órfãos: {len(extratos_orfaos)}")
        print(f"   Lançamentos órfãos: {len(lancamentos_orfaos)}")
        print(f"   Diferenças de valor: {len(diferencas_valor)}")
        print(f"   Duplicatas no extrato: {len(duplicatas_extrato)}")
        
        # 6. Recomendações
        print("\n💡 RECOMENDAÇÕES:")
        if divergencias_count == 0 and (len(extratos_orfaos) > 0 or len(lancamentos_orfaos) > 0 or len(diferencas_valor) > 0):
            print("   ⚠️  Divergências detectadas manualmente mas não cadastradas no sistema!")
            print("   📝 Execute a função verificar_divergencias() para detectar automaticamente")
        elif divergencias_count > 0:
            print("   ✅ Sistema detectou divergências corretamente")
            print("   🔄 Use os filtros da aba divergências para analisar")
        else:
            print("   ✅ Nenhuma divergência detectada - dados consistentes!")
        
    except Exception as e:
        print(f"❌ Erro na análise: {e}")
        
    finally:
        conn.close()

def executar_verificacao_divergencias():
    """Executa a verificação de divergências via API"""
    print("\n🔄 EXECUTANDO VERIFICAÇÃO DE DIVERGÊNCIAS...")
    
    try:
        from app import app, verificar_divergencias
        
        with app.app_context():
            verificar_divergencias()
            print("✅ Verificação de divergências executada com sucesso!")
            
    except Exception as e:
        print(f"❌ Erro ao executar verificação: {e}")

if __name__ == "__main__":
    testar_divergencias()
    
    # Perguntar se quer executar verificação
    resposta = input("\n🤔 Executar verificação de divergências? (s/n): ").lower().strip()
    if resposta in ['s', 'sim', 'y', 'yes']:
        executar_verificacao_divergencias()
        print("\n🔄 Executando nova análise após verificação...")
        testar_divergencias()