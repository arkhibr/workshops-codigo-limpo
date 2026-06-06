"""
MÓDULO DE DASHBOARD DE VENDAS — versão consolidada após revisão de deriva
Referência: Clean Code, Cap. 1 e 17; Regra do Escoteiro

Sinais de deriva eliminados em relação ao exercício:
  - Duplicação removida: getTotal() e calcular_soma_vendas() eliminadas;
    calcular_total_periodo() é a única função de cálculo de total.
  - Estilo unificado: todos os nomes em snake_case português com type hints.
  - Dependência desnecessária removida: UtilPercentual substituído por
    f-string nativa (stdlib resolve sem dependência externa).
  - Formatação unificada: espaçamento, assinaturas e estilo consistentes.

Execute: python3 sessao-6/tutorial-15-manutenibilidade-agentes/exercicios/gabarito.py
"""

from __future__ import annotations

META_MENSAL = 10_000.0  # valor-alvo de vendas por mês


# ── Funções de cálculo ────────────────────────────────────────────────────────

def calcular_total_periodo(vendas: list[dict]) -> float:
    """Retorna a soma dos valores das vendas no período."""
    return sum(v["valor"] for v in vendas)


def calcular_percentual_meta(total: float) -> float:
    """Retorna o percentual atingido em relação à meta mensal."""
    if META_MENSAL == 0:
        return 0.0
    return total / META_MENSAL


# ── Formatação ────────────────────────────────────────────────────────────────

def formatar_reais(valor: float) -> str:
    """Formata um número como moeda brasileira usando a stdlib."""
    formatado = f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return f"R$ {formatado}"


def formatar_percentual(valor: float) -> str:
    """Formata um número fracionário como percentual com uma casa decimal."""
    return f"{valor * 100:.1f}%"


# ── Dashboard ─────────────────────────────────────────────────────────────────

def exibir_dashboard(vendas: list[dict], periodo: str = "Período Atual") -> None:
    """Imprime o dashboard de vendas com total, percentual de meta e status."""
    total = calcular_total_periodo(vendas)
    percentual = calcular_percentual_meta(total)

    print(f"=== Dashboard: {periodo} ===")
    print(f"Vendas registradas: {len(vendas)}")
    print(f"Total: {formatar_reais(total)}")
    print(f"Meta atingida: {formatar_percentual(percentual)}")

    if total >= META_MENSAL:
        print("STATUS: META ATINGIDA")
    else:
        faltam = META_MENSAL - total
        print(f"STATUS: faltam {formatar_reais(faltam)}")


# ── Execução de demonstração ──────────────────────────────────────────────────

if __name__ == "__main__":
    vendas_fevereiro = [
        {"descricao": "Produto A", "valor": 3200.00},
        {"descricao": "Produto B", "valor": 1750.00},
        {"descricao": "Produto C", "valor": 4100.00},
    ]

    exibir_dashboard(vendas_fevereiro, "Fevereiro/2026")
    print()
    print("calcular_total_periodo:", calcular_total_periodo(vendas_fevereiro))
