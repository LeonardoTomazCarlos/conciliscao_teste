"""
Script para corrigir duplicações no app.py
"""

# Ler o arquivo atual
with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Remover a seção duplicada
lines = content.split('\n')
clean_lines = []
skip_mode = False

for i, line in enumerate(lines):
    # Começar a pular depois do logout
    if '@app.route(\'/api/usuarios\', methods=[\'GET\'])' in line and not skip_mode:
        skip_mode = True
        continue
    
    # Parar de pular quando chegar nas rotas de admin limpas
    if '# === ROTAS DE ADMINISTRAÇÃO ===' in line and skip_mode:
        skip_mode = False
        clean_lines.append(line)
        continue
    
    if not skip_mode:
        clean_lines.append(line)

# Escrever o arquivo limpo
with open('app.py', 'w', encoding='utf-8') as f:
    f.write('\n'.join(clean_lines))

print("Arquivo app.py corrigido!")
