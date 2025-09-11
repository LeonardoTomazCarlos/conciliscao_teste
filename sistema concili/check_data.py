from app import *

with app.app_context():
    print("=== VERIFICAÇÃO DE DADOS NÃO CONCILIADOS ===")

    # Contar extratos e lançamentos
    total_extratos = ExtratoBancario.query.count()
    total_lancamentos = LancamentoContabil.query.count()
    extratos_conciliados = ExtratoBancario.query.filter_by(conciliado=True).count()
    lancamentos_conciliados = LancamentoContabil.query.filter_by(
        conciliado=True
    ).count()
    extratos_nao_conciliados = ExtratoBancario.query.filter_by(conciliado=False).all()
    lancamentos_nao_conciliados = LancamentoContabil.query.filter_by(
        conciliado=False
    ).all()

    print(f"\nEXTRATOS:")
    print(f"  Total: {total_extratos}")
    print(f"  Conciliados: {extratos_conciliados}")
    print(f"  Não conciliados: {len(extratos_nao_conciliados)}")

    print(f"\nLANÇAMENTOS:")
    print(f"  Total: {total_lancamentos}")
    print(f"  Conciliados: {lancamentos_conciliados}")
    print(f"  Não conciliados: {len(lancamentos_nao_conciliados)}")

    if extratos_nao_conciliados:
        print(f"\nPRIMEIROS 3 EXTRATOS NÃO CONCILIADOS:")
        for i, e in enumerate(extratos_nao_conciliados[:3]):
            print(
                f"  {i+1}. ID: {e.id}, Data: {e.data}, Desc: {e.descricao[:50]}..., Valor: {e.valor}"
            )

    if lancamentos_nao_conciliados:
        print(f"\nPRIMEIROS 3 LANÇAMENTOS NÃO CONCILIADOS:")
        for i, l in enumerate(lancamentos_nao_conciliados[:3]):
            print(
                f"  {i+1}. ID: {l.id}, Data: {l.data}, Desc: {l.descricao[:50]}..., Valor: {l.valor}"
            )

    # Verificar procedimentos
    procedimentos = ProcedimentoConciliacao.query.all()
    print(f"\nPROCEDIMENTOS: {len(procedimentos)}")
    if procedimentos:
        ultimo_proc = procedimentos[-1]
        print(
            f"  Último procedimento: ID {ultimo_proc.id}, Data: {ultimo_proc.data_criacao}"
        )
