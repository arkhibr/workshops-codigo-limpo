"""
Versão revisada — Módulo de Carrinho de Compras (consistente)
Referência: Tutorial 11 — Geração multi-arquivo com agentes
Execute: python3 carrinho.py

Correção em relação a gerado/carrinho.py:
  - finalizar_carrinho agora passa o cupom do carrinho para calcular_total.
  - A assinatura de calcular_total (em precificacao.py) exige 'cupom' como
    segundo argumento; esta versão fornece corretamente o argumento.
  - O desconto do cupom é refletido no total — inconsistência resolvida.

Diferença cross-file resolvida:
  ANTES: total = _calcular_total_local(carrinho.itens)      ← ignorava cupom
  DEPOIS: total = calcular_total(carrinho.itens, carrinho.cupom)  ← correto
"""

from dataclasses import dataclass, field
from typing import Optional


# ─── Entidades (replicadas para auto-contenção deste arquivo) ────────────────

@dataclass
class ItemCarrinho:
    produto_id:     str
    descricao:      str
    preco_unitario: float
    quantidade:     int


@dataclass
class Cupom:
    codigo:              str
    percentual_desconto: float

    def __post_init__(self) -> None:
        if not (0.0 <= self.percentual_desconto <= 1.0):
            raise ValueError(
                f"percentual_desconto deve estar entre 0.0 e 1.0 "
                f"(recebido: {self.percentual_desconto})"
            )


@dataclass
class Carrinho:
    id:    str
    itens: list[ItemCarrinho] = field(default_factory=list)
    cupom: Optional[Cupom]   = None


# ─── Lógica de precificação (versão local — alinhada com precificacao.py) ─────

def _subtotal_item(item: ItemCarrinho) -> float:
    return round(item.preco_unitario * item.quantidade, 2)


def calcular_total(
    itens: list[ItemCarrinho],
    cupom: Optional[Cupom],   # ← segundo argumento obrigatório — alinhado com precificacao.py
) -> float:
    """
    Cálculo de total com suporte a cupom.

    Esta versão está alinhada com a assinatura de calcular_total em precificacao.py:
    ambos os arquivos esperam (itens, cupom) — inconsistência resolvida.
    """
    if not itens:
        raise ValueError("A lista de itens não pode ser vazia")
    bruto = sum(_subtotal_item(i) for i in itens)
    if cupom is None:
        return round(bruto, 2)
    valor_desconto = round(bruto * cupom.percentual_desconto, 2)
    return round(bruto - valor_desconto, 2)


# ─── Operações de carrinho ────────────────────────────────────────────────────

def adicionar_item(carrinho: Carrinho, item: ItemCarrinho) -> None:
    """Adiciona item; acumula quantidade se produto_id já existir."""
    for existente in carrinho.itens:
        if existente.produto_id == item.produto_id:
            existente.quantidade += item.quantidade
            return
    carrinho.itens.append(item)


def remover_item(carrinho: Carrinho, produto_id: str) -> None:
    """Remove o item com produto_id fornecido. Silencioso se não existir."""
    carrinho.itens = [i for i in carrinho.itens if i.produto_id != produto_id]


def aplicar_cupom(carrinho: Carrinho, cupom: Cupom) -> None:
    """Associa cupom ao carrinho, substituindo qualquer cupom anterior."""
    carrinho.cupom = cupom


def finalizar_carrinho(carrinho: Carrinho) -> dict:
    """
    Finaliza o carrinho e retorna resumo com total incluindo desconto do cupom.

    CORREÇÃO: total calculado com calcular_total(itens, carrinho.cupom) —
    agora passa o cupom corretamente; o desconto é refletido no total.
    """
    total = calcular_total(carrinho.itens, carrinho.cupom)   # ← corrigido: passa cupom

    bruto = sum(_subtotal_item(i) for i in carrinho.itens)
    desconto = round(bruto - total, 2) if total < bruto else 0.0

    return {
        "carrinho_id":    carrinho.id,
        "qtd_itens":      sum(i.quantidade for i in carrinho.itens),
        "subtotal":       bruto,
        "desconto_cupom": desconto,
        "total":          total,
        "cupom":          carrinho.cupom.codigo if carrinho.cupom else None,
    }


def formatar_carrinho(carrinho: Carrinho) -> str:
    """Formata o estado atual do carrinho para exibição."""
    linhas = [f"Carrinho {carrinho.id}:"]
    for item in carrinho.itens:
        linhas.append(
            f"  [{item.produto_id}] {item.descricao}: "
            f"R$ {item.preco_unitario:.2f} x {item.quantidade} = "
            f"R$ {_subtotal_item(item):.2f}"
        )
    bruto = sum(_subtotal_item(i) for i in carrinho.itens)
    linhas.append(f"  Subtotal: R$ {bruto:.2f}")
    if carrinho.cupom:
        linhas.append(f"  Cupom: {carrinho.cupom.codigo} (-{carrinho.cupom.percentual_desconto:.0%})")
    return "\n".join(linhas)


# ─── Execução de demonstração ─────────────────────────────────────────────────

if __name__ == "__main__":
    print("=== Carrinho de Compras (revisado — desconto de cupom correto) ===\n")

    carrinho = Carrinho(id="C-2026-001")

    adicionar_item(carrinho, ItemCarrinho("P001", "Teclado mecânico",  349.90, 1))
    adicionar_item(carrinho, ItemCarrinho("P002", "Mouse sem fio",      89.90, 2))
    adicionar_item(carrinho, ItemCarrinho("P003", "Mousepad XL",         49.90, 1))

    print(formatar_carrinho(carrinho))
    print()

    cupom_bv = Cupom(codigo="BEMVINDO10", percentual_desconto=0.10)
    aplicar_cupom(carrinho, cupom_bv)
    print(f"Cupom aplicado: {carrinho.cupom.codigo} (-10%)")

    resumo = finalizar_carrinho(carrinho)
    print(f"\nResumo final:")
    print(f"  Carrinho:  {resumo['carrinho_id']}")
    print(f"  Itens:     {resumo['qtd_itens']}")
    print(f"  Subtotal:  R$ {resumo['subtotal']:.2f}")
    print(f"  Desconto:  -R$ {resumo['desconto_cupom']:.2f} (cupom {resumo['cupom']})")
    print(f"  Total:     R$ {resumo['total']:.2f}  ← CORRETO: desconto de 10% aplicado")

    print()
    print("Consistência: calcular_total(itens, carrinho.cupom) — assinatura alinhada com precificacao.py.")
