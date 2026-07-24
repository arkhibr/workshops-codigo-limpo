"""
integracao_ruins.py — Anti-padrões de Testes de Integração (passam, mas mentem)

Todos os testes abaixo PASSAM — o problema não é a execução, é a estrutura.
Cada um ilustra um anti-padrão que compromete a confiança que o teste deveria
dar. Compare com integracao_bons.py.

Execute: pytest integracao_ruins.py -v
(o teste de rede real está marcado @pytest.mark.skip para não depender de
internet/CI offline — ver README, seção 5, sobre essa exceção documentada)
"""
import httpx
import pytest
from fastapi.testclient import TestClient
from app import criar_app

# ❌ 1. TestClient global compartilhado entre todos os testes do módulo.
# Estado (pedidos criados) vaza de um teste para o outro — a ordem de
# execução passa a importar, e paralelizar a suíte quebra tudo.
cliente = TestClient(criar_app())


def test_cria_pedido():
    # ❌ 2. Só verifica status_code — nunca olha o corpo da resposta.
    # Esse teste passaria mesmo se o total viesse errado, o cliente viesse
    # None, ou o status inicial não fosse "aberto".
    resposta = cliente.post("/pedidos", json={
        "cliente": "Ana",
        "itens": [{"produto": "Livro", "quantidade": 2, "preco_unitario": 30.0}],
    })
    assert resposta.status_code == 201


def test_busca_pedido_criado_anteriormente():
    # ❌ 3. Ordem importa: este teste assume que o pedido id=1 já existe
    # porque test_cria_pedido() rodou antes e usou o `cliente` global.
    # Rodar só este teste isoladamente (pytest -k busca_pedido) quebra.
    resposta = cliente.get("/pedidos/1")
    assert resposta.status_code == 200


@pytest.mark.skip(reason="depende de rede real — anti-padrão ilustrado")
def test_consulta_servico_externo():
    # ❌ 4. Dependência de rede real: chama um serviço HTTP de verdade pela
    # internet. Isso torna o teste lento, flaky (falha se a rede cair ou o
    # serviço estiver fora do ar) e não-repetível em ambientes isolados/CI
    # sem acesso externo. Marcado como skip para não quebrar CI offline —
    # mas o defeito estrutural é o mesmo mesmo quando "passa".
    resposta = httpx.get("https://httpbin.org/status/200")
    assert resposta.status_code == 200
