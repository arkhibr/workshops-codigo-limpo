"""
SAÍDA TÍPICA DE IA — endpoint de consulta de cliente (prompt funcional puro)
Referência: Tutorial 13 — Segurança em Código Gerado por IA

⚠️  Este arquivo é INTENCIONALMENTE INSEGURO.
    Representa o código que uma IA gera quando segurança não é especificada no prompt.
    Analise as brechas antes de ver a versão revisada.

Brechas demonstradas:
  1. Credencial hardcoded no código-fonte
  2. Query montada por concatenação de string (injeção simulada)
  3. Sem validação do parâmetro de entrada

Execute: python3 sessao-6/tutorial-13-seguranca-codigo-ia/exemplos/consulta_gerado.py
"""

# Prompt usado: "cria uma função que consulta cliente por ID no banco de dados"

# ─── Brecha 1: credencial hardcoded ───────────────────────────────────────────
DB_SENHA = "s3nh4_producao_2024"       # visível para qualquer um com acesso ao repo
API_KEY = "sk-abc123xyz789secret"      # token de API hardcoded

# banco de dados simulado em memória (substitui conexão real para a demonstração)
_banco = {
    "1001": {"nome": "Ana Lima",    "email": "ana@exemplo.com",    "saldo": 1500.00},
    "2002": {"nome": "Carlos Souza","email": "carlos@exemplo.com", "saldo": 3200.00},
}


def consultar_cliente(parametro):
    # ─── Brecha 2: concatenação de string ─────────────────────────────────────
    # A IA montou a "query" juntando o parâmetro diretamente na string.
    # Em um banco real, isso permitiria injeção de SQL.
    # Aqui simulamos o efeito: a entrada controla quais registros são retornados.
    query = "SELECT * FROM clientes WHERE id = " + str(parametro)
    print(f"  Query executada: {query}")

    # ─── Simulação do efeito da injeção ───────────────────────────────────────
    # Sem parametrização, a entrada controla a lógica de busca.
    # Uma entrada como "1001 OR true" faz a condição sempre ser verdadeira
    # e retorna TODOS os registros — como aconteceria em SQL real.
    if " OR " in str(parametro).upper() or "%" in str(parametro):
        # simula o efeito de uma condição sempre-verdadeira (injeção bem-sucedida)
        print("  [INJEÇÃO DETECTADA NA SIMULAÇÃO] Condição sempre verdadeira — retornando todos os registros:")
        return list(_banco.values())

    # ─── Brecha 3: sem validação ───────────────────────────────────────────────
    # Aceita qualquer valor sem verificar formato ou tipo.
    resultado = _banco.get(str(parametro))
    return resultado


# ─── Execução de demonstração ─────────────────────────────────────────────────

if __name__ == "__main__":
    print("=== Demonstração: consulta_gerado.py (INTENCIONALMENTE INSEGURO) ===")
    print()

    print("--- Consulta normal (ID legítimo) ---")
    resultado = consultar_cliente("1001")
    print(f"  Resultado: {resultado}")
    print()

    print("--- Consulta com entrada maliciosa (injeção simulada) ---")
    # em SQL real: WHERE id = 1001 OR 1=1  → retorna todos os registros
    entrada_maliciosa = "1001 OR 1=1"
    resultado_injetado = consultar_cliente(entrada_maliciosa)
    print(f"  Registros retornados: {len(resultado_injetado)}")
    for cliente in resultado_injetado:
        print(f"    {cliente}")
    print()

    print("--- Brecha 1: segredos visíveis no código ---")
    print(f"  DB_SENHA = '{DB_SENHA}'")
    print(f"  API_KEY  = '{API_KEY}'")
    print()

    print("Conclusão: sem validação e sem parametrização, a entrada do usuário")
    print("controla quais dados são retornados — e as credenciais estão expostas.")
