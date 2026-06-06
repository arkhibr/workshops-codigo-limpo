"""
VERSÃO REVISADA — endpoint de consulta de cliente com segurança aplicada
Referência: Tutorial 13 — Segurança em Código Gerado por IA

Brechas corrigidas em relação à versão gerada:
  1. Credencial lida de configuração separada (simula variável de ambiente)
  2. Consulta parametrizada — entrada nunca é concatenada na query
  3. Validação explícita da entrada antes de qualquer operação
  4. Entrada maliciosa rejeitada com mensagem descritiva

Execute: python3 sessao-6/tutorial-13-seguranca-codigo-ia/exemplos/consulta_revisado.py
"""

from __future__ import annotations

import os
import re

# ─── Configuração lida de "ambiente" (sem segredo no código) ──────────────────
# Em produção: os.getenv("DB_SENHA") leria da variável de ambiente real.
# Aqui simulamos com um valor padrão explicitamente marcado como placeholder.
DB_SENHA = os.getenv("DB_SENHA", "<não configurado>")
API_KEY = os.getenv("API_KEY", "<não configurado>")

# ─── Constantes de validação ──────────────────────────────────────────────────
FORMATO_ID_VALIDO = re.compile(r"^\d{1,10}$")  # apenas dígitos, 1–10 caracteres

# ─── Banco de dados simulado em memória ───────────────────────────────────────
_banco_clientes: dict[str, dict] = {
    "1001": {"nome": "Ana Lima",    "email": "ana@exemplo.com",    "saldo": 1500.00},
    "2002": {"nome": "Carlos Souza","email": "carlos@exemplo.com", "saldo": 3200.00},
}


def _validar_id_cliente(id_cliente: str) -> None:
    """
    Verifica se o ID do cliente tem formato válido.

    Lança:
        ValueError: se o ID não for composto apenas por dígitos (1–10 caracteres).
    """
    if not FORMATO_ID_VALIDO.match(id_cliente):
        raise ValueError(
            f"ID inválido: '{id_cliente}'. Esperado: até 10 dígitos numéricos."
        )


def consultar_cliente(id_cliente: str) -> dict:
    """
    Consulta e retorna os dados do cliente pelo ID informado.

    A consulta é parametrizada: o ID é usado como chave de busca exata
    no repositório em memória — nunca concatenado em string de query.

    Lança:
        ValueError: se o ID for inválido ou o cliente não for encontrado.
    """
    _validar_id_cliente(id_cliente)

    # consulta parametrizada — busca por chave exata, sem concatenação de string
    cliente = _banco_clientes.get(id_cliente)

    if cliente is None:
        raise ValueError(f"Cliente com ID '{id_cliente}' não encontrado.")

    return cliente


# ─── Execução de demonstração ─────────────────────────────────────────────────

if __name__ == "__main__":
    print("=== Demonstração: consulta_revisado.py (seguro) ===")
    print()

    print("--- Consulta normal (ID legítimo) ---")
    try:
        resultado = consultar_cliente("1001")
        print(f"  Resultado: {resultado}")
    except ValueError as erro:
        print(f"  Erro: {erro}")
    print()

    print("--- Consulta com entrada maliciosa (deve ser rejeitada) ---")
    entrada_maliciosa = "1001 OR 1=1"
    try:
        resultado = consultar_cliente(entrada_maliciosa)
        print(f"  Resultado: {resultado}")
    except ValueError as erro:
        print(f"  Rejeitado corretamente: {erro}")
    print()

    print("--- Consulta com ID inexistente ---")
    try:
        resultado = consultar_cliente("9999")
        print(f"  Resultado: {resultado}")
    except ValueError as erro:
        print(f"  Não encontrado (esperado): {erro}")
    print()

    print("--- Configuração: segredos fora do código ---")
    print(f"  DB_SENHA lida do ambiente: '{DB_SENHA}'")
    print(f"  API_KEY lida do ambiente:  '{API_KEY}'")
    print()

    print("Conclusão: entrada maliciosa rejeitada antes de chegar à consulta;")
    print("credenciais não estão no código-fonte.")
