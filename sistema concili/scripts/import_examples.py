import os
import shutil
import sqlite3
from datetime import datetime
import csv

BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DB_PATH = os.path.join(BASE, 'instance', 'conciliacao.db')
EX_DIR = os.path.join(BASE, 'exemplos')

if not os.path.exists(DB_PATH):
    print('DB not found:', DB_PATH)
    raise SystemExit(1)

# backup
ts = datetime.now().strftime('%Y%m%d_%H%M%S')
backup = DB_PATH + f'.bak_examples_{ts}'
shutil.copy2(DB_PATH, backup)
print('Backup created at', backup)

conn = sqlite3.connect(DB_PATH)
conn.row_factory = sqlite3.Row
cur = conn.cursor()

# get user id for Leonardo.Tomaz
user = cur.execute("SELECT id FROM usuario WHERE LOWER(username)=?", ('leonardo.tomaz',)).fetchone()
if not user:
    user = cur.execute("SELECT id FROM usuario WHERE LOWER(username)=?", ('leonardo',)).fetchone()
if not user:
    user = cur.execute("SELECT id FROM usuario WHERE username='admin'").fetchone()
user_id = user['id']
print('Using user id', user_id)

# helper to insert extratos
def insert_extratos_from_csv(path):
    with open(path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            cur.execute('INSERT INTO extrato_bancario (conta_id, usuario_id, data, descricao, valor, tipo, categoria, conciliado, arquivo_origem, formato_arquivo, numero_documento, hash_transacao, transacao_recorrente, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (
                1, user_id, row['data'], row['descricao'], float(row['valor']), row['tipo'], 'Exemplo', 0, os.path.basename(path), 'CSV', row.get('numero_documento', ''), '', 0, datetime.now(), datetime.now()
            ))

# helper to insert lancamentos
def insert_lancamentos_from_csv(path):
    with open(path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            cur.execute('INSERT INTO lancamento_contabil (usuario_id, data, descricao, valor, tipo, categoria, conciliado, arquivo_origem, numero_documento, centro_custo, conta_contabil, fornecedor_cliente, hash_transacao, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (
                user_id, row['data'], row['descricao'], float(row['valor']), row['tipo'], 'Exemplo', 0, os.path.basename(path), row.get('numero_documento', ''), '', '', '', '', datetime.now(), datetime.now()
            ))

# Insert examples
insert_extratos_from_csv(os.path.join(EX_DIR, 'conciliacoes_extratos.csv'))
insert_lancamentos_from_csv(os.path.join(EX_DIR, 'conciliacoes_lancamentos.csv'))

conn.commit()

# Now create automatic conciliação for matching values
extratos = cur.execute("SELECT id, data, valor, tipo FROM extrato_bancario WHERE arquivo_origem=?", ('conciliacoes_extratos.csv',)).fetchall()
lancamentos = cur.execute("SELECT id, data, valor, tipo FROM lancamento_contabil WHERE arquivo_origem=?", ('conciliacoes_lancamentos.csv',)).fetchall()

matched = 0
for e in extratos:
    for l in lancamentos:
        if e['valor'] == l['valor'] and e['data'] == l['data'] and e['tipo'] == l['tipo']:
            # check existing
            exists = cur.execute('SELECT id FROM conciliacao WHERE extrato_id=? AND lancamento_id=?', (e['id'], l['id'])).fetchone()
            if not exists:
                cur.execute('INSERT INTO conciliacao (extrato_id, lancamento_id, usuario_id, data_conciliacao, observacoes, tipo_conciliacao, status) VALUES (?, ?, ?, ?, ?, ?, ?)', (
                    e['id'], l['id'], user_id, datetime.now(), 'Conciliação automática (exemplo)', 'automatica', 'ativa'
                ))
                cur.execute('UPDATE extrato_bancario SET conciliado=1 WHERE id=?', (e['id'],))
                cur.execute('UPDATE lancamento_contabil SET conciliado=1 WHERE id=?', (l['id'],))
                matched += 1

conn.commit()
print('Inserted', matched, 'automatic conciliacoes')

# create some divergencias (e.g., value mismatch)
# pick one extrato and one lancamento with similar description but different value
cur.execute("SELECT id, descricao, valor FROM extrato_bancario WHERE arquivo_origem=? LIMIT 1", ('conciliacoes_extratos.csv',))
e1 = cur.fetchone()
cur.execute("SELECT id, descricao, valor FROM lancamento_contabil WHERE arquivo_origem=? LIMIT 1", ('conciliacoes_lancamentos.csv',))
l1 = cur.fetchone()
if e1 and l1 and e1['valor'] != l1['valor']:
    cur.execute('INSERT INTO divergencia (tipo, extrato_id, lancamento_id, descricao, status, created_at) VALUES (?, ?, ?, ?, ?, ?)', (
        'valor_incorreto', e1['id'], l1['id'], f'Diferença exemplo: Extrato {e1["valor"]} vs Lancamento {l1["valor"]}', 'pendente', datetime.now()
    ))
    conn.commit()
    print('Created 1 divergencia example')

conn.close()
print('Done')
