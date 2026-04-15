"""
GABARITO — Tutorial 06: Dívida Técnica
Referência: Clean Code, Cap. 17
Execute: python gabarito.py

Dívidas identificadas e pagas:
  1. MAGIC_NUMBER — 15.0, 25.0, 40.0, 2.5, 3.2, 4.0, 1.8, 2.1, 2.8, 0.12, 0.18, 0.25, 1.3
  2. DUPLICAÇÃO   — lógica de cálculo por faixa de peso copiada em calc_frete e estimar
  3. FUNÇÕES      — calc_frete faz validação de modalidade, cálculo por faixa, soma de km e taxa de urgência
  4. NOMES        — tp, kg, km, t, urg não revelam intenção; estimar é ambíguo
"""

# ── Constantes ─────────────────────────────────────────────────────────────────
# Dívida 1 paga: todos os magic numbers têm nome e estão agrupados por modalidade

# Estrutura de tarifas por modalidade: (taxa_base, custo_por_kg_faixa_1, custo_por_kg_faixa_2, custo_por_km)
# Faixa 1: 0-5 kg (cobrada pela taxa base)
# Faixa 2: 5-20 kg (custo adicional por kg)
# Faixa 3: acima de 20 kg (custo adicional por kg, mais barato por volume)

MODALIDADE_ECONOMICA = "A"
MODALIDADE_PADRAO = "B"
MODALIDADE_EXPRESSA = "C"

LIMITE_FAIXA_1_KG = 5
LIMITE_FAIXA_2_KG = 20

TARIFAS_POR_MODALIDADE = {
    MODALIDADE_ECONOMICA: {
        "taxa_base": 15.0,
        "custo_faixa_2_por_kg": 2.5,
        "custo_faixa_3_por_kg": 1.8,
        "custo_por_km": 0.12,
    },
    MODALIDADE_PADRAO: {
        "taxa_base": 25.0,
        "custo_faixa_2_por_kg": 3.2,
        "custo_faixa_3_por_kg": 2.1,
        "custo_por_km": 0.18,
    },
    MODALIDADE_EXPRESSA: {
        "taxa_base": 40.0,
        "custo_faixa_2_por_kg": 4.0,
        "custo_faixa_3_por_kg": 2.8,
        "custo_por_km": 0.25,
    },
}

FATOR_URGENCIA = 1.3  # acréscimo de 30% para entregas urgentes


# ── Funções auxiliares ─────────────────────────────────────────────────────────
# Dívida 3 paga: cada função faz uma única coisa

def _calcular_custo_pelo_peso(peso_kg: float, tarifas: dict) -> float:
    """Calcula o custo do frete considerando as faixas de peso."""
    if peso_kg <= LIMITE_FAIXA_1_KG:
        return tarifas["taxa_base"]

    if peso_kg <= LIMITE_FAIXA_2_KG:
        excedente_faixa_2 = peso_kg - LIMITE_FAIXA_1_KG
        return tarifas["taxa_base"] + excedente_faixa_2 * tarifas["custo_faixa_2_por_kg"]

    # Faixa 3: acima de 20 kg
    custo_faixa_2_completa = (LIMITE_FAIXA_2_KG - LIMITE_FAIXA_1_KG) * tarifas["custo_faixa_2_por_kg"]
    excedente_faixa_3 = peso_kg - LIMITE_FAIXA_2_KG
    return (
        tarifas["taxa_base"]
        + custo_faixa_2_completa
        + excedente_faixa_3 * tarifas["custo_faixa_3_por_kg"]
    )


def _calcular_custo_pela_distancia(distancia_km: float, tarifas: dict) -> float:
    return distancia_km * tarifas["custo_por_km"]


# ── Funções públicas ───────────────────────────────────────────────────────────
# Dívida 2 paga: lógica centralizada em uma única função; calc_frete e estimar_frete
#               chamam a mesma lógica de cálculo por modalidade

def _calcular_frete_por_modalidade(
    modalidade: str,
    peso_kg: float,
    distancia_km: float,
) -> float:
    """Calcula o frete base (sem urgência) para uma modalidade específica."""
    if modalidade not in TARIFAS_POR_MODALIDADE:
        raise ValueError(f"Modalidade inválida: {modalidade}. Use A, B ou C.")

    tarifas = TARIFAS_POR_MODALIDADE[modalidade]
    custo_peso = _calcular_custo_pelo_peso(peso_kg, tarifas)
    custo_distancia = _calcular_custo_pela_distancia(distancia_km, tarifas)
    return custo_peso + custo_distancia


def calcular_frete(
    modalidade: str,
    peso_kg: float,
    distancia_km: float,
    urgente: bool = False,
) -> float:
    """Calcula o valor final do frete, aplicando acréscimo de urgência se solicitado."""
    # Dívida 4 paga: parâmetros com nomes descritivos (modalidade, peso_kg, distancia_km, urgente)
    valor_base = _calcular_frete_por_modalidade(modalidade, peso_kg, distancia_km)

    if urgente:
        # Taxa de urgência: 30% de acréscimo — definido em contrato comercial
        valor_base *= FATOR_URGENCIA

    return round(valor_base, 2)


def estimar_frete(modalidade: str, peso_kg: float, distancia_km: float) -> float:
    """Estimativa de frete sem urgência — alias para calcular_frete sem flag de urgência."""
    return calcular_frete(modalidade, peso_kg, distancia_km, urgente=False)


# ── Execução de demonstração ───────────────────────────────────────────────────

if __name__ == "__main__":
    print("=== Gabarito: Cálculo de Frete Refatorado ===\n")

    print("Frete A, 3kg, 100km:", calcular_frete("A", 3, 100))
    print("Frete A, 15kg, 200km:", calcular_frete("A", 15, 200))
    print("Frete A, 30kg, 300km:", calcular_frete("A", 30, 300))
    print("Frete B, 10kg, 150km:", calcular_frete("B", 10, 150))
    print("Frete C, 25kg, 400km:", calcular_frete("C", 25, 400))
    print("Frete A urgente, 5kg, 100km:", calcular_frete("A", 5, 100, urgente=True))
    print("Estimativa A, 3kg, 100km:", estimar_frete("A", 3, 100))

    print("\n=== Comparação com versão original (valores devem ser iguais) ===\n")
    from exercicio import calc_frete, estimar

    casos = [
        ("A", 3, 100, False),
        ("A", 15, 200, False),
        ("A", 30, 300, False),
        ("B", 10, 150, False),
        ("C", 25, 400, False),
        ("A", 5, 100, True),
    ]

    todos_iguais = True
    for modalidade, peso, distancia, urgente in casos:
        original = calc_frete(modalidade, peso, distancia, urg=urgente)
        refatorado = calcular_frete(modalidade, peso, distancia, urgente=urgente)
        status = "OK" if original == refatorado else "DIVERGÊNCIA"
        if status == "DIVERGÊNCIA":
            todos_iguais = False
        print(f"  {modalidade} {peso}kg {distancia}km {'urgente' if urgente else '       '}: "
              f"original={original} refatorado={refatorado} [{status}]")

    print(f"\nTodos os valores batem: {'SIM' if todos_iguais else 'NÃO — verifique a refatoração'}")
