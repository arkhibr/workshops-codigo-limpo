"""
Refatoração revisada — Cálculo de Comissão de Vendas com Faixas
Referência: Tutorial 13 — Refatoração assistida avançada
Execute: python3 comissao_revisado.py

Correção aplicada em relação a comissao_gerado.py:
  - O operador de comparação foi corrigido de '>' para '>=' nos limites de faixa.
  - A versão gerada usava 'valor > limite_inferior', o que fazia um valor exato
    no limite (ex.: 10.000) cair para a faixa anterior (6% → 4%).
  - A versão revisada usa 'valor >= limite_inferior', preservando o comportamento
    exato do if/elif original onde '>= 10.000' entrava na faixa de 6%.
  - A verificação de equivalência é completa: inclui os limites exatos de cada faixa.
"""

from dataclasses import dataclass
from typing import NamedTuple


# ─── Domínio ──────────────────────────────────────────────────────────────────

@dataclass
class Venda:
    vendedor_id: str
    valor:       float


# ─── Versão ORIGINAL (if/elif em escada) — comportamento de referência ────────

def calcular_comissao_original(venda: Venda) -> float:
    """Calcula comissão usando if/elif por faixas de valor."""
    valor = venda.valor
    if valor >= 50_000:
        return valor * 0.10
    elif valor >= 20_000:
        return valor * 0.08
    elif valor >= 10_000:
        return valor * 0.06
    elif valor >= 5_000:
        return valor * 0.04
    else:
        return valor * 0.02


# ─── Versão REFATORADA correta (tabela de faixas com operador correto) ────────

class FaixaComissao(NamedTuple):
    limite_inferior: float
    percentual:      float


TABELA_COMISSAO: list[FaixaComissao] = [
    FaixaComissao(50_000, 0.10),
    FaixaComissao(20_000, 0.08),
    FaixaComissao(10_000, 0.06),
    FaixaComissao(5_000,  0.04),
    FaixaComissao(0,      0.02),
]


def calcular_comissao_refatorada(venda: Venda) -> float:
    """
    Calcula comissão percorrendo a tabela de faixas.

    Usa '>=' para preservar o comportamento exato do original:
    valor == limite_inferior entra na faixa desse limite (não na faixa abaixo).
    """
    for faixa in TABELA_COMISSAO:
        if venda.valor >= faixa.limite_inferior:
            return venda.valor * faixa.percentual
    return venda.valor * TABELA_COMISSAO[-1].percentual


# ─── Verificação COMPLETA (inclui limites exatos de cada faixa) ──────────────

def verificar_equivalencia() -> None:
    """
    Compara a versão refatorada contra a original para todos os casos relevantes:
    - Casos no interior de cada faixa
    - Casos nos limites exatos de cada faixa (onde a regressão se manifesta)
    - Caso abaixo do menor limite
    """
    casos = [
        # Interior das faixas
        Venda("interior-baixo",    1_000),
        Venda("interior-faixa2",   7_500),
        Venda("interior-faixa3",  15_000),
        Venda("interior-faixa4",  35_000),
        Venda("interior-alto",    80_000),
        # Limites exatos — onde a regressão de borda se manifesta
        Venda("limite-faixa2",     5_000),   # >= 5000 → 4% (não 2%)
        Venda("limite-faixa3",    10_000),   # >= 10000 → 6% (não 4%)
        Venda("limite-faixa4",    20_000),   # >= 20000 → 8% (não 6%)
        Venda("limite-faixa5",    50_000),   # >= 50000 → 10% (não 8%)
        # Um passo abaixo dos limites
        Venda("abaixo-faixa2",     4_999),
        Venda("abaixo-faixa3",     9_999),
        Venda("abaixo-faixa4",    19_999),
        Venda("abaixo-faixa5",    49_999),
    ]

    print("=== Verificação de equivalência (completa — inclui bordas) ===\n")
    todos_ok = True
    for venda in casos:
        esperado = calcular_comissao_original(venda)
        obtido   = calcular_comissao_refatorada(venda)
        if abs(obtido - esperado) < 0.001:
            print(f"  OK: {venda.vendedor_id:<22}  valor={venda.valor:>8.0f}  comissão={obtido:>9.2f}")
        else:
            print(
                f"  FALHOU: {venda.vendedor_id:<22}  valor={venda.valor:>8.0f}"
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
    print("=== Comissão de Vendas — refatoração revisada (operador correto) ===\n")

    demonstracao = [
        Venda("V01",  1_000),
        Venda("V02",  5_000),   # limite exato — deve ser 4%, não 2%
        Venda("V03", 10_000),   # limite exato — deve ser 6%, não 4%
        Venda("V04", 20_000),   # limite exato — deve ser 8%, não 6%
        Venda("V05", 50_000),   # limite exato — deve ser 10%, não 8%
        Venda("V06", 80_000),
    ]

    print(f"  {'Vendedor':<10} {'Valor':>10}  {'Original':>10}  {'Refatorada':>10}  {'Status':>8}")
    print("  " + "-" * 58)
    for venda in demonstracao:
        orig  = calcular_comissao_original(venda)
        refat = calcular_comissao_refatorada(venda)
        status = "OK" if abs(orig - refat) < 0.001 else "DIFERENTE"
        print(f"  {venda.vendedor_id:<10} R${venda.valor:>9,.0f}  R${orig:>9.2f}  R${refat:>9.2f}  {status:>8}")

    print()
    verificar_equivalencia()
