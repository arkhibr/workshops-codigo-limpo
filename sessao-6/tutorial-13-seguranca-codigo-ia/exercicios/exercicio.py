"""
EXERCÍCIO — busca de pedidos gerada por IA (com brechas de segurança)
Referência: Tutorial 13 — Segurança em Código Gerado por IA

⚠️  Este arquivo é INTENCIONALMENTE INSEGURO — é a saída da IA que você vai corrigir.

Tarefas:
  (1) Tire o segredo do código — mova para variável de configuração ou ambiente.
  (2) Parametrize e valide a entrada do usuário antes de usá-la na busca.
  (3) Liste todas as brechas que você identificou antes de começar a corrigir.

Execute: python3 sessao-6/tutorial-13-seguranca-codigo-ia/exercicios/exercicio.py
Gabarito: python3 sessao-6/tutorial-13-seguranca-codigo-ia/exercicios/gabarito.py
"""

# Prompt usado (fraco): "cria uma função que busca pedidos de um cliente pelo nome"

# ─── Brecha 1: chave de integração hardcoded ───────────────────────────────────
CHAVE_INTEGRACAO = "tok-pedidos-abc987xyz"   # exposta no código-fonte

# pedidos simulados em memória (substitui banco real)
_pedidos = [
    {"id": "PED-001", "cliente": "Ana Lima",    "valor": 250.00, "status": "entregue"},
    {"id": "PED-002", "cliente": "Carlos Souza","valor": 89.90,  "status": "em_transito"},
    {"id": "PED-003", "cliente": "Ana Lima",    "valor": 410.00, "status": "processando"},
    {"id": "PED-004", "cliente": "Julia Rocha", "valor": 75.00,  "status": "entregue"},
]


def buscar_pedidos(nome_cliente):
    # ─── Brecha 2: filtro montado por concatenação de string ──────────────────
    # A IA concatenou o valor diretamente no "filtro" de busca.
    # Em um banco real, isso seria vulnerável a injeção de SQL.
    # Aqui a concatenação está na string de log/diagnóstico, mas em produção
    # o mesmo padrão seria usado na query real.
    filtro = "SELECT * FROM pedidos WHERE cliente = '" + nome_cliente + "'"
    print(f"  Filtro aplicado: {filtro}")

    # ─── Brecha 3: sem validação do parâmetro ─────────────────────────────────
    # Aceita qualquer valor sem verificar tipo, formato ou tamanho.
    # Uma entrada vazia retorna lista vazia silenciosamente;
    # uma entrada com aspas quebra o SQL em bancos reais.
    resultados = [p for p in _pedidos if p["cliente"] == nome_cliente]

    # simulação do efeito de injeção por aspas simples na entrada
    if "'" in str(nome_cliente) or "--" in str(nome_cliente):
        print("  [INJEÇÃO SIMULADA] Aspas/comentário na entrada — em SQL real quebraria a query ou vazaria dados.")
        return list(_pedidos)  # simula retorno de todos os registros

    return resultados


# ─── Execução de demonstração ─────────────────────────────────────────────────

if __name__ == "__main__":
    print("=== Exercício: busca de pedidos (INTENCIONALMENTE INSEGURO) ===")
    print()

    print("--- Busca normal ---")
    pedidos = buscar_pedidos("Ana Lima")
    print(f"  Pedidos encontrados: {len(pedidos)}")
    for p in pedidos:
        print(f"    {p}")
    print()

    print("--- Busca com entrada maliciosa (aspas simples) ---")
    entrada_maliciosa = "Ana Lima' OR '1'='1"
    pedidos_injetados = buscar_pedidos(entrada_maliciosa)
    print(f"  Registros retornados: {len(pedidos_injetados)}")
    for p in pedidos_injetados:
        print(f"    {p}")
    print()

    print("--- Brecha: chave de integração visível ---")
    print(f"  CHAVE_INTEGRACAO = '{CHAVE_INTEGRACAO}'")
