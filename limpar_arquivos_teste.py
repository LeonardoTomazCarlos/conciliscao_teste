#!/usr/bin/env python3
"""
Script para limpar arquivos de teste antigos e manter apenas os criados recentemente
"""
import os
import glob
from pathlib import Path

def limpar_arquivos_teste():
    """Remover arquivos de teste antigos, mantendo apenas os criados recentemente"""
    
    print("🧹 LIMPANDO ARQUIVOS DE TESTE ANTIGOS...")
    print("=" * 60)
    
    # Diretório do sistema
    sistema_dir = "sistema concili"
    
    # Arquivos que DEVEM SER MANTIDOS (criados recentemente)
    arquivos_manter = [
        "extrato_bancario_teste_divergencias.csv",
        "lancamentos_contabeis_teste_divergencias.csv", 
        "extrato_bancario_divergencias_complexas.csv",
        "lancamentos_contabeis_divergencias_complexas.csv"
    ]
    
    print("✅ Arquivos que serão MANTIDOS:")
    for arquivo in arquivos_manter:
        print(f"   📌 {arquivo}")
    
    print("\n🗑️ Arquivos que serão REMOVIDOS:")
    
    # Padrões de arquivos de teste para remover
    padroes_remover = [
        "extrato_*.csv",
        "lancamentos_*.csv", 
        "teste_*.csv",
        "filtro_*.csv",
        "*divergencias.csv",  # arquivos antigos divergencias (sem "teste_")
        "*divergentes.csv",
        "*duplicatas.csv",
        "*orfaos.csv",
        "*exemplo.csv",
        "*dezembro.csv"
    ]
    
    arquivos_removidos = []
    
    for padrao in padroes_remover:
        caminho_padrao = os.path.join(sistema_dir, padrao)
        arquivos_encontrados = glob.glob(caminho_padrao)
        
        for arquivo_path in arquivos_encontrados:
            arquivo_nome = os.path.basename(arquivo_path)
            
            # Verificar se o arquivo deve ser mantido
            if arquivo_nome in arquivos_manter:
                print(f"   🛡️ PROTEGIDO: {arquivo_nome}")
                continue
            
            try:
                os.remove(arquivo_path)
                arquivos_removidos.append(arquivo_nome)
                print(f"   🗑️ REMOVIDO: {arquivo_nome}")
            except Exception as e:
                print(f"   ❌ ERRO ao remover {arquivo_nome}: {e}")
    
    # Limpar também arquivos de upload antigos
    uploads_dir = "uploads"
    if os.path.exists(uploads_dir):
        print(f"\n🧹 Limpando diretório {uploads_dir}...")
        
        for padrao in padroes_remover:
            caminho_padrao = os.path.join(uploads_dir, padrao)
            arquivos_encontrados = glob.glob(caminho_padrao)
            
            for arquivo_path in arquivos_encontrados:
                arquivo_nome = os.path.basename(arquivo_path)
                try:
                    os.remove(arquivo_path)
                    arquivos_removidos.append(f"uploads/{arquivo_nome}")
                    print(f"   🗑️ REMOVIDO: uploads/{arquivo_nome}")
                except Exception as e:
                    print(f"   ❌ ERRO ao remover uploads/{arquivo_nome}: {e}")
    
    print("\n" + "=" * 60)
    print(f"📊 RESUMO DA LIMPEZA:")
    print(f"   • Arquivos mantidos: {len(arquivos_manter)}")
    print(f"   • Arquivos removidos: {len(arquivos_removidos)}")
    
    if arquivos_removidos:
        print(f"\n🗑️ Lista completa dos arquivos removidos:")
        for arquivo in sorted(set(arquivos_removidos)):
            print(f"   - {arquivo}")
    
    print(f"\n✅ LIMPEZA CONCLUÍDA!")
    print(f"📁 Arquivos mantidos para teste de divergências:")
    for arquivo in arquivos_manter:
        caminho_completo = os.path.join(sistema_dir, arquivo)
        if os.path.exists(caminho_completo):
            print(f"   ✅ {arquivo}")
        else:
            print(f"   ❌ {arquivo} (NÃO ENCONTRADO)")
    
    return len(arquivos_removidos)

def verificar_arquivos_mantidos():
    """Verificar se os arquivos que deveriam ser mantidos ainda existem"""
    print("\n🔍 VERIFICAÇÃO FINAL DOS ARQUIVOS MANTIDOS:")
    print("=" * 50)
    
    sistema_dir = "sistema concili"
    arquivos_verificar = [
        "extrato_bancario_teste_divergencias.csv",
        "lancamentos_contabeis_teste_divergencias.csv", 
        "extrato_bancario_divergencias_complexas.csv",
        "lancamentos_contabeis_divergencias_complexas.csv"
    ]
    
    todos_ok = True
    for arquivo in arquivos_verificar:
        caminho = os.path.join(sistema_dir, arquivo)
        if os.path.exists(caminho):
            tamanho = os.path.getsize(caminho)
            print(f"   ✅ {arquivo} ({tamanho} bytes)")
        else:
            print(f"   ❌ {arquivo} (NÃO ENCONTRADO)")
            todos_ok = False
    
    if todos_ok:
        print("\n🎉 TODOS OS ARQUIVOS DE TESTE ESTÃO DISPONÍVEIS!")
    else:
        print("\n⚠️ ALGUNS ARQUIVOS DE TESTE ESTÃO FALTANDO!")
    
    return todos_ok

if __name__ == '__main__':
    try:
        print("🚀 INICIANDO LIMPEZA DE ARQUIVOS DE TESTE...")
        
        # Mudar para o diretório correto
        if not os.path.exists("sistema concili"):
            print("❌ Diretório 'sistema concili' não encontrado!")
            print("   Execute este script a partir do diretório raiz do projeto.")
            exit(1)
        
        # Executar limpeza
        removidos = limpar_arquivos_teste()
        
        # Verificar resultado
        verificar_arquivos_mantidos()
        
        print(f"\n✅ OPERAÇÃO CONCLUÍDA COM SUCESSO!")
        print(f"   📊 {removidos} arquivos antigos removidos")
        print(f"   📁 4 arquivos de teste mantidos")
        
    except Exception as e:
        print(f"❌ ERRO GERAL: {e}")
        import traceback
        traceback.print_exc()