from app import *

with app.app_context():
    print("=== CRIANDO DIVERGÊNCIAS DE EXEMPLO ===")

    # Buscar alguns extratos e lançamentos não conciliados
    extratos = ExtratoBancario.query.filter_by(conciliado=False).limit(3).all()
    lancamentos = LancamentoContabil.query.filter_by(conciliado=False).limit(3).all()

    print(f"Extratos disponíveis: {len(extratos)}")
    print(f"Lançamentos disponíveis: {len(lancamentos)}")

    # Criar divergências de exemplo
    if extratos:
        # Divergência de valor
        div1 = Divergencia(
            tipo="valor_incorreto",
            extrato_id=extratos[0].id,
            descricao=f"Diferença de valor: esperado R$ {float(extratos[0].valor) + 100:.2f}, encontrado R$ {extratos[0].valor}",
            status="pendente",
        )
        db.session.add(div1)

        if len(extratos) > 1:
            # Divergência de duplicata
            div2 = Divergencia(
                tipo="duplicata",
                extrato_id=extratos[1].id,
                descricao=f"Possível lançamento duplicado encontrado no extrato",
                status="pendente",
            )
            db.session.add(div2)

    if lancamentos:
        # Divergência de lançamento órfão
        div3 = Divergencia(
            tipo="lancamento_orfao",
            lancamento_id=lancamentos[0].id,
            descricao=f"Lançamento sem correspondência no extrato bancário",
            status="pendente",
        )
        db.session.add(div3)

        if len(lancamentos) > 1:
            # Divergência de categoria
            div4 = Divergencia(
                tipo="categoria_incorreta",
                lancamento_id=lancamentos[1].id,
                descricao=f"Categoria do lançamento não corresponde ao padrão esperado",
                status="pendente",
            )
            db.session.add(div4)

    try:
        db.session.commit()
        print("✅ Divergências criadas com sucesso!")

        # Verificar quantas divergências existem agora
        total_div = Divergencia.query.count()
        pendentes = Divergencia.query.filter_by(status="pendente").count()
        print(f"Total de divergências: {total_div}")
        print(f"Divergências pendentes: {pendentes}")

    except Exception as e:
        db.session.rollback()
        print(f"❌ Erro ao criar divergências: {e}")
