"""
VERSÃO REVISADA — cálculo de preço com descontos após revisão de código gerado por IA
Referência: Clean Code, Cap. 2–3; engenharia de contexto em prompts de código

Problemas corrigidos em relação à versão gerada:
  - Nomes descritivos em português para todos os identificadores
  - Parâmetros soltos substituídos por @dataclass ItemPedido
  - Números mágicos extraídos como constantes nomeadas
  - Regras de desconto separadas em funções próprias
  - Acumulação indevida de descontos eliminada (aplica apenas o maior)
  - Validação com exceção descritiva em vez de comportamento silencioso

Nota didática: mesmo a partir de um prompt estruturado, a IA gerou a
comparação de descontos inline na função principal — foi preciso extrair
`_selecionar_maior_desconto` manualmente para manter a responsabilidade única.

Execute: python3 sessao-5/tutorial-09-engenharia-de-prompt/exemplos/preco_revisado.py
"""

from __future__ import annotations

from dataclasses import dataclass

DESCONTO_VOLUME_PCT = 0.10       # desconto por quantidade elevada
QUANTIDADE_MINIMA_VOLUME = 5     # quantidade mínima para desconto por volume
DESCONTO_PREMIUM_PCT = 0.15      # desconto para itens da categoria premium
SEM_DESCONTO = 0.0               # sentinela para ausência de desconto


@dataclass
class ItemPedido:
    descricao: str
    preco_unitario: float
    quantidade: int
    categoria: str = "padrao"


def _desconto_por_volume(item: ItemPedido) -> float:
    """Retorna o percentual de desconto por volume, ou SEM_DESCONTO."""
    if item.quantidade >= QUANTIDADE_MINIMA_VOLUME:
        return DESCONTO_VOLUME_PCT
    return SEM_DESCONTO


def _desconto_por_categoria(item: ItemPedido) -> float:
    """Retorna o percentual de desconto por categoria, ou SEM_DESCONTO."""
    if item.categoria == "premium":
        return DESCONTO_PREMIUM_PCT
    return SEM_DESCONTO


def _selecionar_maior_desconto(item: ItemPedido) -> float:
    """Retorna o maior desconto aplicável ao item (descontos não se acumulam)."""
    return max(_desconto_por_volume(item), _desconto_por_categoria(item))


def calcular_preco_final(item: ItemPedido) -> float:
    """
    Calcula o preço final do item aplicando o maior desconto elegível.

    Lança ValueError se preco_unitario for menor ou igual a zero.
    """
    if item.preco_unitario <= 0:
        raise ValueError(
            f"Preço unitário inválido para '{item.descricao}': {item.preco_unitario}. "
            "O valor deve ser maior que zero."
        )

    desconto = _selecionar_maior_desconto(item)
    preco_com_desconto = item.preco_unitario * (1 - desconto) * item.quantidade
    return round(preco_com_desconto, 2)


# ─── Execução de demonstração ─────────────────────────────────────────────────

if __name__ == "__main__":
    item_simples = ItemPedido(
        descricao="Camiseta Básica",
        preco_unitario=50.0,
        quantidade=3,
    )
    print("Preço item simples (sem desconto):", calcular_preco_final(item_simples))

    item_volume = ItemPedido(
        descricao="Camiseta Básica",
        preco_unitario=50.0,
        quantidade=6,
    )
    print("Preço com desconto por volume:", calcular_preco_final(item_volume))

    item_premium = ItemPedido(
        descricao="Tênis Premium",
        preco_unitario=200.0,
        quantidade=2,
        categoria="premium",
    )
    print("Preço com desconto premium:", calcular_preco_final(item_premium))

    # volume + premium: aplica apenas o maior (premium = 15% > volume = 10%)
    item_premium_volume = ItemPedido(
        descricao="Tênis Premium",
        preco_unitario=200.0,
        quantidade=6,
        categoria="premium",
    )
    print("Preço premium com volume (aplica apenas o maior):", calcular_preco_final(item_premium_volume))

    # preço inválido — deve lançar exceção
    try:
        item_invalido = ItemPedido(descricao="Produto Inválido", preco_unitario=0.0, quantidade=1)
        calcular_preco_final(item_invalido)
    except ValueError as erro:
        print(f"\nValidação: {erro}")
