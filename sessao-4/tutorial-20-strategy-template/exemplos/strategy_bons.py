"""
strategy_bons.py — Strategy para algoritmo variável + Template Method para esqueleto fixo.
Execute: python3 strategy_bons.py
"""
from typing import List, Protocol
from dataclasses import dataclass
from abc import ABC, abstractmethod


# ─── Strategy ─────────────────────────────────────────────────────────────────

class EstrategiaImposto(Protocol):
    def calcular(self, valor: float) -> float: ...
    def nome(self) -> str: ...

class SimplesNacional:
    def calcular(self, valor: float) -> float: return round(valor * 0.06, 2)
    def nome(self) -> str: return "Simples Nacional"

class LucroPresumido:
    def calcular(self, valor: float) -> float: return round(valor * 0.132, 2)
    def nome(self) -> str: return "Lucro Presumido"

class LucroReal:
    def calcular(self, valor: float) -> float: return round(valor * 0.34, 2)
    def nome(self) -> str: return "Lucro Real"

class MEI:                          # adicionado sem alterar as classes acima
    def calcular(self, valor: float) -> float: return round(valor * 0.05, 2)
    def nome(self) -> str: return "MEI"

class CalculadorImposto:
    def __init__(self, estrategia: EstrategiaImposto) -> None:
        self._estrategia = estrategia

    def calcular(self, valor: float) -> float:
        return self._estrategia.calcular(valor)

    def trocar_estrategia(self, estrategia: EstrategiaImposto) -> None:
        self._estrategia = estrategia


# ─── Template Method ──────────────────────────────────────────────────────────

@dataclass
class DadosVenda:
    produto:    str
    valor:      float
    quantidade: int

class RelatorioBase(ABC):
    def gerar(self, dados: List[DadosVenda]) -> str:  # template method
        filtrados = self._filtrar(dados)
        linhas    = self._formatar_linhas(filtrados)
        total     = self._calcular_total(filtrados)
        return self._montar_saida(linhas, total)

    def _filtrar(self, dados: List[DadosVenda]) -> List[DadosVenda]:
        return [d for d in dados if d.valor > 0]

    @abstractmethod
    def _formatar_linhas(self, dados: List[DadosVenda]) -> List[str]: ...

    def _calcular_total(self, dados: List[DadosVenda]) -> float:
        return sum(d.valor * d.quantidade for d in dados)

    @abstractmethod
    def _montar_saida(self, linhas: List[str], total: float) -> str: ...

class RelatorioVendas(RelatorioBase):
    def _formatar_linhas(self, dados: List[DadosVenda]) -> List[str]:
        return [f"  {d.produto}: {d.quantidade} × R${d.valor:.2f}" for d in dados]

    def _montar_saida(self, linhas: List[str], total: float) -> str:
        return "=== Relatório de Vendas ===\n" + "\n".join(linhas) + f"\nTotal: R${total:.2f}"

class RelatorioFinanceiro(RelatorioBase):
    def _formatar_linhas(self, dados: List[DadosVenda]) -> List[str]:
        return [f"  R${d.valor * d.quantidade:.2f} ({d.produto})" for d in dados]

    def _montar_saida(self, linhas: List[str], total: float) -> str:
        return "=== Relatório Financeiro ===\n" + "\n".join(linhas) + f"\nReceita: R${total:.2f}"


# ─── Verificação ──────────────────────────────────────────────────────────────

def verificar_strategy() -> None:
    calc = CalculadorImposto(SimplesNacional())
    assert calc.calcular(10000.0) == 600.0
    print("OK: Strategy — SimplesNacional: R$600,00")

    calc.trocar_estrategia(LucroReal())
    assert calc.calcular(10000.0) == 3400.0
    print("OK: Strategy — LucroReal trocado em runtime: R$3.400,00")

    calc.trocar_estrategia(MEI())
    assert calc.calcular(10000.0) == 500.0
    print("OK: Strategy — MEI adicionado sem alterar CalculadorImposto: R$500,00")

def verificar_template() -> None:
    dados = [DadosVenda("Webcam HD", 299.90, 2), DadosVenda("Teclado", 189.90, 1)]

    rv = RelatorioVendas().gerar(dados)
    assert "Relatório de Vendas" in rv and "Total" in rv
    print("OK: Template Method — RelatorioVendas gerado")

    rf = RelatorioFinanceiro().gerar(dados)
    assert "Relatório Financeiro" in rf and "Receita" in rf
    print("OK: Template Method — RelatorioFinanceiro gerado")
    print("OK: Template Method — _filtrar e _calcular_total não duplicados")


if __name__ == "__main__":
    print("=== Strategy _bons — Strategy + Template Method ===\n")
    verificar_strategy()
    print()
    verificar_template()
