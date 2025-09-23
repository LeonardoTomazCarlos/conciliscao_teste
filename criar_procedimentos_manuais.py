#!/usr/bin/env python3
"""Script para criar procedimentos manuais de teste"""
import sys
import os

# Adicionar o diretório do sistema ao path
sys.path.append(os.path.join(os.path.dirname(__file__), 'sistema concili'))

from app import app, db, ProcedimentoConciliacao, Usuario
from datetime import datetime
import uuid

def criar_procedimentos_manuais():
    """Criar alguns procedimentos manuais para teste"""
    with app.app_context():
        print("🔧 CRIANDO PROCEDIMENTOS MANUAIS DE TESTE...")
        print("=" * 50)
        
        # Buscar um usuário admin
        admin_user = Usuario.query.filter_by(perfil='admin').first()
        if not admin_user:
            print("❌ Nenhum usuário admin encontrado! Criando um...")
            admin_user = Usuario(
                username='admin_test',
                email='admin@test.com',
                perfil='admin',
                ativo=True
            )
            admin_user.set_password('admin123')
            db.session.add(admin_user)
            db.session.commit()
            print(f"✅ Usuário admin criado: {admin_user.username}")
        
        # Criar 3 procedimentos manuais
        procedimentos_criados = []
        
        for i in range(3):
            proc_uuid = str(uuid.uuid4())
            procedimento = ProcedimentoConciliacao(
                uuid=proc_uuid,
                tipo_procedimento='Conciliação',
                metodo='manual',  # MÉTODO MANUAL
                status='concluido' if i < 2 else 'em_andamento',
                data_criacao=datetime.now(),
                usuario_id=admin_user.id,
                descricao=f'Procedimento manual de teste #{i+1}',
                total_conciliacoes=10 + i * 5,
                valor_total=1000.00 + (i * 500.00)
            )
            
            db.session.add(procedimento)
            procedimentos_criados.append(procedimento)
            print(f"✅ Criado procedimento manual {i+1}: {proc_uuid}")
        
        # Criar 1 procedimento com método diferente para teste
        proc_uuid = str(uuid.uuid4())
        procedimento_interativo = ProcedimentoConciliacao(
            uuid=proc_uuid,
            tipo_procedimento='Conciliação',
            metodo='interativo',  # MÉTODO DIFERENTE
            status='concluido',
            data_criacao=datetime.now(),
            usuario_id=admin_user.id,
            descricao='Procedimento interativo de teste',
            total_conciliacoes=5,
            valor_total=750.00
        )
        
        db.session.add(procedimento_interativo)
        procedimentos_criados.append(procedimento_interativo)
        print(f"✅ Criado procedimento interativo: {proc_uuid}")
        
        # Salvar na base de dados
        db.session.commit()
        
        print("\n" + "=" * 50)
        print(f"✅ SUCESSO! {len(procedimentos_criados)} procedimentos criados.")
        
        # Verificar se foram criados
        manual_count = ProcedimentoConciliacao.query.filter_by(metodo='manual').count()
        interativo_count = ProcedimentoConciliacao.query.filter_by(metodo='interativo').count()
        auto_count = ProcedimentoConciliacao.query.filter_by(metodo='automatico').count()
        
        print(f"📊 Contagem atual na base de dados:")
        print(f"   • Automáticos: {auto_count}")
        print(f"   • Manuais: {manual_count}")
        print(f"   • Interativos: {interativo_count}")
        
        return procedimentos_criados

if __name__ == '__main__':
    try:
        criar_procedimentos_manuais()
        print("\n🎉 Agora você pode testar o filtro 'Manual' na aplicação!")
    except Exception as e:
        print(f"❌ Erro ao criar procedimentos: {e}")
        import traceback
        traceback.print_exc()