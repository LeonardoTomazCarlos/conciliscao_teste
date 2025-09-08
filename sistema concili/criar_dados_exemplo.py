#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para criar dados de exemplo para testar os filtros de conciliação
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app, db, ProcedimentoConciliacao, Usuario
from datetime import datetime, timedelta
import random

def criar_dados_exemplo():
    """Cria dados de exemplo para testar os filtros"""
    
    with app.app_context():
        print("🔧 Criando dados de exemplo para teste dos filtros...")
        
        # Verificar se existe pelo menos um usuário
        usuario = Usuario.query.first()
        if not usuario:
            print("❌ Nenhum usuário encontrado. Execute o sistema primeiro.")
            return
        
        # Limpar procedimentos existentes (opcional)
        resposta = input("🗑️  Limpar procedimentos existentes? (s/N): ")
        if resposta.lower() == 's':
            ProcedimentoConciliacao.query.delete()
            db.session.commit()
            print("✅ Procedimentos existentes removidos")
        
        # Criar procedimentos de exemplo
        tipos = ['automatico', 'manual', 'parcial']
        status_opcoes = ['em_andamento', 'concluido', 'erro', 'cancelado']
        metodos = ['data_valor', 'data_valor_descricao', 'valor_descricao']
        
        procedimentos_criados = 0
        
        # Criar procedimentos dos últimos 60 dias
        for i in range(20):
            # Data aleatória nos últimos 60 dias
            dias_atras = random.randint(0, 60)
            data_criacao = datetime.now() - timedelta(days=dias_atras)
            
            # Valores aleatórios
            tipo = random.choice(tipos)
            status = random.choice(status_opcoes)
            metodo = random.choice(metodos)
            
            # Estatísticas aleatórias
            total_extratos = random.randint(5, 100)
            total_lancamentos = random.randint(5, 100)
            conciliados = random.randint(0, min(total_extratos, total_lancamentos))
            divergencias = random.randint(0, 10)
            
        procedimento = ProcedimentoConciliacao(
            usuario_id=usuario.id,
            uuid=f"proc-{i+1:04d}",
            tipo_procedimento=tipo,
            metodo=metodo,
            status=status,
            descricao=f"Procedimento de exemplo {i+1}",
            total_conciliacoes=conciliados,
            valor_total=round(random.uniform(1000, 50000), 2),
            observacoes=f"Procedimento de exemplo {i+1} - Tipo: {tipo}, Status: {status}"
        )
        
        db.session.add(procedimento)
        procedimentos_criados += 1
        
        # Commit das mudanças
        try:
            db.session.commit()
            print(f"✅ {procedimentos_criados} procedimentos de exemplo criados com sucesso!")
            
            # Mostrar estatísticas
            print("\n📊 Estatísticas dos dados criados:")
            for tipo in tipos:
                count = ProcedimentoConciliacao.query.filter_by(tipo_procedimento=tipo).count()
                print(f"   - {tipo}: {count} procedimentos")
            
            print("\n📊 Status dos procedimentos:")
            for status in status_opcoes:
                count = ProcedimentoConciliacao.query.filter_by(status=status).count()
                print(f"   - {status}: {count} procedimentos")
            
            total = ProcedimentoConciliacao.query.count()
            print(f"\n🎯 Total de procedimentos no banco: {total}")
            
        except Exception as e:
            db.session.rollback()
            print(f"❌ Erro ao criar dados de exemplo: {e}")

def listar_procedimentos():
    """Lista os procedimentos existentes"""
    
    with app.app_context():
        procedimentos = ProcedimentoConciliacao.query.order_by(ProcedimentoConciliacao.created_at.desc()).all()
        
        print(f"\n📋 Procedimentos existentes ({len(procedimentos)}):")
        print("-" * 80)
        
        for proc in procedimentos[:10]:  # Mostrar apenas os 10 mais recentes
            print(f"ID: {proc.id:3d} | {proc.created_at.strftime('%Y-%m-%d %H:%M')} | "
                  f"{proc.tipo_procedimento:10s} | {proc.status:12s} | "
                  f"Conciliações:{proc.total_conciliacoes:3d} | Valor: R$ {float(proc.valor_total):8.2f}")
        
        if len(procedimentos) > 10:
            print(f"... e mais {len(procedimentos) - 10} procedimentos")

if __name__ == "__main__":
    print("🧪 SCRIPT DE DADOS DE EXEMPLO PARA FILTROS\n")
    
    # Executa automaticamente
    print("Criando dados de exemplo...")
    criar_dados_exemplo()
    print("\nListando procedimentos existentes...")
    listar_procedimentos()
