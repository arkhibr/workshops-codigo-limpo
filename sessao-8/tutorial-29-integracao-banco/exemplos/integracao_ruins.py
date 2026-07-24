"""
integracao_ruins.py — Anti-padrões de Testes de Integração de Banco (passam, mas mentem)

Todos os testes abaixo PASSAM — o problema não é a execução, é a estrutura.
Cada um ilustra um anti-padrão que compromete a confiança que o teste deveria
dar. Compare com integracao_bons.py.

Execute: pytest integracao_ruins.py -v
(o arquivo usado pelo anti-padrão 2 fica em tempfile.gettempdir() — não no
diretório do tutorial — só para não sujar o repositório com um .db versionado;
o defeito estrutural, um arquivo compartilhado e nunca limpo entre execuções,
é o mesmo independente de onde o arquivo mora)
"""
import os
import tempfile
import sqlite3
from unittest.mock import MagicMock

import pytest


# ❌ 1. Mocka o próprio repositório: nenhum SQL roda de verdade.
# O teste "passa" porque o mock devolve exatamente o que foi programado pra
# devolver — SQL inválido, violação de constraint (FK, CHECK) ou uma
# transação mal fechada nunca seriam detectados aqui.
# ❌ mockar o que você quer testar prova nada
def test_inserir_pedido_chama_repositorio_mockado():
    repositorio_mock = MagicMock()
    repositorio_mock.inserir_pedido.return_value = 1

    pedido_id = repositorio_mock.inserir_pedido(conn=None, cliente_id=999, total=-50.0)

    # "Verde", mas isso não prova que o banco aceitaria cliente_id=999
    # (inexistente) nem total=-50.0 (viola CHECK total >= 0).
    assert pedido_id == 1
    repositorio_mock.inserir_pedido.assert_called_once()


# ❌ 2. Banco em arquivo persistente COMPARTILHADO entre execuções — sem
# limpeza. Cada rodada da suíte reaproveita o mesmo arquivo .db: os dados de
# uma execução anterior continuam lá na próxima, os testes ficam
# ordem-dependentes (um teste enxerga o que o anterior deixou) e rodar a
# suíte duas vezes seguidas pode dar resultados diferentes.
CAMINHO_BANCO_COMPARTILHADO = os.path.join(tempfile.gettempdir(), "teste.db")


def _conexao_compartilhada() -> sqlite3.Connection:
    # ❌ 3. Sem criar_schema isolado — assume que as tabelas já existem
    # (criadas por uma execução anterior, ou por outro teste). Na primeira
    # vez que o arquivo não existe, isso falha com "no such table"; depois
    # da primeira execução, o arquivo fica no disco para sempre.
    conn = sqlite3.connect(CAMINHO_BANCO_COMPARTILHADO)
    conn.row_factory = sqlite3.Row
    conn.execute(
        "CREATE TABLE IF NOT EXISTS clientes ("
        " id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT)"
    )
    return conn


def test_insere_cliente_no_banco_compartilhado():
    conn = _conexao_compartilhada()
    conn.execute("INSERT INTO clientes (nome) VALUES ('Ana')")
    conn.commit()

    total_depois = conn.execute("SELECT COUNT(*) FROM clientes").fetchone()[0]

    # ❌ Esse assert só funciona por acaso: se a suíte já rodou antes, o
    # arquivo já tem linhas de execuções passadas, e total_depois cresce a
    # cada rodada — o teste não é repetível nem independente.
    assert total_depois >= 1
    conn.close()
