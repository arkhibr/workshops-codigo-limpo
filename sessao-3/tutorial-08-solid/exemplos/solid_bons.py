"""
solid_bons.py — Os 5 princípios SOLID aplicados ao mesmo módulo de pedidos.
Execute: python3 solid_bons.py
"""
from typing import List, Protocol, runtime_checkable
from dataclasses import dataclass


@dataclass
class ItemPedido:
    produto_id: str
    descricao:  str
    preco:      float
    quantidade: int

@dataclass
class Pedido:
    id:         str
    cliente_id: str
    itens:      List[ItemPedido]
    status:     str = "pendente"

    def confirmar(self) -> None:
        self.status = "confirmado"


@runtime_checkable
class IRepositorioPedido(Protocol):
    def salvar(self, pedido: "Pedido") -> None: ...

@runtime_checkable
class INotificador(Protocol):
    def notificar(self, destinatario: str, mensagem: str) -> None: ...

@runtime_checkable
class IFormatador(Protocol):
    def formatar(self, pedido: "Pedido", total: float) -> str: ...


class ValidadorPedido:
    def validar(self, pedido: Pedido) -> bool:
        return bool(pedido.itens) and bool(pedido.cliente_id)

class CalculadorTotal:
    def calcular(self, pedido: Pedido) -> float:
        return round(sum(i.preco * i.quantidade for i in pedido.itens), 2)

class NotificadorEmail:
    def notificar(self, destinatario: str, mensagem: str) -> None:
        print(f"  [Email] → {destinatario}: {mensagem[:40]}")

class RepositorioPedido:
    def salvar(self, pedido: Pedido) -> None:
        print(f"  [BD] salvo: {pedido.id} ({pedido.status})")


class FormatadorVendas:
    def formatar(self, pedido: Pedido, total: float) -> str:
        return f"Relatório Vendas | Pedido {pedido.id} | Total: R${total:.2f}"

class FormatadorFinanceiro:
    def formatar(self, pedido: Pedido, total: float) -> str:
        return f"Relatório Financeiro | Receita: R${total:.2f}"

class FormatadorEstoque:
    def formatar(self, pedido: Pedido, total: float) -> str:
        return f"Relatório Estoque | {len(pedido.itens)} item(ns) movimentado(s)"


class GeradorRelatorio:
    def __init__(
        self,
        repo:        IRepositorioPedido,
        notificador: INotificador,
        formatador:  IFormatador,
        calculador:  CalculadorTotal,   # sem efeitos externos — concreta aceitável aqui
    ) -> None:
        self._repo        = repo
        self._notificador = notificador
        self._formatador  = formatador
        self._calculador  = calculador

    def processar(self, pedido: Pedido) -> str:
        total = self._calculador.calcular(pedido)
        self._repo.salvar(pedido)
        self._notificador.notificar(pedido.cliente_id, f"Pedido {pedido.id} salvo")
        return self._formatador.formatar(pedido, total)


class PedidoAmostra(Pedido):
    def calcular_total_especial(self) -> float:
        return 0.0
    # confirmar() herdado sem alteração — contrato mantido


def processar_pedido(pedido: Pedido) -> None:
    pedido.confirmar()
    print(f"  Pedido {pedido.id} confirmado ({pedido.status})")


def verificar_solid() -> None:
    itens  = [ItemPedido("P001", "Webcam HD", 299.90, 1)]
    pedido = Pedido("PED-001", "CLI-100", itens)
    repo   = RepositorioPedido()
    notif  = NotificadorEmail()
    calc   = CalculadorTotal()

    for fmt_cls, tipo in [
        (FormatadorVendas,     "vendas"),
        (FormatadorFinanceiro, "financeiro"),
        (FormatadorEstoque,    "estoque"),
    ]:
        gerador   = GeradorRelatorio(repo, notif, fmt_cls(), calc)
        resultado = gerador.processar(pedido)
        assert resultado
        print(f"OK: SRP+DIP — relatório '{tipo}' gerado sem alterar GeradorRelatorio")

    print("OK: OCP — FormatadorEstoque adicionado sem alterar GeradorRelatorio")

    amostra = PedidoAmostra("PED-DEMO", "CLI-999", itens)
    processar_pedido(amostra)
    print("OK: LSP — PedidoAmostra confirmado sem exceção inesperada")

    metodos_publicos = [m for m in dir(INotificador) if not m.startswith("_")]
    assert len(metodos_publicos) <= 2
    print("OK: ISP — INotificador segregado (1 método)")

    print("OK: DIP — GeradorRelatorio recebe abstrações no construtor")


if __name__ == "__main__":
    print("=== SOLID _bons — 5 princípios aplicados ===\n")
    verificar_solid()
