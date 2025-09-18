#!/usr/bin/env python3
"""
Script para limpar TODOS os erros do app.py de uma vez só
"""
import re

def limpar_app():
    with open('app.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. Remover o monkey patch problemático
    content = re.sub(r'# Monkey patch para compatibilidade\s*\n.*datetime\.utcnow = utc_now.*\n', '', content)
    
    # 2. Substituir TODAS as ocorrências de datetime.utcnow por datetime.now(timezone.utc)
    content = re.sub(r'datetime\.utcnow', 'lambda: datetime.now(timezone.utc)', content)
    
    # 3. Adicionar import do timezone no topo
    if 'from datetime import timezone' not in content:
        content = re.sub(r'(from datetime import datetime)', r'\1, timezone', content)
    
    # 4. Remover todas as referências a utc_now e utc_default
    content = re.sub(r'def utc_now.*?\n.*?\n', '', content, flags=re.DOTALL)
    content = re.sub(r'def utc_default.*?\n.*?\n', '', content, flags=re.DOTALL)
    
    # 5. Simplificar os modelos - remover default e onupdate problemáticos
    # Em vez de usar funções, vamos deixar o SQLAlchemy gerenciar
    content = re.sub(r',\s*default=lambda:\s*datetime\.now\(timezone\.utc\)', '', content)
    content = re.sub(r',\s*onupdate=lambda:\s*datetime\.now\(timezone\.utc\)', '', content)
    content = re.sub(r'default=lambda:\s*datetime\.now\(timezone\.utc\),?\s*', '', content)
    content = re.sub(r'onupdate=lambda:\s*datetime\.now\(timezone\.utc\),?\s*', '', content)
    
    # 6. Usar nullable=False onde necessário e deixar SQLAlchemy gerenciar timestamps
    content = re.sub(
        r'(\w+_at = db\.Column\(db\.DateTime)([^)]*)\)',
        r'\1, nullable=False, default=db.func.now())',
        content
    )
    
    # Para data_criacao e data_conciliacao também
    content = re.sub(
        r'(data_criacao = db\.Column\(db\.DateTime)([^)]*)\)',
        r'\1, nullable=False, default=db.func.now())',
        content
    )
    content = re.sub(
        r'(data_conciliacao = db\.Column\(db\.DateTime)([^)]*)\)',
        r'\1, nullable=True, default=db.func.now())',
        content
    )
    
    # 7. Limpar imports desnecessários
    content = re.sub(r'from datetime import timezone\n', '', content)
    
    with open('app.py', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Arquivo app.py limpo!")

if __name__ == '__main__':
    limpar_app()