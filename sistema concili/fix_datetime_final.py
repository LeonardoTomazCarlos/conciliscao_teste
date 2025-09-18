#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script para corrigir TODOS os datetime.utcnow no app.py
"""

import re

arquivo_path = 'c:\\Users\\samue\\OneDrive\\Documentos\\GitHub\\conciliscao_teste\\sistema concili\\app.py'

print("Iniciando correcao do app.py...")

# Ler o arquivo
with open(arquivo_path, 'r', encoding='utf-8') as file:
    content = file.read()

print(f"Arquivo lido: {len(content)} caracteres")

# Contar ocorrências antes
datetime_utcnow_count = content.count('datetime.utcnow')
print(f"Encontradas {datetime_utcnow_count} ocorrencias de 'datetime.utcnow'")

# Fazer substituições específicas para evitar problemas
# 1. Substituir 'datetime.utcnow()' (com parênteses)
content = content.replace('datetime.utcnow()', 'utc_now()')

# 2. Substituir 'datetime.utcnow' (sem parênteses)
content = content.replace('datetime.utcnow', 'utc_now')

# Verificar depois
datetime_utcnow_count_after = content.count('datetime.utcnow')
utc_now_count = content.count('utc_now')

print(f"Apos substituicao:")
print(f"  - datetime.utcnow restantes: {datetime_utcnow_count_after}")
print(f"  - utc_now encontrados: {utc_now_count}")

# Salvar o arquivo
with open(arquivo_path, 'w', encoding='utf-8') as file:
    file.write(content)

print("Arquivo salvo com sucesso!")
print("Substituicoes concluidas!")