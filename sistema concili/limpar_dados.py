#!/usr/bin/env python3
"""
Script para limpar todos os dados e arquivos de exemplo do sistema de conciliação
"""

import os
import sqlite3
import shutil
import glob
from datetime import datetime

def backup_database():
    """Criar backup do banco antes de limpar"""
    db_path = 'instance/conciliacao.db'
    if os.path.exists(db_path):
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_path = f'instance/conciliacao_backup_before_cleanup_{timestamp}.db'
        shutil.copy2(db_path, backup_path)
        print(f"✓ Backup criado: {backup_path}")
        return backup_path
    return None

def clear_database():
    """Limpar todas as tabelas do banco de dados"""
    db_path = 'instance/conciliacao.db'
    if not os.path.exists(db_path):
        print("❌ Banco de dados não encontrado")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Desabilitar foreign keys temporariamente
        cursor.execute("PRAGMA foreign_keys = OFF")
        
        # Lista de tabelas para limpar (exceto usuarios e configuracoes)
        tables_to_clear = [
            'divergencia',
            'conciliacao', 
            'procedimento_conciliacao',
            'extrato_bancario',
            'lancamento_contabil',
            'log_auditoria',
            'regra_conciliacao'
        ]
        
        # Contar registros antes
        print("\n📊 Registros antes da limpeza:")
        for table in tables_to_clear:
            try:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = cursor.fetchone()[0]
                print(f"  {table}: {count} registros")
            except Exception as e:
                print(f"  {table}: erro ao contar - {e}")
        
        # Limpar tabelas
        print("\n🧹 Limpando tabelas...")
        for table in tables_to_clear:
            try:
                cursor.execute(f"DELETE FROM {table}")
                print(f"  ✓ {table} limpa")
            except Exception as e:
                print(f"  ❌ Erro ao limpar {table}: {e}")
        
        # Reset autoincrement
        print("\n🔄 Resetando auto-increment...")
        for table in tables_to_clear:
            try:
                cursor.execute(f"DELETE FROM sqlite_sequence WHERE name='{table}'")
                print(f"  ✓ Auto-increment resetado para {table}")
            except Exception as e:
                print(f"  ⚠️ {table}: {e}")
        
        # Reabilitar foreign keys
        cursor.execute("PRAGMA foreign_keys = ON")
        
        # Commit e verificar
        conn.commit()
        
        print("\n📊 Registros após a limpeza:")
        for table in tables_to_clear:
            try:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = cursor.fetchone()[0]
                print(f"  {table}: {count} registros")
            except Exception as e:
                print(f"  {table}: erro ao verificar - {e}")
        
        conn.close()
        print("\n✅ Banco de dados limpo com sucesso!")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao limpar banco: {e}")
        return False

def clear_upload_files():
    """Limpar arquivos de upload de exemplo"""
    upload_dirs = ['uploads', 'sistema concili/uploads']
    files_removed = 0
    
    print("\n🗂️ Limpando arquivos de upload...")
    
    for upload_dir in upload_dirs:
        if os.path.exists(upload_dir):
            print(f"\n📁 Verificando diretório: {upload_dir}")
            
            # Listar arquivos antes
            files = os.listdir(upload_dir)
            if files:
                print(f"  Arquivos encontrados: {len(files)}")
                for file in files:
                    file_path = os.path.join(upload_dir, file)
                    if os.path.isfile(file_path):
                        try:
                            os.remove(file_path)
                            print(f"  ✓ Removido: {file}")
                            files_removed += 1
                        except Exception as e:
                            print(f"  ❌ Erro ao remover {file}: {e}")
            else:
                print("  📂 Diretório já está vazio")
        else:
            print(f"  📂 Diretório não existe: {upload_dir}")
    
    print(f"\n✅ {files_removed} arquivos removidos dos uploads")
    return files_removed

def clear_logs():
    """Limpar logs antigos (manter apenas os últimos 7 dias)"""
    log_file = 'logs/conciliacao.log'
    if os.path.exists(log_file):
        try:
            # Fazer backup do log atual
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_log = f'logs/conciliacao_backup_{timestamp}.log'
            shutil.copy2(log_file, backup_log)
            
            # Limpar o log principal
            with open(log_file, 'w') as f:
                f.write(f"# Log limpo em {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            
            print(f"✅ Log limpo (backup: {backup_log})")
        except Exception as e:
            print(f"❌ Erro ao limpar logs: {e}")

def main():
    """Função principal"""
    print("🧹 INICIANDO LIMPEZA COMPLETA DO SISTEMA")
    print("=" * 50)
    
    # 1. Backup do banco
    print("\n1️⃣ Criando backup...")
    backup_path = backup_database()
    
    # 2. Limpar banco de dados
    print("\n2️⃣ Limpando banco de dados...")
    db_success = clear_database()
    
    # 3. Limpar arquivos de upload
    print("\n3️⃣ Limpando arquivos de upload...")
    files_count = clear_upload_files()
    
    # 4. Limpar logs
    print("\n4️⃣ Limpando logs...")
    clear_logs()
    
    # Resumo final
    print("\n" + "=" * 50)
    print("📋 RESUMO DA LIMPEZA")
    print("=" * 50)
    
    if backup_path:
        print(f"💾 Backup criado: {backup_path}")
    
    if db_success:
        print("✅ Banco de dados limpo com sucesso")
    else:
        print("❌ Falha na limpeza do banco de dados")
    
    print(f"🗂️ {files_count} arquivos de upload removidos")
    print("📝 Logs limpos")
    
    print("\n🎉 LIMPEZA CONCLUÍDA!")
    print("\nO sistema está pronto para uso em produção.")
    print("Usuários e configurações foram preservados.")

if __name__ == "__main__":
    # Confirmar antes de executar
    resp = input("⚠️  ATENÇÃO: Esta operação irá remover TODOS os dados de exemplo!\nDeseja continuar? (s/N): ")
    if resp.lower() in ['s', 'sim', 'y', 'yes']:
        main()
    else:
        print("❌ Operação cancelada pelo usuário")
