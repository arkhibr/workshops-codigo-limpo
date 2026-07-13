"""
GABARITO 25 — Dublês de Teste
Seam via construtor: ServicoEntrega(api_cep, repositorio). ApiCepStub
devolve cidade/uf fixos; RepositorioEnderecoFake guarda em memória e
expõe foi_salvo() para inspeção. Sem time.sleep — roda em milissegundos.
Execute: pytest gabarito.py -v
"""


class ServicoEntrega:
    def __init__(self, api_cep, repositorio):
        self.api_cep = api_cep
        self.repositorio = repositorio

    def confirmar_endereco(self, pedido_id: str, cep: str) -> dict:
        endereco = self.api_cep.consultar(cep)
        self.repositorio.salvar(pedido_id, endereco)
        return endereco


class ApiCepStub:
    """Stub: devolve resposta fixa e pré-programada, sem chamada de rede real."""

    def __init__(self, cidade: str = "São Paulo", uf: str = "SP"):
        self._cidade = cidade
        self._uf = uf

    def consultar(self, cep: str) -> dict:
        return {"cep": cep, "cidade": self._cidade, "uf": self._uf}


class RepositorioEnderecoFake:
    """Fake: implementação funcional leve, em memória — sem banco real."""

    def __init__(self):
        self._enderecos = {}

    def salvar(self, pedido_id: str, endereco: dict) -> None:
        self._enderecos[pedido_id] = endereco

    def foi_salvo(self, pedido_id: str) -> bool:
        return pedido_id in self._enderecos


def test_confirma_endereco_retorna_uf_do_cep_consultado():
    # Arrange
    api_cep = ApiCepStub(cidade="São Paulo", uf="SP")
    repositorio = RepositorioEnderecoFake()
    servico = ServicoEntrega(api_cep, repositorio)

    # Act
    resultado = servico.confirmar_endereco("P001", "01000-000")

    # Assert
    assert resultado["uf"] == "SP"


def test_confirma_endereco_salva_endereco_no_repositorio():
    api_cep = ApiCepStub()
    repositorio = RepositorioEnderecoFake()
    servico = ServicoEntrega(api_cep, repositorio)

    servico.confirmar_endereco("P002", "20000-000")

    assert repositorio.foi_salvo("P002")


def test_confirma_endereco_usa_cidade_configurada_no_stub():
    api_cep = ApiCepStub(cidade="Rio de Janeiro", uf="RJ")
    repositorio = RepositorioEnderecoFake()
    servico = ServicoEntrega(api_cep, repositorio)

    resultado = servico.confirmar_endereco("P003", "20000-000")

    assert resultado["cidade"] == "Rio de Janeiro"
