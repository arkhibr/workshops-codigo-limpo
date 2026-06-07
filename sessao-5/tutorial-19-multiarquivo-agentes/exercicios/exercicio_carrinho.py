"""
Exercício — Módulo de Carrinho de Compras com Frete (chamador não atualizado)
Referência: Tutorial 11 — Geração multi-arquivo com agentes
Execute: python3 exercicio_carrinho.py

INSTRUÇÕES:
  (1) Execute este arquivo e exercicio_precificacao.py separadamente — ambos rodam sem erro.
  (2) Revise o diff entre os dois arquivos como se estivesse revisando uma mudança
      de agente em altitude: olhe os dois juntos, não isoladamente.
  (3) Ache a inconsistência cross-file: onde a assinatura mudou mas o chamador não acompanhou?
  (4) Corrija a mudança e compare com gabarito_carrinho.py e gabarito_precificacao.py.

CONTEXTO: o agente recebeu a tarefa "adicionar cálculo de frete ao pedido".
Ele adicionou o campo 'regiao' ao Pedido e atualizou precificacao.py corretamente.
Mas NÃO atualizou todos os chamadores neste arquivo.

A inconsistência está em fechar_pedido — revise o diff dos dois arquivos juntos.
"""

from dataclasses import dataclass, field
from typing import Optional


# ─── Entidades (replicadas para auto-contenção) ───────────────────────────────

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
    regiao: str              = ""    # ← campo adicionado pelo agente


# ─── Lógica de precificação (versão local — NÃO atualizada pelo agente) ───────
# Em produção o código chamaria calcular_total_pedido de precificacao.py assim:
#
#   from precificacao import calcular_total_pedido
#   resultado = calcular_total_pedido(pedido.itens)   ← CHAMADA ANTIGA — falta regiao
#
# A nova assinatura exige: calcular_total_pedido(itens, regiao)
# ⚠️  INCONSISTÊNCIA CROSS-FILE: fechar_pedido não foi atualizado pelo agente.

def _subtotal_item(item: ItemPedido) -> float:
    return round(item.preco_unitario * item.quantidade, 2)


def _calcular_total_local(itens: list[ItemPedido]) -> float:
    """Cálculo de total SEM frete (versão anterior — não atualizada)."""
    if not itens:
        raise ValueError("A lista de itens não pode ser vazia")
    return round(sum(_subtotal_item(i) for i in itens), 2)


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
    Fecha o pedido e retorna um resumo.

    BUG LATENTE: em produção isto chamaria calcular_total_pedido de precificacao.py.
    Como o agente atualizou a assinatura mas não atualizou este chamador,
    a chamada seria:

        resultado = calcular_total_pedido(pedido.itens)   ← TypeError: missing 'regiao'

    O resultado: pedido.regiao é ignorado — o frete nunca é calculado.
    O total retornado não inclui frete, mesmo que a região esteja definida.
    """
    total = _calcular_total_local(pedido.itens)   # ← versão antiga (sem frete)

    return {
        "pedido_id": pedido.id,
        "qtd_itens": sum(i.quantidade for i in pedido.itens),
        "regiao":    pedido.regiao,
        "total":     total,
        # ⚠️  frete não está incluído — inconsistência cross-file
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
        linhas.append(f"  Região:   {pedido.regiao} (frete não calculado — inconsistência)")
    return "\n".join(linhas)


# ─── Execução de demonstração ─────────────────────────────────────────────────

if __name__ == "__main__":
    print("=== Carrinho de Compras com Frete (exercício — chamador não atualizado) ===\n")

    pedido = Pedido(id="P-2026-042")

    adicionar_item(pedido, ItemPedido("P001", "Teclado mecânico",  89.90, 1))
    adicionar_item(pedido, ItemPedido("P002", "Mouse sem fio",      49.90, 2))

    definir_regiao(pedido, "nordeste")

    print(formatar_pedido(pedido))
    print()

    resumo = fechar_pedido(pedido)
    subtotal = sum(_subtotal_item(i) for i in pedido.itens)
    frete_nordeste = 29.90
    esperado = round(subtotal + frete_nordeste, 2)

    print("Resumo do pedido:")
    print(f"  Pedido:   {resumo['pedido_id']}")
    print(f"  Itens:    {resumo['qtd_itens']}")
    print(f"  Região:   {resumo['regiao']}")
    print(f"  Total:    R$ {resumo['total']:.2f}  <- ERRADO: frete da região 'nordeste' não incluído")
    print(f"  Esperado: R$ {esperado:.2f}  (subtotal R$ {subtotal:.2f} + frete R$ {frete_nordeste:.2f} nordeste)")

    print()
    print("DICA: revise o diff de exercicio_precificacao.py e exercicio_carrinho.py juntos.")
    print("A inconsistência está em fechar_pedido — qual argumento está faltando?")
