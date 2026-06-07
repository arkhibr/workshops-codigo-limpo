"""
exercicio.py — Cálculo de desconto de fidelidade por faixas de tempo.

Código funcional sem testes de caracterização.
Tarefa:
  (1) Escreva os testes de caracterização incluindo as bordas exatas de cada faixa.
  (2) Só então peça à IA que adicione uma nova faixa (clientes > 36 meses: 20%).
  (3) Rode a suite antes e depois — compare os resultados.

Execute: python3 exercicio.py
"""

from __future__ import annotations

from typing import Optional


# ---------------------------------------------------------------------------
# Constantes de domínio
# ---------------------------------------------------------------------------

DESCONTO_NOVATO     = 0.00   # clientes com menos de 6 meses — sem desconto
DESCONTO_INICIANTE  = 0.05   # clientes de 6 a 11 meses — 5%
DESCONTO_REGULAR    = 0.10   # clientes de 12 a 23 meses — 10%
DESCONTO_FIEL       = 0.15   # clientes com 24 meses ou mais — 15%


# ---------------------------------------------------------------------------
# Lógica de desconto
# ---------------------------------------------------------------------------

def calcular_desconto_fidelidade(meses_cliente: int, valor_compra: float) -> float:
    """
    Calcula o desconto de fidelidade com base no tempo como cliente.

    Faixas de fidelidade:
      - até 5 meses: sem desconto (0%)
      - 6 a 11 meses: desconto de 5%
      - 12 a 23 meses: desconto de 10%
      - 24 meses ou mais: desconto de 15%

    Retorna o valor do desconto em reais (não o valor final da compra).
    """
    if meses_cliente < 0:
        raise ValueError(f"meses_cliente inválido: {meses_cliente}. Deve ser zero ou maior.")
    if valor_compra <= 0:
        raise ValueError(f"valor_compra inválido: {valor_compra}. Deve ser maior que zero.")

    if meses_cliente < 6:
        percentual = DESCONTO_NOVATO
    elif meses_cliente < 12:
        percentual = DESCONTO_INICIANTE
    elif meses_cliente < 24:
        percentual = DESCONTO_REGULAR
    else:
        percentual = DESCONTO_FIEL

    desconto = valor_compra * percentual
    return round(desconto, 2)


def descricao_fidelidade(meses_cliente: int) -> str:
    """Retorna a categoria de fidelidade do cliente."""
    if meses_cliente < 0:
        return "inválido"
    if meses_cliente < 6:
        return "novato (até 5 meses)"
    if meses_cliente < 12:
        return "iniciante (6 a 11 meses)"
    if meses_cliente < 24:
        return "regular (12 a 23 meses)"
    return "fiel (24 meses ou mais)"


# ---------------------------------------------------------------------------
# Demo — comportamento atual sem testes de caracterização
# ---------------------------------------------------------------------------

def _demonstrar_descontos() -> None:
    """Demonstra os descontos calculados para diferentes perfis de cliente."""
    clientes = [
        (3,  200.00, "cliente novo"),
        (9,  200.00, "cliente iniciante"),
        (18, 200.00, "cliente regular"),
        (30, 200.00, "cliente fiel"),
    ]

    print("Descontos por fidelidade (valor de compra: R$ 200,00):")
    print(f"  {'Meses':>6}  {'Categoria':<28}  {'Desconto':>10}  {'Valor final':>12}")
    print("  " + "-" * 64)
    for meses, valor, rotulo in clientes:
        desconto = calcular_desconto_fidelidade(meses, valor)
        categoria = descricao_fidelidade(meses)
        final = valor - desconto
        print(f"  {meses:>6}  {categoria:<28}  R${desconto:>8.2f}  R${final:>10.2f}")
    print()

    print("Dica para o exercício: quais valores de 'meses_cliente' são as fronteiras")
    print("exatas entre as faixas? Esses são os casos que a sua suite precisa cobrir.")
    print()


if __name__ == "__main__":
    print("=== Desconto de Fidelidade — exercício de caracterização ===\n")

    _demonstrar_descontos()

    print("TODO: escreva as funções verificar_*() cobrindo mid-band E bordas exatas.")
    print("Fronteiras a cobrir: 5/6, 11/12 e 23/24 meses.")
    print("Só depois de ter a suite passando, peça à IA que adicione a faixa > 36 meses.")
