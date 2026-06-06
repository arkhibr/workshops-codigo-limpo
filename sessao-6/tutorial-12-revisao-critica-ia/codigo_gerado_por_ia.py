"""
gateway_pagamento.py — Módulo de integração com gateway de pagamento

Gerado por IA a partir do prompt em prompt_original.md.
ATENÇÃO: contém problemas propositais para revisar. Não corrigir aqui.

Como executar:
    python3 sessao-6/tutorial-12-revisao-critica-ia/codigo_gerado_por_ia.py
"""

import json
import time
import random
import hashlib
from typing import Optional

# ---------------------------------------------------------------------------
# PROBLEMA 1 — Segurança: chave de API hardcoded em código-fonte.
# Em produção essa string estaria exposta em qualquer repositório.
# ---------------------------------------------------------------------------
API_KEY = "sk-prod-2b7f3e9a4c1d0f6e8a2b5c7d9e1f3a5b"
BASE_URL = "https://api.gateway-pagamentos.com.br/v2"


# ---------------------------------------------------------------------------
# Simulação local da lib fictícia (necessária para o arquivo rodar).
# O método alucinado está isolado em _cobrar_parcelado (não chamado na demo).
# ---------------------------------------------------------------------------
class _GatewayHttpClient:
    """Simulação mínima de cliente HTTP — usada para o arquivo rodar sem rede."""

    def post(self, url: str, payload: dict, headers: dict) -> dict:
        # Simula resposta de sucesso para a demo
        return {
            "status": "aprovado",
            "codigo_autorizacao": f"AUTH-{random.randint(100000, 999999)}",
            "mensagem": "Transação aprovada",
        }

    def get(self, url: str, headers: dict) -> dict:
        return {"status": "aprovado"}


_cliente_http = _GatewayHttpClient()


# ---------------------------------------------------------------------------
# PROBLEMA 6 — Comentário que mente: afirma validar o CPF,
# mas a função apenas verifica se a string tem 11 dígitos.
# Não aplica o algoritmo de verificação de dígitos verificadores.
# ---------------------------------------------------------------------------
def _validar_cpf(cpf: str) -> bool:
    """Valida o CPF do titular do cartão conforme regras da Receita Federal."""
    cpf_limpo = cpf.replace(".", "").replace("-", "")
    return len(cpf_limpo) == 11 and cpf_limpo.isdigit()


def _montar_headers() -> dict:
    return {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}",
    }


def cobrar(
    valor: float,
    numero_cartao: str,
    cpf_titular: str,
    parcelas: int = 1,
    descricao: str = "",
) -> dict:
    """
    Realiza uma cobrança no cartão de crédito.

    Retorna dicionário com status, código de autorização e mensagem.
    """
    # PROBLEMA 5 — Edge case ausente: não verifica valor <= 0.
    # Uma cobrança de R$ 0,00 ou valor negativo é enviada normalmente ao gateway.

    if not _validar_cpf(cpf_titular):
        return {"ok": False, "erro": "CPF inválido"}

    # PROBLEMA 2 — Injeção: URL montada por concatenação de string.
    # Se 'descricao' contiver caracteres especiais ou path traversal,
    # a URL resultante fica malformada ou pode ser explorada.
    url = BASE_URL + "/cobrancas?descricao=" + descricao

    payload = {
        "valor": valor,
        "cartao": numero_cartao,
        "cpf": cpf_titular,
        "parcelas": parcelas,
    }

    resposta_bruta = _cliente_http.post(url, payload, _montar_headers())

    # PROBLEMA 3 — Lógica invertida: a condição verifica 'not aprovado'
    # mas o bloco de sucesso está dentro do if, e o bloco de falha no else.
    # O resultado: status "aprovado" cai no bloco de erro e vice-versa.
    if resposta_bruta.get("status") != "aprovado":
        return {
            "ok": True,
            "codigo_autorizacao": resposta_bruta.get("codigo_autorizacao"),
            "mensagem": resposta_bruta.get("mensagem"),
        }
    else:
        return {
            "ok": False,
            "erro": f"Cobrança recusada: {resposta_bruta.get('mensagem')}",
        }


def _cobrar_parcelado(valor: float, numero_cartao: str, parcelas: int) -> dict:
    """
    Cobra em parcelas usando o endpoint de parcelamento dedicado.

    ATENÇÃO — PROBLEMA 4 (alucinação): _cliente_http.post_parcelado()
    não existe na lib simulada acima. Esta função não é chamada pela demo
    e está aqui apenas para que o revisor identifique a alucinação.
    """
    url = BASE_URL + "/cobrancas/parceladas"
    payload = {"valor": valor, "cartao": numero_cartao, "parcelas": parcelas}
    # Método inexistente — lançaria AttributeError em runtime
    return _cliente_http.post_parcelado(url, payload, _montar_headers())


def estornar(codigo_autorizacao: str, motivo: str = "") -> dict:
    """Estorna uma cobrança previamente aprovada pelo código de autorização."""
    url = BASE_URL + "/estornos/" + codigo_autorizacao
    payload = {"motivo": motivo}
    resposta = _cliente_http.post(url, payload, _montar_headers())
    return {"ok": True, "mensagem": resposta.get("mensagem", "Estorno processado")}


def consultar_status(codigo_autorizacao: str) -> dict:
    """Consulta o status atual de uma transação pelo código de autorização."""
    url = BASE_URL + "/transacoes/" + codigo_autorizacao
    resposta = _cliente_http.get(url, _montar_headers())
    return {"status": resposta.get("status"), "detalhes": resposta}


# ---------------------------------------------------------------------------
# Demo — caminho feliz. Todos os retornos esperados são impressos.
# NOTA: _cobrar_parcelado NÃO é chamado; a alucinação não estoura aqui.
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("=== Gateway de Pagamento — Demo ===\n")

    resultado = cobrar(
        valor=250.00,
        numero_cartao="4111111111111111",
        cpf_titular="123.456.789-09",
        parcelas=1,
        descricao="Pedido #1042",
    )
    print("Cobrança (caminho feliz):")
    print(json.dumps(resultado, indent=2, ensure_ascii=False))

    # Demonstra estorno e consulta
    if resultado.get("ok"):
        codigo = resultado.get("codigo_autorizacao", "AUTH-000000")
        print("\nEstorno:")
        print(json.dumps(estornar(codigo, "Solicitação do cliente"), indent=2, ensure_ascii=False))

        print("\nConsulta de status:")
        print(json.dumps(consultar_status(codigo), indent=2, ensure_ascii=False))
    else:
        print("\n[ATENÇÃO] A cobrança retornou ok=False — isso é o Problema 3 (condição invertida).")
        print("Na demo, o gateway simulado retorna 'aprovado', mas a lógica invertida")
        print("classifica isso como erro. Esse é exatamente o bug plantado para revisar.")
