"""
EXERCÍCIO 25 — Dublês de Teste
Tempo estimado: 15 minutos

INSTRUÇÕES:
  ServicoEntrega abaixo depende de ApiCepReal (chamada de rede real, lenta)
  e RepositorioEnderecoReal (banco real). O teste fornecido não usa nenhum
  double e é lento e frágil.

  1. Crie um Stub para a API de CEP (resposta fixa).
  2. Crie um Fake para o repositório de endereço (em memória).
  3. Reescreva o teste para não depender de infraestrutura real.
  Execute: pytest exercicio.py -v
"""
import time


class ApiCepReal:
    def consultar(self, cep: str) -> dict:
        time.sleep(0.3)
        return {"cep": cep, "cidade": "São Paulo", "uf": "SP"}


class RepositorioEnderecoReal:
    def salvar(self, pedido_id: str, endereco: dict) -> None:
        time.sleep(0.2)


class ServicoEntrega:
    def __init__(self):
        self.api_cep = ApiCepReal()
        self.repositorio = RepositorioEnderecoReal()

    def confirmar_endereco(self, pedido_id: str, cep: str) -> dict:
        endereco = self.api_cep.consultar(cep)
        self.repositorio.salvar(pedido_id, endereco)
        return endereco


def test_confirma_endereco_sem_nenhum_double():
    # lento: ~0.5s de sleep simulando chamadas reais
    servico = ServicoEntrega()
    resultado = servico.confirmar_endereco("P001", "01000-000")
    assert resultado["uf"] == "SP"
