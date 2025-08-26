from datetime import datetime

def analisar_cnab400(filepath):
    """Analisa a estrutura do arquivo CNAB400"""
    print(f"Analisando arquivo: {filepath}")
    print("=" * 50)
    
    with open(filepath, 'r', encoding='utf-8') as file:
        for i, line in enumerate(file, 1):
            print(f"Linha {i}: {len(line)} caracteres")
            print(f"Conteúdo: {line[:100]}...")
            
            if len(line) >= 400:
                # Analisar estrutura CNAB400
                tipo_registro = line[0]
                print(f"  Tipo de registro: {tipo_registro}")
                
                if tipo_registro == '0':  # Header
                    print("  → HEADER")
                    print(f"    Data: {line[94:100]}")  # Posição da data
                elif tipo_registro == '1':  # Detalhe
                    print("  → DETALHE")
                    print(f"    Nosso número: {line[62:82]}")
                    print(f"    Vencimento: {line[82:88]}")
                    print(f"    Valor: {line[88:101]}")
                    print(f"    Nome: {line[101:141]}")
                elif tipo_registro == '9':  # Trailer
                    print("  → TRAILER")
                    print(f"    Total de registros: {line[394:400]}")
            
            print("-" * 30)

def processar_cnab400_melhorado(filepath):
    """Versão melhorada do processador CNAB400"""
    registros = []
    
    with open(filepath, 'r', encoding='utf-8') as file:
        for line in file:
            if len(line) < 400:
                continue
                
            tipo_registro = line[0]
            
            if tipo_registro == '1':  # Detalhe
                try:
                    # Extrair dados do CNAB400
                    nosso_numero = line[62:82].strip()
                    vencimento_str = line[82:88]
                    valor_str = line[88:101]
                    nome_cliente = line[101:141].strip()
                    
                    # Converter data (DDMMYY)
                    if vencimento_str and vencimento_str != '000000':
                        data = datetime.strptime(vencimento_str, '%d%m%y').date()
                    else:
                        data = datetime.now().date()
                    
                    # Converter valor (em centavos)
                    if valor_str and valor_str.strip() != '0':
                        valor = float(valor_str) / 100
                    else:
                        valor = 0.0
                    
                    if valor > 0:
                        registros.append({
                            'data': data,
                            'descricao': f"Cobrança {nosso_numero} - {nome_cliente}",
                            'valor': valor,
                            'tipo': 'credito',
                            'numero_documento': nosso_numero
                        })
                        
                except Exception as e:
                    print(f"Erro ao processar linha: {e}")
                    continue
    
    return registros

# Testar análise
print("ANÁLISE DOS ARQUIVOS CNAB400")
print("=" * 60)

analisar_cnab400("cnab_arquivo1.ret")
print("\n" + "=" * 60)
analisar_cnab400("cnab_arquivo2.ret")

print("\n" + "=" * 60)
print("PROCESSAMENTO MELHORADO")
print("=" * 60)

# Testar processamento melhorado
registros1 = processar_cnab400_melhorado("cnab_arquivo1.ret")
print(f"Arquivo 1 - Registros encontrados: {len(registros1)}")
for i, reg in enumerate(registros1, 1):
    print(f"  {i}. {reg['data']} - {reg['descricao']} - R$ {reg['valor']:.2f}")

registros2 = processar_cnab400_melhorado("cnab_arquivo2.ret")
print(f"\nArquivo 2 - Registros encontrados: {len(registros2)}")
for i, reg in enumerate(registros2, 1):
    print(f"  {i}. {reg['data']} - {reg['descricao']} - R$ {reg['valor']:.2f}")
