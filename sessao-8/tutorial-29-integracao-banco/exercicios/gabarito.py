"""
GABARITO 29 — Testes de Integração de Banco de Dados
Suíte refatorada: fixture cria sqlite3.connect(":memory:") por teste,
chama criar_schema, e verifica a soma real (SQL de verdade) e o isolamento
entre clientes — nenhum mock, nenhum arquivo compartilhado.
Execute: pytest gabarito.py -v
"""
import sqlite3
import pytest
import repositorio


def total_gasto_pelo_cliente(conn: sqlite3.Connection, cliente_id: int) -> float:
    pedidos = repositorio.listar_pedidos_do_cliente(conn, cliente_id)
    return sum(p["total"] for p in pedidos)


@pytest.fixture
def conn():
    c = sqlite3.connect(":memory:")
    c.execute("PRAGMA foreign_keys = ON")
    repositorio.criar_schema(c)
    yield c
    c.close()


def test_total_gasto_soma_os_pedidos_do_cliente(conn):
    cliente_id = repositorio.inserir_cliente(conn, "Ana")
    repositorio.inserir_pedido(conn, cliente_id, 30.0)
    repositorio.inserir_pedido(conn, cliente_id, 20.0)

    total = total_gasto_pelo_cliente(conn, cliente_id)

    assert total == 50.0


def test_total_gasto_e_zero_para_cliente_sem_pedidos(conn):
    cliente_id = repositorio.inserir_cliente(conn, "Ana")

    total = total_gasto_pelo_cliente(conn, cliente_id)

    assert total == 0.0


def test_total_gasto_nao_soma_pedidos_de_outro_cliente(conn):
    ana = repositorio.inserir_cliente(conn, "Ana")
    bob = repositorio.inserir_cliente(conn, "Bob")
    repositorio.inserir_pedido(conn, ana, 30.0)
    repositorio.inserir_pedido(conn, bob, 100.0)

    total_ana = total_gasto_pelo_cliente(conn, ana)

    assert total_ana == 30.0
