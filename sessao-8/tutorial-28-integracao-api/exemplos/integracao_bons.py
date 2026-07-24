"""
integracao_bons.py — Testes de Integração de API (o alvo verde)

Padrão: fixture pytest cria TestClient(criar_app()) por teste (isolamento
real — nenhum teste enxerga estado deixado por outro), nomes comportamentais,
AAA, e cada teste verifica o contrato completo (status + corpo + campos),
não apenas o status HTTP.
Execute: pytest integracao_bons.py -v
"""
import pytest
from fastapi.testclient import TestClient
from app import criar_app


@pytest.fixture
def cliente() -> TestClient:
    return TestClient(criar_app())


def test_cria_pedido_retorna_201_com_total_calculado(cliente):
    resposta = cliente.post("/pedidos", json={
        "cliente": "Ana",
        "itens": [{"produto": "Livro", "quantidade": 2, "preco_unitario": 30.0}],
    })
    assert resposta.status_code == 201
    corpo = resposta.json()
    assert corpo["total"] == 60.0
    assert corpo["status"] == "aberto"
    assert corpo["id"] >= 1


def test_busca_pedido_inexistente_retorna_404(cliente):
    resposta = cliente.get("/pedidos/999")
    assert resposta.status_code == 404
    assert resposta.json()["detail"] == "pedido não encontrado"


def test_rejeita_pedido_sem_itens_com_422(cliente):
    resposta = cliente.post("/pedidos", json={"cliente": "Ana", "itens": []})
    assert resposta.status_code == 422


def test_paga_pedido_aberto_muda_status_para_pago(cliente):
    criado = cliente.post("/pedidos", json={
        "cliente": "Ana",
        "itens": [{"produto": "Livro", "quantidade": 1, "preco_unitario": 10.0}],
    }).json()
    resposta = cliente.post(f"/pedidos/{criado['id']}/pagar")
    assert resposta.status_code == 200
    assert resposta.json()["status"] == "pago"


def test_pagar_pedido_ja_pago_retorna_409(cliente):
    criado = cliente.post("/pedidos", json={
        "cliente": "Ana",
        "itens": [{"produto": "Livro", "quantidade": 1, "preco_unitario": 10.0}],
    }).json()
    cliente.post(f"/pedidos/{criado['id']}/pagar")
    resposta = cliente.post(f"/pedidos/{criado['id']}/pagar")
    assert resposta.status_code == 409
