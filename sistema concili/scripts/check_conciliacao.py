import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'instance', 'conciliacao.db')
DB_PATH = os.path.abspath(DB_PATH)

print(f"DB: {DB_PATH}")
if not os.path.exists(DB_PATH):
    print("Database file not found.")
    raise SystemExit(1)

conn = sqlite3.connect(DB_PATH)
conn.row_factory = sqlite3.Row
cur = conn.cursor()

# list tables
cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = [r[0] for r in cur.fetchall()]
print('\nTables:', tables)

# show schema for conciliacao and usuario if exist
for t in ('conciliacao', 'usuario'):
    if t in tables:
        print(f"\nSchema for {t}:")
        for row in cur.execute(f"PRAGMA table_info({t})"):
            print(dict(row))

# show last 20 conciliacoes
if 'conciliacao' not in tables:
    print('\nNo conciliacao table present.')
    raise SystemExit(0)

print('\nLast 20 conciliacoes:')
rows = cur.execute('SELECT * FROM conciliacao ORDER BY id DESC LIMIT 20').fetchall()
if not rows:
    print('  (no rows)')
else:
    for r in rows:
        d = dict(r)
        # try to resolve usuario name if possible
        usuario_id = d.get('usuario_id') or d.get('usuario')
        username = None
        if usuario_id and 'usuario' in tables:
            # fetch full usuario row and pick a sensible display field if present
            q = cur.execute('SELECT * FROM usuario WHERE id = ?', (usuario_id,)).fetchone()
            if q:
                qd = dict(q)
                # prefer username, nome_completo, nome, email (legacy column names tolerated)
                username = qd.get('username') or qd.get('nome_completo') or qd.get('nome') or qd.get('email')
        d['usuario_resolved'] = username
        print('  -', d)

# count total
cnt = cur.execute('SELECT COUNT(*) FROM conciliacao').fetchone()[0]
print(f"\nTotal conciliacoes: {cnt}")

conn.close()
