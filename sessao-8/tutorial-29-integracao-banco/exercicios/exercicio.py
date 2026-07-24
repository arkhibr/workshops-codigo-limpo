"""
EXERCÍCIO 29 — Testes de Integração de Banco de Dados
Tempo estimado: 20 minutos

INSTRUÇÕES:
  A suíte abaixo testa total_gasto_pelo_cliente(conn, cliente_id) mas tem os
  mesmos 3 problemas estruturais de exemplos/integracao_ruins.py:
    1. Mocka a conexão (unittest.mock.MagicMock) — nenhum SQL roda de
       verdade, então uma soma errada ou uma query mal escrita nunca seria
       pega.
    2. Depende de um banco em arquivo (teste.db) — persistente e
       compartilhado entre execuções, nunca limpo.
    3. Sem schema isolado por teste — assume que as tabelas e os dados já
       existem (deixados por uma execução anterior).

  Refatore aplicando os padrões de exemplos/integracao_bons.py: fixture
  pytest que cria sqlite3.connect(":memory:") por teste, chama criar_schema,
  e verifica a soma real (e o isolamento entre clientes).
  Execute: pytest exercicio.py -v (deve passar antes e depois da refatoração)

NOTA DE AUTOCONTENÇÃO: repositorio.py, neste diretório, é uma cópia local do
SUT (idêntico a exemplos/repositorio.py) — o repositório não permite que um
arquivo importe de outro diretório, então o repositório é replicado aqui
para que o exercício rode de forma independente.
"""
import os
import tempfile
from unittest.mock import MagicMock

import repositorio

# ❌ 2. Banco em arquivo persistente compartilhado — sem limpeza entre
# execuções. Os dados de uma rodada anterior continuam lá na próxima.
CAMINHO_BANCO_COMPARTILHADO = os.path.join(tempfile.gettempdir(), "exercicio_29_teste.db")


def total_gasto_pelo_cliente_ruim(conn, cliente_id: int) -> float:
    # Implementação de referência usada só para alimentar o mock abaixo —
    # não é isso que o teste está exercitando de fato.
    pedidos = repositorio.listar_pedidos_do_cliente(conn, cliente_id)
    return sum(p["total"] for p in pedidos)


def test_total_gasto_soma_os_pedidos_do_cliente():
    # ❌ 1. Mocka a própria conexão — nenhum SQL roda. O teste "passa" porque
    # o mock devolve exatamente os dados programados, não porque a query
    # de repositorio.listar_pedidos_do_cliente está correta.
    conn_mock = MagicMock()
    conn_mock.execute.return_value.fetchall.return_value = [
        {"id": 1, "cliente_id": 1, "total": 30.0, "status": "aberto"},
        {"id": 2, "cliente_id": 1, "total": 20.0, "status": "aberto"},
    ]

    total = total_gasto_pelo_cliente_ruim(conn_mock, cliente_id=1)

    assert total == 50.0


def test_total_gasto_no_banco_compartilhado():
    # ❌ 3. Sem criar_schema isolado — assume que a tabela `pedidos` e o
    # cliente id=1 já existem no arquivo compartilhado (criados por uma
    # execução anterior deste mesmo teste).
    import sqlite3
    conn = sqlite3.connect(CAMINHO_BANCO_COMPARTILHADO)
    conn.row_factory = sqlite3.Row
    conn.execute(
        "CREATE TABLE IF NOT EXISTS pedidos ("
        " id INTEGER PRIMARY KEY AUTOINCREMENT,"
        " cliente_id INTEGER NOT NULL, total REAL NOT NULL,"
        " status TEXT NOT NULL DEFAULT 'aberto')"
    )
    conn.execute("INSERT INTO pedidos (cliente_id, total) VALUES (1, 15.0)")
    conn.commit()

    total = total_gasto_pelo_cliente_ruim(conn, cliente_id=1)

    # ❌ Esse assert só funciona por acaso: a cada execução da suíte, mais
    # uma linha de 15.0 é inserida no arquivo compartilhado, e o total
    # cresce — o teste não é repetível nem independente.
    assert total >= 15.0
    conn.close()
