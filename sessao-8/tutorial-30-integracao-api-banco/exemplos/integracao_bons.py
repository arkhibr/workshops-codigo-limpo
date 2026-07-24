"""
integracao_bons.py — Integração ponta-a-ponta API+Banco (o alvo verde)

Padrão: fixture pytest monta sqlite3.connect(":memory:") + TestClient(criar_app(conn))
por teste — a request HTTP percorre a stack real (rota -> validação -> SQL) até o
banco. O ponto pedagógico deste tutorial-âncora: cada teste verifica os DOIS
lados — a resposta HTTP **e** o estado persistido, consultando `conn` diretamente.
Verificar só a resposta prova que a API "respondeu certo"; reler o banco prova que
o dado realmente foi gravado.
Execute: pytest integracao_bons.py -v
"""
import sqlite3
import pytest
from fastapi.testclient import TestClient
from app import criar_app


@pytest.fixture
def contexto():
    # check_same_thread=False: o TestClient roda os handlers síncronos em uma
    # worker thread do pool do anyio, diferente da thread principal do teste
    # que criou a conexão. As chamadas continuam sequenciais (nunca
    # concorrentes) então relaxar a checagem de afinidade de thread aqui é
    # seguro — é só isso, não é sinal de acesso concorrente ao sqlite3.
    conn = sqlite3.connect(":memory:", check_same_thread=False)
    cliente = TestClient(criar_app(conn))
    yield cliente, conn
    conn.close()


def test_post_pedido_persiste_no_banco(contexto):
    cliente, conn = contexto
    resposta = cliente.post("/pedidos", json={
        "cliente": "Ana",
        "itens": [{"produto": "Livro", "quantidade": 3, "preco_unitario": 10.0}],
    })
    assert resposta.status_code == 201
    pedido_id = resposta.json()["id"]
    # verifica o OUTRO lado: o dado realmente foi ao banco
    # (tuple(...): criar_app() define conn.row_factory = sqlite3.Row, e
    # sqlite3.Row não compara igual a uma tupla comum via ==)
    linha = conn.execute("SELECT cliente, total FROM pedidos WHERE id = ?",
                         (pedido_id,)).fetchone()
    assert tuple(linha) == ("Ana", 30.0)


def test_get_le_pedido_persistido(contexto):
    cliente, _ = contexto
    criado = cliente.post("/pedidos", json={
        "cliente": "Bob",
        "itens": [{"produto": "Caneta", "quantidade": 2, "preco_unitario": 5.0}],
    }).json()
    resposta = cliente.get(f"/pedidos/{criado['id']}")
    assert resposta.status_code == 200
    assert resposta.json()["total"] == 10.0
