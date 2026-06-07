"""
Refatoração de IA — Cálculo de Comissão de Vendas com Faixas
Referência: Tutorial 13 — Refatoração assistida avançada
Execute: python3 comissao_gerado.py

Contexto: o código ORIGINAL usava um if/elif em escada para calcular a comissão
por faixas de valor. A IA refatorou para uma tabela de faixas (lista de tuplas),
tornando o código mais legível e extensível.

O código refatorado é idiomático e polido. A verificação de equivalência incluída
cobre apenas casos no meio de cada faixa — e passa. Um caso de fronteira exata
(valor == limite de faixa) silenciosamente mudou de comportamento.
"""

from dataclasses import dataclass
from typing import NamedTuple


# ─── Domínio ──────────────────────────────────────────────────────────────────

@dataclass
class Venda:
    vendedor_id: str
    valor:       float


# ─── Versão ORIGINAL (if/elif em escada) ─────────────────────────────────────

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


# ─── Versão REFATORADA pela IA (tabela de faixas) ────────────────────────────

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
    """Calcula comissão percorrendo a tabela de faixas."""
    for faixa in TABELA_COMISSAO:
        if venda.valor > faixa.limite_inferior:
            return venda.valor * faixa.percentual
    return venda.valor * TABELA_COMISSAO[-1].percentual


# ─── Verificação FRACA (só casos no meio das faixas) ─────────────────────────

def verificar_equivalencia() -> None:
    """
    Compara a versão refatorada contra a original.
    Cobre casos representativos de cada faixa — não inclui os limites exatos.
    """
    casos = [
        Venda("V01",  1_000),   # faixa 0–4999
        Venda("V02",  7_500),   # faixa 5000–9999
        Venda("V03", 15_000),   # faixa 10000–19999
        Venda("V04", 35_000),   # faixa 20000–49999
        Venda("V05", 80_000),   # faixa 50000+
    ]

    print("=== Verificação de equivalência (fraca — só meio das faixas) ===\n")
    todos_ok = True
    for venda in casos:
        esperado = calcular_comissao_original(venda)
        obtido   = calcular_comissao_refatorada(venda)
        if abs(obtido - esperado) < 0.001:
            print(f"  OK: valor={venda.valor:>8.0f}  comissão={obtido:>8.2f}")
        else:
            print(f"  FALHOU: valor={venda.valor:>8.0f}  esperado={esperado:.2f}  obtido={obtido:.2f}")
            todos_ok = False

    print()
    if todos_ok:
        print("Resultado: todos os casos passaram.")
    else:
        print("Resultado: há divergências.")


# ─── Execução de demonstração ─────────────────────────────────────────────────

if __name__ == "__main__":
    print("=== Comissão de Vendas — refatoração de IA (tabela de faixas) ===\n")

    demonstracao = [
        Venda("V01",  1_000),
        Venda("V02",  7_500),
        Venda("V03", 15_000),
        Venda("V04", 35_000),
        Venda("V05", 80_000),
    ]

    print(f"  {'Vendedor':<10} {'Valor':>10}  {'Original':>10}  {'Refatorada':>10}")
    print("  " + "-" * 46)
    for venda in demonstracao:
        orig = calcular_comissao_original(venda)
        refat = calcular_comissao_refatorada(venda)
        print(f"  {venda.vendedor_id:<10} R${venda.valor:>9,.0f}  R${orig:>9.2f}  R${refat:>9.2f}")

    print()
    verificar_equivalencia()
