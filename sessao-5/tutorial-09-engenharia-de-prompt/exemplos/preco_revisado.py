"""
Revisão corrigida — Cálculo de Preço com Descontos
Referência: Tutorial 09 — Engenharia de contexto e prompt para gerar código
Execute: python3 preco_revisado.py

Correção aplicada em relação a preco_gerado.py:
  - Regra de negócio restaurada: aplica apenas o MAIOR desconto disponível,
    não a composição multiplicativa dos dois.
  - Constantes de faixa de volume nomeadas e consistentes.
  - Demo idêntico ao gerado — resultado agora correto.
"""

from dataclasses import dataclass


# ─── Constantes de domínio ────────────────────────────────────────────────────

DESCONTO_VOLUME_MEDIO      = 0.05   # 5 % para 10–49 unidades
DESCONTO_VOLUME_ALTO       = 0.10   # 10 % para 50+ unidades
DESCONTO_CATEGORIA_PREMIUM = 0.15   # 15 % para categoria "premium"

LIMIAR_VOLUME_MEDIO = 10
LIMIAR_VOLUME_ALTO  = 50


# ─── Entidade ─────────────────────────────────────────────────────────────────

@dataclass
class ItemPedido:
    produto_id:  str
    categoria:   str
    preco_unit:  float
    quantidade:  int


# ─── Cálculo de preço ─────────────────────────────────────────────────────────

def calcular_desconto_volume(quantidade: int) -> float:
    """Retorna o percentual de desconto por volume (0.0 a 1.0)."""
    if quantidade >= LIMIAR_VOLUME_ALTO:
        return DESCONTO_VOLUME_ALTO
    if quantidade >= LIMIAR_VOLUME_MEDIO:
        return DESCONTO_VOLUME_MEDIO
    return 0.0


def calcular_desconto_categoria(categoria: str) -> float:
    """Retorna o percentual de desconto por categoria (0.0 a 1.0)."""
    if categoria == "premium":
        return DESCONTO_CATEGORIA_PREMIUM
    return 0.0


def calcular_preco_final(item: ItemPedido) -> float:
    """
    Calcula o preço final do item aplicando os descontos disponíveis.

    Regra de negócio: vale o MAIOR desconto — apenas um é aplicado.
    Se o item for premium (15%) e tiver volume alto (10%), aplica 15%.
    """
    subtotal = item.preco_unit * item.quantidade

    desconto_volume    = calcular_desconto_volume(item.quantidade)
    desconto_categoria = calcular_desconto_categoria(item.categoria)

    # Regra correta: seleciona o MAIOR desconto disponível.
    melhor_desconto = max(desconto_volume, desconto_categoria)
    return subtotal * (1.0 - melhor_desconto)


def formatar_resultado(item: ItemPedido, preco_final: float) -> str:
    subtotal = item.preco_unit * item.quantidade
    economia = subtotal - preco_final
    return (
        f"  {item.produto_id} ({item.categoria}): "
        f"subtotal=R${subtotal:.2f}  final=R${preco_final:.2f}  "
        f"economia=R${economia:.2f}"
    )


# ─── Execução de demonstração ─────────────────────────────────────────────────

if __name__ == "__main__":
    print("=== Cálculo de Preço (revisado — regra de negócio correta) ===\n")

    itens = [
        ItemPedido("P001", "eletronicos",  100.00,  5),   # sem desconto
        ItemPedido("P002", "eletronicos",  100.00, 20),   # só volume médio (5%)
        ItemPedido("P003", "premium",      200.00,  3),   # só categoria (15%)
        ItemPedido("P004", "premium",      200.00, 60),   # maior = categoria (15%)
    ]

    for item in itens:
        preco = calcular_preco_final(item)
        print(formatar_resultado(item, preco))

    print()
    print("Caso crítico — P004 (premium, 60 unidades):")
    item_critico = itens[3]
    subtotal = item_critico.preco_unit * item_critico.quantidade
    preco_correto = calcular_preco_final(item_critico)
    preco_esperado = subtotal * (1.0 - DESCONTO_CATEGORIA_PREMIUM)  # maior desconto = 15%
    print(f"  subtotal             = R${subtotal:.2f}")
    print(f"  desconto maior (15%) = R${subtotal * DESCONTO_CATEGORIA_PREMIUM:.2f}")
    print(f"  preço esperado       = R${preco_esperado:.2f}")
    print(f"  preço calculado      = R${preco_correto:.2f}  ← CORRETO")
