#!/usr/bin/env python3
"""
Script para remover duplicações do app.py
"""

def remover_duplicacoes():
    with open('app.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    print(f"Tamanho original: {len(content)} caracteres")
    
    # Verificar se o conteúdo está duplicado
    meio = len(content) // 2
    primeira_metade = content[:meio]
    segunda_metade = content[meio:]
    
    if primeira_metade == segunda_metade:
        print("DETECTADA DUPLICAÇÃO COMPLETA DO ARQUIVO!")
        content_limpo = primeira_metade
    else:
        print("Procurando por duplicações parciais...")
        
        # Dividir em linhas e remover duplicações consecutivas
        linhas = content.split('\n')
        linhas_limpas = []
        
        for i, linha in enumerate(linhas):
            # Adicionar linha se não for igual à anterior
            if i == 0 or linha != linhas[i-1]:
                linhas_limpas.append(linha)
        
        content_limpo = '\n'.join(linhas_limpas)
    
    print(f"Tamanho após limpeza: {len(content_limpo)} caracteres")
    
    with open('app.py', 'w', encoding='utf-8') as f:
        f.write(content_limpo)
    
    print("✅ Duplicações removidas!")

if __name__ == '__main__':
    remover_duplicacoes()