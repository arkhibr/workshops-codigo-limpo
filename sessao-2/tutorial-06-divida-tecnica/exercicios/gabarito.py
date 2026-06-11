"""
GABARITO — Tutorial 06: Dívida Técnica
Execute: python3 gabarito.py

Quatro passos aplicados em sequência sobre o código original:

  Passo 1 — Dívidas identificadas:
    MAGIC_NUMBER  15.0/25.0/40.0 (taxa_base), 2.5/3.2/4.0 (faixa 2),
                  1.8/2.1/2.8 (faixa 3), 0.12/0.18/0.25 (km), 1.3 (urgência),
                  5 e 20 (limites de faixa)
    NOMES         tp, kg, km, t, urg não revelam intenção; estimar é ambíguo
    DUPLICAÇÃO    corpo idêntico em calc_frete e estimar
    FUNÇÕES       calc_frete faz: validar modalidade + calcular por faixa de peso
                  + acrescentar custo de km + aplicar urgência (quatro coisas)

  Passo 2 — constantes extraídas
  Passo 3 — parâmetros renomeados
  Passo 4 — _calcular_por_modalidade extraída; estimar_frete chama calcular_frete
"""

# ── Passo 2: constantes nomeadas ─────────────────────────────────────────────

LIMITE_FAIXA_1_KG = 5
LIMITE_FAIXA_2_KG = 20
FATOR_URGENCIA    = 1.3

TARIFAS = {
    "A": {"taxa_base": 15.0, "custo_faixa_2": 2.5, "custo_faixa_3": 1.8, "custo_km": 0.12},
    "B": {"taxa_base": 25.0, "custo_faixa_2": 3.2, "custo_faixa_3": 2.1, "custo_km": 0.18},
    "C": {"taxa_base": 40.0, "custo_faixa_2": 4.0, "custo_faixa_3": 2.8, "custo_km": 0.25},
}


# ── Passo 4: lógica extraída — zero duplicação ────────────────────────────────

def _calcular_por_modalidade(modalidade: str, peso_kg: float, distancia_km: float) -> float:
    if modalidade not in TARIFAS:
        raise ValueError(f"Modalidade inválida: {modalidade}. Use A, B ou C.")
    t = TARIFAS[modalidade]
    if peso_kg <= LIMITE_FAIXA_1_KG:
        custo = t["taxa_base"]
    elif peso_kg <= LIMITE_FAIXA_2_KG:
        custo = t["taxa_base"] + (peso_kg - LIMITE_FAIXA_1_KG) * t["custo_faixa_2"]
    else:
        custo = (
            t["taxa_base"]
            + (LIMITE_FAIXA_2_KG - LIMITE_FAIXA_1_KG) * t["custo_faixa_2"]
            + (peso_kg - LIMITE_FAIXA_2_KG) * t["custo_faixa_3"]
        )
    custo += distancia_km * t["custo_km"]
    return custo


# ── Passos 3+4: funções públicas com nomes descritivos ───────────────────────

def calcular_frete(modalidade: str, peso_kg: float, distancia_km: float, urgente: bool = False) -> float:
    valor = _calcular_por_modalidade(modalidade, peso_kg, distancia_km)
    if urgente:
        valor *= FATOR_URGENCIA
    return round(valor, 2)


def estimar_frete(modalidade: str, peso_kg: float, distancia_km: float) -> float:
    return calcular_frete(modalidade, peso_kg, distancia_km, urgente=False)


# ── Verificação ──────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=== Gabarito T06 — valores esperados ===\n")

    casos = [
        ("A",  3, 100, False,  27.0),
        ("A", 15, 200, False,  64.0),
        ("A", 30, 300, False, 106.5),
        ("B", 10, 150, False,  68.0),
        ("C", 25, 400, False, 214.0),
        ("A",  5, 100, True,   35.1),
    ]

    ok = True
    for modalidade, peso, dist, urgente, esperado in casos:
        resultado = calcular_frete(modalidade, peso, dist, urgente)
        status = "OK" if resultado == esperado else f"ERRO — esperado {esperado}"
        if resultado != esperado:
            ok = False
        label = "urgente" if urgente else "       "
        print(f"  {modalidade} {peso:2}kg {dist:3}km {label}: {resultado} [{status}]")

    print(f"\nEstimativa A, 3kg, 100km: {estimar_frete('A', 3, 100)}")
    print(f"\nTodos corretos: {'SIM' if ok else 'NÃO'}")
