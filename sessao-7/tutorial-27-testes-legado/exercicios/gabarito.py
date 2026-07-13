"""
GABARITO 27 — Testes de Unidade em Código Legado (Âncora)
Seam via construtor: ProcessadorReembolso(gateway, auditoria). GatewayPagamentoStub
devolve {"status": "estornado", "valor": ...}; ServicoAuditoriaFake guarda os
eventos registrados em uma lista, para inspeção. O primeiro teste é de
caracterização — congela o comportamento atual antes de qualquer melhoria.
Execute: pytest gabarito.py -v
"""


class ProcessadorReembolso:
    def __init__(self, gateway, auditoria):
        self.gateway = gateway
        self.auditoria = auditoria

    def processar_reembolso(self, transacao_id: str, valor: float) -> dict:
        resultado = self.gateway.estornar(transacao_id, valor)
        self.auditoria.registrar("reembolso", {"transacao_id": transacao_id, "valor": valor})
        return resultado


class GatewayPagamentoStub:
    """Stub: devolve resposta fixa e pré-programada, sem chamada de rede real."""

    def __init__(self, status: str = "estornado"):
        self._status = status

    def estornar(self, transacao_id: str, valor: float) -> dict:
        return {"status": self._status, "valor": valor}


class ServicoAuditoriaFake:
    """Fake: guarda os eventos registrados em memória, para inspeção posterior."""

    def __init__(self):
        self.eventos_registrados = []

    def registrar(self, evento: str, detalhes: dict) -> None:
        self.eventos_registrados.append({"evento": evento, "detalhes": detalhes})


def test_caracterizacao_processa_reembolso_com_sucesso():
    # Teste de caracterização: congela o comportamento atual do
    # ProcessadorReembolso como oráculo, agora que o seam permite isolá-lo.
    gateway = GatewayPagamentoStub(status="estornado")
    auditoria = ServicoAuditoriaFake()
    processador = ProcessadorReembolso(gateway, auditoria)

    resultado = processador.processar_reembolso("TX001", 150.0)

    assert resultado == {"status": "estornado", "valor": 150.0}


def test_reembolso_registra_evento_de_auditoria():
    gateway = GatewayPagamentoStub()
    auditoria = ServicoAuditoriaFake()
    processador = ProcessadorReembolso(gateway, auditoria)

    processador.processar_reembolso("TX002", 80.0)

    assert len(auditoria.eventos_registrados) == 1
    assert auditoria.eventos_registrados[0]["evento"] == "reembolso"
    assert auditoria.eventos_registrados[0]["detalhes"] == {"transacao_id": "TX002", "valor": 80.0}
