"""
Saída do agente de IA — Módulo de Precificação (carrinho de compras)
Referência: Tutorial 11 — Geração multi-arquivo com agentes
Execute: python3 precificacao.py

ATENÇÃO: saída de agente após mudança multi-arquivo — inconsistência cross-file presente.
O agente recebeu a tarefa "adicionar suporte a cupom de desconto ao carrinho".
Ele atualizou ESTE arquivo corretamente: calcular_total agora exige um segundo
argumento 'cupom: Optional[Cupom]' (sem valor padrão).

INCONSISTÊNCIA CROSS-FILE: carrinho.py ainda chama calcular_total(itens) — sem
o argumento 'cupom'. Essa chamada levantaria TypeError em produção. Cada arquivo
roda sua própria demo sem erro; a inconsistência só aparece ao revisar o diff
de ambos os arquivos juntos. Veja exemplos/diff-comentado.md.
"""

from dataclasses import dataclass
from typing import Optional


# ─── Entidades ────────────────────────────────────────────────────────────────

@dataclass
class ItemCarrinho:
    produto_id:    str
    descricao:     str
    preco_unitario: float
    quantidade:    int


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
    cupom: Optional[Cupom],   # ← ASSINATURA NOVA — agente adicionou este parâmetro
                               #   sem valor padrão; chamadores devem ser atualizados.
                               #   carrinho.py ainda chama calcular_total(itens) → TypeError
) -> float:
    """
    Calcula o valor total aplicando desconto do cupom.

    Levanta ValueError se a lista estiver vazia.
    Levanta TypeError (em chamadores não atualizados) se cupom for omitido.
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
    print("=== Precificação (saída do agente — assinatura nova com cupom) ===\n")

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
    print("Assinatura NOVA (este arquivo): calcular_total(itens, cupom)")
    print("Assinatura ANTIGA (carrinho.py): calcular_total(itens)  ← inconsistência cross-file")
    print("Ver exemplos/diff-comentado.md para o diff anotado.")
