"""
Exercício — Refatoração de IA com regressão de borda
Referência: Tutorial 13 — Refatoração assistida avançada
Execute: python3 exercicio.py

Contexto: uma IA refatorou o cálculo de bônus por meta de vendas.
O código original usava if/elif por faixas de atingimento (em percentual).
A versão refatorada usa uma tabela de faixas — idiomática e legível.

Tarefas:
  (1) Escreva a função verificar_equivalencia incluindo os limites exatos
      de cada faixa de atingimento (ex.: exatamente 80%, 100%, 120%).
  (2) Rode a verificação contra a versão refatorada abaixo.
  (3) Identifique qual caso de borda regrediu e corrija a refatoração.

Compare sua solução com gabarito.py.
"""

from dataclasses import dataclass
from typing import NamedTuple


# ─── Domínio ──────────────────────────────────────────────────────────────────

@dataclass
class MetaVendedor:
    vendedor_id:   str
    salario_base:  float
    atingimento:   float   # percentual: 0.0 a qualquer valor (ex.: 1.25 = 125%)


# ─── Versão ORIGINAL (if/elif em escada) ─────────────────────────────────────

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


# ─── Versão REFATORADA pela IA (tabela de faixas) ────────────────────────────

class FaixaBonus(NamedTuple):
    atingimento_minimo: float
    percentual_bonus:   float


TABELA_BONUS: list[FaixaBonus] = [
    FaixaBonus(1.20, 0.30),
    FaixaBonus(1.00, 0.20),
    FaixaBonus(0.80, 0.10),
]


def calcular_bonus_refatorado(meta: MetaVendedor) -> float:
    """Calcula bônus percorrendo a tabela de faixas de atingimento."""
    for faixa in TABELA_BONUS:
        if meta.atingimento > faixa.atingimento_minimo:
            return meta.salario_base * faixa.percentual_bonus
    return 0.0


# ─── Verificação FRACA (só casos no interior das faixas) ─────────────────────

def verificar_equivalencia() -> None:
    """
    TODO: implemente uma verificação completa que inclua os limites exatos.
    Esta versão cobre apenas o interior de cada faixa — não os limites.
    """
    salario = 5_000.0
    casos = [
        MetaVendedor("V01", salario, 0.60),   # abaixo do mínimo → 0
        MetaVendedor("V02", salario, 0.90),   # interior faixa 80–99%
        MetaVendedor("V03", salario, 1.10),   # interior faixa 100–119%
        MetaVendedor("V04", salario, 1.30),   # acima de 120%
    ]

    print("=== Verificação de equivalência (fraca — só interior das faixas) ===\n")
    todos_ok = True
    for meta in casos:
        esperado = calcular_bonus_original(meta)
        obtido   = calcular_bonus_refatorado(meta)
        if abs(obtido - esperado) < 0.001:
            print(f"  OK: atingimento={meta.atingimento:.0%}  bônus={obtido:>8.2f}")
        else:
            print(
                f"  FALHOU: atingimento={meta.atingimento:.0%}"
                f"  esperado={esperado:.2f}  obtido={obtido:.2f}"
            )
            todos_ok = False

    print()
    if todos_ok:
        print("Resultado: todos os casos passaram.")
    else:
        print("Resultado: há divergências.")


# ─── Execução de demonstração ─────────────────────────────────────────────────

if __name__ == "__main__":
    print("=== Bônus por Meta — refatoração de IA (tabela de faixas) ===\n")

    salario_base = 5_000.0
    demonstracao = [
        MetaVendedor("V01", salario_base, 0.60),
        MetaVendedor("V02", salario_base, 0.90),
        MetaVendedor("V03", salario_base, 1.10),
        MetaVendedor("V04", salario_base, 1.30),
    ]

    print(f"  {'Vendedor':<10} {'Atingimento':>12}  {'Original':>10}  {'Refatorada':>10}")
    print("  " + "-" * 48)
    for meta in demonstracao:
        orig  = calcular_bonus_original(meta)
        refat = calcular_bonus_refatorado(meta)
        print(
            f"  {meta.vendedor_id:<10} {meta.atingimento:>12.0%}"
            f"  R${orig:>9.2f}  R${refat:>9.2f}"
        )

    print()
    verificar_equivalencia()
