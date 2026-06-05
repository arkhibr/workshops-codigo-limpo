"""
SAÍDA TÍPICA DE IA — cálculo de preço com descontos (a partir de prompt fraco)
Referência: Clean Code, Cap. 2–3; engenharia de contexto em prompts de código

⚠️  Este arquivo é INTENCIONALMENTE IMPERFEITO.
    Representa o tipo de código que uma IA gera a partir de um prompt vago.
    Analise os problemas antes de ver a versão revisada.

Execute: python3 sessao-5/tutorial-09-engenharia-de-prompt/exemplos/preco_gerado.py
"""

# Prompt usado: "calcula o preço com desconto"


def calc(x, y, q):  # o que é x? y? q?
    # aplica desconto
    if q >= 5:
        x = x * 0.9  # número mágico — por que 0.9? o que representa?
    if y == "premium":
        x = x * 0.85  # outro número mágico — acumula com o anterior?
    total = x * q
    return round(total, 2)


def get_preco(items):  # nome em inglês; "items" — lista de quê?
    result = 0
    for i in items:
        # i[0] = preco, i[1] = categoria, i[2] = quantidade
        result += calc(i[0], i[1], i[2])  # acessa por índice — frágil
    return result


# ─── Execução de demonstração ─────────────────────────────────────────────────

if __name__ == "__main__":
    # item simples: preço 50.0, categoria "padrao", quantidade 3
    p1 = calc(50.0, "padrao", 3)
    print("Preço item 1 (sem desconto):", p1)

    # item com desconto por volume: quantidade 6
    p2 = calc(50.0, "padrao", 6)
    print("Preço item 2 (desconto volume):", p2)

    # item premium com volume: qual desconto prevalece?
    p3 = calc(50.0, "premium", 6)
    print("Preço item 3 (premium + volume, acumulados):", p3)

    # pedido com múltiplos itens
    pedido = [
        (50.0, "padrao", 3),
        (80.0, "premium", 2),
        (30.0, "padrao", 5),
    ]
    total = get_preco(pedido)
    print("\nTotal do pedido:", total)
