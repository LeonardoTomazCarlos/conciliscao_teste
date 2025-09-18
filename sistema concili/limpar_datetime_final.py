#!/usr/bin/env python3
"""
Script final para limpar TODAS as referências datetime.utcnow
"""
import re

def limpar_todas_referencias():
    with open('app.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. Remover comentário sobre datetime.utcnow
    content = re.sub(r'# Função para substituir datetime\.utcnow\(\) obsoleto\s*\n', '', content)
    
    # 2. Remover definição da função utc_now e linha de monkey patch
    content = re.sub(r'def utc_now.*?\n.*?\n.*?datetime\.utcnow = utc_now\s*\n', '', content, flags=re.DOTALL)
    
    # 3. Substituir todas as outras ocorrências:
    # - Em modelos SQLAlchemy, usar None (deixar SQLAlchemy gerenciar)
    content = re.sub(r'default=datetime\.utcnow', 'nullable=False', content)
    content = re.sub(r'onupdate=datetime\.utcnow', '', content)
    
    # - Em código Python, usar datetime.now()
    content = re.sub(r'datetime\.utcnow\(\)', 'datetime.now()', content)
    
    # 4. Limpar vírgulas duplas
    content = re.sub(r',\s*,', ',', content)
    content = re.sub(r'nullable=False,\s*nullable=False', 'nullable=False', content)
    
    # 5. Limpar linha com monkey patch restante se existir
    content = re.sub(r'datetime\.utcnow = .*\n', '', content)
    
    with open('app.py', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Todas as referências datetime.utcnow foram removidas!")

if __name__ == '__main__':
    limpar_todas_referencias()