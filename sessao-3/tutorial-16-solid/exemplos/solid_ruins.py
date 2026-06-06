"""
solid_ruins.py — Violações dos 5 princípios SOLID em um módulo de pedidos.
Execute: python3 solid_ruins.py
"""
from typing import List
from dataclasses import dataclass


@dataclass
class ItemPedido:
    produto_id: str
    descricao:  str
    preco:      float
    quantidade: int

@dataclass
class Pedido:
    id:          str
    cliente_id:  str
    itens:       List[ItemPedido]
    status:      str = "pendente"

    def confirmar(self) -> None:
        self.status = "confirmado"


class BancoDadosSQLite:
    def salvar(self, tabela: str, dados: dict) -> None:
        print(f"  [BD] salvo em {tabela}: {dados['id']}")

class EmailSmtp:
    def enviar(self, dest: str, msg: str) -> None:
        print(f"  [Email] → {dest}: {msg[:40]}")


class GeradorRelatorioPedidos:
    # DIP violation: instancia dependências concretas
    def __init__(self) -> None:
        self.db    = BancoDadosSQLite()
        self.email = EmailSmtp()

    # SRP violation: valida pedido
    def validar_pedido(self, pedido: Pedido) -> bool:
        return bool(pedido.itens) and bool(pedido.cliente_id)

    # SRP violation: calcula total
    def calcular_total(self, pedido: Pedido) -> float:
        return sum(i.preco * i.quantidade for i in pedido.itens)

    # SRP violation: envia e-mail
    def enviar_confirmacao(self, pedido: Pedido) -> None:
        self.email.enviar(pedido.cliente_id, f"Pedido {pedido.id} confirmado")

    # SRP violation: persiste no banco
    def salvar_pedido(self, pedido: Pedido) -> None:
        self.db.salvar("pedidos", {"id": pedido.id, "status": pedido.status})

    # OCP violation: adicionar novo tipo exige alterar este método
    def gerar(self, tipo: str, pedido: Pedido) -> str:
        total = self.calcular_total(pedido)
        if tipo == "vendas":
            return f"Relatório Vendas | Pedido {pedido.id} | Total: R${total:.2f}"
        elif tipo == "financeiro":
            return f"Relatório Financeiro | Receita: R${total:.2f}"
        elif tipo == "estoque":
            return f"Relatório Estoque | {len(pedido.itens)} item(ns) movimentado(s)"
        else:
            raise ValueError(f"Tipo desconhecido: {tipo}")


class IProcessador:
    """ISP violation: interface com 6 métodos — clientes implementam todos."""
    def validar(self)      -> bool:  raise NotImplementedError
    def calcular(self)     -> float: raise NotImplementedError
    def notificar(self)    -> None:  raise NotImplementedError
    def arquivar(self)     -> None:  raise NotImplementedError
    def exportar_csv(self) -> str:   raise NotImplementedError
    def exportar_pdf(self) -> bytes: raise NotImplementedError


class ProcessadorSimples(IProcessador):
    """Precisa apenas de validar e calcular — mas é forçado a implementar tudo."""
    def validar(self)       -> bool:  return True
    def calcular(self)      -> float: return 0.0
    def notificar(self)     -> None:  pass
    def arquivar(self)      -> None:  pass
    def exportar_csv(self)  -> str:   return ""
    def exportar_pdf(self)  -> bytes: return b""


class PedidoAmostra(Pedido):
    """LSP violation: confirmar() lança exceção que a base nunca lança."""
    def confirmar(self) -> None:
        raise NotImplementedError("PedidoAmostra não pode ser confirmado")


def processar_pedido(pedido: Pedido) -> None:
    pedido.confirmar()
    print(f"  Pedido {pedido.id} confirmado com sucesso")


if __name__ == "__main__":
    print("=== SOLID _ruins — violações dos 5 princípios ===\n")

    itens = [ItemPedido("P001", "Webcam HD", 299.90, 1)]
    pedido = Pedido("PED-001", "CLI-100", itens)

    gerador = GeradorRelatorioPedidos()
    gerador.salvar_pedido(pedido)
    gerador.enviar_confirmacao(pedido)
    print(gerador.gerar("vendas",     pedido))
    print(gerador.gerar("financeiro", pedido))
    print(gerador.gerar("estoque",    pedido))

    print("\nISP — ProcessadorSimples implementa 6 métodos, usa 2:")
    proc = ProcessadorSimples()
    print(f"  validar={proc.validar()}, calcular={proc.calcular()}")

    print("\nLSP — PedidoAmostra quebra contrato de Pedido:")
    amostra = PedidoAmostra("PED-DEMO", "CLI-999", itens)
    try:
        processar_pedido(amostra)
    except NotImplementedError as e:
        print(f"  Erro inesperado: {e}")
