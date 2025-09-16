#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Carrega arquivos CSV de teste com divergências, executa a conciliação
e imprime um resumo das divergências detectadas, sem depender do servidor HTTP.
"""

import os
import sys
from datetime import datetime

# Garantir import do app.py (pasta pai de scripts)
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
APP_DIR = os.path.abspath(os.path.join(CURRENT_DIR, os.pardir))
if APP_DIR not in sys.path:
    sys.path.insert(0, APP_DIR)

from app import (
    app,
    db,
    ExtratoBancario,
    LancamentoContabil,
    Conciliacao,
    Divergencia,
    process_csv_file,
    generate_hash,
    executar_processo_conciliacao,
)


def limpar_banco():
    Conciliacao.query.delete()
    Divergencia.query.delete()
    ExtratoBancario.query.delete()
    LancamentoContabil.query.delete()
    db.session.commit()


def importar_csvs(extrato_path: str, lancamentos_path: str):
    """Importa registros de CSV para as tabelas de Extrato e Lançamentos."""
    # Extrato
    regs_extrato = process_csv_file(extrato_path)
    imp_e = 0
    for r in regs_extrato:
        hash_tx = generate_hash(r['descricao'], r['valor'], r['data'], r['tipo'])
        e = ExtratoBancario(
            data=r['data'],
            descricao=r['descricao'],
            valor=r['valor'],
            tipo=r['tipo'],
            categoria=r.get('categoria', 'Não categorizado'),
            arquivo_origem=os.path.basename(extrato_path),
            formato_arquivo='CSV',
            numero_documento=r.get('numero_documento', ''),
            hash_transacao=hash_tx,
        )
        db.session.add(e)
        imp_e += 1

    # Lançamentos
    regs_lct = process_csv_file(lancamentos_path)
    imp_l = 0
    for r in regs_lct:
        hash_tx = generate_hash(r['descricao'], r['valor'], r['data'], r['tipo'])
        l = LancamentoContabil(
            data=r['data'],
            descricao=r['descricao'],
            valor=r['valor'],
            tipo=r['tipo'],
            categoria=r.get('categoria', 'Não categorizado'),
            arquivo_origem=os.path.basename(lancamentos_path),
            numero_documento=r.get('numero_documento', ''),
            centro_custo=r.get('centro_custo', ''),
            conta_contabil=r.get('conta_contabil', ''),
            fornecedor_cliente=r.get('fornecedor_cliente', ''),
            hash_transacao=hash_tx,
        )
        db.session.add(l)
        imp_l += 1

    db.session.commit()
    return imp_e, imp_l


def main():
    base_dir = APP_DIR  # pasta "sistema concili"
    extrato_csv = os.path.join(base_dir, 'extrato_bancario_divergencias_teste.csv')
    lanc_csv = os.path.join(base_dir, 'lancamentos_contabeis_divergencias_teste.csv')

    if not os.path.exists(extrato_csv) or not os.path.exists(lanc_csv):
        print('❌ Arquivos de teste não encontrados:')
        print(f'  - {extrato_csv}')
        print(f'  - {lanc_csv}')
        sys.exit(1)

    with app.app_context():
        print('🧹 Limpando dados anteriores...')
        limpar_banco()

        print('📥 Importando CSVs de teste com divergências...')
        imp_e, imp_l = importar_csvs(extrato_csv, lanc_csv)
        print(f'   - Extratos importados: {imp_e}')
        print(f'   - Lançamentos importados: {imp_l}')

        print('🔄 Executando conciliação...')
        resultado = executar_processo_conciliacao()
        print('📊 Resultado da conciliação:')
        for k in ['conciliadas', 'divergencias', 'nao_encontradas']:
            print(f'   - {k}: {resultado.get(k, 0)}')
        if msg := resultado.get('message'):
            print(f'   - mensagem: {msg}')

        # Resumo de divergências e órfãos
        total_div = Divergencia.query.filter_by(status='pendente').count()
        extratos_orfaos = ExtratoBancario.query.filter_by(conciliado=False).count()
        lanc_orfaos = LancamentoContabil.query.filter_by(conciliado=False).count()

        print('\n🧾 Resumo:')
        print(f'   - Divergências pendentes: {total_div}')
        print(f'   - Extratos não conciliados (órfãos): {extratos_orfaos}')
        print(f'   - Lançamentos não conciliados (órfãos): {lanc_orfaos}')

        # Exibir algumas divergências
        if total_div:
            print('\n🔍 Exemplos de divergências:')
            for d in Divergencia.query.order_by(Divergencia.created_at.desc()).limit(5).all():
                print(f"   - [{d.tipo}] {d.descricao}")

        print('\n✅ Teste finalizado.')


if __name__ == '__main__':
    main()
