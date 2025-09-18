#!/usr/bin/env python3
"""
Script para corrigir definitivamente todos os problemas de datetime no app.py
Substitui datetime.utcnow por datetime.now(timezone.utc)
"""

import re

def fix_datetime_in_file():
    file_path = "app.py"
    
    try:
        # Ler o arquivo
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Adicionar import de timezone se não existir
        if 'from datetime import timezone' not in content:
            # Procurar a linha de import datetime
            import_pattern = r'from datetime import datetime'
            if re.search(import_pattern, content):
                content = re.sub(
                    import_pattern,
                    'from datetime import datetime, timezone',
                    content
                )
            else:
                # Se não encontrar, adicionar no topo
                content = 'from datetime import datetime, timezone\n' + content
        
        # Remover o monkey patch que estava causando problemas
        content = re.sub(r'datetime\.utcnow = utc_now\n', '', content)
        
        # Substituir todas as ocorrências de datetime.utcnow
        patterns_to_replace = [
            (r'datetime\.utcnow\(\)', 'datetime.now(timezone.utc)'),
            (r'datetime\.utcnow', 'lambda: datetime.now(timezone.utc)'),
            (r'default=lambda: datetime\.now\(timezone\.utc\)\(\)', 'default=lambda: datetime.now(timezone.utc)'),
        ]
        
        for pattern, replacement in patterns_to_replace:
            content = re.sub(pattern, replacement, content)
        
        # Remover as funções utc_now e utc_default que não são mais necessárias
        content = re.sub(r'def utc_now\(\):\s*return datetime\.now\(timezone\.utc\)\s*\n', '', content)
        content = re.sub(r'def utc_default\(\):\s*return datetime\.now\(timezone\.utc\)\s*\n', '', content)
        
        # Escrever o arquivo corrigido
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ Arquivo app.py corrigido com sucesso!")
        print("🔄 Todas as instâncias de datetime.utcnow foram substituídas")
        print("📦 Import de timezone adicionado")
        print("🧹 Funções desnecessárias removidas")
        
    except Exception as e:
        print(f"❌ Erro ao corrigir arquivo: {e}")

if __name__ == "__main__":
    fix_datetime_in_file()