from app import *

with app.app_context():
    extratos = ExtratoBancario.query.count()
    lancamentos = LancamentoContabil.query.count()
    conciliacoes = Conciliacao.query.count()
    
    print(f"📊 Estado atual do banco:")
    print(f"   - Extratos: {extratos}")
    print(f"   - Lançamentos: {lancamentos}")
    print(f"   - Conciliações: {conciliacoes}")
    
    if extratos == 0 or lancamentos == 0:
        print("\n🔄 Carregando dados dos arquivos de teste...")
        
        # Importar pandas para ler CSVs
        import pandas as pd
        import os
        
        # Verificar se existe arquivo pequeno
        if os.path.exists('teste_extrato_pequeno.csv'):
            print("📂 Carregando teste_extrato_pequeno.csv...")
            df_extrato = pd.read_csv('teste_extrato_pequeno.csv')
            
            for _, row in df_extrato.iterrows():
                extrato = ExtratoBancario(
                    data=pd.to_datetime(row['Data']).date(),
                    valor=float(row['Valor']),
                    descricao=row['Descricao'],
                    documento=row.get('Documento', '')
                )
                db.session.add(extrato)
            
        if os.path.exists('teste_lancamentos_pequeno.csv'):
            print("📂 Carregando teste_lancamentos_pequeno.csv...")
            df_lancamentos = pd.read_csv('teste_lancamentos_pequeno.csv')
            
            for _, row in df_lancamentos.iterrows():
                lancamento = LancamentoContabil(
                    data=pd.to_datetime(row['Data']).date(),
                    valor=float(row['Valor']),
                    descricao=row['Descricao'],
                    categoria=row.get('Categoria', 'Geral')
                )
                db.session.add(lancamento)
        
        try:
            db.session.commit()
            print("✅ Dados carregados com sucesso!")
            
            extratos = ExtratoBancario.query.count()
            lancamentos = LancamentoContabil.query.count()
            print(f"📊 Novo estado:")
            print(f"   - Extratos: {extratos}")
            print(f"   - Lançamentos: {lancamentos}")
            
        except Exception as e:
            db.session.rollback()
            print(f"❌ Erro ao carregar dados: {e}")
    else:
        print("✅ Já existem dados no banco!")
