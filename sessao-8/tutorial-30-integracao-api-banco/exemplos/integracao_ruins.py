"""
integracao_ruins.py — Anti-padrões de Integração ponta-a-ponta (passam, mas mentem)

Todos os testes abaixo PASSAM — o problema não é a execução, é a estrutura.
Cada um ilustra o anti-padrão central deste tutorial-âncora: "integração
vertical falsa" — o teste parece exercitar API + banco, mas na verdade nunca
toca SQL de verdade, e/ou só confere a resposta HTTP sem nunca reler o banco.
Compare com integracao_bons.py.

Execute: pytest integracao_ruins.py -v
"""
import sqlite3
from unittest.mock import MagicMock

from fastapi.testclient import TestClient
from app import criar_app


# ❌ 1. "Integração vertical falsa": injeta um MagicMock no lugar da conexão
# sqlite3 real. A suíte parece testar HTTP -> app -> banco (é o mesmo
# criar_app(conn) do SUT real), mas nenhum SQL roda de verdade — nenhum
# INSERT, nenhuma constraint, nenhum commit acontece. O teste "passa" porque
# o mock devolve exatamente o que foi programado para devolver, não porque a
# stack real funciona.
def test_post_pedido_com_banco_mockado():
    conn_mock = MagicMock()
    conn_mock.execute.return_value.lastrowid = 1

    cliente = TestClient(criar_app(conn_mock))
    resposta = cliente.post("/pedidos", json={
        "cliente": "Ana",
        "itens": [{"produto": "Livro", "quantidade": 3, "preco_unitario": 10.0}],
    })

    # "Verde", mas isso não prova que o banco de verdade aceitaria (ou
    # gravaria corretamente) este pedido — o mock nunca deixou o SQL rodar,
    # então um INSERT com SQL errado ou uma constraint violada (CHECK total
    # >= 0) nunca seria detectado aqui.
    assert resposta.status_code == 201


# ❌ 2. Só verifica a resposta HTTP — nunca confere o banco. Um bug de
# persistência (campo trocado, commit esquecido, total gravado errado) passa
# despercebido porque o teste nunca releu `conn` para confirmar o que foi
# efetivamente gravado.
def test_post_pedido_so_confere_resposta_http():
    conn = sqlite3.connect(":memory:", check_same_thread=False)
    cliente = TestClient(criar_app(conn))

    resposta = cliente.post("/pedidos", json={
        "cliente": "Bob",
        "itens": [{"produto": "Caneta", "quantidade": 2, "preco_unitario": 5.0}],
    })

    # ❌ Só olha o status e o corpo da resposta — nunca faz
    # conn.execute("SELECT ...") para confirmar que o pedido foi persistido
    # com os valores certos. Se app.py tivesse um bug de persistência (por
    # exemplo, gravar `total` errado ou esquecer o commit), esse teste
    # continuaria verde.
    assert resposta.status_code == 201
    assert resposta.json()["cliente"] == "Bob"
