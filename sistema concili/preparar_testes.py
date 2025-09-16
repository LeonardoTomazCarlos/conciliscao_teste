#!/usr/bin/env python3
"""
Script para limpar dados e preparar para novos testes
"""

import os
import sys

# Adicionar o diretório do app ao path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def limpar_dados_teste():
    """Limpa todos os dados para começar testes frescos"""
    
    print("🧹 LIMPEZA DE DADOS PARA TESTE")
    print("="*50)
    
    try:
        from app import app, db, ExtratoBancario, LancamentoContabil, Conciliacao, Divergencia, ProcedimentoConciliacao
        
        with app.app_context():
            print("✅ Contexto da aplicação carregado")
            
            # Contar dados antes da limpeza
            extratos_antes = ExtratoBancario.query.count()
            lancamentos_antes = LancamentoContabil.query.count()
            conciliacoes_antes = Conciliacao.query.count()
            divergencias_antes = Divergencia.query.count()
            procedimentos_antes = ProcedimentoConciliacao.query.count()
            
            print(f"\n📊 DADOS ANTES DA LIMPEZA:")
            print(f"   Extratos: {extratos_antes}")
            print(f"   Lançamentos: {lancamentos_antes}")
            print(f"   Conciliações: {conciliacoes_antes}")
            print(f"   Divergências: {divergencias_antes}")
            print(f"   Procedimentos: {procedimentos_antes}")
            
            # Perguntar confirmação
            if extratos_antes > 0 or lancamentos_antes > 0:
                resposta = input(f"\n⚠️  Deseja realmente APAGAR todos os dados? (s/n): ").lower().strip()
                if resposta not in ['s', 'sim', 'y', 'yes']:
                    print("❌ Operação cancelada pelo usuário")
                    return False
            
            print("\n🗑️  Iniciando limpeza...")
            
            # Limpar na ordem correta (FK dependencies)
            print("   Removendo divergências...")
            Divergencia.query.delete()
            
            print("   Removendo conciliações...")
            Conciliacao.query.delete()
            
            print("   Removendo procedimentos...")
            ProcedimentoConciliacao.query.delete()
            
            print("   Removendo extratos bancários...")
            ExtratoBancario.query.delete()
            
            print("   Removendo lançamentos contábeis...")
            LancamentoContabil.query.delete()
            
            # Salvar mudanças
            db.session.commit()
            
            # Verificar limpeza
            extratos_depois = ExtratoBancario.query.count()
            lancamentos_depois = LancamentoContabil.query.count()
            conciliacoes_depois = Conciliacao.query.count()
            divergencias_depois = Divergencia.query.count()
            procedimentos_depois = ProcedimentoConciliacao.query.count()
            
            print(f"\n✅ LIMPEZA CONCLUÍDA:")
            print(f"   Extratos: {extratos_antes} → {extratos_depois}")
            print(f"   Lançamentos: {lancamentos_antes} → {lancamentos_depois}")
            print(f"   Conciliações: {conciliacoes_antes} → {conciliacoes_depois}")
            print(f"   Divergências: {divergencias_antes} → {divergencias_depois}")
            print(f"   Procedimentos: {procedimentos_antes} → {procedimentos_depois}")
            
            if all(x == 0 for x in [extratos_depois, lancamentos_depois, conciliacoes_depois, divergencias_depois, procedimentos_depois]):
                print("\n🎉 BANCO LIMPO COM SUCESSO!")
                print("   Pronto para novos testes")
                return True
            else:
                print("\n⚠️  Alguns dados podem não ter sido removidos")
                return False
                
    except Exception as e:
        print(f"\n❌ Erro na limpeza: {e}")
        import traceback
        traceback.print_exc()
        return False

def listar_arquivos_teste():
    """Lista os arquivos de teste disponíveis"""
    
    print("\n📁 ARQUIVOS DE TESTE DISPONÍVEIS:")
    print("="*50)
    
    arquivos_teste = [
        "extrato_teste_dezembro.csv",
        "lancamentos_teste_dezembro.csv",
        "extrato_com_duplicatas.csv", 
        "lancamentos_com_duplicatas.csv",
        "extrato_diferenca_valores.csv",
        "lancamentos_diferenca_valores.csv",
        "extratos_orfaos.csv",
        "lancamentos_orfaos.csv",
        "extrato_datas_divergentes.csv",
        "lancamentos_datas_divergentes.csv"
    ]
    
    print("📊 CENÁRIOS BÁSICOS:")
    print("   extrato_teste_dezembro.csv - Extratos dezembro (29 transações)")
    print("   lancamentos_teste_dezembro.csv - Lançamentos dezembro (31 transações)")
    
    print("\n🔄 CENÁRIOS DE DUPLICATAS:")
    print("   extrato_com_duplicatas.csv - Extratos com duplicatas")
    print("   lancamentos_com_duplicatas.csv - Lançamentos com duplicatas")
    
    print("\n💰 CENÁRIOS DE DIFERENÇAS:")
    print("   extrato_diferenca_valores.csv - Valores ligeiramente diferentes")
    print("   lancamentos_diferenca_valores.csv - Valores com pequenas diferenças")
    
    print("\n🔍 CENÁRIOS DE ÓRFÃOS:")
    print("   extratos_orfaos.csv - Extratos sem lançamentos")
    print("   lancamentos_orfaos.csv - Lançamentos sem extratos")
    
    print("\n📅 CENÁRIOS DE DATAS:")
    print("   extrato_datas_divergentes.csv - Datas específicas")
    print("   lancamentos_datas_divergentes.csv - Mesmos valores, datas diferentes")
    
    # Verificar se os arquivos existem
    print("\n🔍 VERIFICAÇÃO DE ARQUIVOS:")
    for arquivo in arquivos_teste:
        if os.path.exists(arquivo):
            tamanho = os.path.getsize(arquivo)
            print(f"   ✅ {arquivo} ({tamanho} bytes)")
        else:
            print(f"   ❌ {arquivo} (não encontrado)")

def menu_principal():
    """Menu principal do script"""
    
    while True:
        print("\n" + "="*60)
        print("🧪 PREPARAÇÃO PARA TESTES - SISTEMA CONCILIAÇÃO")
        print("="*60)
        print("1. 🧹 Limpar todos os dados")
        print("2. 📁 Listar arquivos de teste")
        print("3. 📖 Ver guia de testes")
        print("4. 🚀 Executar detecção de divergências")
        print("5. ❌ Sair")
        print("="*60)
        
        opcao = input("Escolha uma opção (1-5): ").strip()
        
        if opcao == "1":
            limpar_dados_teste()
            
        elif opcao == "2":
            listar_arquivos_teste()
            
        elif opcao == "3":
            print("\n📖 GUIA DE TESTES:")
            print("   1. Execute: Limpar todos os dados")
            print("   2. Acesse: http://localhost:5000")
            print("   3. Faça upload dos arquivos CSV")
            print("   4. Execute conciliação automática")
            print("   5. Verifique divergências detectadas")
            print("   6. Teste os filtros na aba divergências")
            print("\n📄 Consulte GUIA_TESTES_COMPLETO.md para detalhes")
            
        elif opcao == "4":
            print("\n🔄 Executando detecção de divergências...")
            try:
                os.system("python forcar_deteccao_divergencias.py")
            except:
                print("❌ Erro ao executar. Certifique-se que o arquivo existe.")
                
        elif opcao == "5":
            print("\n👋 Saindo... Bons testes!")
            break
            
        else:
            print("\n❌ Opção inválida! Escolha entre 1-5")

if __name__ == "__main__":
    menu_principal()