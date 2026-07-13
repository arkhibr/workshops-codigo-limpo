"""
legado_bons.py — Seam via injeção de construtor + doubles + teste de caracterização.
Execute: pytest legado_bons.py -v
"""


class GerenciadorEstoque:
    def __init__(self, banco, servico_precos, cache_precos=None):
        self._banco = banco
        self._servico_precos = servico_precos
        self._cache_precos = cache_precos if cache_precos is not None else {}

    def recalcular_estoque(self, produto_id: str, quantidade_vendida: int) -> int:
        preco = self._cache_precos.get(produto_id)
        if preco is None:
            preco = self._servico_precos.consultar(produto_id)
            self._cache_precos[produto_id] = preco
        estoque_atual = self._banco.buscar_estoque(produto_id)
        novo_estoque = estoque_atual - quantidade_vendida
        valor_total = novo_estoque * preco
        self._banco.atualizar_estoque(produto_id, novo_estoque, valor_total)
        return novo_estoque


class BancoEstoqueFake:
    """Fake em memória — também atua como builder do estado inicial (com_estoque)."""

    def __init__(self):
        self._estoques = {}
        self.ultimo_valor_total = None

    def com_estoque(self, produto_id: str, quantidade: int) -> "BancoEstoqueFake":
        self._estoques[produto_id] = quantidade
        return self

    def buscar_estoque(self, produto_id: str) -> int:
        return self._estoques.get(produto_id, 0)

    def atualizar_estoque(self, produto_id: str, quantidade: int, valor_total: float) -> None:
        self._estoques[produto_id] = quantidade
        self.ultimo_valor_total = valor_total


class ServicoPrecoStub:
    def __init__(self, preco: float):
        self._preco = preco
        self.chamadas = 0

    def consultar(self, produto_id: str) -> float:
        self.chamadas += 1
        return self._preco


def test_caracterizacao_recalculo_com_estoque_suficiente():
    # Teste de caracterização: congela o comportamento atual do legado como
    # oráculo, sem julgar se a regra de negócio está correta.
    banco = BancoEstoqueFake().com_estoque("PROD1", 100)
    precos = ServicoPrecoStub(preco=10.0)
    gerenciador = GerenciadorEstoque(banco, precos)

    novo_estoque = gerenciador.recalcular_estoque("PROD1", 30)

    assert novo_estoque == 70
    assert banco.ultimo_valor_total == 700.0


def test_recalculo_com_venda_maior_que_estoque_gera_saldo_negativo():
    # Caso de borda descoberto durante a caracterização: o legado não valida
    # estoque insuficiente. Documentamos o comportamento atual; decidir se
    # corrige é uma decisão de produto, não deste teste.
    banco = BancoEstoqueFake().com_estoque("PROD1", 10)
    precos = ServicoPrecoStub(preco=5.0)
    gerenciador = GerenciadorEstoque(banco, precos)

    novo_estoque = gerenciador.recalcular_estoque("PROD1", 30)

    assert novo_estoque == -20


def test_recalculo_reaproveita_preco_em_cache_na_segunda_chamada():
    banco = BancoEstoqueFake().com_estoque("PROD1", 100)
    precos = ServicoPrecoStub(preco=10.0)
    gerenciador = GerenciadorEstoque(banco, precos)

    gerenciador.recalcular_estoque("PROD1", 10)
    gerenciador.recalcular_estoque("PROD1", 5)

    assert precos.chamadas == 1
