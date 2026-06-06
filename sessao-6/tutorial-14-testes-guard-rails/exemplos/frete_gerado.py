"""
SAÍDA TÍPICA DE IA — cálculo de frete com faixas de peso (mudança assistida sem proteção)
Referência: Feathers (testes de caracterização) + Clean Code, Cap. 9 (Testes)

⚠️  Este arquivo é INTENCIONALMENTE IMPERFEITO.
    A mudança assistida adicionou a faixa acima de 15 kg, mas deslocou
    o limite entre a faixa 2 e a faixa 3: pedidos de 10,01–15 kg que
    antes custavam R$ 1,80/kg + R$ 3,00 agora caem na faixa mais barata.
    A regressão é silenciosa porque a suite só cobre casos "felizes"
    (um por faixa) e NENHUM deles está na zona afetada.
    Todas as verificações imprimem OK — mas o valor está errado para
    pedidos entre 10 kg e 15 kg.

Execute: python3 sessao-6/tutorial-14-testes-guard-rails/exemplos/frete_gerado.py
"""

# Faixas originais (antes da mudança assistida):
#   até 5 kg      → R$ 2,00/kg
#   5,01–10 kg    → R$ 1,80/kg + R$ 3,00 fixo
#   acima de 10 kg → R$ 1,50/kg + R$ 5,00 fixo
#
# Prompt usado para a mudança:
#   "Adiciona faixa acima de 15 kg com R$ 1,20/kg + R$ 8,00 fixo."
#
# A IA adicionou a nova faixa mas usou "> 15" onde deveria ser "> 10"
# para a faixa intermediária — deslocando o limite silenciosamente.

DISTANCIA_BASE_KM = 100.0  # distância de referência para normalização


def calcular_frete(peso: float, distancia: float) -> float:
    """
    Calcula o frete com base no peso (kg) e na distância (km).
    O resultado é proporcional à distância em relação à base de 100 km.

    ⚠️ REGRESSÃO INTRODUZIDA PELA MUDANÇA ASSISTIDA:
    O limite entre faixa 2 e faixa 3 foi deslocado de 10 kg para 15 kg.
    Pedidos de 10,01–15 kg recebem valor incorreto (mais barato do que deveriam).
    """
    fator_distancia = distancia / DISTANCIA_BASE_KM

    if peso <= 5.0:
        # Faixa 1 — intacta
        valor_base = peso * 2.00
    elif peso <= 15.0:
        # Faixa 2 — REGRESSÃO: deveria ser "peso <= 10.0"
        # Pedidos 10,01–15 kg caem aqui em vez de na faixa 3
        valor_base = peso * 1.80 + 3.00
    elif peso <= 30.0:
        # Faixa 3 — deslocada pela mudança (era "acima de 10 kg")
        valor_base = peso * 1.50 + 5.00
    else:
        # Faixa 4 — nova faixa adicionada pela mudança assistida
        valor_base = peso * 1.20 + 8.00

    return round(valor_base * fator_distancia, 2)


# ─── Suite fraca: apenas caminhos felizes ─────────────────────────────────────
# Cobre apenas um caso por faixa — nenhum está na zona 10–15 kg afetada.

def verificar_frete_faixa1() -> None:
    """Faixa 1: peso de 3 kg, distância de 100 km."""
    resultado = calcular_frete(peso=3.0, distancia=100.0)
    esperado = 6.00  # 3 * 2.00 * (100/100)
    if abs(resultado - esperado) < 0.01:
        print("OK: frete faixa 1 (3 kg, 100 km)")
    else:
        print(f"FALHOU: frete faixa 1 (esperado {esperado}, obtido {resultado})")


def verificar_frete_faixa2() -> None:
    """Faixa 2: peso de 8 kg, distância de 100 km."""
    resultado = calcular_frete(peso=8.0, distancia=100.0)
    esperado = 17.40  # 8 * 1.80 + 3.00 = 17.40, * 1.0
    if abs(resultado - esperado) < 0.01:
        print("OK: frete faixa 2 (8 kg, 100 km)")
    else:
        print(f"FALHOU: frete faixa 2 (esperado {esperado}, obtido {resultado})")


def verificar_frete_faixa3() -> None:
    """Faixa 3: peso de 20 kg, distância de 100 km — caso feliz, não afetado."""
    resultado = calcular_frete(peso=20.0, distancia=100.0)
    esperado = 35.00  # 20 * 1.50 + 5.00 = 35.00, * 1.0
    if abs(resultado - esperado) < 0.01:
        print("OK: frete faixa 3 (20 kg, 100 km)")
    else:
        print(f"FALHOU: frete faixa 3 (esperado {esperado}, obtido {resultado})")


def verificar_frete_faixa4() -> None:
    """Faixa 4 (nova): peso de 40 kg, distância de 100 km."""
    resultado = calcular_frete(peso=40.0, distancia=100.0)
    esperado = 56.00  # 40 * 1.20 + 8.00 = 56.00, * 1.0
    if abs(resultado - esperado) < 0.01:
        print("OK: frete faixa 4 (40 kg, 100 km)")
    else:
        print(f"FALHOU: frete faixa 4 (esperado {esperado}, obtido {resultado})")


# ─── Execução de demonstração ─────────────────────────────────────────────────

if __name__ == "__main__":
    print("=== Demonstração: frete_gerado.py ===")
    print()
    print("Cálculos (caminho feliz):")
    print(f"  3 kg, 100 km  → R$ {calcular_frete(3.0, 100.0):.2f}")
    print(f"  8 kg, 100 km  → R$ {calcular_frete(8.0, 100.0):.2f}")
    print(f"  20 kg, 100 km → R$ {calcular_frete(20.0, 100.0):.2f}")
    print(f"  40 kg, 100 km → R$ {calcular_frete(40.0, 100.0):.2f}")
    print()
    print("Verificações (suite fraca — apenas caminho feliz):")
    verificar_frete_faixa1()
    verificar_frete_faixa2()
    verificar_frete_faixa3()
    verificar_frete_faixa4()
    print()
    print("Todas as verificações passaram — mas a regressão está presente.")
    print("Tente: calcular_frete(12.0, 100.0)")
    print(f"  Obtido:  R$ {calcular_frete(12.0, 100.0):.2f}  (faixa 2 com limite deslocado)")
    print(f"  Correto: R$ {round(12.0 * 1.50 + 5.00, 2):.2f}  (deveria ser faixa 3)")
    print()
    print("⚠ A suite fraca não cobriu o intervalo 10–15 kg — regressão invisível.")
