from datetime import datetime

def gerar_cnab400(nome_arquivo, transacoes, numero_inicial_lote=1):
    linhas = []

    # Header
    data_hoje = datetime.today().strftime("%d%m%Y")
    header = (
        f"01REMESSA01COBRANCA       12345678901234567890NOME DA EMPRESA         "
        f"001BANCO EXEMPLO       {data_hoje}                                                                                          "
        f"{str(numero_inicial_lote).zfill(6)}"
    )
    linhas.append(header)

    # Detalhes
    for i, transacao in enumerate(transacoes, start=2):
        segmento = (
            f"1"  # Código do registro
            f"025"  # Código da agência
            f"{transacao['conta'].zfill(15)}"
            f"{transacao['nosso_numero'].zfill(20)}"
            f"{transacao['vencimento']}"  # Data de vencimento
            f"{str(int(transacao['valor'] * 100)).zfill(13)}"
            f"{transacao['nome_cliente'][:40].ljust(40)}"
            + "0" * 247 + f"{str(i).zfill(6)}"
        )
        linhas.append(segmento)

    # Trailer
    trailer = "9".ljust(393) + f"{str(len(linhas)).zfill(6)}"
    linhas.append(trailer)

    # Salvar arquivo
    with open(nome_arquivo, "w", encoding="utf-8") as f:
        for linha in linhas:
            f.write(linha[:400].ljust(400) + "\n")  # Linha com exatamente 400 caracteres

    print(f"Arquivo gerado: {nome_arquivo}")

# Exemplo de uso
transacoes_arquivo1 = [
    {"conta": "1234567890", "nosso_numero": "123456", "vencimento": "250825", "valor": 100.00, "nome_cliente": "CLIENTE UM"},
    {"conta": "1234567890", "nosso_numero": "123457", "vencimento": "250825", "valor": 50.00, "nome_cliente": "CLIENTE DOIS"},
]

transacoes_arquivo2 = [
    {"conta": "1234567890", "nosso_numero": "123456", "vencimento": "250825", "valor": 100.00, "nome_cliente": "CLIENTE UM"},  # Igual
    {"conta": "1234567890", "nosso_numero": "123458", "vencimento": "250825", "valor": 75.00, "nome_cliente": "CLIENTE TRES"},  # Novo
]

gerar_cnab400("cnab_arquivo1.ret", transacoes_arquivo1, 1)
gerar_cnab400("cnab_arquivo2.ret", transacoes_arquivo2, 2)
