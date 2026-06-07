"""
Gabarito — Módulo de Precificação com Frete (consistente)
Referência: Tutorial 11 — Geração multi-arquivo com agentes
Execute: python3 gabarito_precificacao.py

Este arquivo é idêntico a exercicio_precificacao.py — a assinatura de
calcular_total_pedido já estava correta no exercício. A correção necessária
estava em exercicio_carrinho.py (fechar_pedido), que precisava passar 'regiao'.
"""

from dataclasses import dataclass


# ─── Constantes de frete ──────────────────────────────────────────────────────

FRETE_POR_REGIAO: dict[str, float] = {
    "sudeste":    15.90,
    "sul":        18.90,
    "nordeste":   29.90,
    "norte":      39.90,
    "centroeste": 24.90,
}

FRETE_GRATIS_ACIMA: float = 299.00


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
    regiao: str,
) -> ResultadoPedido:
    """
    Calcula o total do pedido incluindo frete.
    Alinhado com gabarito_carrinho.py: ambos os arquivos usam (itens, regiao).
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
        linhas.append(f"  Frete:    grátis (acima de R$ {FRETE_GRATIS_ACIMA:.2f})")
    else:
        linhas.append(f"  Frete:    R$ {resultado.frete:7.2f}")
    linhas.append(f"  Total:    R$ {resultado.total:7.2f}")
    return "\n".join(linhas)


# ─── Execução de demonstração ─────────────────────────────────────────────────

if __name__ == "__main__":
    print("=== Precificação com Frete (gabarito — consistente com gabarito_carrinho.py) ===\n")

    itens: list[ItemPedido] = [
        ItemPedido("P001", "Teclado mecânico",  89.90, 1),
        ItemPedido("P002", "Mouse sem fio",      49.90, 2),
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

    # Região inválida → ValueError
    try:
        calcular_total_pedido(itens, "marte")
    except ValueError as erro:
        print(f"Região inválida → ValueError: {erro}")

    print()
    print("Consistência: gabarito_carrinho.py chama calcular_total_pedido(itens, pedido.regiao).")
