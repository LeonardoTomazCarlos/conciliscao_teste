#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from app import db, app, Usuario, ContaBancaria, ExtratoBancario, LancamentoContabil
from datetime import datetime

def teste_conexao_db():
    """Testa a conexão com o banco de dados"""
    try:
        with app.app_context():
            print("🔍 Testando conexão com banco de dados...")
            
            # Criar todas as tabelas
            db.create_all()
            print("✅ Tabelas criadas/verificadas com sucesso!")
            
            # Verificar usuários existentes
            usuarios = Usuario.query.all()
            print(f"👥 Usuários no banco: {len(usuarios)}")
            for usuario in usuarios:
                print(f"   - {usuario.username} ({usuario.email}) - Perfil: {usuario.perfil}")
            
            # Verificar contas bancárias
            contas = ContaBancaria.query.all()
            print(f"🏦 Contas bancárias: {len(contas)}")
            
            # Verificar extratos
            extratos = ExtratoBancario.query.all()
            print(f"📊 Registros de extrato: {len(extratos)}")
            
            # Verificar lançamentos
            lancamentos = LancamentoContabil.query.all()
            print(f"📝 Lançamentos contábeis: {len(lancamentos)}")
            
            # Teste de inserção
            print("\n🧪 Testando inserção de dados...")
            
            # Verificar se já existe conta de teste
            conta_teste = ContaBancaria.query.filter_by(banco='Banco Teste').first()
            if not conta_teste:
                conta_teste = ContaBancaria(
                    banco='Banco Teste',
                    agencia='1234',
                    conta='567890',
                    tipo_conta='corrente',
                    saldo_atual=1000.00
                )
                db.session.add(conta_teste)
                db.session.commit()
                print("✅ Conta de teste criada!")
            else:
                print("ℹ️ Conta de teste já existe")
            
            print("\n🎉 CONEXÃO COM BANCO DE DADOS FUNCIONANDO PERFEITAMENTE!")
            print(f"📁 Localização do banco: instance/conciliacao.db")
            print(f"🔧 Tipo: SQLite")
            print(f"⚙️ ORM: SQLAlchemy")
            
    except Exception as e:
        print(f"❌ Erro ao conectar com banco: {e}")
        return False
    
    return True

if __name__ == "__main__":
    teste_conexao_db()
