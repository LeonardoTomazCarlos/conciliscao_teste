import sqlite3
import os
from datetime import datetime, timedelta

DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'instance', 'conciliacao.db'))
conn = sqlite3.connect(DB_PATH)
conn.row_factory = sqlite3.Row
cur = conn.cursor()

# simulate filter: today
today = datetime.now().date()
start = datetime.combine(today, datetime.min.time())
end = datetime.combine(today, datetime.max.time())

rows = cur.execute('SELECT id, usuario_id, data_conciliacao FROM conciliacao WHERE data_conciliacao >= ? AND data_conciliacao <= ?', (start, end)).fetchall()
print(f"Conciliacoes hoje: {len(rows)}")
for r in rows:
    print(dict(r))

conn.close()
