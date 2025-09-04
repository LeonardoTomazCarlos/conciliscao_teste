import os
import sys
import shutil
import sqlite3
from datetime import datetime

if len(sys.argv) < 2:
    print("Usage: python scripts/reassign_conciliacoes.py <username>")
    sys.exit(1)

username = sys.argv[1]
BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DB_PATH = os.path.join(BASE, 'instance', 'conciliacao.db')

if not os.path.exists(DB_PATH):
    print('Database file not found:', DB_PATH)
    sys.exit(1)

# make a timestamped backup
ts = datetime.now().strftime('%Y%m%d_%H%M%S')
backup_path = DB_PATH + f'.bak_{ts}'
shutil.copy2(DB_PATH, backup_path)
print('Backup created at', backup_path)

conn = sqlite3.connect(DB_PATH)
conn.row_factory = sqlite3.Row
cur = conn.cursor()

# find target user
user = cur.execute('SELECT id, username, nome_completo FROM usuario WHERE LOWER(username)=?', (username.lower(),)).fetchone()
if not user:
    print(f"User '{username}' not found in DB.")
    conn.close()
    sys.exit(1)

user_id = user['id']
print(f"Target user: id={user_id}, username={user['username']}, nome={user['nome_completo']}")

# Count conciliacoes currently owned by admin (1) and target
count_admin = cur.execute('SELECT COUNT(*) FROM conciliacao WHERE usuario_id = 1').fetchone()[0]
count_target = cur.execute('SELECT COUNT(*) FROM conciliacao WHERE usuario_id = ?', (user_id,)).fetchone()[0]
print(f"Before: admin(1) conciliacoes = {count_admin}, {user['username']} conciliacoes = {count_target}")

if count_admin == 0:
    print('No conciliacoes found for usuario_id=1. No changes made.')
    conn.close()
    sys.exit(0)

# Perform update: reassign all where usuario_id = 1 to target user
cur.execute('UPDATE conciliacao SET usuario_id = ? WHERE usuario_id = 1', (user_id,))
conn.commit()

count_admin_after = cur.execute('SELECT COUNT(*) FROM conciliacao WHERE usuario_id = 1').fetchone()[0]
count_target_after = cur.execute('SELECT COUNT(*) FROM conciliacao WHERE usuario_id = ?', (user_id,)).fetchone()[0]
print(f"After: admin(1) conciliacoes = {count_admin_after}, {user['username']} conciliacoes = {count_target_after}")

# show last 20 conciliacoes of the target user
rows = cur.execute('SELECT id, extrato_id, lancamento_id, data_conciliacao, tipo_conciliacao, status FROM conciliacao WHERE usuario_id = ? ORDER BY id DESC LIMIT 20', (user_id,)).fetchall()
print('\nÚltimas conciliações atribuídas ao usuário:')
for r in rows:
    d = dict(r)
    print(d)

conn.close()
print('\nReatribuição concluída (verifique logs e histórico no sistema).')
