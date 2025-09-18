#!/usr/bin/env python3
"""
Script para adicionar type hints básicos e corrigir problemas de configuração
"""

import re

def fix_type_hints_and_config():
    file_path = "app.py"
    
    try:
        # Ler o arquivo
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Adicionar imports de typing se não existir
        if 'from typing import' not in content:
            # Adicionar imports após os imports existentes
            typing_import = 'from typing import Optional, Dict, Any, List, Union\n'
            # Encontrar a primeira linha que não é import
            lines = content.split('\n')
            import_end = 0
            for i, line in enumerate(lines):
                if not (line.startswith('from ') or line.startswith('import ') or line.strip() == ''):
                    import_end = i
                    break
            
            lines.insert(import_end, typing_import.strip())
            content = '\n'.join(lines)
        
        # Corrigir a função load_user
        old_load_user = r'def load_user\(user_id\):'
        new_load_user = 'def load_user(user_id: str) -> Optional[object]:'
        content = re.sub(old_load_user, new_load_user, content)
        
        # Corrigir a função log_auditoria
        old_log_auditoria = r'def log_auditoria\(acao, tabela=None, registro_id=None, dados_anteriores=None, dados_novos=None\):'
        new_log_auditoria = 'def log_auditoria(acao: str, tabela: Optional[str] = None, registro_id: Optional[int] = None, dados_anteriores: Optional[Dict[str, Any]] = None, dados_novos: Optional[Dict[str, Any]] = None) -> None:'
        content = re.sub(old_log_auditoria, new_log_auditoria, content)
        
        # Corrigir a função admin_required
        old_admin_required = r'def admin_required\(f\):'
        new_admin_required = 'def admin_required(f: Any) -> Any:'
        content = re.sub(old_admin_required, new_admin_required, content)
        
        # Corrigir decorated_function
        old_decorated = r'def decorated_function\(\*args, \*\*kwargs\):'
        new_decorated = 'def decorated_function(*args: Any, **kwargs: Any) -> Any:'
        content = re.sub(old_decorated, new_decorated, content)
        
        # Corrigir a configuração do login_manager.login_view
        old_login_view = r"login_manager\.login_view = 'login'"
        new_login_view = "login_manager.login_view = 'login'  # type: ignore"
        content = re.sub(old_login_view, new_login_view, content)
        
        # Remover o monkey patch problemático
        content = re.sub(r'datetime\.utcnow = utc_now\n', '', content)
        
        # Remover funções utc_now e utc_default duplicadas
        content = re.sub(r'# Função para substituir datetime\.utcnow\(\) obsoleto\ndef utc_now\(\):\s*return datetime\.now\(timezone\.utc\)\s*\n', '', content)
        content = re.sub(r'# Função lambda para usar como default no SQLAlchemy\nutc_default = lambda: datetime\.now\(timezone\.utc\)\s*\n', '', content)
        content = re.sub(r'# Compatibilidade com código antigo\ndatetime\.utcnow = utc_now\s*\n', '', content)
        
        # Escrever o arquivo corrigido
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ Type hints e configurações corrigidas com sucesso!")
        print("📝 Adicionados type hints básicos")
        print("🔧 Configuração do LoginManager corrigida")
        print("🧹 Código duplicado removido")
        
    except Exception as e:
        print(f"❌ Erro ao corrigir arquivo: {e}")

if __name__ == "__main__":
    fix_type_hints_and_config()