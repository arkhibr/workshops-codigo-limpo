"""
Versão revisada — Módulo de Precificação com Cupom (consistente)
Referência: Tutorial 11 — Geração multi-arquivo com agentes
Execute: python3 precificacao.py

Correção em relação a gerado/precificacao.py:
  Nenhuma — a assinatura de calcular_total estava correta no arquivo gerado.
  A revisão consiste em garantir que carrinho.py (o chamador) seja atualizado
  para passar o argumento 'cupom' — tornando os dois arquivos consistentes.

Diferença cross-file resolvida:
  ANTES (gerado): carrinho.py chamava calcular_total(itens)   ← faltava cupom
  DEPOIS (revisado): carrinho.py chama calcular_total(itens, cupom)  ← correto
"""

from dataclasses import dataclass
from typing import Optional


# ─── Entidades ────────────────────────────────────────────────────────────────

@dataclass
class ItemCarrinho:
    produto_id:     str
    descricao:      str
    preco_unitario: float
    quantidade:     int


@dataclass
class Cupom:
    codigo:              str
    percentual_desconto: float  # 0.0 a 1.0

    def __post_init__(self) -> None:
        if not (0.0 <= self.percentual_desconto <= 1.0):
            raise ValueError(
                f"percentual_desconto deve estar entre 0.0 e 1.0 "
                f"(recebido: {self.percentual_desconto})"
            )


# ─── Constantes ───────────────────────────────────────────────────────────────

CUPONS_VALIDOS: dict[str, Cupom] = {
    "BEMVINDO10":    Cupom(codigo="BEMVINDO10",    percentual_desconto=0.10),
    "BLACKFRIDAY20": Cupom(codigo="BLACKFRIDAY20", percentual_desconto=0.20),
}


# ─── Operações de precificação ────────────────────────────────────────────────

def subtotal_item(item: ItemCarrinho) -> float:
    """Retorna preço unitário × quantidade, arredondado em 2 casas."""
    return round(item.preco_unitario * item.quantidade, 2)


def resolver_cupom(codigo: str) -> Optional[Cupom]:
    """
    Resolve um código de cupom para o objeto Cupom correspondente.
    Retorna None se o código for inválido ou inativo.
    """
    return CUPONS_VALIDOS.get(codigo.upper())


def calcular_total(
    itens: list[ItemCarrinho],
    cupom: Optional[Cupom],   # parâmetro obrigatório — sem valor padrão
) -> float:
    """
    Calcula o valor total aplicando desconto do cupom.

    Levanta ValueError se a lista estiver vazia.
    cupom=None → sem desconto.
    """
    if not itens:
        raise ValueError("A lista de itens não pode ser vazia")

    bruto = sum(subtotal_item(i) for i in itens)

    if cupom is None:
        return round(bruto, 2)

    valor_desconto = round(bruto * cupom.percentual_desconto, 2)
    return round(bruto - valor_desconto, 2)


def formatar_resumo(
    itens: list[ItemCarrinho],
    cupom: Optional[Cupom],
) -> str:
    """Formata linha de resumo com subtotal, desconto e total."""
    bruto = sum(subtotal_item(i) for i in itens)
    total = calcular_total(itens, cupom)
    if cupom is not None:
        desconto = round(bruto - total, 2)
        return (
            f"Subtotal: R$ {bruto:7.2f} | "
            f"Desconto {cupom.codigo} (-{cupom.percentual_desconto:.0%}): "
            f"-R$ {desconto:.2f} | "
            f"Total: R$ {total:7.2f}"
        )
    return f"Subtotal: R$ {bruto:7.2f} | Total: R$ {total:7.2f}"


# ─── Execução de demonstração ─────────────────────────────────────────────────

if __name__ == "__main__":
    print("=== Precificação (revisado — consistente com carrinho.py) ===\n")

    itens_demo: list[ItemCarrinho] = [
        ItemCarrinho("P001", "Teclado mecânico",  349.90, 1),
        ItemCarrinho("P002", "Mouse sem fio",       89.90, 2),
        ItemCarrinho("P003", "Mousepad XL",          49.90, 1),
    ]

    print("Itens do carrinho:")
    for item in itens_demo:
        print(f"  {item.descricao}: R$ {item.preco_unitario:.2f} x {item.quantidade}"
              f" = R$ {subtotal_item(item):.2f}")
    print()

    # Sem cupom
    print(formatar_resumo(itens_demo, None))

    # Com cupom BEMVINDO10 (10%)
    cupom_bv = resolver_cupom("BEMVINDO10")
    print(formatar_resumo(itens_demo, cupom_bv))

    # Com cupom BLACKFRIDAY20 (20%)
    cupom_bf = resolver_cupom("BLACKFRIDAY20")
    print(formatar_resumo(itens_demo, cupom_bf))

    # Cupom inválido → None → sem desconto
    cupom_inv = resolver_cupom("INVALIDO")
    print(f"Cupom 'INVALIDO' → {cupom_inv!r} → sem desconto")
    print(formatar_resumo(itens_demo, cupom_inv))

    print()
    print("Consistência: carrinho.py chama calcular_total(itens, cupom) — assinatura alinhada.")
