"""
EXERCÍCIO 28 — Testes de Integração de API
Tempo estimado: 20 minutos

INSTRUÇÕES:
  A suíte abaixo testa a rota POST /pedidos/{id}/pagar mas tem 3 problemas
  estruturais (os mesmos de exemplos/integracao_ruins.py):
    1. TestClient global compartilhado entre os testes (estado vaza).
    2. Só verifica status_code — nunca olha o corpo da resposta.
    3. Ordem importa — um teste assume que o pedido criado por outro teste
       ainda existe, com o id que ele espera.

  Refatore aplicando os padrões de exemplos/integracao_bons.py: fixture
  pytest que cria um TestClient(criar_app()) novo por teste, nomes
  comportamentais, e asserções sobre o contrato completo (status + corpo).
  Execute: pytest exercicio.py -v (deve passar antes e depois da refatoração)
"""
from fastapi.testclient import TestClient
from app import criar_app

# ❌ 1. Client global — o mesmo app e os mesmos pedidos são reaproveitados
# por todos os testes do módulo.
cliente = TestClient(criar_app())


def test_cria_pedido_para_pagar_depois():
    # ❌ 2. Só checa o status — não confirma id, total ou status "aberto".
    resposta = cliente.post("/pedidos", json={
        "cliente": "Bruno",
        "itens": [{"produto": "Caneta", "quantidade": 3, "preco_unitario": 5.0}],
    })
    assert resposta.status_code == 201


def test_paga_pedido():
    # ❌ 3. Ordem importa: assume que o pedido id=1, criado pelo teste
    # anterior via `cliente` global, ainda existe e está "aberto".
    resposta = cliente.post("/pedidos/1/pagar")
    assert resposta.status_code == 200


def test_pagar_pedido_novamente_falha():
    # ❌ 3 (de novo): depende do teste anterior já ter pago o pedido id=1.
    resposta = cliente.post("/pedidos/1/pagar")
    assert resposta.status_code == 409
