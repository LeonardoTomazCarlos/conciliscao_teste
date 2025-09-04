#!/usr/bin/env python3
"""
Migração: Adicionar tabela procedimento_conciliacao e campo procedimento_id em conciliacao
Data: 2025-09-03
"""

import sqlite3
import os
import uuid
from datetime import datetime

def run_migration():
    """Executar migração para adicionar sistema de procedimentos"""
    
    db_path = 'instance/conciliacao.db'
    if not os.path.exists(db_path):
        print("❌ Banco de dados não encontrado")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Verificar se já foi migrado
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='procedimento_conciliacao'")
        if cursor.fetchone():
            print("⚠️ Migração já foi aplicada")
            return True
        
        print("🚀 Iniciando migração...")
        
        # 1. Criar tabela procedimento_conciliacao
        cursor.execute("""
            CREATE TABLE procedimento_conciliacao (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                uuid VARCHAR(36) UNIQUE NOT NULL,
                tipo_procedimento VARCHAR(50) NOT NULL,
                metodo VARCHAR(20) NOT NULL DEFAULT 'automatico',
                data_criacao DATETIME NOT NULL,
                usuario_id INTEGER NOT NULL,
                status VARCHAR(20) DEFAULT 'em_andamento',
                descricao TEXT,
                total_conciliacoes INTEGER DEFAULT 0,
                valor_total DECIMAL(15,2) DEFAULT 0.00,
                observacoes TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (usuario_id) REFERENCES usuario (id)
            )
        """)
        print("✅ Tabela procedimento_conciliacao criada")
        
        # 2. Adicionar coluna procedimento_id na tabela conciliacao
        cursor.execute("ALTER TABLE conciliacao ADD COLUMN procedimento_id INTEGER")
        print("✅ Coluna procedimento_id adicionada à tabela conciliacao")
        
        # 3. Criar procedimento padrão para conciliações existentes (se houver)
        cursor.execute("SELECT COUNT(*) FROM conciliacao")
        count_conciliacoes = cursor.fetchone()[0]
        
        if count_conciliacoes > 0:
            # Criar procedimento "migração" para conciliações existentes
            procedimento_uuid = str(uuid.uuid4())
            cursor.execute("""
                INSERT INTO procedimento_conciliacao 
                (uuid, tipo_procedimento, metodo, data_criacao, usuario_id, status, descricao, total_conciliacoes)
                VALUES (?, 'migracao', 'manual', ?, 1, 'concluido', 'Conciliações migradas do sistema anterior', ?)
            """, (procedimento_uuid, datetime.now(), count_conciliacoes))
            
            procedimento_id = cursor.lastrowid
            
            # Associar todas as conciliações existentes a este procedimento
            cursor.execute("UPDATE conciliacao SET procedimento_id = ?", (procedimento_id,))
            
            print(f"✅ {count_conciliacoes} conciliações existentes migradas para procedimento {procedimento_uuid}")
        
        # 4. Criar índices para performance
        cursor.execute("CREATE INDEX idx_procedimento_uuid ON procedimento_conciliacao(uuid)")
        cursor.execute("CREATE INDEX idx_procedimento_usuario ON procedimento_conciliacao(usuario_id)")
        cursor.execute("CREATE INDEX idx_conciliacao_procedimento ON conciliacao(procedimento_id)")
        print("✅ Índices criados")
        
        # 5. Commit das mudanças
        conn.commit()
        print("✅ Migração concluída com sucesso!")
        
        # 6. Verificar estrutura final
        cursor.execute("SELECT COUNT(*) FROM procedimento_conciliacao")
        proc_count = cursor.fetchone()[0]
        print(f"📊 Total de procedimentos: {proc_count}")
        
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
        
        # Remover coluna procedimento_id da tabela conciliacao
        # SQLite não suporta DROP COLUMN, então recriar a tabela
        cursor.execute("""
            CREATE TABLE conciliacao_temp AS 
            SELECT id, data_conciliacao, tipo_conciliacao, status, observacoes, 
                   extrato_id, lancamento_id, usuario_id, created_at, updated_at
            FROM conciliacao
        """)
        
        cursor.execute("DROP TABLE conciliacao")
        cursor.execute("ALTER TABLE conciliacao_temp RENAME TO conciliacao")
        
        # Remover tabela procedimento_conciliacao
        cursor.execute("DROP TABLE IF EXISTS procedimento_conciliacao")
        
        # Recriar índices da tabela conciliacao
        cursor.execute("CREATE INDEX idx_conciliacao_usuario ON conciliacao(usuario_id)")
        cursor.execute("CREATE INDEX idx_conciliacao_data ON conciliacao(data_conciliacao)")
        
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

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == '--rollback':
        print("⚠️ ATENÇÃO: Revertendo migração!")
        resp = input("Tem certeza? (s/N): ")
        if resp.lower() in ['s', 'sim']:
            rollback_migration()
    else:
        print("🔄 Aplicando migração de procedimentos...")
        if run_migration():
            print("\n🎉 Migração aplicada com sucesso!")
            print("O sistema agora suporta agrupamento de conciliações por procedimento.")
        else:
            print("\n❌ Falha na migração!")
