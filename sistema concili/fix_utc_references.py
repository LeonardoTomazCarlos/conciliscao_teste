#!/usr/bin/env python3
"""
Script final para corrigir todas as referências a utc_now restantes
"""

import re

def fix_all_utc_references():
    file_path = "app.py"
    
    try:
        # Ler o arquivo
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Substituir todas as referências restantes a utc_now
        content = re.sub(r'default=utc_now', 'default=lambda: datetime.now(timezone.utc)', content)
        content = re.sub(r'onupdate=utc_now', 'onupdate=lambda: datetime.now(timezone.utc)', content)
        content = re.sub(r'utc_now\(\)', 'datetime.now(timezone.utc)', content)
        
        # Escrever o arquivo corrigido
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ Todas as referências a utc_now foram corrigidas!")
        
    except Exception as e:
        print(f"❌ Erro ao corrigir arquivo: {e}")

if __name__ == "__main__":
    fix_all_utc_references()