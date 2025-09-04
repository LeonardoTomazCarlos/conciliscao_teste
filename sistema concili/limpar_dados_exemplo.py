#!/usr/bin/env python3
"""
Script para limpar todos os dados e arquivos de exemplo do sistema de conciliação
"""

import os
import sqlite3
import shutil
from datetime import datetime

def backup_database():
    """Criar backup antes de limpar"""
    db_path = 'instance/conciliacao.db'
    if os.path.exists(db_path):
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_path = f'instance/conciliacao.db.bak_clean_{timestamp}'
        shutil.copy2(db_path, backup_path)
        print(f"✓ Backup criado: {backup_path}")
        return backup_path
    return None

def clean_database():
    """Limpar todas as tabelas do banco de dados, mantendo apenas estrutura"""
    db_path = 'instance/conciliacao.db'
    
    if not os.path.exists(db_path):
        print("❌ Banco de dados não encontrado")
        return
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Desabilitar foreign keys temporariamente
        cursor.execute("PRAGMA foreign_keys = OFF")
        
        # Lista de tabelas para limpar (manter estrutura, remover dados)
        tables_to_clean = [
            'conciliacao',
            'extrato_bancario', 
            'lancamento_contabil',
            'divergencia',
            'log_auditoria',
            'regra_conciliacao'
        ]
        
        # Contar registros antes da limpeza
        total_before = 0
        for table in tables_to_clean:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]
            total_before += count
            print(f"📊 {table}: {count} registros")
        
        print(f"\n📈 Total de registros antes da limpeza: {total_before}")
        
        # Limpar cada tabela
        for table in tables_to_clean:
            cursor.execute(f"DELETE FROM {table}")
            print(f"🧹 Tabela {table} limpa")
        
        # Reset auto-increment counters
        cursor.execute("DELETE FROM sqlite_sequence WHERE name IN ('conciliacao', 'extrato_bancario', 'lancamento_contabil', 'divergencia', 'log_auditoria', 'regra_conciliacao')")
        
        # Reabilitar foreign keys
        cursor.execute("PRAGMA foreign_keys = ON")
        
        # Commit changes
        conn.commit()
        
        # Verificar limpeza
        total_after = 0
        for table in tables_to_clean:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]
            total_after += count
        
        print(f"📉 Total de registros após limpeza: {total_after}")
        print("✓ Banco de dados limpo com sucesso!")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Erro ao limpar banco de dados: {e}")

def clean_upload_files():
    """Limpar arquivos de upload de exemplo"""
    upload_dir = 'uploads'
    
    if not os.path.exists(upload_dir):
        print(f"❌ Diretório {upload_dir} não encontrado")
        return
    
    # Arquivos de exemplo para remover
    example_files = [
        'cnab_arquivo1.ret',
        'cnab_arquivo2.ret', 
        'cnb_teste.txt.txt',
        'DataLancamentoDescricaoValorTip.txt',
        'empresas_exportadas_20250422_2140.csv',
        'extratos_divergentes.csv',
        'extratos_duplicatas.csv',
        'extrato_com_divergencias.csv',
        'extrato_exemplo.csv',
        'extrato_teste_completo.csv',
        'lancamentos_com_divergencias.csv',
        'lancamentos_divergentes.csv',
        'lancamentos_exemplo.csv',
        'lancamentos_teste_completo.csv',
        'teste_extratos.csv',
        'teste_lancamentos.csv'
    ]
    
    # Arquivos pessoais/não-exemplo (manter)
    keep_files = [
        'MARMITASIMPORTANTE.xlsx',
        'Pasta1.xlsx', 
        'Samuel__Carlos_de_Souza_Curriculo.pdf',
        'Texto_do_seu_paragrafo.pdf'
    ]
    
    removed_count = 0
    kept_count = 0
    
    for filename in os.listdir(upload_dir):
        file_path = os.path.join(upload_dir, filename)
        
        if filename in example_files:
            try:
                os.remove(file_path)
                print(f"🗑️  Removido: {filename}")
                removed_count += 1
            except Exception as e:
                print(f"❌ Erro ao remover {filename}: {e}")
        elif filename in keep_files:
            print(f"📁 Mantido: {filename}")
            kept_count += 1
        else:
            print(f"❓ Arquivo não categorizado (mantido): {filename}")
            kept_count += 1
    
    print(f"\n📊 Resumo uploads:")
    print(f"   - Removidos: {removed_count} arquivos de exemplo")
    print(f"   - Mantidos: {kept_count} arquivos")

def clean_old_backups():
    """Limpar backups antigos, manter apenas os 3 mais recentes"""
    instance_dir = 'instance'
    
    if not os.path.exists(instance_dir):
        print(f"❌ Diretório {instance_dir} não encontrado")
        return
    
    # Encontrar todos os arquivos de backup
    backup_files = []
    for filename in os.listdir(instance_dir):
        if filename.startswith('conciliacao.db.bak_') and filename != 'conciliacao.db':
            file_path = os.path.join(instance_dir, filename)
            mtime = os.path.getmtime(file_path)
            backup_files.append((filename, file_path, mtime))
    
    # Ordenar por data de modificação (mais recente primeiro)
    backup_files.sort(key=lambda x: x[2], reverse=True)
    
    print(f"📁 Encontrados {len(backup_files)} arquivos de backup")
    
    # Manter apenas os 3 mais recentes
    keep_count = 3
    removed_count = 0
    
    for i, (filename, file_path, mtime) in enumerate(backup_files):
        if i < keep_count:
            print(f"📁 Mantido: {filename}")
        else:
            try:
                os.remove(file_path)
                print(f"🗑️  Removido backup antigo: {filename}")
                removed_count += 1
            except Exception as e:
                print(f"❌ Erro ao remover {filename}: {e}")
    
    print(f"📊 Backups: mantidos {min(keep_count, len(backup_files))}, removidos {removed_count}")

def main():
    """Função principal para limpeza completa"""
    print("🧹 INICIANDO LIMPEZA DE DADOS E ARQUIVOS DE EXEMPLO")
    print("=" * 60)
    
    # Confirmar antes de prosseguir
    print("\n⚠️  ATENÇÃO: Esta operação irá:")
    print("   - Limpar TODOS os dados das tabelas do banco")
    print("   - Remover arquivos de exemplo da pasta uploads")
    print("   - Manter apenas 3 backups mais recentes")
    print("   - Criar backup antes da limpeza")
    
    confirm = input("\n❓ Deseja continuar? (s/N): ").strip().lower()
    if confirm not in ['s', 'sim', 'y', 'yes']:
        print("❌ Operação cancelada pelo usuário")
        return
    
    print("\n🚀 Iniciando limpeza...")
    
    # 1. Backup do banco atual
    print("\n📋 PASSO 1: Criando backup...")
    backup_path = backup_database()
    
    # 2. Limpar banco de dados
    print("\n📋 PASSO 2: Limpando banco de dados...")
    clean_database()
    
    # 3. Limpar arquivos de upload
    print("\n📋 PASSO 3: Limpando arquivos de upload...")
    clean_upload_files()
    
    # 4. Limpar backups antigos
    print("\n📋 PASSO 4: Limpando backups antigos...")
    clean_old_backups()
    
    print("\n" + "=" * 60)
    print("✅ LIMPEZA CONCLUÍDA COM SUCESSO!")
    print("\n📌 O que foi feito:")
    print("   ✓ Backup criado antes da limpeza")
    print("   ✓ Todas as tabelas de dados foram limpas")
    print("   ✓ Arquivos de exemplo foram removidos")
    print("   ✓ Backups antigos foram organizados")
    print("\n🎯 Sistema limpo e pronto para uso em produção!")

if __name__ == "__main__":
    main()
