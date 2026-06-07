"""
frete_revisado.py — Cálculo de frete com faixas de peso (corrigido).

Suite completa de caracterização com valores de borda exatos.
A fronteira de 10 kg é testada explicitamente — o que revelaria a regressão
introduzida em frete_gerado.py (< 10 em vez de <= 10).

Execute: python3 frete_revisado.py
"""

from __future__ import annotations

from typing import Optional


# ---------------------------------------------------------------------------
# Constantes de domínio
# ---------------------------------------------------------------------------

TARIFA_BASE_POR_KG = 2.50          # R$/kg para frete padrão
TARIFA_DISTANCIA_POR_KM = 0.08     # R$/km adicional
FATOR_REGIONAL = 1.15              # multiplicador para destinos regionais


# ---------------------------------------------------------------------------
# Faixas de peso e tarifas diferenciadas
# ---------------------------------------------------------------------------

TARIFA_LEVE = 8.00       # envios até 2 kg — taxa mínima fixa
TARIFA_PADRAO = 25.00    # envios de 2 kg até 10 kg — faixa padrão (inclui 10 kg)
TARIFA_MEDIA = 45.00     # envios acima de 10 kg até 20 kg — faixa intermediária
TARIFA_PESADA = 80.00    # envios acima de 20 kg — carga pesada


# ---------------------------------------------------------------------------
# Lógica de cálculo (fronteira correta: <= 10)
# ---------------------------------------------------------------------------

def calcular_frete(peso_kg: float, distancia_km: float,
                   regional: bool = False) -> float:
    """
    Calcula o frete com base no peso e na distância.

    Faixas de peso:
      - até 2 kg: tarifa leve (R$ 8,00 base)
      - 2 kg < peso <= 10 kg: tarifa padrão (R$ 25,00 base)
      - 10 kg < peso <= 20 kg: tarifa intermediária (R$ 45,00 base)
      - acima de 20 kg: tarifa de carga pesada (R$ 80,00 base)

    A componente de distância é somada à tarifa base.
    Destinos regionais recebem multiplicador adicional.
    """
    if peso_kg <= 0:
        raise ValueError(f"Peso inválido: {peso_kg} kg. Deve ser maior que zero.")
    if distancia_km <= 0:
        raise ValueError(f"Distância inválida: {distancia_km} km. Deve ser maior que zero.")

    if peso_kg <= 2.0:
        tarifa_base = TARIFA_LEVE
    elif peso_kg <= 10.0:         # ← fronteira correta: inclui exatamente 10 kg na faixa padrão
        tarifa_base = TARIFA_PADRAO
    elif peso_kg <= 20.0:
        tarifa_base = TARIFA_MEDIA
    else:
        tarifa_base = TARIFA_PESADA

    componente_distancia = distancia_km * TARIFA_DISTANCIA_POR_KM
    frete_calculado = tarifa_base + componente_distancia

    if regional:
        frete_calculado *= FATOR_REGIONAL

    return round(frete_calculado, 2)


def descricao_faixa(peso_kg: float) -> str:
    """Retorna a descrição textual da faixa de peso aplicada ao envio."""
    if peso_kg <= 0:
        return "peso inválido"
    if peso_kg <= 2.0:
        return "leve (até 2 kg)"
    if peso_kg <= 10.0:
        return "padrão (2 kg a 10 kg)"
    if peso_kg <= 20.0:
        return "intermediária (10 kg a 20 kg)"
    return "carga pesada (acima de 20 kg)"


# ---------------------------------------------------------------------------
# Suite COMPLETA de caracterização (inclui bordas exatas)
# ---------------------------------------------------------------------------

def verificar_faixa_leve() -> None:
    """Faixa leve: até 2 kg inclusive."""
    casos = [
        (0.5,  50, False,  12.00, "0.5 kg, 50 km — faixa leve"),
        (1.0,  50, False,  12.00, "1 kg, 50 km — faixa leve mid-band"),
        (2.0,  50, False,  12.00, "2 kg, 50 km — borda superior faixa leve"),
    ]
    for peso, distancia, regional, esperado, descricao in casos:
        obtido = calcular_frete(peso, distancia, regional)
        if abs(obtido - esperado) < 0.001:
            print(f"OK: {descricao}")
        else:
            print(f"FALHOU: {descricao} (esperado {esperado:.2f}, obtido {obtido:.2f})")


def verificar_faixa_padrao() -> None:
    """Faixa padrão: acima de 2 kg até 10 kg inclusive.

    O caso de 10 kg é a fronteira crítica — frete_gerado.py a classifica
    erroneamente como intermediária (usa < 10 em vez de <= 10).
    """
    casos = [
        (2.1,  100, False, 33.00, "2.1 kg, 100 km — borda inferior faixa padrão"),
        (5.0,  100, False, 33.00, "5 kg, 100 km — faixa padrão mid-band"),
        (8.0,  100, False, 33.00, "8 kg, 100 km — faixa padrão mid-band"),
        (10.0, 100, False, 33.00, "10 kg, 100 km — borda SUPERIOR faixa padrão (fronteira crítica)"),
    ]
    for peso, distancia, regional, esperado, descricao in casos:
        obtido = calcular_frete(peso, distancia, regional)
        if abs(obtido - esperado) < 0.001:
            print(f"OK: {descricao}")
        else:
            print(f"FALHOU: {descricao} (esperado {esperado:.2f}, obtido {obtido:.2f})")


def verificar_faixa_intermediaria() -> None:
    """Faixa intermediária: acima de 10 kg até 20 kg inclusive."""
    casos = [
        (10.1, 100, False, 53.00, "10.1 kg, 100 km — borda inferior faixa intermediária"),
        (15.0, 100, False, 53.00, "15 kg, 100 km — faixa intermediária mid-band"),
        (20.0, 100, False, 53.00, "20 kg, 100 km — borda superior faixa intermediária"),
    ]
    for peso, distancia, regional, esperado, descricao in casos:
        obtido = calcular_frete(peso, distancia, regional)
        if abs(obtido - esperado) < 0.001:
            print(f"OK: {descricao}")
        else:
            print(f"FALHOU: {descricao} (esperado {esperado:.2f}, obtido {obtido:.2f})")


def verificar_faixa_pesada() -> None:
    """Faixa pesada: acima de 20 kg."""
    casos = [
        (20.1, 100, False, 88.00, "20.1 kg, 100 km — borda inferior carga pesada"),
        (25.0, 100, False, 88.00, "25 kg, 100 km — carga pesada mid-band"),
        (50.0, 100, False, 88.00, "50 kg, 100 km — carga pesada extremo"),
    ]
    for peso, distancia, regional, esperado, descricao in casos:
        obtido = calcular_frete(peso, distancia, regional)
        if abs(obtido - esperado) < 0.001:
            print(f"OK: {descricao}")
        else:
            print(f"FALHOU: {descricao} (esperado {esperado:.2f}, obtido {obtido:.2f})")


def verificar_componente_regional() -> None:
    """Destinos regionais recebem multiplicador de 1.15."""
    casos = [
        (5.0,  100, True, 37.95, "5 kg, 100 km — regional (padrão × 1.15)"),
        (15.0, 100, True, 60.95, "15 kg, 100 km — regional (intermediária × 1.15)"),
    ]
    for peso, distancia, regional, esperado, descricao in casos:
        obtido = calcular_frete(peso, distancia, regional)
        if abs(obtido - esperado) < 0.001:
            print(f"OK: {descricao}")
        else:
            print(f"FALHOU: {descricao} (esperado {esperado:.2f}, obtido {obtido:.2f})")


def verificar_entradas_invalidas() -> None:
    """Peso e distância inválidos devem levantar ValueError."""
    casos_invalidos = [
        (0.0,  100, "peso zero"),
        (-1.0, 100, "peso negativo"),
        (5.0,  0.0, "distância zero"),
        (5.0,  -50, "distância negativa"),
    ]
    for peso, distancia, descricao in casos_invalidos:
        try:
            calcular_frete(peso, distancia)
            print(f"FALHOU: {descricao} — deveria levantar ValueError, mas não levantou")
        except ValueError:
            print(f"OK: {descricao} — ValueError levantado corretamente")


# ---------------------------------------------------------------------------
# Demo comparativo (mostra a diferença entre gerado e revisado para 10 kg)
# ---------------------------------------------------------------------------

def _demonstrar_diferenca_fronteira() -> None:
    """
    Demonstra a diferença entre a versão gerada e a revisada para 10 kg exato.

    Na versão gerada: peso < 10 → 10 kg cai na faixa intermediária (R$ 53,00).
    Na versão revisada: peso <= 10 → 10 kg permanece na faixa padrão (R$ 33,00).
    """
    frete_10kg = calcular_frete(10.0, 100)
    print(f"Frete para 10 kg, 100 km (nesta versão): R$ {frete_10kg:.2f}")
    print(f"  Faixa: {descricao_faixa(10.0)}")
    print(f"  Esperado (faixa padrão): R$ 33,00")
    if abs(frete_10kg - 33.00) < 0.001:
        print("  Fronteira correta: 10 kg está na faixa padrão.")
    else:
        print("  REGRESSÃO: 10 kg caiu na faixa errada.")
    print()


if __name__ == "__main__":
    print("=== Cálculo de Frete — versão revisada com suite completa ===\n")

    _demonstrar_diferenca_fronteira()

    print("--- Verificações completas (incluindo bordas) ---")
    verificar_faixa_leve()
    verificar_faixa_padrao()
    verificar_faixa_intermediaria()
    verificar_faixa_pesada()
    verificar_componente_regional()
    verificar_entradas_invalidas()
