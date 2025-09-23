#!/usr/bin/env python3
"""
Script para limpar TODOS os extratos e lançamentos da pasta uploads e outras localizações
"""
import os
import glob
import shutil

def limpar_uploads_completo():
    """Remover todos os extratos e lançamentos da pasta uploads e outras pastas"""
    
    print("🧹 LIMPANDO PASTA UPLOADS E OUTRAS LOCALIZAÇÕES...")
    print("=" * 60)
    
    # Localizações para verificar e limpar
    diretorios_limpar = [
        "uploads",
        "sistema concili/uploads", 
        "sistema concili/exemplos",
        "temp",
        "tmp"
    ]
    
    # Padrões de arquivos para remover (extratos e lançamentos)
    padroes_remover = [
        "*extrato*.csv",
        "*lancamento*.csv",
        "*lancamentos*.csv", 
        "*estrato*.csv",  # possível erro de digitação
        "*.csv"  # todos os CSVs na pasta uploads
    ]
    
    total_removidos = 0
    arquivos_removidos = []
    
    for diretorio in diretorios_limpar:
        if not os.path.exists(diretorio):
            print(f"📁 {diretorio} - NÃO EXISTE")
            continue
            
        print(f"\n📁 VERIFICANDO: {diretorio}")
        
        # Listar arquivos primeiro
        arquivos_encontrados = []
        for padrao in padroes_remover:
            caminho_padrao = os.path.join(diretorio, padrao)
            arquivos_encontrados.extend(glob.glob(caminho_padrao))
        
        # Remover duplicatas da lista
        arquivos_encontrados = list(set(arquivos_encontrados))
        
        if not arquivos_encontrados:
            print(f"   ✅ VAZIO - Nenhum arquivo encontrado")
            continue
        
        print(f"   📊 Encontrados {len(arquivos_encontrados)} arquivos:")
        
        for arquivo_path in arquivos_encontrados:
            arquivo_nome = os.path.basename(arquivo_path)
            try:
                # Verificar se é arquivo (não pasta)
                if os.path.isfile(arquivo_path):
                    tamanho = os.path.getsize(arquivo_path)
                    os.remove(arquivo_path)
                    arquivos_removidos.append(f"{diretorio}/{arquivo_nome}")
                    total_removidos += 1
                    print(f"   🗑️ REMOVIDO: {arquivo_nome} ({tamanho} bytes)")
                else:
                    print(f"   ⚠️ IGNORADO: {arquivo_nome} (não é arquivo)")
            except Exception as e:
                print(f"   ❌ ERRO ao remover {arquivo_nome}: {e}")
    
    # Limpar pastas vazias criadas desnecessariamente
    pastas_para_verificar = ["temp", "tmp"]
    for pasta in pastas_para_verificar:
        if os.path.exists(pasta) and not os.listdir(pasta):
            try:
                os.rmdir(pasta)
                print(f"🗑️ PASTA VAZIA REMOVIDA: {pasta}")
            except:
                pass
    
    print("\n" + "=" * 60)
    print(f"📊 RESUMO DA LIMPEZA DE UPLOADS:")
    print(f"   • Total de arquivos removidos: {total_removidos}")
    print(f"   • Diretórios verificados: {len(diretorios_limpar)}")
    
    if arquivos_removidos:
        print(f"\n🗑️ Arquivos removidos:")
        for arquivo in sorted(arquivos_removidos):
            print(f"   - {arquivo}")
    else:
        print(f"\n✅ Nenhum arquivo encontrado para remoção")
    
    return total_removidos

def verificar_uploads_limpo():
    """Verificar se as pastas estão realmente limpas"""
    print("\n🔍 VERIFICAÇÃO FINAL DAS PASTAS:")
    print("=" * 40)
    
    diretorios_verificar = [
        "uploads",
        "sistema concili/uploads",
        "sistema concili/exemplos"
    ]
    
    tudo_limpo = True
    
    for diretorio in diretorios_verificar:
        if not os.path.exists(diretorio):
            print(f"📁 {diretorio} - NÃO EXISTE ✅")
            continue
        
        arquivos = []
        try:
            arquivos = [f for f in os.listdir(diretorio) if os.path.isfile(os.path.join(diretorio, f))]
        except:
            pass
        
        if not arquivos:
            print(f"📁 {diretorio} - VAZIO ✅")
        else:
            print(f"📁 {diretorio} - CONTÉM {len(arquivos)} ARQUIVOS ⚠️")
            for arquivo in arquivos[:5]:  # mostrar apenas primeiros 5
                print(f"   - {arquivo}")
            if len(arquivos) > 5:
                print(f"   ... e mais {len(arquivos) - 5} arquivos")
            tudo_limpo = False
    
    if tudo_limpo:
        print("\n🎉 TODAS AS PASTAS ESTÃO LIMPAS!")
    else:
        print("\n⚠️ ALGUMAS PASTAS AINDA CONTÊM ARQUIVOS!")
    
    return tudo_limpo

def criar_estrutura_limpa():
    """Garantir que as pastas necessárias existam vazias"""
    print("\n🏗️ CRIANDO ESTRUTURA LIMPA:")
    
    pastas_criar = ["uploads"]
    
    for pasta in pastas_criar:
        if not os.path.exists(pasta):
            os.makedirs(pasta)
            print(f"   📁 CRIADA: {pasta}")
        else:
            print(f"   📁 JÁ EXISTE: {pasta}")

if __name__ == '__main__':
    try:
        print("🚀 INICIANDO LIMPEZA COMPLETA DE UPLOADS...")
        
        # Executar limpeza
        removidos = limpar_uploads_completo()
        
        # Criar estrutura limpa
        criar_estrutura_limpa()
        
        # Verificar resultado
        limpo = verificar_uploads_limpo()
        
        print(f"\n✅ OPERAÇÃO CONCLUÍDA!")
        print(f"   📊 {removidos} arquivos removidos")
        print(f"   🧹 Pasta uploads limpa e pronta")
        
        if limpo:
            print(f"   🎯 Sistema pronto para novos uploads")
        
    except Exception as e:
        print(f"❌ ERRO GERAL: {e}")
        import traceback
        traceback.print_exc()