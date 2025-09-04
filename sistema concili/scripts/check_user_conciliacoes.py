import sqlite3
import os
import sys

if len(sys.argv) < 2:
    print("Usage: python scripts/check_user_conciliacoes.py <username>")
    sys.exit(1)

username_to_check = sys.argv[1]
DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'instance', 'conciliacao.db')
DB_PATH = os.path.abspath(DB_PATH)

if not os.path.exists(DB_PATH):
    print("Database file not found:", DB_PATH)
    sys.exit(1)

conn = sqlite3.connect(DB_PATH)
conn.row_factory = sqlite3.Row
cur = conn.cursor()

# find user (case-insensitive)
user = cur.execute('SELECT * FROM usuario WHERE LOWER(username)=?', (username_to_check.lower(),)).fetchone()
if not user:
    print(f"Usuário '{username_to_check}' não encontrado no banco.")
    conn.close()
    sys.exit(0)

user_id = user['id']
nome_completo = user['nome_completo'] if 'nome_completo' in user.keys() else None
print(f"Usuário encontrado: id={user_id}, username={user['username']}, nome_completo={nome_completo}")

# count conciliacoes for this user
count = cur.execute('SELECT COUNT(*) FROM conciliacao WHERE usuario_id = ?', (user_id,)).fetchone()[0]
print(f"Total de conciliações para {user['username']}: {count}")

if count > 0:
    rows = cur.execute('SELECT id, extrato_id, lancamento_id, data_conciliacao, tipo_conciliacao, status, observacoes FROM conciliacao WHERE usuario_id = ? ORDER BY data_conciliacao DESC LIMIT 20', (user_id,)).fetchall()
    print('\nÚltimas conciliações:')
    for r in rows:
        print(dict(r))

conn.close()
