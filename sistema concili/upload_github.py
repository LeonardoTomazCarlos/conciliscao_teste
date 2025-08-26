#!/usr/bin/env python3
"""
Script para facilitar o upload do Sistema de Conciliação Bancária para o GitHub
"""

import os
import subprocess
import sys

def executar_comando(comando, descricao):
    """Executa um comando e mostra o resultado"""
    print(f"\n🔄 {descricao}...")
    try:
        resultado = subprocess.run(comando, shell=True, capture_output=True, text=True)
        if resultado.returncode == 0:
            print(f"✅ {descricao} - Sucesso!")
            if resultado.stdout:
                print(resultado.stdout)
        else:
            print(f"❌ {descricao} - Erro!")
            print(resultado.stderr)
            return False
    except Exception as e:
        print(f"❌ Erro ao executar comando: {e}")
        return False
    return True

def verificar_git():
    """Verifica se o Git está instalado"""
    return executar_comando("git --version", "Verificando se o Git está instalado")

def inicializar_repositorio():
    """Inicializa o repositório Git"""
    if os.path.exists(".git"):
        print("✅ Repositório Git já inicializado")
        return True
    
    return executar_comando("git init", "Inicializando repositório Git")

def adicionar_arquivos():
    """Adiciona todos os arquivos ao Git"""
    return executar_comando("git add .", "Adicionando arquivos ao repositório")

def fazer_commit():
    """Faz o primeiro commit"""
    mensagem = "feat: Sistema de Conciliação Bancária v1.0\n\n- Upload de extratos bancários (CSV, Excel, OFX, CNAB, PDF)\n- Upload de lançamentos contábeis\n- Conciliação automática e manual\n- Detecção de duplicatas\n- Sistema de auditoria\n- Interface web responsiva\n- API REST completa\n- Relatórios e estatísticas"
    
    return executar_comando(f'git commit -m "{mensagem}"', "Fazendo primeiro commit")

def configurar_remote():
    """Configura o repositório remoto no GitHub"""
    print("\n🌐 Configuração do GitHub:")
    print("1. Acesse: https://github.com/new")
    print("2. Crie um novo repositório chamado 'sistema-conciliacao-bancaria'")
    print("3. NÃO inicialize com README, .gitignore ou license")
    print("4. Copie a URL do repositório (ex: https://github.com/seu-usuario/sistema-conciliacao-bancaria.git)")
    
    url = input("\nCole a URL do seu repositório: ").strip()
    
    if not url:
        print("❌ URL não fornecida")
        return False
    
    return executar_comando(f"git remote add origin {url}", "Configurando repositório remoto")

def fazer_push():
    """Faz o push para o GitHub"""
    return executar_comando("git push -u origin main", "Enviando código para o GitHub")

def main():
    """Função principal"""
    print("🚀 UPLOAD DO SISTEMA DE CONCILIAÇÃO BANCÁRIA PARA O GITHUB")
    print("=" * 60)
    
    # Verificar se estamos no diretório correto
    if not os.path.exists("app.py"):
        print("❌ Erro: Execute este script no diretório do projeto")
        sys.exit(1)
    
    # Passos para upload
    passos = [
        ("Verificar Git", verificar_git),
        ("Inicializar repositório", inicializar_repositorio),
        ("Adicionar arquivos", adicionar_arquivos),
        ("Fazer commit", fazer_commit),
        ("Configurar remote", configurar_remote),
        ("Fazer push", fazer_push)
    ]
    
    for descricao, funcao in passos:
        if not funcao():
            print(f"\n❌ Falha no passo: {descricao}")
            print("Verifique os erros acima e tente novamente")
            sys.exit(1)
    
    print("\n🎉 SUCESSO! Seu projeto foi enviado para o GitHub!")
    print("\n📋 Próximos passos:")
    print("1. Acesse seu repositório no GitHub")
    print("2. Configure as GitHub Pages (opcional)")
    print("3. Adicione uma descrição ao repositório")
    print("4. Configure as issues e pull requests")
    print("5. Compartilhe o link do repositório")

if __name__ == "__main__":
    main()
