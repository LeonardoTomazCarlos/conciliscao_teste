#!/usr/bin/env python3
"""
Script para testar a detecção de divergências do sistema de conciliação
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, db, ExtratoBancario, LancamentoContabil, Divergencia, verificar_divergencias
from datetime import datetime
import logging

def limpar_dados_teste():
    """Limpa dados de teste existentes"""
    print("Limpando dados de teste existentes...")
    
    with app.app_context():
        # Deletar divergências
        Divergencia.query.delete()
        
        # Deletar extratos e lançamentos de teste
        ExtratoBancario.query.filter(ExtratoBancario.descricao.like('%TESTE%')).delete()
        LancamentoContabil.query.filter(LancamentoContabil.descricao.like('%TESTE%')).delete()
        
        db.session.commit()
        print("Dados de teste limpos com sucesso!")

def criar_dados_teste():
    """Cria dados de teste específicos para divergências"""
    print("Criando dados de teste...")
    
    with app.app_context():
        # 1. Transação órfã no extrato (sem correspondência)
        extrato_orfao = ExtratoBancario(
            data=datetime(2024, 1, 15),
            descricao="TESTE ÓRFÃO EXTRATO - Transação sem correspondência",
            valor=500.00,
            tipo="debito",
            categoria="Teste",
            arquivo_origem="teste.csv",
            formato_arquivo="CSV",
            conciliado=False
        )
        db.session.add(extrato_orfao)
        
        # 2. Transação órfã no lançamento (sem correspondência)
        lancamento_orfao = LancamentoContabil(
            data=datetime(2024, 1, 16),
            descricao="TESTE ÓRFÃO CONTÁBIL - Lançamento sem correspondência",
            valor=750.00,
            tipo="credito",
            categoria="Teste",
            arquivo_origem="teste.csv",
            conciliado=False
        )
        db.session.add(lancamento_orfao)
        
        # 3. Transações duplicadas no extrato
        extrato_dup1 = ExtratoBancario(
            data=datetime(2024, 1, 17),
            descricao="TESTE DUPLICATA - Transação repetida",
            valor=300.00,
            tipo="debito",
            categoria="Teste",
            arquivo_origem="teste.csv",
            formato_arquivo="CSV",
            conciliado=False
        )
        db.session.add(extrato_dup1)
        
        extrato_dup2 = ExtratoBancario(
            data=datetime(2024, 1, 17),
            descricao="TESTE DUPLICATA - Transação repetida",
            valor=300.00,
            tipo="debito",
            categoria="Teste",
            arquivo_origem="teste.csv",
            formato_arquivo="CSV",
            conciliado=False
        )
        db.session.add(extrato_dup2)
        
        # 4. Transações com valores diferentes (divergência de valor)
        extrato_valor = ExtratoBancario(
            data=datetime(2024, 1, 18),
            descricao="TESTE VALOR DIVERGENTE - Pagamento fornecedor",
            valor=1000.00,
            tipo="debito",
            categoria="Teste",
            arquivo_origem="teste.csv",
            formato_arquivo="CSV",
            conciliado=False
        )
        db.session.add(extrato_valor)
        
        lancamento_valor = LancamentoContabil(
            data=datetime(2024, 1, 18),
            descricao="TESTE VALOR DIFERENTE - Pagamento fornecedor",
            valor=1050.00,  # Valor diferente
            tipo="debito",
            categoria="Teste",
            arquivo_origem="teste.csv",
            conciliado=False
        )
        db.session.add(lancamento_valor)
        
        # 5. Transações com datas diferentes (divergência de data)
        extrato_data = ExtratoBancario(
            data=datetime(2024, 1, 19),
            descricao="TESTE DATA DIVERGENTE - Receita cliente",
            valor=2000.00,
            tipo="credito",
            categoria="Teste",
            arquivo_origem="teste.csv",
            formato_arquivo="CSV",
            conciliado=False
        )
        db.session.add(extrato_data)
        
        lancamento_data = LancamentoContabil(
            data=datetime(2024, 1, 20),  # Data diferente
            descricao="TESTE DATA DIFERENTE - Receita cliente",
            valor=2000.00,
            tipo="credito",
            categoria="Teste",
            arquivo_origem="teste.csv",
            conciliado=False
        )
        db.session.add(lancamento_data)
        
        db.session.commit()
        print("Dados de teste criados com sucesso!")

def verificar_dados_criados():
    """Verifica se os dados foram criados corretamente"""
    print("\nVerificando dados criados:")
    
    with app.app_context():
        extratos = ExtratoBancario.query.filter(ExtratoBancario.descricao.like('%TESTE%')).all()
        lancamentos = LancamentoContabil.query.filter(LancamentoContabil.descricao.like('%TESTE%')).all()
        
        print(f"Extratos criados: {len(extratos)}")
        for e in extratos:
            print(f"  - ID {e.id}: {e.descricao} | R$ {e.valor} | {e.data.strftime('%d/%m/%Y')}")
        
        print(f"Lançamentos criados: {len(lancamentos)}")
        for l in lancamentos:
            print(f"  - ID {l.id}: {l.descricao} | R$ {l.valor} | {l.data.strftime('%d/%m/%Y')}")

def executar_verificacao_divergencias():
    """Executa a verificação de divergências"""
    print("\nExecutando verificação de divergências...")
    
    with app.app_context():
        try:
            divergencias_criadas = verificar_divergencias()
            print(f"Verificação concluída: {divergencias_criadas} divergências criadas")
            
            # Listar divergências encontradas
            divergencias = Divergencia.query.all()
            print(f"\nTotal de divergências no sistema: {len(divergencias)}")
            
            for div in divergencias:
                print(f"  - Tipo: {div.tipo}")
                print(f"    Descrição: {div.descricao}")
                print(f"    Status: {div.status}")
                if div.extrato_id:
                    print(f"    Extrato ID: {div.extrato_id}")
                if div.lancamento_id:
                    print(f"    Lançamento ID: {div.lancamento_id}")
                print("    ---")
                
        except Exception as e:
            print(f"Erro na verificação: {e}")

def main():
    """Função principal do teste"""
    print("=== TESTE DE DETECÇÃO DE DIVERGÊNCIAS ===")
    
    # Configurar logging
    logging.basicConfig(level=logging.INFO)
    
    try:
        # 1. Limpar dados existentes
        limpar_dados_teste()
        
        # 2. Criar dados de teste
        criar_dados_teste()
        
        # 3. Verificar dados criados
        verificar_dados_criados()
        
        # 4. Executar verificação
        executar_verificacao_divergencias()
        
        print("\n=== TESTE CONCLUÍDO ===")
        
    except Exception as e:
        print(f"Erro durante o teste: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())