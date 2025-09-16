#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script para testar especificamente os filtros de conciliação
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app, db, ExtratoBancario, LancamentoContabil
from datetime import datetime, timedelta

def testar_dados_conciliacao():
    """Testa se há dados para conciliação"""
    with app.app_context():
        print("🔍 Testando dados de conciliação...")
        
        # Contar extratos
        total_extratos = ExtratoBancario.query.count()
        print(f"📊 Total de extratos bancários: {total_extratos}")
        
        # Contar lançamentos
        total_lancamentos = LancamentoContabil.query.count()
        print(f"📋 Total de lançamentos contábeis: {total_lancamentos}")
        
        if total_extratos == 0:
            print("⚠️ Não há extratos bancários!")
            criar_dados_exemplo()
            
        if total_lancamentos == 0:
            print("⚠️ Não há lançamentos contábeis!")
            criar_dados_exemplo()
            
        # Mostrar alguns extratos
        extratos = ExtratoBancario.query.limit(5).all()
        print(f"\n📄 Primeiros {len(extratos)} extratos:")
        for e in extratos:
            print(f"  - {e.data} | {e.descricao} | R$ {e.valor}")
            
        # Mostrar alguns lançamentos  
        lancamentos = LancamentoContabil.query.limit(5).all()
        print(f"\n📝 Primeiros {len(lancamentos)} lançamentos:")
        for l in lancamentos:
            print(f"  - {l.data} | {l.descricao} | R$ {l.valor}")

def criar_dados_exemplo():
    """Cria dados de exemplo para teste"""
    with app.app_context():
        print("🔧 Criando dados de exemplo...")
        
        # Criar extratos bancários de exemplo
        hoje = datetime.now().date()
        for i in range(10):
            data = hoje - timedelta(days=i)
            extrato = ExtratoBancario(
                data=data,
                descricao=f"Transação bancária {i+1}",
                valor=100.00 + (i * 10),
                tipo="debito" if i % 2 == 0 else "credito",
                arquivo_origem="exemplo.csv"
            )
            db.session.add(extrato)
            
        # Criar lançamentos contábeis de exemplo
        for i in range(10):
            data = hoje - timedelta(days=i)
            lancamento = LancamentoContabil(
                data=data,
                descricao=f"Lançamento contábil {i+1}",
                valor=100.00 + (i * 10),
                tipo="debito" if i % 2 == 0 else "credito",
                conta_contabil="1.1.01.001",
                arquivo_origem="exemplo.csv"
            )
            db.session.add(lancamento)
            
        db.session.commit()
        print("✅ Dados de exemplo criados!")

def testar_filtros():
    """Testa os filtros de conciliação"""
    with app.app_context():
        print("\n🔍 Testando filtros...")
        
        # Testar filtro por data
        data_inicio = datetime.now() - timedelta(days=7)
        data_fim = datetime.now()
        
        extratos_periodo = ExtratoBancario.query.filter(
            ExtratoBancario.data >= data_inicio,
            ExtratoBancario.data <= data_fim
        ).all()
        
        print(f"📅 Extratos dos últimos 7 dias: {len(extratos_periodo)}")
        
        # Testar filtro por tipo
        extratos_debito = ExtratoBancario.query.filter(
            ExtratoBancario.tipo == "debito"
        ).all()
        
        print(f"📤 Extratos de débito: {len(extratos_debito)}")

def iniciar_servidor_teste():
    """Inicia servidor para teste manual"""
    print("\n🚀 Iniciando servidor para teste manual...")
    print("📍 URL: http://localhost:8080")
    print("🔐 Login: admin / admin123")
    print("📋 Teste os filtros na seção 'Conciliação'")
    print("-" * 50)
    
    app.run(host='0.0.0.0', port=8080, debug=True, use_reloader=False)

if __name__ == '__main__':
    testar_dados_conciliacao()
    testar_filtros()
    
    resposta = input("\n❓ Deseja iniciar o servidor para teste manual? (s/n): ")
    if resposta.lower() in ['s', 'sim', 'y', 'yes']:
        iniciar_servidor_teste()
    else:
        print("✅ Teste concluído!")
