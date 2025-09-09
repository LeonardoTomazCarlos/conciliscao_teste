from flask import Flask, jsonify
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

@app.route('/api/conciliacao/executar', methods=['POST'])
def test_conciliacao():
    """Teste simples da rota de conciliação"""
    try:
        logging.info("🔄 Teste de conciliação iniciado")
        
        # Simulação simples
        resultado = {
            'conciliadas': 0,
            'divergencias': 0, 
            'nao_encontradas': 0,
            'message': 'Não há dados para conciliar. Faça upload de extratos e lançamentos primeiro.'
        }
        
        logging.info(f"✅ Resultado: {resultado}")
        
        return jsonify({
            'success': True,
            'message': 'Teste executado com sucesso',
            **resultado
        })
        
    except Exception as e:
        logging.error(f"❌ Erro no teste: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    print("Servidor de teste iniciado em http://localhost:8080")
    app.run(debug=True, host='0.0.0.0', port=8080)
