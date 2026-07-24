"""
GABARITO 28 — Testes de Integração de API
Suíte refatorada: fixture por teste (isolamento real), nomes comportamentais,
contrato completo verificado (status + corpo), sem dependência de ordem.
Execute: pytest gabarito.py -v
"""
import pytest
from fastapi.testclient import TestClient
from app import criar_app


@pytest.fixture
def cliente() -> TestClient:
    return TestClient(criar_app())


def _cria_pedido_aberto(cliente: TestClient) -> dict:
    return cliente.post("/pedidos", json={
        "cliente": "Bruno",
        "itens": [{"produto": "Caneta", "quantidade": 3, "preco_unitario": 5.0}],
    }).json()


def test_cria_pedido_retorna_201_com_status_aberto(cliente):
    resposta = cliente.post("/pedidos", json={
        "cliente": "Bruno",
        "itens": [{"produto": "Caneta", "quantidade": 3, "preco_unitario": 5.0}],
    })
    assert resposta.status_code == 201
    corpo = resposta.json()
    assert corpo["total"] == 15.0
    assert corpo["status"] == "aberto"


def test_paga_pedido_aberto_muda_status_para_pago(cliente):
    pedido = _cria_pedido_aberto(cliente)
    resposta = cliente.post(f"/pedidos/{pedido['id']}/pagar")
    assert resposta.status_code == 200
    assert resposta.json()["status"] == "pago"


def test_pagar_pedido_ja_pago_retorna_409(cliente):
    pedido = _cria_pedido_aberto(cliente)
    cliente.post(f"/pedidos/{pedido['id']}/pagar")
    resposta = cliente.post(f"/pedidos/{pedido['id']}/pagar")
    assert resposta.status_code == 409
    assert resposta.json()["detail"] == "pedido já pago"


def test_pagar_pedido_inexistente_retorna_404(cliente):
    resposta = cliente.post("/pedidos/999/pagar")
    assert resposta.status_code == 404
    assert resposta.json()["detail"] == "pedido não encontrado"
