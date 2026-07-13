"""
dubles_bons.py — Stub, Mock e Fake usados pelo que cada um resolve melhor.
Execute: pytest dubles_bons.py -v
"""
from dataclasses import dataclass
from unittest.mock import Mock


@dataclass
class ResultadoPagamento:
    status: str
    valor: float


class ProcessadorPagamento:
    def __init__(self, gateway, notificacao):
        self._gateway = gateway
        self._notificacao = notificacao

    def processar(self, valor: float, destinatario: str) -> ResultadoPagamento:
        resultado = self._gateway.cobrar(valor)
        if resultado.status == "aprovado":
            self._notificacao.enviar(destinatario, "Pagamento aprovado")
        return resultado


class GatewayPagamentoStub:
    """Stub: devolve resposta fixa e pré-programada, sem verificar interação."""

    def __init__(self, status: str = "aprovado"):
        self._status = status

    def cobrar(self, valor: float) -> ResultadoPagamento:
        return ResultadoPagamento(status=self._status, valor=valor)


class RepositorioPedidoFake:
    """Fake: implementação funcional leve, em memória — sem instrumentação de chamadas."""

    def __init__(self):
        self._pedidos = {}

    def salvar(self, pedido_id: str, dados: dict) -> None:
        self._pedidos[pedido_id] = dados

    def buscar(self, pedido_id: str):
        return self._pedidos.get(pedido_id)


def test_processa_pagamento_aprovado_notifica_cliente():
    # Arrange — Stub para o gateway, Mock para verificar a notificação
    gateway = GatewayPagamentoStub(status="aprovado")
    notificacao = Mock()
    processador = ProcessadorPagamento(gateway, notificacao)

    # Act
    resultado = processador.processar(100.0, "cliente@teste.com")

    # Assert — comportamento observável, não implementação interna
    assert resultado.status == "aprovado"
    notificacao.enviar.assert_called_once_with("cliente@teste.com", "Pagamento aprovado")


def test_pagamento_recusado_nao_notifica_cliente():
    gateway = GatewayPagamentoStub(status="recusado")
    notificacao = Mock()
    processador = ProcessadorPagamento(gateway, notificacao)

    processador.processar(100.0, "cliente@teste.com")

    notificacao.enviar.assert_not_called()


def test_fake_repositorio_guarda_e_recupera_pedido():
    repositorio = RepositorioPedidoFake()
    repositorio.salvar("P001", {"total": 100.0})
    assert repositorio.buscar("P001") == {"total": 100.0}


def test_dummy_notificacao_nao_e_exercitada_quando_pagamento_recusado():
    # Dummy: passado para satisfazer o parâmetro `notificacao`, exigido
    # pelo construtor de ProcessadorPagamento, mas nunca de fato invocado
    # neste caminho — quando o pagamento é recusado, o `if` dentro de
    # `processar()` pula a chamada a `self._notificacao.enviar(...)`.
    # Um `object()` comum, sem nenhum método implementado, já basta: se
    # o código de produção chamasse `.enviar()` nele por engano, o teste
    # falharia na hora com AttributeError — a prova de que a notificação
    # não foi de fato exercitada neste caminho.
    gateway = GatewayPagamentoStub(status="recusado")
    notificacao_dummy = object()
    processador = ProcessadorPagamento(gateway, notificacao_dummy)

    resultado = processador.processar(100.0, "cliente@teste.com")

    assert resultado.status == "recusado"


def test_spy_registra_chamadas_para_inspecao_posterior():
    # Spy: Mock usado sem expectativa pré-programada — só registra e é
    # inspecionado depois, ao contrário do Mock com assert_called_once_with.
    spy = Mock(wraps=RepositorioPedidoFake())
    spy.salvar("P002", {"total": 200.0})
    assert spy.salvar.call_count == 1
    assert spy.buscar("P002") == {"total": 200.0}
