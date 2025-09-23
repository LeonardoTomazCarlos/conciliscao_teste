#!/usr/bin/env python3
"""
Script para testar especificamente os arquivos de divergência criados
"""
import sys
import os

# Adicionar o diretório do sistema ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'sistema concili'))

try:
    from app import db, ExtratoBancario, LancamentoContabil, Divergencia, app, verificar_divergencias
    
    with app.app_context():
        print("🧹 LIMPANDO DADOS EXISTENTES...")
        
        # Limpar tabelas
        Divergencia.query.delete()
        ExtratoBancario.query.delete()
        LancamentoContabil.query.delete()
        db.session.commit()
        
        print("✅ Dados limpos!")
        
        print("\n📤 IMPORTANDO ARQUIVOS DE TESTE...")
        
        # Simular importação manual dos arquivos de teste
        import csv
        from datetime import datetime
        
        # Importar extratos de teste
        with open('sistema concili/extrato_bancario_multiplas_divergencias.csv', 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                extrato = ExtratoBancario(
                    data=datetime.strptime(row['Data'], '%Y-%m-%d').date(),
                    descricao=row['Descrição'],
                    valor=float(row['Valor']),
                    tipo=row['Tipo'],
                    conciliado=False
                )
                db.session.add(extrato)
        
        # Importar lançamentos de teste
        with open('sistema concili/lancamentos_contabeis_multiplas_divergencias.csv', 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                lancamento = LancamentoContabil(
                    data=datetime.strptime(row['Data'], '%Y-%m-%d').date(),
                    descricao=row['Descrição'],
                    valor=float(row['Valor']),
                    tipo=row['Tipo'],
                    conciliado=False
                )
                db.session.add(lancamento)
        
        db.session.commit()
        
        # Verificar dados importados
        extratos = ExtratoBancario.query.all()
        lancamentos = LancamentoContabil.query.all()
        
        print(f"✅ {len(extratos)} extratos importados")
        print(f"✅ {len(lancamentos)} lançamentos importados")
        
        print("\n🔍 DETECTANDO DIVERGÊNCIAS...")
        
        # Executar detecção de divergências
        divergencias_criadas = verificar_divergencias()
        
        # Verificar resultados
        divergencias = Divergencia.query.all()
        
        print(f"✅ {divergencias_criadas} novas divergências criadas")
        print(f"📊 Total de divergências no banco: {len(divergencias)}")
        
        if len(divergencias) > 0:
            print("\n🔍 DIVERGÊNCIAS DETECTADAS:")
            tipos = {}
            for div in divergencias:
                tipo = div.tipo
                if tipo not in tipos:
                    tipos[tipo] = 0
                tipos[tipo] += 1
            
            for tipo, count in tipos.items():
                print(f"   • {tipo}: {count}")
            
            print("\n📋 Detalhes das divergências:")
            for i, div in enumerate(divergencias, 1):
                print(f"   {i}. {div.tipo}: {div.descricao}")
        
        print("\n" + "=" * 60)
        print("🎯 RESULTADO FINAL:")
        print(f"   📊 {len(extratos)} extratos de teste")
        print(f"   📋 {len(lancamentos)} lançamentos de teste")
        print(f"   🔍 {len(divergencias)} divergências detectadas")
        
        if len(divergencias) >= 10:  # Esperamos pelo menos 10-15 divergências dos nossos arquivos
            print("\n✅ SUCESSO! O sistema está detectando as divergências dos arquivos de teste!")
        else:
            print("\n⚠️ ATENÇÃO: Menos divergências detectadas do que esperado.")
            print("   Pode ser necessário ajustar os algoritmos de detecção.")

except Exception as e:
    print(f"❌ Erro: {e}")
    import traceback
    traceback.print_exc()