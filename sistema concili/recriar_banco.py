import os
import sqlite3

# Deletar o banco de dados existente
db_path = "instance/conciliacao.db"
if os.path.exists(db_path):
    os.remove(db_path)
    print(f"Banco de dados {db_path} removido.")

# Criar diretório instance se não existir
os.makedirs("instance", exist_ok=True)

print("Banco de dados removido. Agora reinicie o servidor Flask para recriar as tabelas.")
