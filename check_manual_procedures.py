#!/usr/bin/env python3
import sqlite3

# Conectar à base de dados
conn = sqlite3.connect('instance/conciliacao.db')
cursor = conn.cursor()

print("🔍 VERIFICANDO PROCEDIMENTOS NA BASE DE DADOS:")
print("=" * 50)

# Verificar métodos existentes
cursor.execute('SELECT metodo, COUNT(*) FROM procedimento_conciliacao GROUP BY metodo')
print("Métodos na base de dados:")
for row in cursor.fetchall():
    metodo, count = row
    print(f"  '{metodo}': {count} procedimentos")

print("\n" + "=" * 50)

# Verificar procedimentos manuais especificamente
cursor.execute('SELECT COUNT(*) FROM procedimento_conciliacao WHERE metodo = ?', ('manual',))
manual_count = cursor.fetchone()[0]
print(f"Total de procedimentos com método 'manual': {manual_count}")

# Verificar se há procedimentos com método diferente de 'automatico' e 'manual'
cursor.execute('''
    SELECT DISTINCT metodo 
    FROM procedimento_conciliacao 
    WHERE metodo NOT IN ('automatico', 'manual')
''')
outros_metodos = cursor.fetchall()
if outros_metodos:
    print(f"Outros métodos encontrados: {[m[0] for m in outros_metodos]}")

# Mostrar alguns exemplos de procedimentos manuais
cursor.execute('''
    SELECT id, uuid, tipo_procedimento, metodo, status, data_criacao 
    FROM procedimento_conciliacao 
    WHERE metodo = ? 
    ORDER BY data_criacao DESC 
    LIMIT 5
''', ('manual',))

manual_procs = cursor.fetchall()
if manual_procs:
    print(f"\nExemplos de procedimentos manuais (últimos 5):")
    for proc in manual_procs:
        id_proc, uuid, tipo, metodo, status, data = proc
        print(f"  ID: {id_proc}, UUID: {uuid[:8]}..., Tipo: {tipo}, Status: {status}, Data: {data}")
else:
    print("\n❌ Nenhum procedimento manual encontrado!")

conn.close()