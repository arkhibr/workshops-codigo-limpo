"""
Saída do agente de IA — Módulo de Carrinho de Compras
Referência: Tutorial 11 — Geração multi-arquivo com agentes
Execute: python3 carrinho.py

ATENÇÃO: saída de agente após mudança multi-arquivo — inconsistência cross-file presente.
O agente recebeu a tarefa "adicionar suporte a cupom de desconto ao carrinho".
Ele atualizou precificacao.py corretamente (nova assinatura com 'cupom'),
mas NÃO atualizou os chamadores neste arquivo.

INCONSISTÊNCIA CROSS-FILE: a linha abaixo (em finalizar_carrinho) usa a assinatura
ANTIGA de calcular_total:

    total = calcular_total(itens)          ← ANTIGA (sem cupom) — não atualizada

A assinatura NOVA em precificacao.py exige:

    total = calcular_total(itens, cupom)   ← NOVA (com cupom obrigatório)

Em produção, finalizar_carrinho levantaria TypeError: "missing 1 required positional
argument: 'cupom'". Cada arquivo roda sua própria demo sem erro — a inconsistência
só aparece ao revisar o diff de ambos juntos. Veja exemplos/diff-comentado.md.
"""

from dataclasses import dataclass, field
from typing import Optional


# ─── Entidades (replicadas para manter auto-contenção deste arquivo) ──────────
# Em um módulo real estas viriam de precificacao.py; aqui são redeclaradas para
# que carrinho.py rode de forma independente.

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


@dataclass
class Carrinho:
    id:     str
    itens:  list[ItemCarrinho] = field(default_factory=list)
    cupom:  Optional[Cupom]   = None


# ─── Operações de carrinho ────────────────────────────────────────────────────

def adicionar_item(carrinho: Carrinho, item: ItemCarrinho) -> None:
    """Adiciona um item ao carrinho. Itens com mesmo produto_id têm quantidade somada."""
    for existente in carrinho.itens:
        if existente.produto_id == item.produto_id:
            existente.quantidade += item.quantidade
            return
    carrinho.itens.append(item)


def remover_item(carrinho: Carrinho, produto_id: str) -> None:
    """Remove o item com o produto_id fornecido. Silencioso se não existir."""
    carrinho.itens = [i for i in carrinho.itens if i.produto_id != produto_id]


def aplicar_cupom(carrinho: Carrinho, cupom: Cupom) -> None:
    """Associa um cupom ao carrinho, substituindo qualquer cupom anterior."""
    carrinho.cupom = cupom


def _subtotal_item(item: ItemCarrinho) -> float:
    return round(item.preco_unitario * item.quantidade, 2)


# ── Função auxiliar local (NÃO atualizada pelo agente) ───────────────────────
# Esta versão de _calcular_total_local foi copiada da versão ANTERIOR de
# calcular_total (precificacao.py antes da mudança) e não recebe cupom.
# Em produção o código chamaria calcular_total de precificacao.py assim:
#
#   from precificacao import calcular_total
#   total = calcular_total(itens)      ← CHAMADA ANTIGA — falta o argumento cupom
#
# A nova assinatura exige: calcular_total(itens, cupom)
# ⚠️  INCONSISTÊNCIA CROSS-FILE: este módulo não foi atualizado pelo agente.

def _calcular_total_local(itens: list[ItemCarrinho]) -> float:
    """Cálculo de total SEM suporte a cupom (versão anterior — não atualizada)."""
    if not itens:
        raise ValueError("A lista de itens não pode ser vazia")
    return round(sum(_subtotal_item(i) for i in itens), 2)


def finalizar_carrinho(carrinho: Carrinho) -> dict:
    """
    Finaliza o carrinho e retorna um resumo com total.

    BUG LATENTE: em produção isto chamaria calcular_total de precificacao.py.
    Como o agente atualizou a assinatura mas não atualizou este chamador,
    a chamada seria:

        total = calcular_total(carrinho.itens)   ← TypeError: missing 'cupom'

    O resultado: carrinho.cupom é ignorado — o desconto nunca é aplicado.
    """
    total = _calcular_total_local(carrinho.itens)   # ← usa versão antiga (sem cupom)

    return {
        "carrinho_id": carrinho.id,
        "qtd_itens":   sum(i.quantidade for i in carrinho.itens),
        "total":       total,
        "cupom":       carrinho.cupom.codigo if carrinho.cupom else None,
        # ⚠️  total não reflete o desconto do cupom — inconsistência cross-file
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
        linhas.append(f"  Cupom: {carrinho.cupom.codigo} (não aplicado — inconsistência)")
    return "\n".join(linhas)


# ─── Execução de demonstração ─────────────────────────────────────────────────

if __name__ == "__main__":
    print("=== Carrinho de Compras (saída do agente — chamador não atualizado) ===\n")

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
    print(f"  Carrinho: {resumo['carrinho_id']}")
    print(f"  Itens:    {resumo['qtd_itens']}")
    print(f"  Cupom:    {resumo['cupom']}")
    print(f"  Total:    R$ {resumo['total']:.2f}  ← ERRADO: desconto de 10% não foi aplicado")

    bruto = sum(_subtotal_item(i) for i in carrinho.itens)
    esperado = round(bruto * 0.90, 2)
    print(f"  Esperado: R$ {esperado:.2f}  (com 10% de desconto BEMVINDO10)")

    print()
    print("A inconsistência cross-file: calcular_total em precificacao.py exige 'cupom'")
    print("mas finalizar_carrinho chama a versão antiga sem esse argumento.")
    print("O cupom está no carrinho mas o desconto nunca chega ao total.")
