"""
Exercício — Módulo de Precificação com Frete (saída de agente com inconsistência)
Referência: Tutorial 11 — Geração multi-arquivo com agentes
Execute: python3 exercicio_precificacao.py

INSTRUÇÕES:
  (1) Execute este arquivo e exercicio_carrinho.py separadamente — ambos rodam sem erro.
  (2) Revise o diff entre os dois arquivos como se estivesse revisando uma mudança
      de agente em altitude: olhe os dois juntos, não isoladamente.
  (3) Ache a inconsistência cross-file: onde a assinatura mudou mas o chamador não acompanhou?
  (4) Corrija a mudança e compare com gabarito_carrinho.py e gabarito_precificacao.py.

CONTEXTO: o agente recebeu a tarefa "adicionar cálculo de frete ao pedido".
Ele atualizou ESTE arquivo corretamente: calcular_total_pedido agora recebe
'regiao: str' como segundo argumento obrigatório e retorna um ResultadoPedido
com subtotal, frete e total discriminados.

Veja exercicio_carrinho.py para encontrar onde o chamador não foi atualizado.
"""

from dataclasses import dataclass
from typing import Optional


# ─── Constantes de frete ──────────────────────────────────────────────────────

FRETE_POR_REGIAO: dict[str, float] = {
    "sudeste": 15.90,
    "sul":     18.90,
    "nordeste": 29.90,
    "norte":   39.90,
    "centroeste": 24.90,
}

FRETE_GRATIS_ACIMA: float = 299.00   # frete grátis para pedidos acima deste valor


# ─── Entidades ────────────────────────────────────────────────────────────────

@dataclass
class ItemPedido:
    produto_id:     str
    descricao:      str
    preco_unitario: float
    quantidade:     int


@dataclass
class ResultadoPedido:
    subtotal: float
    frete:    float
    total:    float
    regiao:   str


# ─── Operações de precificação ────────────────────────────────────────────────

def subtotal_item(item: ItemPedido) -> float:
    """Retorna preço unitário × quantidade, arredondado em 2 casas."""
    return round(item.preco_unitario * item.quantidade, 2)


def calcular_frete(subtotal: float, regiao: str) -> float:
    """
    Calcula o valor de frete para a região informada.

    Frete grátis se subtotal >= FRETE_GRATIS_ACIMA.
    Levanta ValueError para região desconhecida.
    """
    regiao_norm = regiao.lower().strip()
    if regiao_norm not in FRETE_POR_REGIAO:
        regioes = ", ".join(sorted(FRETE_POR_REGIAO))
        raise ValueError(
            f"Região desconhecida: '{regiao}'. Regiões válidas: {regioes}"
        )
    if subtotal >= FRETE_GRATIS_ACIMA:
        return 0.0
    return FRETE_POR_REGIAO[regiao_norm]


def calcular_total_pedido(
    itens: list[ItemPedido],
    regiao: str,              # ← NOVO parâmetro — agente adicionou; obrigatório
) -> ResultadoPedido:
    """
    Calcula o total do pedido incluindo frete.

    MUDANÇA: 'regiao' foi adicionado nesta iteração do agente.
    exercicio_carrinho.py ainda chama calcular_total_pedido(itens) sem 'regiao'.
    ⚠️  INCONSISTÊNCIA CROSS-FILE: a assinatura mudou aqui mas não nos chamadores.
    """
    if not itens:
        raise ValueError("A lista de itens não pode ser vazia")

    subtotal = sum(subtotal_item(i) for i in itens)
    frete = calcular_frete(subtotal, regiao)
    total = round(subtotal + frete, 2)

    return ResultadoPedido(
        subtotal=round(subtotal, 2),
        frete=frete,
        total=total,
        regiao=regiao,
    )


def formatar_resultado(resultado: ResultadoPedido) -> str:
    """Formata o resultado do pedido para exibição."""
    linhas = [
        f"  Região:   {resultado.regiao}",
        f"  Subtotal: R$ {resultado.subtotal:7.2f}",
    ]
    if resultado.frete == 0.0:
        linhas.append(f"  Frete:    R$ {'0.00':>7}  (grátis — pedido acima de R$ {FRETE_GRATIS_ACIMA:.2f})")
    else:
        linhas.append(f"  Frete:    R$ {resultado.frete:7.2f}")
    linhas.append(f"  Total:    R$ {resultado.total:7.2f}")
    return "\n".join(linhas)


# ─── Execução de demonstração ─────────────────────────────────────────────────

if __name__ == "__main__":
    print("=== Precificação com Frete (exercício — assinatura nova) ===\n")

    itens: list[ItemPedido] = [
        ItemPedido("P001", "Teclado mecânico",  89.90, 1),
        ItemPedido("P002", "Mouse sem fio",       49.90, 2),
    ]

    print("Itens do pedido:")
    for item in itens:
        print(f"  {item.descricao}: R$ {item.preco_unitario:.2f} x {item.quantidade}"
              f" = R$ {subtotal_item(item):.2f}")
    print()

    # Pedido para o Nordeste (subtotal < 299 → frete cobrado)
    resultado_ne = calcular_total_pedido(itens, "nordeste")
    print("Pedido — Nordeste:")
    print(formatar_resultado(resultado_ne))

    print()

    # Pedido para o Sudeste (subtotal < 299 → frete cobrado)
    resultado_se = calcular_total_pedido(itens, "sudeste")
    print("Pedido — Sudeste:")
    print(formatar_resultado(resultado_se))

    print()
    print("Assinatura NOVA (este arquivo): calcular_total_pedido(itens, regiao)")
    print("Veja exercicio_carrinho.py para encontrar onde o chamador não foi atualizado.")
