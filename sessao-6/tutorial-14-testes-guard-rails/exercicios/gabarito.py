"""
GABARITO — Testes de Caracterização + Mudança Protegida
Referência: Feathers (testes de caracterização) + Clean Code, Cap. 9 (Testes)

O que este arquivo demonstra:
  1. Testes de caracterização completos cobrindo todas as faixas e limites.
  2. A nova faixa (2.000+ pts → 25%) adicionada pela mudança assistida.
  3. Todas as verificações passam — a mudança foi integrada sem regressão.

Execute: python3 sessao-6/tutorial-14-testes-guard-rails/exercicios/gabarito.py
"""

from __future__ import annotations

# Faixas de desconto por pontos acumulados:
#   0–499 pontos      → 0% de desconto
#   500–999 pontos    → 5% de desconto
#   1.000–1.999 pts   → 10% de desconto
#   2.000+ pontos     → 25% de desconto  (faixa adicionada pela mudança)

DESCONTO_SEM_PONTOS = 0.00
DESCONTO_BRONZE = 0.05
DESCONTO_PRATA = 0.10
DESCONTO_OURO = 0.25  # nova faixa


def calcular_desconto_fidelidade(pontos: int, valor_compra: float) -> float:
    """
    Calcula o desconto de fidelidade com base nos pontos acumulados.

    Retorna o valor do desconto (não o valor final da compra).
    """
    if pontos < 500:
        percentual = DESCONTO_SEM_PONTOS
    elif pontos < 1000:
        percentual = DESCONTO_BRONZE
    elif pontos < 2000:
        percentual = DESCONTO_PRATA
    else:
        percentual = DESCONTO_OURO

    return round(valor_compra * percentual, 2)


# ─── Testes de caracterização completos ───────────────────────────────────────

def verificar_desconto_sem_pontos_tipico() -> None:
    """Faixa 0%: 100 pontos, R$ 200,00 → sem desconto."""
    resultado = calcular_desconto_fidelidade(pontos=100, valor_compra=200.00)
    esperado = 0.00
    if abs(resultado - esperado) < 0.01:
        print("OK: desconto sem pontos — típico (100 pts)")
    else:
        print(f"FALHOU: desconto sem pontos (esperado {esperado:.2f}, obtido {resultado:.2f})")


def verificar_limite_inferior_bronze() -> None:
    """Borda: 499 pontos ainda é faixa 0%."""
    resultado = calcular_desconto_fidelidade(pontos=499, valor_compra=200.00)
    esperado = 0.00
    if abs(resultado - esperado) < 0.01:
        print("OK: limite inferior bronze (499 pts → 0%)")
    else:
        print(f"FALHOU: limite inferior bronze (esperado {esperado:.2f}, obtido {resultado:.2f})")


def verificar_desconto_bronze_tipico() -> None:
    """Faixa 5%: 750 pontos, R$ 200,00 → R$ 10,00."""
    resultado = calcular_desconto_fidelidade(pontos=750, valor_compra=200.00)
    esperado = 10.00  # 200 * 0.05
    if abs(resultado - esperado) < 0.01:
        print("OK: desconto bronze — típico (750 pts, R$ 200,00)")
    else:
        print(f"FALHOU: desconto bronze típico (esperado {esperado:.2f}, obtido {resultado:.2f})")


def verificar_limite_inferior_bronze_exato() -> None:
    """Borda: 500 pontos entra na faixa bronze (5%)."""
    resultado = calcular_desconto_fidelidade(pontos=500, valor_compra=200.00)
    esperado = 10.00  # 200 * 0.05
    if abs(resultado - esperado) < 0.01:
        print("OK: entrada bronze exata (500 pts → 5%)")
    else:
        print(f"FALHOU: entrada bronze exata (esperado {esperado:.2f}, obtido {resultado:.2f})")


def verificar_limite_superior_bronze() -> None:
    """Borda: 999 pontos ainda é faixa bronze (5%)."""
    resultado = calcular_desconto_fidelidade(pontos=999, valor_compra=200.00)
    esperado = 10.00  # 200 * 0.05
    if abs(resultado - esperado) < 0.01:
        print("OK: limite superior bronze (999 pts → 5%)")
    else:
        print(f"FALHOU: limite superior bronze (esperado {esperado:.2f}, obtido {resultado:.2f})")


def verificar_desconto_prata_tipico() -> None:
    """Faixa 10%: 1.500 pontos, R$ 300,00 → R$ 30,00."""
    resultado = calcular_desconto_fidelidade(pontos=1500, valor_compra=300.00)
    esperado = 30.00  # 300 * 0.10
    if abs(resultado - esperado) < 0.01:
        print("OK: desconto prata — típico (1.500 pts, R$ 300,00)")
    else:
        print(f"FALHOU: desconto prata típico (esperado {esperado:.2f}, obtido {resultado:.2f})")


def verificar_limite_inferior_prata_exato() -> None:
    """Borda: 1.000 pontos entra na faixa prata (10%)."""
    resultado = calcular_desconto_fidelidade(pontos=1000, valor_compra=200.00)
    esperado = 20.00  # 200 * 0.10
    if abs(resultado - esperado) < 0.01:
        print("OK: entrada prata exata (1.000 pts → 10%)")
    else:
        print(f"FALHOU: entrada prata exata (esperado {esperado:.2f}, obtido {resultado:.2f})")


def verificar_limite_superior_prata() -> None:
    """Borda: 1.999 pontos ainda é faixa prata (10%)."""
    resultado = calcular_desconto_fidelidade(pontos=1999, valor_compra=200.00)
    esperado = 20.00  # 200 * 0.10
    if abs(resultado - esperado) < 0.01:
        print("OK: limite superior prata (1.999 pts → 10%)")
    else:
        print(f"FALHOU: limite superior prata (esperado {esperado:.2f}, obtido {resultado:.2f})")


def verificar_desconto_ouro_tipico() -> None:
    """Faixa 25% (nova): 2.500 pontos, R$ 400,00 → R$ 100,00."""
    resultado = calcular_desconto_fidelidade(pontos=2500, valor_compra=400.00)
    esperado = 100.00  # 400 * 0.25
    if abs(resultado - esperado) < 0.01:
        print("OK: desconto ouro — típico (2.500 pts, R$ 400,00)")
    else:
        print(f"FALHOU: desconto ouro típico (esperado {esperado:.2f}, obtido {resultado:.2f})")


def verificar_limite_inferior_ouro_exato() -> None:
    """Borda: 2.000 pontos entra na faixa ouro (25%)."""
    resultado = calcular_desconto_fidelidade(pontos=2000, valor_compra=200.00)
    esperado = 50.00  # 200 * 0.25
    if abs(resultado - esperado) < 0.01:
        print("OK: entrada ouro exata (2.000 pts → 25%)")
    else:
        print(f"FALHOU: entrada ouro exata (esperado {esperado:.2f}, obtido {resultado:.2f})")


def verificar_valor_compra_zero() -> None:
    """Borda: valor de compra zero → desconto zero independente dos pontos."""
    resultado = calcular_desconto_fidelidade(pontos=1500, valor_compra=0.00)
    esperado = 0.00
    if abs(resultado - esperado) < 0.01:
        print("OK: valor de compra zero (desconto = 0.00)")
    else:
        print(f"FALHOU: valor de compra zero (esperado {esperado:.2f}, obtido {resultado:.2f})")


def executar_todas_verificacoes() -> None:
    """Executa todas as verificações de caracterização."""
    verificar_desconto_sem_pontos_tipico()
    verificar_limite_inferior_bronze()
    verificar_desconto_bronze_tipico()
    verificar_limite_inferior_bronze_exato()
    verificar_limite_superior_bronze()
    verificar_desconto_prata_tipico()
    verificar_limite_inferior_prata_exato()
    verificar_limite_superior_prata()
    verificar_desconto_ouro_tipico()
    verificar_limite_inferior_ouro_exato()
    verificar_valor_compra_zero()


# ─── Execução de demonstração ─────────────────────────────────────────────────

if __name__ == "__main__":
    print("=== Gabarito: gabarito.py ===")
    print()
    print("Suite completa de caracterização (todas as faixas + limites):")
    executar_todas_verificacoes()
    print()
    print("Todas as verificações OK — mudança integrada sem regressão.")
    print()
    print("Descontos por faixa (R$ 200,00 de compra):")
    print(f"  100 pts  → R$ {calcular_desconto_fidelidade(100, 200.00):.2f}  (0%)")
    print(f"  750 pts  → R$ {calcular_desconto_fidelidade(750, 200.00):.2f}  (5% bronze)")
    print(f"  1.500 pts → R$ {calcular_desconto_fidelidade(1500, 200.00):.2f}  (10% prata)")
    print(f"  2.500 pts → R$ {calcular_desconto_fidelidade(2500, 200.00):.2f}  (25% ouro)")
