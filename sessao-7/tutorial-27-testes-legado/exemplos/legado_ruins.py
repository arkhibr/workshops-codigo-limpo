"""
legado_ruins.py — Módulo legado sem seams, sem testes, com estado global escondido.
Execute: pytest legado_ruins.py -v
"""
import pytest


class ConexaoBancoReal:
    def buscar_estoque(self, produto_id: str) -> int:
        raise ConnectionError("Não há banco de dados real disponível neste ambiente")

    def atualizar_estoque(self, produto_id: str, quantidade: int, valor_total: float) -> None:
        raise ConnectionError("Não há banco de dados real disponível neste ambiente")


class ServicoPrecoExternoReal:
    def consultar(self, produto_id: str) -> float:
        raise ConnectionError("Não há serviço de preço real disponível neste ambiente")


class GerenciadorEstoque:
    _cache_precos = {}  # estado global mutável compartilhado entre todas as instâncias

    def __init__(self):
        # sem seam: dependências instanciadas diretamente, impossível testar em isolamento
        self.banco = ConexaoBancoReal()
        self.servico_precos = ServicoPrecoExternoReal()

    def recalcular_estoque(self, produto_id: str, quantidade_vendida: int) -> int:
        preco = GerenciadorEstoque._cache_precos.get(produto_id)
        if preco is None:
            preco = self.servico_precos.consultar(produto_id)
            GerenciadorEstoque._cache_precos[produto_id] = preco
        estoque_atual = self.banco.buscar_estoque(produto_id)
        novo_estoque = estoque_atual - quantidade_vendida
        valor_total = novo_estoque * preco
        self.banco.atualizar_estoque(produto_id, novo_estoque, valor_total)
        return novo_estoque


def test_impossivel_testar_sem_infraestrutura_real():
    """
    Sem seam, não há como substituir banco/serviço de preço por um double.
    Este teste documenta a impossibilidade: falha por falta de
    infraestrutura real, não por um bug de lógica.
    """
    with pytest.raises(ConnectionError):
        gerenciador = GerenciadorEstoque()
        gerenciador.recalcular_estoque("PROD1", 10)
