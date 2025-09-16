#!/usr/bin/env python3
"""
Script para forçar a detecção de divergências
"""

import os
import sys
from datetime import datetime

# Adicionar o diretório do app ao path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def executar_deteccao_forcada():
    """Executa detecção forçada de divergências"""
    
    print("🔧 DETECÇÃO FORÇADA DE DIVERGÊNCIAS")
    print("="*50)
    
    try:
        from app import app, db, Divergencia, ExtratoBancario, LancamentoContabil, Conciliacao
        from sqlalchemy import func
        
        with app.app_context():
            print("✅ Contexto da aplicação carregado")
            
            # Limpar divergências antigas
            print("🧹 Limpando divergências antigas...")
            divergencias_antigas = Divergencia.query.count()
            Divergencia.query.delete()
            db.session.commit()
            print(f"   Removidas {divergencias_antigas} divergências antigas")
            
            # 1. Detectar extratos órfãos
            print("\n🔍 Detectando extratos órfãos...")
            extratos_orfaos = ExtratoBancario.query.filter(
                ~ExtratoBancario.conciliacoes.any()
            ).all()
            
            print(f"   Encontrados {len(extratos_orfaos)} extratos órfãos")
            
            for extrato in extratos_orfaos:
                divergencia = Divergencia(
                    tipo='extrato_orfao',
                    extrato_id=extrato.id,
                    descricao=f'Extrato sem lançamento: {extrato.descricao} - R$ {extrato.valor} (Data: {extrato.data})',
                    status='pendente'
                )
                db.session.add(divergencia)
                print(f"   Criada divergência: ID {extrato.id} - {extrato.descricao[:50]}...")
            
            # 2. Detectar lançamentos órfãos
            print("\n🔍 Detectando lançamentos órfãos...")
            lancamentos_orfaos = LancamentoContabil.query.filter(
                ~LancamentoContabil.conciliacoes.any()
            ).all()
            
            print(f"   Encontrados {len(lancamentos_orfaos)} lançamentos órfãos")
            
            for lancamento in lancamentos_orfaos:
                divergencia = Divergencia(
                    tipo='lancamento_orfao',
                    lancamento_id=lancamento.id,
                    descricao=f'Lançamento sem extrato: {lancamento.descricao} - R$ {lancamento.valor} (Data: {lancamento.data})',
                    status='pendente'
                )
                db.session.add(divergencia)
                print(f"   Criada divergência: ID {lancamento.id} - {lancamento.descricao[:50]}...")
            
            # 3. Detectar diferenças de valor nas conciliações
            print("\n🔍 Detectando diferenças de valor...")
            conciliacoes = Conciliacao.query.filter_by(status='ativa').all()
            
            diferencas_encontradas = 0
            for conciliacao in conciliacoes:
                diferenca = abs(conciliacao.extrato.valor - conciliacao.lancamento.valor)
                if diferenca > 0.01:
                    divergencia = Divergencia(
                        tipo='diferenca_valor',
                        extrato_id=conciliacao.extrato_id,
                        lancamento_id=conciliacao.lancamento_id,
                        descricao=f'Diferença de valor: Extrato R$ {conciliacao.extrato.valor} vs Lançamento R$ {conciliacao.lancamento.valor} (Diferença: R$ {diferenca:.2f})',
                        status='pendente'
                    )
                    db.session.add(divergencia)
                    diferencas_encontradas += 1
                    print(f"   Diferença encontrada: R$ {diferenca:.2f}")
            
            print(f"   Total de diferenças: {diferencas_encontradas}")
            
            # 4. Detectar duplicatas no extrato
            print("\n🔍 Detectando duplicatas no extrato...")
            duplicatas_extrato = 0
            extratos = ExtratoBancario.query.all()
            
            for extrato in extratos:
                duplicatas = ExtratoBancario.query.filter(
                    ExtratoBancario.descricao == extrato.descricao,
                    ExtratoBancario.valor == extrato.valor,
                    ExtratoBancario.data == extrato.data,
                    ExtratoBancario.id != extrato.id
                ).all()
                
                if duplicatas:
                    # Verificar se já foi criada divergência para este extrato
                    divergencia_existente = Divergencia.query.filter_by(
                        tipo='duplicata',
                        extrato_id=extrato.id
                    ).first()
                    
                    if not divergencia_existente:
                        divergencia = Divergencia(
                            tipo='duplicata',
                            extrato_id=extrato.id,
                            descricao=f'Duplicata no extrato: {extrato.descricao} - R$ {extrato.valor} (Encontradas {len(duplicatas)} transações idênticas)',
                            status='pendente'
                        )
                        db.session.add(divergencia)
                        duplicatas_extrato += 1
                        print(f"   Duplicata: {extrato.descricao[:50]}...")
            
            print(f"   Total de duplicatas no extrato: {duplicatas_extrato}")
            
            # 5. Detectar duplicatas nos lançamentos
            print("\n🔍 Detectando duplicatas nos lançamentos...")
            duplicatas_lancamento = 0
            lancamentos = LancamentoContabil.query.all()
            
            for lancamento in lancamentos:
                duplicatas = LancamentoContabil.query.filter(
                    LancamentoContabil.descricao == lancamento.descricao,
                    LancamentoContabil.valor == lancamento.valor,
                    LancamentoContabil.data == lancamento.data,
                    LancamentoContabil.id != lancamento.id
                ).all()
                
                if duplicatas:
                    # Verificar se já foi criada divergência para este lançamento
                    divergencia_existente = Divergencia.query.filter_by(
                        tipo='duplicata',
                        lancamento_id=lancamento.id
                    ).first()
                    
                    if not divergencia_existente:
                        divergencia = Divergencia(
                            tipo='duplicata',
                            lancamento_id=lancamento.id,
                            descricao=f'Duplicata no lançamento: {lancamento.descricao} - R$ {lancamento.valor} (Encontradas {len(duplicatas)} transações idênticas)',
                            status='pendente'
                        )
                        db.session.add(divergencia)
                        duplicatas_lancamento += 1
                        print(f"   Duplicata: {lancamento.descricao[:50]}...")
            
            print(f"   Total de duplicatas nos lançamentos: {duplicatas_lancamento}")
            
            # Salvar todas as divergências
            print("\n💾 Salvando divergências...")
            db.session.commit()
            
            # Contar total de divergências criadas
            total_divergencias = Divergencia.query.count()
            print(f"✅ Total de divergências criadas: {total_divergencias}")
            
            # Listar resumo das divergências por tipo
            print("\n📊 RESUMO POR TIPO:")
            tipos = db.session.query(Divergencia.tipo, func.count(Divergencia.id)).group_by(Divergencia.tipo).all()
            for tipo, quantidade in tipos:
                print(f"   {tipo}: {quantidade}")
            
            return total_divergencias
            
    except Exception as e:
        print(f"❌ Erro na detecção: {e}")
        import traceback
        traceback.print_exc()
        return 0

if __name__ == "__main__":
    total = executar_deteccao_forcada()
    print(f"\n🎯 RESULTADO: {total} divergências detectadas e salvas!")