"""
strategy_ruins.py — if/elif de algoritmo + esqueleto duplicado.
Execute: python3 strategy_ruins.py
"""
from typing import List
from dataclasses import dataclass


# ─── Sem Strategy: if/elif cresce a cada novo regime ─────────────────────────

def calcular_imposto(regime: str, valor: float) -> float:
    """Adicionar 'MEI' exige alterar esta função."""
    if regime == "simples":
        return round(valor * 0.06, 2)
    elif regime == "presumido":
        return round(valor * 0.132, 2)   # IRPJ+CSLL+PIS+COFINS simplificado
    elif regime == "real":
        return round(valor * 0.34, 2)
    else:
        raise ValueError(f"Regime desconhecido: {regime}")


# ─── Sem Template Method: esqueleto duplicado em duas classes ─────────────────

@dataclass
class DadosVenda:
    produto:    str
    valor:      float
    quantidade: int

class RelatorioVendas:
    def gerar(self, dados: List[DadosVenda]) -> str:
        # Etapa 1: filtrar
        filtrados = [d for d in dados if d.valor > 0]
        # Etapa 2: formatar linhas (DUPLICADO em RelatorioFinanceiro)
        linhas = [f"  {d.produto}: {d.quantidade} × R${d.valor:.2f}" for d in filtrados]
        # Etapa 3: calcular totais (DUPLICADO)
        total = sum(d.valor * d.quantidade for d in filtrados)
        # Etapa 4: montar saída (DUPLICADO)
        return "=== Relatório de Vendas ===\n" + "\n".join(linhas) + f"\nTotal: R${total:.2f}"

class RelatorioFinanceiro:
    def gerar(self, dados: List[DadosVenda]) -> str:
        # Etapa 1: filtrar (DUPLICADO)
        filtrados = [d for d in dados if d.valor > 0]
        # Etapa 2: formatar linhas — única diferença real
        linhas = [f"  R${d.valor * d.quantidade:.2f} ({d.produto})" for d in filtrados]
        # Etapa 3: calcular totais (DUPLICADO)
        total = sum(d.valor * d.quantidade for d in filtrados)
        # Etapa 4: montar saída (DUPLICADO)
        return "=== Relatório Financeiro ===\n" + "\n".join(linhas) + f"\nReceita: R${total:.2f}"


if __name__ == "__main__":
    print("=== Strategy _ruins ===\n")
    for regime in ["simples", "presumido", "real"]:
        imp = calcular_imposto(regime, 10000.0)
        print(f"  {regime}: R${imp:.2f}")

    dados = [DadosVenda("Webcam HD", 299.90, 2), DadosVenda("Teclado", 189.90, 1)]
    print("\n" + RelatorioVendas().gerar(dados))
    print("\n" + RelatorioFinanceiro().gerar(dados))
