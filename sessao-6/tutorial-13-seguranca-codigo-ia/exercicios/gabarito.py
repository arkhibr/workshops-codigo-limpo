"""
GABARITO — busca de pedidos com segurança aplicada
Referência: Tutorial 13 — Segurança em Código Gerado por IA

Brechas corrigidas em relação ao exercício:
  1. Chave de integração lida de variável de ambiente (sem segredo no código)
  2. Nome do cliente validado antes de qualquer operação de busca
  3. Busca parametrizada — filtragem por comparação exata, sem concatenação de string
  4. Entrada maliciosa rejeitada com mensagem clara antes de processar

Execute: python3 sessao-6/tutorial-13-seguranca-codigo-ia/exercicios/gabarito.py
"""

from __future__ import annotations

import os
import re

# ─── Configuração lida de "ambiente" (sem segredo no código) ──────────────────
CHAVE_INTEGRACAO = os.getenv("CHAVE_INTEGRACAO", "<não configurado>")

# ─── Constantes de validação ──────────────────────────────────────────────────
FORMATO_NOME_VALIDO = re.compile(r"^[A-Za-zÀ-ÿ\s]{2,80}$")  # letras e espaços, 2–80 chars

# ─── Pedidos simulados em memória ─────────────────────────────────────────────
_pedidos: list[dict] = [
    {"id": "PED-001", "cliente": "Ana Lima",    "valor": 250.00, "status": "entregue"},
    {"id": "PED-002", "cliente": "Carlos Souza","valor": 89.90,  "status": "em_transito"},
    {"id": "PED-003", "cliente": "Ana Lima",    "valor": 410.00, "status": "processando"},
    {"id": "PED-004", "cliente": "Julia Rocha", "valor": 75.00,  "status": "entregue"},
]


def _validar_nome_cliente(nome_cliente: str) -> None:
    """
    Verifica se o nome do cliente tem formato válido.

    Lança:
        ValueError: se o nome contiver caracteres não permitidos ou estiver fora do tamanho esperado.
    """
    if not FORMATO_NOME_VALIDO.match(nome_cliente):
        raise ValueError(
            f"Nome inválido: '{nome_cliente}'. "
            "Esperado: letras e espaços, entre 2 e 80 caracteres."
        )


def buscar_pedidos_do_cliente(nome_cliente: str) -> list[dict]:
    """
    Retorna todos os pedidos do cliente informado.

    A busca é parametrizada: o nome é comparado por igualdade exata
    — nunca concatenado em string de query SQL.

    Lança:
        ValueError: se o nome do cliente tiver formato inválido.
    """
    _validar_nome_cliente(nome_cliente)

    # busca parametrizada — comparação exata, sem concatenação de string
    return [p for p in _pedidos if p["cliente"] == nome_cliente]


# ─── Execução de demonstração ─────────────────────────────────────────────────

if __name__ == "__main__":
    print("=== Gabarito: busca de pedidos (seguro) ===")
    print()

    print("--- Busca normal ---")
    try:
        pedidos = buscar_pedidos_do_cliente("Ana Lima")
        print(f"  Pedidos encontrados: {len(pedidos)}")
        for p in pedidos:
            print(f"    {p}")
    except ValueError as erro:
        print(f"  Erro: {erro}")
    print()

    print("--- Busca com entrada maliciosa (deve ser rejeitada) ---")
    entrada_maliciosa = "Ana Lima' OR '1'='1"
    try:
        pedidos = buscar_pedidos_do_cliente(entrada_maliciosa)
        print(f"  Pedidos encontrados: {len(pedidos)}")
    except ValueError as erro:
        print(f"  Rejeitado corretamente: {erro}")
    print()

    print("--- Busca com nome inexistente ---")
    try:
        pedidos = buscar_pedidos_do_cliente("Maria Silva")
        print(f"  Pedidos encontrados: {len(pedidos)}")
    except ValueError as erro:
        print(f"  Erro: {erro}")
    print()

    print("--- Configuração: chave fora do código ---")
    print(f"  CHAVE_INTEGRACAO lida do ambiente: '{CHAVE_INTEGRACAO}'")
    print()

    print("Conclusão: entrada maliciosa rejeitada pela validação;")
    print("chave de integração não está no código-fonte.")
