"""
GABARITO 30 — Integração ponta-a-ponta API+Banco (tutorial-âncora)
Suíte refatorada: além de conferir a resposta HTTP, relê o pedido diretamente
via `conn.execute(...)` para confirmar que o status "pago" foi realmente
persistido — verificando os DOIS lados, não só o contrato HTTP.
Execute: pytest gabarito.py -v
"""
import sqlite3
import pytest
from fastapi.testclient import TestClient
from app import criar_app


@pytest.fixture
def contexto():
    conn = sqlite3.connect(":memory:", check_same_thread=False)
    cliente = TestClient(criar_app(conn))
    yield cliente, conn
    conn.close()


def _cria_pedido_aberto(cliente: TestClient) -> dict:
    return cliente.post("/pedidos", json={
        "cliente": "Ana",
        "itens": [{"produto": "Livro", "quantidade": 1, "preco_unitario": 10.0}],
    }).json()


def test_pagar_pedido_persiste_status_pago_no_banco(contexto):
    cliente, conn = contexto
    criado = _cria_pedido_aberto(cliente)

    resposta = cliente.post(f"/pedidos/{criado['id']}/pagar")

    assert resposta.status_code == 200
    assert resposta.json()["status"] == "pago"
    # ✅ verifica o OUTRO lado: o status "pago" foi realmente gravado
    linha = conn.execute(
        "SELECT status FROM pedidos WHERE id = ?", (criado["id"],)
    ).fetchone()
    assert tuple(linha) == ("pago",)


def test_pagar_pedido_inexistente_retorna_404(contexto):
    cliente, _ = contexto
    resposta = cliente.post("/pedidos/999/pagar")
    assert resposta.status_code == 404


def test_pagar_pedido_ja_pago_retorna_409_e_nao_altera_banco(contexto):
    cliente, conn = contexto
    criado = _cria_pedido_aberto(cliente)
    cliente.post(f"/pedidos/{criado['id']}/pagar")

    resposta = cliente.post(f"/pedidos/{criado['id']}/pagar")

    assert resposta.status_code == 409
    # ✅ confirma que o banco continua com status "pago" (não foi corrompido
    # pela segunda tentativa de pagamento)
    linha = conn.execute(
        "SELECT status FROM pedidos WHERE id = ?", (criado["id"],)
    ).fetchone()
    assert tuple(linha) == ("pago",)
