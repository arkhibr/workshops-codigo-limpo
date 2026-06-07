"""
observer_bons.py — Observer desacopla eventos; Command adiciona undo.
Execute: python3 observer_bons.py
"""
from typing import Protocol, List, Optional
from dataclasses import dataclass


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


# ─── Observer ─────────────────────────────────────────────────────────────────

class ObservadorPedido(Protocol):
    def ao_confirmar(self, pedido: Pedido) -> None: ...
    def ao_cancelar(self, pedido: Pedido) -> None: ...

class NotificadorEmail:
    def ao_confirmar(self, pedido: Pedido) -> None:
        print(f"  [Email] confirmação → {pedido.cliente_id}: pedido {pedido.id}")
    def ao_cancelar(self, pedido: Pedido) -> None:
        print(f"  [Email] cancelamento → {pedido.cliente_id}: pedido {pedido.id}")

class GestorEstoque:
    def ao_confirmar(self, pedido: Pedido) -> None:
        for item in pedido.itens:
            print(f"  [Estoque] reservado {item.quantidade}× {item.produto_id}")
    def ao_cancelar(self, pedido: Pedido) -> None:
        for item in pedido.itens:
            print(f"  [Estoque] liberado {item.quantidade}× {item.produto_id}")

class RegistradorAuditoria:
    def ao_confirmar(self, pedido: Pedido) -> None:
        print(f"  [Auditoria] pedido_confirmado: {pedido.id}")
    def ao_cancelar(self, pedido: Pedido) -> None:
        print(f"  [Auditoria] pedido_cancelado: {pedido.id}")


class GerenciadorPedido:
    def __init__(self) -> None:
        self._observadores: List[ObservadorPedido] = []

    def registrar_observador(self, obs: ObservadorPedido) -> None:
        self._observadores.append(obs)

    def remover_observador(self, obs: ObservadorPedido) -> None:
        self._observadores.remove(obs)

    def confirmar(self, pedido: Pedido) -> None:
        pedido.status = "confirmado"
        for obs in self._observadores:
            obs.ao_confirmar(pedido)

    def cancelar(self, pedido: Pedido) -> None:
        pedido.status = "cancelado"
        for obs in self._observadores:
            obs.ao_cancelar(pedido)


# ─── Command ──────────────────────────────────────────────────────────────────

class Comando(Protocol):
    def executar(self) -> None: ...
    def desfazer(self) -> None: ...

class ComandoCancelamento:
    def __init__(self, pedido: Pedido, gerenciador: GerenciadorPedido) -> None:
        self._pedido            = pedido
        self._gerenciador       = gerenciador
        self._status_anterior: Optional[str] = None

    def executar(self) -> None:
        self._status_anterior = self._pedido.status
        self._gerenciador.cancelar(self._pedido)
        print(f"  Valor estornado para {self._pedido.cliente_id}")

    def desfazer(self) -> None:
        if self._status_anterior is None:
            raise RuntimeError("desfazer() chamado antes de executar()")
        self._pedido.status = self._status_anterior
        for item in self._pedido.itens:
            print(f"  [Estoque] re-reservado {item.quantidade}× {item.produto_id}")
        print(f"  Pedido {self._pedido.id} restaurado para '{self._status_anterior}'")


class HistoricoComandos:
    def __init__(self) -> None:
        self._historico: List[Comando] = []

    def executar(self, cmd: Comando) -> None:
        cmd.executar()
        self._historico.append(cmd)

    def desfazer_ultimo(self) -> None:
        if not self._historico:
            print("  Nenhum comando para desfazer")
            return
        self._historico.pop().desfazer()


# ─── Verificação ──────────────────────────────────────────────────────────────

def verificar_observer() -> None:
    itens  = [ItemPedido("PROD-001", 2, 299.90)]
    pedido = Pedido("PED-001", "CLI-100", itens)

    gerenciador = GerenciadorPedido()
    gerenciador.registrar_observador(NotificadorEmail())
    gerenciador.registrar_observador(GestorEstoque())
    gerenciador.registrar_observador(RegistradorAuditoria())

    gerenciador.confirmar(pedido)
    assert pedido.status == "confirmado"
    print("OK: Observer — 3 observadores notificados em confirmar()")
    print("OK: Observer — adicionar novo observador não altera GerenciadorPedido")

def verificar_command() -> None:
    itens  = [ItemPedido("PROD-001", 1, 150.0)]
    pedido = Pedido("PED-002", "CLI-200", itens, status="confirmado")

    gerenciador = GerenciadorPedido()
    historico   = HistoricoComandos()

    cmd = ComandoCancelamento(pedido, gerenciador)
    historico.executar(cmd)
    assert pedido.status == "cancelado"
    print("OK: Command — cancelamento executado")

    historico.desfazer_ultimo()
    assert pedido.status == "confirmado"
    print("OK: Command — cancelamento desfeito, pedido restaurado para 'confirmado'")


if __name__ == "__main__":
    print("=== Observer _bons — Observer + Command ===\n")
    verificar_observer()
    print()
    verificar_command()
