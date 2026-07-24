"""
EXERCÍCIO 30 — Integração ponta-a-ponta API+Banco (tutorial-âncora)
Tempo estimado: 25 minutos

INSTRUÇÕES:
  A suíte abaixo testa a rota POST /pedidos/{id}/pagar mas tem o mesmo
  problema estrutural de exemplos/integracao_ruins.py (anti-padrão 2):
    - Só verifica a resposta HTTP — nunca confere o banco. O teste "prova"
      que a API respondeu {"status": "pago"}, mas não prova que o status
      "pago" foi realmente PERSISTIDO. Um bug em pagar_pedido() que devolvesse
      a resposta certa sem gravar o UPDATE (ou sem commitar) passaria
      despercebido.

  Refatore aplicando o padrão de exemplos/integracao_bons.py: depois de
  chamar a rota, releia o pedido diretamente via `conn.execute(...)` e
  confirme que o status "pago" está lá — não só na resposta HTTP.
  Execute: pytest exercicio.py -v (deve passar antes e depois da refatoração)

NOTA DE AUTOCONTENÇÃO: app.py, neste diretório, é uma cópia local do SUT
(idêntico a exemplos/app.py, com a rota adicional POST /pedidos/{id}/pagar)
— o repositório não permite que um arquivo importe de outro diretório, então
o SUT é replicado aqui para que o exercício rode de forma independente.
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


def test_pagar_pedido_muda_status_para_pago(contexto):
    cliente, conn = contexto
    criado = cliente.post("/pedidos", json={
        "cliente": "Ana",
        "itens": [{"produto": "Livro", "quantidade": 1, "preco_unitario": 10.0}],
    }).json()

    resposta = cliente.post(f"/pedidos/{criado['id']}/pagar")

    # ❌ Só confere a resposta HTTP — nunca relê o banco para confirmar que
    # o status "pago" foi de fato persistido em `pedidos`.
    assert resposta.status_code == 200
    assert resposta.json()["status"] == "pago"
