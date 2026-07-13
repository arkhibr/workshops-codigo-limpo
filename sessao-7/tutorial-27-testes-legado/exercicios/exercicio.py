"""
EXERCÍCIO 27 — Testes de Unidade em Código Legado (Âncora)
Tempo estimado: 10 minutos

INSTRUÇÕES:
  ProcessadorReembolso abaixo não tem seams nem testes: instancia
  GatewayPagamentoReal e ServicoAuditoriaReal diretamente.

  1. Introduza seams (injeção via construtor).
  2. Escreva um teste de CARACTERIZAÇÃO para o comportamento atual.
  3. Use doubles (Stub para o gateway, Fake para a auditoria).
  Execute: pytest exercicio.py -v
"""


class GatewayPagamentoReal:
    def estornar(self, transacao_id: str, valor: float) -> dict:
        raise ConnectionError("Gateway real não disponível neste ambiente")


class ServicoAuditoriaReal:
    def registrar(self, evento: str, detalhes: dict) -> None:
        raise ConnectionError("Serviço de auditoria real não disponível neste ambiente")


class ProcessadorReembolso:
    def __init__(self):
        self.gateway = GatewayPagamentoReal()
        self.auditoria = ServicoAuditoriaReal()

    def processar_reembolso(self, transacao_id: str, valor: float) -> dict:
        resultado = self.gateway.estornar(transacao_id, valor)
        self.auditoria.registrar("reembolso", {"transacao_id": transacao_id, "valor": valor})
        return resultado
