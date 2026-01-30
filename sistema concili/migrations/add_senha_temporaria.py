#!/usr/bin/env python3
"""
Migração: Adicionar coluna senha_temporaria na tabela usuario
Data: 2025-10-30
"""

import sqlite3
import os
from datetime import datetime

def run_migration():
    """Executar migração para adicionar campo senha_temporaria"""
    
    db_path = 'instance/conciliacao.db'
    if not os.path.exists(db_path):
        print("❌ Banco de dados não encontrado")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Verificar se a coluna já foi adicionada
        cursor.execute("PRAGMA table_info(usuario)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'senha_temporaria' in columns:
            print("⚠️ Migração já foi aplicada - coluna senha_temporaria já existe")
            return True
        
        print("🚀 Iniciando migração para adicionar senha_temporaria...")
        
        # 1. Adicionar coluna senha_temporaria na tabela usuario
        cursor.execute("ALTER TABLE usuario ADD COLUMN senha_temporaria BOOLEAN DEFAULT 0")
        print("✅ Coluna senha_temporaria adicionada à tabela usuario")
        
        # 2. Definir todos os usuários existentes como não tendo senha temporária
        cursor.execute("UPDATE usuario SET senha_temporaria = 0 WHERE senha_temporaria IS NULL")
        print("✅ Usuários existentes marcados com senha_temporaria = 0")
        
        # 3. Commit das mudanças
        conn.commit()
        print("✅ Migração concluída com sucesso!")
        
        # 4. Verificar estrutura final
        cursor.execute("PRAGMA table_info(usuario)")
        columns_after = cursor.fetchall()
        print("📊 Estrutura da tabela usuario após migração:")
        for column in columns_after:
            if column[1] == 'senha_temporaria':
                print(f"   ✅ {column[1]} - {column[2]} (DEFAULT: {column[4]})")
        
        # 5. Verificar quantidade de usuários
        cursor.execute("SELECT COUNT(*) FROM usuario")
        user_count = cursor.fetchone()[0]
        print(f"📊 Total de usuários atualizados: {user_count}")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Erro na migração: {e}")
        if 'conn' in locals():
            conn.rollback()
            conn.close()
        return False

def rollback_migration():
    """Reverter migração (apenas para desenvolvimento)"""
    
    db_path = 'instance/conciliacao.db'
    if not os.path.exists(db_path):
        print("❌ Banco de dados não encontrado")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("🔄 Revertendo migração...")
        
        # SQLite não suporta DROP COLUMN diretamente, precisamos recriar a tabela
        # 1. Criar tabela temporária sem a coluna senha_temporaria
        cursor.execute("""
            CREATE TABLE usuario_temp AS 
            SELECT id, username, email, password_hash, nome_completo, perfil, 
                   ativo, created_at, ultimo_acesso
            FROM usuario
        """)
        print("✅ Tabela temporária criada")
        
        # 2. Remover tabela original
        cursor.execute("DROP TABLE usuario")
        print("✅ Tabela original removida")
        
        # 3. Renomear tabela temporária
        cursor.execute("ALTER TABLE usuario_temp RENAME TO usuario")
        print("✅ Tabela renomeada")
        
        # 4. Recriar índices se necessário
        cursor.execute("CREATE UNIQUE INDEX IF NOT EXISTS ix_usuario_username ON usuario (username)")
        cursor.execute("CREATE UNIQUE INDEX IF NOT EXISTS ix_usuario_email ON usuario (email)")
        print("✅ Índices recriados")
        
        conn.commit()
        conn.close()
        
        print("✅ Migração revertida com sucesso!")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao reverter migração: {e}")
        if 'conn' in locals():
            conn.rollback()
            conn.close()
        return False

def verify_migration():
    """Verificar se a migração foi aplicada corretamente"""
    
    db_path = 'instance/conciliacao.db'
    if not os.path.exists(db_path):
        print("❌ Banco de dados não encontrado")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Verificar estrutura da tabela
        cursor.execute("PRAGMA table_info(usuario)")
        columns = cursor.fetchall()
        
        print("📋 Estrutura atual da tabela usuario:")
        senha_temporaria_found = False
        for column in columns:
            col_name, col_type, not_null, default_value, pk = column[1], column[2], column[3], column[4], column[5]
            marker = "🆕" if col_name == "senha_temporaria" else "  "
            print(f"{marker} {col_name:<20} | {col_type:<10} | NOT NULL: {bool(not_null)} | DEFAULT: {default_value}")
            if col_name == "senha_temporaria":
                senha_temporaria_found = True
        
        if senha_temporaria_found:
            print("✅ Coluna senha_temporaria encontrada!")
            
            # Verificar dados dos usuários
            cursor.execute("SELECT username, senha_temporaria FROM usuario")
            users = cursor.fetchall()
            print(f"\n👥 Status dos usuários ({len(users)} total):")
            for username, senha_temp in users:
                status = "🔑 TEMPORÁRIA" if senha_temp else "✅ NORMAL"
                print(f"   {username:<15} | {status}")
        else:
            print("❌ Coluna senha_temporaria NÃO encontrada!")
        
        conn.close()
        return senha_temporaria_found
        
    except Exception as e:
        print(f"❌ Erro na verificação: {e}")
        return False

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == '--rollback':
        print("⚠️ ATENÇÃO: Revertendo migração!")
        resp = input("Tem certeza? (s/N): ")
        if resp.lower() in ['s', 'sim']:
            rollback_migration()
    elif len(sys.argv) > 1 and sys.argv[1] == '--verify':
        print("🔍 Verificando migração...")
        verify_migration()
    else:
        print("🔄 Aplicando migração para adicionar senha_temporaria...")
        if run_migration():
            print("\n🎉 Migração aplicada com sucesso!")
            print("O sistema agora suporta senhas temporárias obrigatórias.")
            print("\n🔍 Verificando...")
            verify_migration()
        else:
            print("\n❌ Falha na migração!")