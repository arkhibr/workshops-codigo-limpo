"""
gabarito.py — Desconto de fidelidade com suite completa e nova faixa (> 36 meses).

Demonstra:
  (1) Suite de caracterização completa — mid-band E bordas exatas de cada faixa.
  (2) Nova faixa adicionada corretamente (> 36 meses: 20%) sem regressão.
  (3) Todos os casos da suite passam com o código corrigido.

Execute: python3 gabarito.py
"""

from __future__ import annotations

from typing import Optional


# ---------------------------------------------------------------------------
# Constantes de domínio
# ---------------------------------------------------------------------------

DESCONTO_NOVATO     = 0.00   # clientes com menos de 6 meses — sem desconto
DESCONTO_INICIANTE  = 0.05   # clientes de 6 a 11 meses — 5%
DESCONTO_REGULAR    = 0.10   # clientes de 12 a 23 meses — 10%
DESCONTO_FIEL       = 0.15   # clientes de 24 a 36 meses — 15%
DESCONTO_VETERANO   = 0.20   # clientes com mais de 36 meses — 20% (nova faixa)


# ---------------------------------------------------------------------------
# Lógica de desconto (nova faixa adicionada corretamente)
# ---------------------------------------------------------------------------

def calcular_desconto_fidelidade(meses_cliente: int, valor_compra: float) -> float:
    """
    Calcula o desconto de fidelidade com base no tempo como cliente.

    Faixas de fidelidade:
      - até 5 meses: sem desconto (0%)
      - 6 a 11 meses: desconto de 5%
      - 12 a 23 meses: desconto de 10%
      - 24 a 36 meses: desconto de 15%
      - acima de 36 meses: desconto de 20% (nova faixa)

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
    elif meses_cliente <= 36:
        percentual = DESCONTO_FIEL
    else:
        percentual = DESCONTO_VETERANO

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
    if meses_cliente <= 36:
        return "fiel (24 a 36 meses)"
    return "veterano (acima de 36 meses)"


# ---------------------------------------------------------------------------
# Suite COMPLETA de caracterização (inclui bordas exatas)
# ---------------------------------------------------------------------------

def verificar_faixa_novato() -> None:
    """Faixa novato: 0 a 5 meses — sem desconto."""
    casos = [
        (0,  200.00,  0.00, "0 meses — borda inferior (início absoluto)"),
        (3,  200.00,  0.00, "3 meses — faixa novato mid-band"),
        (5,  200.00,  0.00, "5 meses — borda superior faixa novato"),
    ]
    for meses, valor, esperado, descricao in casos:
        obtido = calcular_desconto_fidelidade(meses, valor)
        if abs(obtido - esperado) < 0.001:
            print(f"OK: {descricao}")
        else:
            print(f"FALHOU: {descricao} (esperado {esperado:.2f}, obtido {obtido:.2f})")


def verificar_faixa_iniciante() -> None:
    """Faixa iniciante: 6 a 11 meses — 5% de desconto."""
    casos = [
        (6,  200.00, 10.00, "6 meses — borda inferior faixa iniciante"),
        (9,  200.00, 10.00, "9 meses — faixa iniciante mid-band"),
        (11, 200.00, 10.00, "11 meses — borda superior faixa iniciante"),
    ]
    for meses, valor, esperado, descricao in casos:
        obtido = calcular_desconto_fidelidade(meses, valor)
        if abs(obtido - esperado) < 0.001:
            print(f"OK: {descricao}")
        else:
            print(f"FALHOU: {descricao} (esperado {esperado:.2f}, obtido {obtido:.2f})")


def verificar_faixa_regular() -> None:
    """Faixa regular: 12 a 23 meses — 10% de desconto."""
    casos = [
        (12, 200.00, 20.00, "12 meses — borda inferior faixa regular"),
        (18, 200.00, 20.00, "18 meses — faixa regular mid-band"),
        (23, 200.00, 20.00, "23 meses — borda superior faixa regular"),
    ]
    for meses, valor, esperado, descricao in casos:
        obtido = calcular_desconto_fidelidade(meses, valor)
        if abs(obtido - esperado) < 0.001:
            print(f"OK: {descricao}")
        else:
            print(f"FALHOU: {descricao} (esperado {esperado:.2f}, obtido {obtido:.2f})")


def verificar_faixa_fiel() -> None:
    """Faixa fiel: 24 a 36 meses — 15% de desconto."""
    casos = [
        (24, 200.00, 30.00, "24 meses — borda inferior faixa fiel"),
        (30, 200.00, 30.00, "30 meses — faixa fiel mid-band"),
        (36, 200.00, 30.00, "36 meses — borda superior faixa fiel"),
    ]
    for meses, valor, esperado, descricao in casos:
        obtido = calcular_desconto_fidelidade(meses, valor)
        if abs(obtido - esperado) < 0.001:
            print(f"OK: {descricao}")
        else:
            print(f"FALHOU: {descricao} (esperado {esperado:.2f}, obtido {obtido:.2f})")


def verificar_faixa_veterano() -> None:
    """Faixa veterano: acima de 36 meses — 20% de desconto (nova faixa)."""
    casos = [
        (37, 200.00, 40.00, "37 meses — borda inferior faixa veterano"),
        (48, 200.00, 40.00, "48 meses — faixa veterano mid-band"),
        (60, 200.00, 40.00, "60 meses — faixa veterano extremo"),
    ]
    for meses, valor, esperado, descricao in casos:
        obtido = calcular_desconto_fidelidade(meses, valor)
        if abs(obtido - esperado) < 0.001:
            print(f"OK: {descricao}")
        else:
            print(f"FALHOU: {descricao} (esperado {esperado:.2f}, obtido {obtido:.2f})")


def verificar_entradas_invalidas() -> None:
    """Entradas inválidas devem levantar ValueError."""
    casos_invalidos = [
        (-1,  200.00, "meses negativos"),
        (12,   0.00, "valor de compra zero"),
        (12, -50.00, "valor de compra negativo"),
    ]
    for meses, valor, descricao in casos_invalidos:
        try:
            calcular_desconto_fidelidade(meses, valor)
            print(f"FALHOU: {descricao} — deveria levantar ValueError, mas não levantou")
        except ValueError:
            print(f"OK: {descricao} — ValueError levantado corretamente")


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------

def _demonstrar_descontos() -> None:
    """Demonstra os descontos calculados para todos os perfis de fidelidade."""
    clientes = [
        (3,  500.00),
        (9,  500.00),
        (18, 500.00),
        (30, 500.00),
        (48, 500.00),
    ]

    print("Descontos por fidelidade (valor de compra: R$ 500,00):")
    print(f"  {'Meses':>6}  {'Categoria':<32}  {'Desconto':>10}  {'Valor final':>12}")
    print("  " + "-" * 68)
    for meses, valor in clientes:
        desconto = calcular_desconto_fidelidade(meses, valor)
        categoria = descricao_fidelidade(meses)
        final = valor - desconto
        print(f"  {meses:>6}  {categoria:<32}  R${desconto:>8.2f}  R${final:>10.2f}")
    print()


if __name__ == "__main__":
    print("=== Desconto de Fidelidade — gabarito com suite completa ===\n")

    _demonstrar_descontos()

    print("--- Verificações completas (incluindo bordas e nova faixa) ---")
    verificar_faixa_novato()
    verificar_faixa_iniciante()
    verificar_faixa_regular()
    verificar_faixa_fiel()
    verificar_faixa_veterano()
    verificar_entradas_invalidas()
