"""
EXERCÍCIO 20 — Strategy e Template Method
Tempo estimado: 20 minutos

INSTRUÇÕES:
  O código abaixo tem dois problemas:
  1. calcular_frete() usa if/elif — adicionar transportadora exige alterar a função.
  2. RelatorioEntregas e RelatorioColetas duplicam o esqueleto de 4 etapas.

  1. Refatore calcular_frete() para Strategy: crie uma interface/protocolo
     EstrategiaFrete com calcular(peso, distancia) e classes concretas.
  2. Refatore os relatórios para Template Method: extraia a classe base
     RelatorioLogistica. Deixe _filtrar() e _calcular_total() com implementação
     padrão na base. Torne apenas _formatar_linhas() e _montar_saida() abstratos
     — são as etapas que diferem entre relatórios.
  3. Execute: python3 exercicio.py (deve rodar antes e depois)
"""
from typing import List
from dataclasses import dataclass


@dataclass
class Entrega:
    id:             str
    transportadora: str
    peso:           float    # kg
    distancia:      float    # km
    valor_nf:       float


def calcular_frete(transportadora: str, peso: float, distancia: float) -> float:
    """Adicionar 'loggi' exige alterar esta função."""
    if transportadora == "correios":
        return round(peso * 2.5 + distancia * 0.10, 2)
    elif transportadora == "jadlog":
        return round(peso * 2.0 + distancia * 0.12, 2)
    elif transportadora == "retirada":
        return 0.0
    else:
        raise ValueError(f"Transportadora desconhecida: {transportadora}")


class RelatorioEntregas:
    def gerar(self, entregas: List[Entrega]) -> str:
        # Etapa 1: filtrar apenas entregas com valor
        filtradas = [e for e in entregas if e.valor_nf > 0]
        # Etapa 2: formatar linhas (DUPLICADO em RelatorioColetas)
        linhas = [f"  {e.id}: {e.transportadora} — R${e.valor_nf:.2f}" for e in filtradas]
        # Etapa 3: calcular total (DUPLICADO)
        total = sum(e.valor_nf for e in filtradas)
        # Etapa 4: montar saída (DUPLICADO)
        return "=== Relatório de Entregas ===\n" + "\n".join(linhas) + f"\nTotal NF: R${total:.2f}"


class RelatorioColetas:
    def gerar(self, entregas: List[Entrega]) -> str:
        # Etapa 1: filtrar (DUPLICADO)
        filtradas = [e for e in entregas if e.valor_nf > 0]
        # Etapa 2: formatar linhas — diferença real está aqui
        linhas = [f"  {e.id}: {e.peso}kg × {e.distancia}km" for e in filtradas]
        # Etapa 3: calcular total (DUPLICADO)
        total = sum(e.valor_nf for e in filtradas)
        # Etapa 4: montar saída (DUPLICADO)
        return "=== Relatório de Coletas ===\n" + "\n".join(linhas) + f"\nVolume: R${total:.2f}"


if __name__ == "__main__":
    entregas = [
        Entrega("ENT-001", "correios",  2.5, 150.0, 89.90),
        Entrega("ENT-002", "jadlog",    5.0, 300.0, 199.90),
        Entrega("ENT-003", "retirada",  0.5, 0.0,   49.90),
    ]
    for e in entregas:
        frete = calcular_frete(e.transportadora, e.peso, e.distancia)
        print(f"{e.id}: frete R${frete:.2f}")

    print("\n" + RelatorioEntregas().gerar(entregas))
    print("\n" + RelatorioColetas().gerar(entregas))
