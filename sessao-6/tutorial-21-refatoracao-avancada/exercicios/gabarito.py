"""
Gabarito — Refatoração de IA com regressão de borda
Referência: Tutorial 13 — Refatoração assistida avançada
Execute: python3 gabarito.py

Correções aplicadas em relação a exercicio.py:
  (1) verificar_equivalencia completa: inclui os limites exatos de atingimento
      (80%, 100%, 120%) onde a regressão de borda se manifesta.
  (2) calcular_bonus_refatorado corrigido: operador '>' substituído por '>='
      para preservar o comportamento do if/elif original nos limites.
"""

from dataclasses import dataclass
from typing import NamedTuple


# ─── Domínio ──────────────────────────────────────────────────────────────────

@dataclass
class MetaVendedor:
    vendedor_id:   str
    salario_base:  float
    atingimento:   float   # percentual: 0.0 a qualquer valor (ex.: 1.25 = 125%)


# ─── Versão ORIGINAL (if/elif em escada) — comportamento de referência ────────

def calcular_bonus_original(meta: MetaVendedor) -> float:
    """Calcula bônus com base no atingimento de meta."""
    if meta.atingimento >= 1.20:
        return meta.salario_base * 0.30
    elif meta.atingimento >= 1.00:
        return meta.salario_base * 0.20
    elif meta.atingimento >= 0.80:
        return meta.salario_base * 0.10
    else:
        return 0.0


# ─── Versão REFATORADA correta (tabela de faixas com operador correto) ────────

class FaixaBonus(NamedTuple):
    atingimento_minimo: float
    percentual_bonus:   float


TABELA_BONUS: list[FaixaBonus] = [
    FaixaBonus(1.20, 0.30),
    FaixaBonus(1.00, 0.20),
    FaixaBonus(0.80, 0.10),
]


def calcular_bonus_refatorado(meta: MetaVendedor) -> float:
    """
    Calcula bônus percorrendo a tabela de faixas de atingimento.

    Usa '>=' para preservar o comportamento exato do original:
    atingimento == limite_minimo entra na faixa desse limite (não abaixo).
    """
    for faixa in TABELA_BONUS:
        if meta.atingimento >= faixa.atingimento_minimo:
            return meta.salario_base * faixa.percentual_bonus
    return 0.0


# ─── Verificação COMPLETA (inclui limites exatos de cada faixa) ──────────────

def verificar_equivalencia() -> None:
    """
    Compara a versão refatorada contra a original para todos os casos relevantes:
    - Casos no interior de cada faixa
    - Casos nos limites exatos (80%, 100%, 120%) onde a regressão se manifesta
    - Casos logo abaixo dos limites
    """
    salario = 5_000.0
    casos = [
        # Interior das faixas
        MetaVendedor("interior-sem-bonus",  salario, 0.60),
        MetaVendedor("interior-faixa1",     salario, 0.90),
        MetaVendedor("interior-faixa2",     salario, 1.10),
        MetaVendedor("interior-faixa3",     salario, 1.30),
        # Limites exatos — onde a regressão de borda se manifesta
        MetaVendedor("limite-faixa1",       salario, 0.80),   # >= 80% → 10% (não 0)
        MetaVendedor("limite-faixa2",       salario, 1.00),   # >= 100% → 20% (não 10%)
        MetaVendedor("limite-faixa3",       salario, 1.20),   # >= 120% → 30% (não 20%)
        # Logo abaixo dos limites
        MetaVendedor("abaixo-faixa1",       salario, 0.799),
        MetaVendedor("abaixo-faixa2",       salario, 0.999),
        MetaVendedor("abaixo-faixa3",       salario, 1.199),
    ]

    print("=== Verificação de equivalência (completa — inclui bordas) ===\n")
    todos_ok = True
    for meta in casos:
        esperado = calcular_bonus_original(meta)
        obtido   = calcular_bonus_refatorado(meta)
        if abs(obtido - esperado) < 0.001:
            print(
                f"  OK: {meta.vendedor_id:<22}  atingimento={meta.atingimento:.1%}"
                f"  bônus={obtido:>8.2f}"
            )
        else:
            print(
                f"  FALHOU: {meta.vendedor_id:<22}  atingimento={meta.atingimento:.1%}"
                f"  esperado={esperado:.2f}  obtido={obtido:.2f}"
            )
            todos_ok = False

    print()
    if todos_ok:
        print("Resultado: todos os casos passaram — refatoração preserva o comportamento.")
    else:
        print("Resultado: há divergências — refatoração altera o comportamento.")


# ─── Execução de demonstração ─────────────────────────────────────────────────

if __name__ == "__main__":
    print("=== Bônus por Meta — gabarito (operador correto) ===\n")

    salario_base = 5_000.0
    demonstracao = [
        MetaVendedor("V01", salario_base, 0.60),
        MetaVendedor("V02", salario_base, 0.80),   # limite exato — deve ser 10%, não 0
        MetaVendedor("V03", salario_base, 1.00),   # limite exato — deve ser 20%, não 10%
        MetaVendedor("V04", salario_base, 1.20),   # limite exato — deve ser 30%, não 20%
        MetaVendedor("V05", salario_base, 1.30),
    ]

    print(f"  {'Vendedor':<10} {'Atingimento':>12}  {'Original':>10}  {'Refatorada':>10}  {'Status':>8}")
    print("  " + "-" * 58)
    for meta in demonstracao:
        orig   = calcular_bonus_original(meta)
        refat  = calcular_bonus_refatorado(meta)
        status = "OK" if abs(orig - refat) < 0.001 else "DIFERENTE"
        print(
            f"  {meta.vendedor_id:<10} {meta.atingimento:>12.0%}"
            f"  R${orig:>9.2f}  R${refat:>9.2f}  {status:>8}"
        )

    print()
    verificar_equivalencia()
