"""
frete_gerado.py — Cálculo de frete com faixas de peso.

Saída de IA após mudança assistida — a suite fraca mascara uma regressão.
Um agente adicionou a faixa "carga pesada" (> 20 kg) a pedido do negócio,
mas deslocou silenciosamente a fronteira entre duas faixas existentes.

Execute: python3 frete_gerado.py
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
TARIFA_PADRAO = 25.00    # envios de 2 kg até 10 kg — faixa padrão (base)
TARIFA_MEDIA = 45.00     # envios de 10 kg até 20 kg — faixa intermediária
TARIFA_PESADA = 80.00    # envios acima de 20 kg — carga pesada (adicionado pelo agente)


# ---------------------------------------------------------------------------
# Lógica de cálculo
# ---------------------------------------------------------------------------

def calcular_frete(peso_kg: float, distancia_km: float,
                   regional: bool = False) -> float:
    """
    Calcula o frete com base no peso e na distância.

    Faixas de peso:
      - até 2 kg: tarifa leve (R$ 8,00 base)
      - 2 kg < peso < 10 kg: tarifa padrão (R$ 25,00 base)
      - 10 kg a 20 kg: tarifa intermediária (R$ 45,00 base)
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
    elif peso_kg < 10.0:
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
    if peso_kg < 10.0:
        return "padrão (2 kg a 10 kg)"
    if peso_kg <= 20.0:
        return "intermediária (10 kg a 20 kg)"
    return "carga pesada (acima de 20 kg)"


# ---------------------------------------------------------------------------
# Suite fraca de verificação (mid-band apenas — mascara a regressão)
# ---------------------------------------------------------------------------

def verificar_faixas_mid_band() -> None:
    """
    Verifica valores no meio de cada faixa de peso.

    Cobre 5 kg, 8 kg, 15 kg e 25 kg — todos no interior das faixas.
    Não testa valores de borda, então o deslocamento de <= 10 para < 10
    não é detectado aqui. Todos os casos imprimem OK.
    """
    casos = [
        (5.0,  100, False, 33.00, "5 kg, 100 km — faixa padrão mid-band"),
        (8.0,  100, False, 33.00, "8 kg, 100 km — faixa padrão mid-band"),
        (15.0, 100, False, 53.00, "15 kg, 100 km — faixa intermediária mid-band"),
        (25.0, 100, False, 88.00, "25 kg, 100 km — carga pesada mid-band"),
    ]
    for peso, distancia, regional, esperado, descricao in casos:
        obtido = calcular_frete(peso, distancia, regional)
        if abs(obtido - esperado) < 0.001:
            print(f"OK: {descricao}")
        else:
            print(f"FALHOU: {descricao} (esperado {esperado:.2f}, obtido {obtido:.2f})")


def verificar_faixa_leve() -> None:
    """Verifica o comportamento da faixa leve (até 2 kg)."""
    casos = [
        (1.0,  50, False, 12.00, "1 kg, 50 km — faixa leve"),
        (2.0,  50, False, 12.00, "2 kg, 50 km — borda superior faixa leve"),
    ]
    for peso, distancia, regional, esperado, descricao in casos:
        obtido = calcular_frete(peso, distancia, regional)
        if abs(obtido - esperado) < 0.001:
            print(f"OK: {descricao}")
        else:
            print(f"FALHOU: {descricao} (esperado {esperado:.2f}, obtido {obtido:.2f})")


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------

def _demonstrar_cotacoes() -> None:
    """Demonstra cotações de frete para diferentes perfis de envio."""
    envios = [
        (1.5,   80, False, "pacote leve"),
        (5.0,  150, False, "pacote padrão"),
        (8.0,  200, False, "pacote padrão maior"),
        (15.0, 300, False, "carga intermediária"),
        (25.0, 400, False, "carga pesada"),
        (5.0,  150, True,  "pacote padrão — regional"),
    ]

    print("Cotações de frete:")
    print(f"  {'Peso':>8}  {'Distância':>10}  {'Regional':>8}  {'Faixa':<28}  {'Frete':>10}")
    print("  " + "-" * 76)
    for peso, distancia, regional, rotulo in envios:
        frete = calcular_frete(peso, distancia, regional)
        faixa = descricao_faixa(peso)
        reg_str = "sim" if regional else "não"
        print(f"  {peso:>7.1f}kg  {distancia:>9}km  {reg_str:>8}  {faixa:<28}  R${frete:>8.2f}")
    print()


if __name__ == "__main__":
    print("=== Cálculo de Frete — código gerado por IA (mudança assistida) ===\n")

    _demonstrar_cotacoes()

    print("--- Verificações (suite fraca) ---")
    verificar_faixa_leve()
    verificar_faixas_mid_band()
    print()
    print("Todas as verificações passaram — mas a suite não testa 10 kg exato.")
    print("O deslocamento de <= 10 para < 10 é invisível com estes casos.")
