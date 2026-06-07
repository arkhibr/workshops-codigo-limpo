"""
Gabarito — Módulo de Carrinho de Compras com Frete (consistente)
Referência: Tutorial 11 — Geração multi-arquivo com agentes
Execute: python3 gabarito_carrinho.py

Correção em relação a exercicio_carrinho.py:
  - fechar_pedido agora chama calcular_total_pedido(pedido.itens, pedido.regiao).
  - O frete da região é calculado e incluído no total retornado.
  - O dict de retorno expõe subtotal, frete e total separadamente.

Diferença cross-file resolvida:
  ANTES: total = _calcular_total_local(pedido.itens)                ← sem frete
  DEPOIS: resultado = calcular_total_pedido(itens, pedido.regiao)   ← com frete
"""

from dataclasses import dataclass, field


# ─── Constantes de frete (replicadas para auto-contenção) ─────────────────────

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


@dataclass
class Pedido:
    id:     str
    itens:  list[ItemPedido] = field(default_factory=list)
    regiao: str              = ""


# ─── Lógica de precificação (alinhada com gabarito_precificacao.py) ───────────

def _subtotal_item(item: ItemPedido) -> float:
    return round(item.preco_unitario * item.quantidade, 2)


def _calcular_frete(subtotal: float, regiao: str) -> float:
    """Cálculo de frete — idêntico a gabarito_precificacao.py."""
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
    regiao: str,              # alinhado com gabarito_precificacao.py
) -> ResultadoPedido:
    """
    Calcula o total incluindo frete.
    Assinatura alinhada com gabarito_precificacao.py: ambos usam (itens, regiao).
    """
    if not itens:
        raise ValueError("A lista de itens não pode ser vazia")
    subtotal = sum(_subtotal_item(i) for i in itens)
    frete = _calcular_frete(subtotal, regiao)
    return ResultadoPedido(
        subtotal=round(subtotal, 2),
        frete=frete,
        total=round(subtotal + frete, 2),
        regiao=regiao,
    )


# ─── Operações de pedido ──────────────────────────────────────────────────────

def adicionar_item(pedido: Pedido, item: ItemPedido) -> None:
    """Adiciona item; acumula quantidade se produto_id já existir."""
    for existente in pedido.itens:
        if existente.produto_id == item.produto_id:
            existente.quantidade += item.quantidade
            return
    pedido.itens.append(item)


def definir_regiao(pedido: Pedido, regiao: str) -> None:
    """Define a região de entrega do pedido."""
    pedido.regiao = regiao.lower().strip()


def fechar_pedido(pedido: Pedido) -> dict:
    """
    Fecha o pedido e retorna um resumo com frete incluído.

    CORREÇÃO: chama calcular_total_pedido(pedido.itens, pedido.regiao) —
    agora passa a região corretamente; o frete é incluído no total.
    """
    resultado = calcular_total_pedido(pedido.itens, pedido.regiao)  # ← correto: passa regiao

    return {
        "pedido_id": pedido.id,
        "qtd_itens": sum(i.quantidade for i in pedido.itens),
        "regiao":    resultado.regiao,
        "subtotal":  resultado.subtotal,
        "frete":     resultado.frete,
        "total":     resultado.total,
    }


def formatar_pedido(pedido: Pedido) -> str:
    """Formata o estado atual do pedido para exibição."""
    linhas = [f"Pedido {pedido.id}:"]
    for item in pedido.itens:
        linhas.append(
            f"  [{item.produto_id}] {item.descricao}: "
            f"R$ {item.preco_unitario:.2f} x {item.quantidade} = "
            f"R$ {_subtotal_item(item):.2f}"
        )
    subtotal = sum(_subtotal_item(i) for i in pedido.itens)
    linhas.append(f"  Subtotal: R$ {subtotal:.2f}")
    if pedido.regiao:
        linhas.append(f"  Região:   {pedido.regiao}")
    return "\n".join(linhas)


# ─── Execução de demonstração ─────────────────────────────────────────────────

if __name__ == "__main__":
    print("=== Carrinho de Compras com Frete (gabarito — total com frete correto) ===\n")

    pedido = Pedido(id="P-2026-042")

    adicionar_item(pedido, ItemPedido("P001", "Teclado mecânico",  89.90, 1))
    adicionar_item(pedido, ItemPedido("P002", "Mouse sem fio",      49.90, 2))

    definir_regiao(pedido, "nordeste")

    print(formatar_pedido(pedido))
    print()

    resumo = fechar_pedido(pedido)
    print("Resumo do pedido:")
    print(f"  Pedido:   {resumo['pedido_id']}")
    print(f"  Itens:    {resumo['qtd_itens']}")
    print(f"  Região:   {resumo['regiao']}")
    print(f"  Subtotal: R$ {resumo['subtotal']:.2f}")
    print(f"  Frete:    R$ {resumo['frete']:.2f}  (nordeste)")
    print(f"  Total:    R$ {resumo['total']:.2f}  <- CORRETO: frete incluído")

    print()

    # Pedido com frete grátis (subtotal > FRETE_GRATIS_ACIMA)
    pedido2 = Pedido(id="P-2026-043")
    adicionar_item(pedido2, ItemPedido("P010", "Monitor 4K 27\"",    1_299.00, 1))
    definir_regiao(pedido2, "sul")

    resumo2 = fechar_pedido(pedido2)
    print(f"Pedido {pedido2.id} — Sul, subtotal R$ {resumo2['subtotal']:.2f}:")
    print(f"  Frete:    R$ {resumo2['frete']:.2f}  (grátis — acima de R$ {FRETE_GRATIS_ACIMA:.2f})")
    print(f"  Total:    R$ {resumo2['total']:.2f}")

    print()
    print("Consistência: calcular_total_pedido(pedido.itens, pedido.regiao) — assinatura alinhada.")
