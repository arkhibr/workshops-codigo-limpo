"""
dubles_ruins.py — Testes sem dublês adequados: lentos ou frágeis.
Execute: pytest dubles_ruins.py -v
"""
import time
from unittest.mock import MagicMock


class GatewayPagamentoReal:
    def cobrar(self, valor: float) -> dict:
        time.sleep(0.3)  # simula latência de rede real
        return {"status": "aprovado", "valor": valor}


class ServicoNotificacaoReal:
    def enviar(self, destinatario: str, mensagem: str) -> bool:
        time.sleep(0.2)
        return True


class ProcessadorPagamento:
    def __init__(self):
        self.gateway = GatewayPagamentoReal()
        self.notificacao = ServicoNotificacaoReal()

    def processar(self, valor: float, destinatario: str) -> dict:
        resultado = self.gateway.cobrar(valor)
        if resultado["status"] == "aprovado":
            self.notificacao.enviar(destinatario, "Pagamento aprovado")
        return resultado


def test_processa_pagamento_sem_nenhum_double():
    # sem double: teste depende de infraestrutura real e é lento (viola o F de FIRST)
    processador = ProcessadorPagamento()
    resultado = processador.processar(100.0, "cliente@teste.com")
    assert resultado["status"] == "aprovado"


def test_processa_pagamento_com_mock_fragil():
    # mock acoplado a detalhes internos: verifica ORDEM exata de chamadas,
    # quebra em qualquer refatoração interna que não muda comportamento observável
    gateway = MagicMock()
    gateway.cobrar.return_value = {"status": "aprovado", "valor": 100.0}
    processador = ProcessadorPagamento()
    processador.gateway = gateway
    processador.notificacao = MagicMock()

    processador.processar(100.0, "cliente@teste.com")

    assert processador.gateway.method_calls[0][0] == "cobrar"
    assert processador.notificacao.method_calls[0][0] == "enviar"
