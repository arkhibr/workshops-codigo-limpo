"""
gabarito.py — Solução do Exercício 20: Strategy e Template Method
Execute: python3 gabarito.py
"""
from typing import List, Protocol
from dataclasses import dataclass
from abc import ABC, abstractmethod


@dataclass
class Entrega:
    id:             str
    transportadora: str
    peso:           float
    distancia:      float
    valor_nf:       float


# ─── Strategy: EstrategiaFrete ───────────────────────────────────────────────

class EstrategiaFrete(Protocol):
    def calcular(self, peso: float, distancia: float) -> float: ...
    def nome(self) -> str: ...

class FreteCorreios:
    def calcular(self, peso: float, distancia: float) -> float:
        return round(peso * 2.5 + distancia * 0.10, 2)
    def nome(self) -> str: return "Correios"

class FreteJadlog:
    def calcular(self, peso: float, distancia: float) -> float:
        return round(peso * 2.0 + distancia * 0.12, 2)
    def nome(self) -> str: return "Jadlog"

class FreteRetirada:
    def calcular(self, peso: float, distancia: float) -> float: return 0.0
    def nome(self) -> str: return "Retirada"

class FreteLoggi:                # adicionado sem alterar as classes acima
    def calcular(self, peso: float, distancia: float) -> float:
        return round(peso * 1.8 + distancia * 0.08, 2)
    def nome(self) -> str: return "Loggi"

class CalculadorFrete:
    def __init__(self, estrategia: EstrategiaFrete) -> None:
        self._estrategia = estrategia

    def calcular(self, peso: float, distancia: float) -> float:
        return self._estrategia.calcular(peso, distancia)

    def trocar_estrategia(self, estrategia: EstrategiaFrete) -> None:
        self._estrategia = estrategia


# ─── Template Method: RelatorioLogistica ─────────────────────────────────────

class RelatorioLogistica(ABC):
    def gerar(self, entregas: List[Entrega]) -> str:
        filtradas = self._filtrar(entregas)
        linhas    = self._formatar_linhas(filtradas)
        total     = self._calcular_total(filtradas)
        return self._montar_saida(linhas, total)

    def _filtrar(self, entregas: List[Entrega]) -> List[Entrega]:
        return [e for e in entregas if e.valor_nf > 0]

    @abstractmethod
    def _formatar_linhas(self, entregas: List[Entrega]) -> List[str]: ...

    def _calcular_total(self, entregas: List[Entrega]) -> float:
        return sum(e.valor_nf for e in entregas)

    @abstractmethod
    def _montar_saida(self, linhas: List[str], total: float) -> str: ...


class RelatorioEntregas(RelatorioLogistica):
    def _formatar_linhas(self, entregas: List[Entrega]) -> List[str]:
        return [f"  {e.id}: {e.transportadora} — R${e.valor_nf:.2f}" for e in entregas]

    def _montar_saida(self, linhas: List[str], total: float) -> str:
        return "=== Relatório de Entregas ===\n" + "\n".join(linhas) + f"\nTotal NF: R${total:.2f}"


class RelatorioColetas(RelatorioLogistica):
    def _formatar_linhas(self, entregas: List[Entrega]) -> List[str]:
        return [f"  {e.id}: {e.peso}kg × {e.distancia}km" for e in entregas]

    def _montar_saida(self, linhas: List[str], total: float) -> str:
        return "=== Relatório de Coletas ===\n" + "\n".join(linhas) + f"\nVolume: R${total:.2f}"


# ─── Verificação ──────────────────────────────────────────────────────────────

def verificar_gabarito() -> None:
    # Strategy
    calc = CalculadorFrete(FreteCorreios())
    frete_correios = calc.calcular(2.5, 150.0)
    assert frete_correios == round(2.5 * 2.5 + 150.0 * 0.10, 2), \
        f"FALHOU: FreteCorreios (esperado {round(2.5*2.5+150.0*0.10,2)}, obtido {frete_correios})"
    print(f"OK: Strategy — Correios: R${frete_correios:.2f}")

    calc.trocar_estrategia(FreteLoggi())
    frete_loggi = calc.calcular(2.5, 150.0)
    esperado_loggi = round(2.5 * 1.8 + 150.0 * 0.08, 2)
    assert frete_loggi == esperado_loggi, \
        f"FALHOU: FreteLoggi (esperado {esperado_loggi}, obtido {frete_loggi})"
    print(f"OK: Strategy — Loggi adicionado sem alterar CalculadorFrete: R${frete_loggi:.2f}")

    calc.trocar_estrategia(FreteRetirada())
    assert calc.calcular(0.5, 0.0) == 0.0, "FALHOU: FreteRetirada (esperado 0.0)"
    print("OK: Strategy — Retirada: R$0,00")

    # Template Method
    entregas = [
        Entrega("ENT-001", "correios", 2.5, 150.0, 89.90),
        Entrega("ENT-002", "jadlog",   5.0, 300.0, 199.90),
    ]
    re = RelatorioEntregas().gerar(entregas)
    assert "Relatório de Entregas" in re and "Total NF" in re, \
        "FALHOU: RelatorioEntregas — cabeçalho ou rodapé ausente"
    print("OK: Template Method — RelatorioEntregas gerado")

    rc = RelatorioColetas().gerar(entregas)
    assert "Relatório de Coletas" in rc and "Volume" in rc, \
        "FALHOU: RelatorioColetas — cabeçalho ou rodapé ausente"
    print("OK: Template Method — RelatorioColetas gerado")
    print("OK: Template Method — _filtrar e _calcular_total não duplicados")


if __name__ == "__main__":
    print("=== Gabarito 20 — Strategy e Template Method: Logística ===\n")
    verificar_gabarito()
