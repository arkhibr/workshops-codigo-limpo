"""
observer_ruins.py — Acoplamento direto e ausência de undo.
Execute: python3 observer_ruins.py
"""
from dataclasses import dataclass, field
from typing import List


@dataclass
class ItemPedido:
    produto_id: str
    quantidade: int
    preco:      float

@dataclass
class Pedido:
    id:         str
    cliente_id: str
    itens:      List[ItemPedido]
    status:     str = "pendente"


# ─── Serviços concretos (acoplados diretamente) ───────────────────────────────

class ServicoEmail:
    def enviar_confirmacao(self, cliente_id: str, pedido_id: str) -> None:
        print(f"  [Email] confirmação → {cliente_id}: pedido {pedido_id}")

class GerenciadorEstoque:
    def reservar(self, itens: List[ItemPedido]) -> None:
        for item in itens:
            print(f"  [Estoque] reservado {item.quantidade}× {item.produto_id}")

class RegistradorAuditoria:
    def registrar(self, evento: str, pedido_id: str) -> None:
        print(f"  [Auditoria] {evento}: {pedido_id}")


# ─── Sem Observer: confirmar() conhece todos os consumidores ─────────────────

class PedidoComAcoplamento:
    def __init__(self) -> None:
        self.email     = ServicoEmail()
        self.estoque   = GerenciadorEstoque()
        self.auditoria = RegistradorAuditoria()

    def confirmar(self, pedido: Pedido) -> None:
        pedido.status = "confirmado"
        # Adicionar SMS exige alterar confirmar()
        self.email.enviar_confirmacao(pedido.cliente_id, pedido.id)
        self.estoque.reservar(pedido.itens)
        self.auditoria.registrar("pedido_confirmado", pedido.id)


# ─── Sem Command: cancelar sem undo ──────────────────────────────────────────

_banco_pedidos: dict = {}

def cancelar_pedido(pedido_id: str) -> None:
    """Se falhar no meio, não há como reverter o que já foi feito."""
    print(f"  Estornando valor do pedido {pedido_id}")
    print(f"  Liberando estoque do pedido {pedido_id}")
    _banco_pedidos[pedido_id] = "cancelado"
    print(f"  Pedido {pedido_id} marcado como cancelado")
    # Sem histórico. Sem desfazer.


if __name__ == "__main__":
    print("=== Observer _ruins — acoplamento + sem undo ===\n")
    itens  = [ItemPedido("PROD-001", 2, 299.90)]
    pedido = Pedido("PED-001", "CLI-100", itens)

    gestor = PedidoComAcoplamento()
    gestor.confirmar(pedido)

    print("\nCancelando pedido (sem undo):")
    cancelar_pedido("PED-001")
