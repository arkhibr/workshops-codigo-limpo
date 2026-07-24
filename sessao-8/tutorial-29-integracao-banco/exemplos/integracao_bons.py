"""
integracao_bons.py — Testes de Integração de Banco de Dados (o alvo verde)

Padrão: fixture pytest cria sqlite3.connect(":memory:") por teste (isolamento
real — nenhum teste enxerga estado deixado por outro), chama criar_schema,
garante PRAGMA foreign_keys = ON, e fecha a conexão no teardown. Os testes
rodam SQL de verdade: constraints (FK, CHECK) e efeitos colaterais reais no
banco são exercitados, não simulados.
Execute: pytest integracao_bons.py -v
"""
import sqlite3
import pytest
import repositorio


@pytest.fixture
def conn():
    c = sqlite3.connect(":memory:")
    c.execute("PRAGMA foreign_keys = ON")
    repositorio.criar_schema(c)
    yield c
    c.close()


def test_insere_e_recupera_pedido_do_cliente(conn):
    cliente_id = repositorio.inserir_cliente(conn, "Ana", vip=True)
    pedido_id = repositorio.inserir_pedido(conn, cliente_id, 90.0)
    pedido = repositorio.buscar_pedido(conn, pedido_id)
    assert pedido == {"id": pedido_id, "cliente_id": cliente_id,
                      "total": 90.0, "status": "aberto"}


def test_rejeita_pedido_com_cliente_inexistente(conn):
    with pytest.raises(sqlite3.IntegrityError):
        repositorio.inserir_pedido(conn, cliente_id=999, total=10.0)


def test_rejeita_pedido_com_total_negativo(conn):
    cliente_id = repositorio.inserir_cliente(conn, "Ana")
    with pytest.raises(sqlite3.IntegrityError):
        repositorio.inserir_pedido(conn, cliente_id, total=-5.0)


def test_lista_apenas_pedidos_do_cliente_pedido(conn):
    ana = repositorio.inserir_cliente(conn, "Ana")
    bob = repositorio.inserir_cliente(conn, "Bob")
    repositorio.inserir_pedido(conn, ana, 10.0)
    repositorio.inserir_pedido(conn, bob, 20.0)
    assert len(repositorio.listar_pedidos_do_cliente(conn, ana)) == 1
