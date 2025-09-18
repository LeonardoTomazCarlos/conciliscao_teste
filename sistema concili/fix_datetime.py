#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script para corrigir datetime.utcnow no app.py
"""

import re

# Ler o arquivo
with open('c:\\Users\\samue\\OneDrive\\Documentos\\GitHub\\conciliscao_teste\\sistema concili\\app.py', 'r', encoding='utf-8') as file:
    content = file.read()

# Substituir datetime.utcnow por utc_now
content_fixed = content.replace('datetime.utcnow', 'utc_now')

# Escrever o arquivo corrigido
with open('c:\\Users\\samue\\OneDrive\\Documentos\\GitHub\\conciliscao_teste\\sistema concili\\app.py', 'w', encoding='utf-8') as file:
    file.write(content_fixed)

print("✅ Arquivo app.py corrigido com sucesso!")
print("📝 Substituições feitas: datetime.utcnow -> utc_now")