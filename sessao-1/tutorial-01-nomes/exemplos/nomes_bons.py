"""
EXEMPLOS: Nomes que seguem os princípios do Clean Code
Referência: Clean Code, Cap. 2 — Meaningful Names
Execute: python nomes_bons.py
"""

# ─── Solução 1: Nomes que revelam intenção ────────────────────────────────────

dias_desde_criacao = 0

def filtrar_pedidos_por_status(pedidos, status):
    pedidos_filtrados = []
    for pedido in pedidos:
        if pedido[0] == status:
            pedidos_filtrados.append(pedido)
    return pedidos_filtrados


# ─── Solução 2: Sem desinformação ─────────────────────────────────────────────

# dict deixa claro que é um mapeamento nome → saldo
saldo_por_titular = {"joao": 1500.0, "maria": 3200.0}

def calcular_hipotenusa(cateto_a, cateto_b):
    return (cateto_a ** 2 + cateto_b ** 2) ** 0.5


# ─── Solução 3: Distinções significativas ─────────────────────────────────────

def get_usuario():
    return {"nome": "João"}

def get_usuario_com_idade():
    return {"nome": "João", "idade": 30}

def get_usuario_nome_maiusculo():
    return {"nome": "JOÃO"}


# ─── Solução 4: Nomes pronunciáveis ──────────────────────────────────────────

class GerenciadorDeRegistros:
    def __init__(self):
        self.data_criacao     = "2026-01-01 10:00:00"
        self.data_modificacao = "2026-01-02 15:30:00"
        self.quantidade_maxima = 10


# ─── Solução 5: Sem notação húngara ───────────────────────────────────────────

nome     = "João Silva"
idade    = 30
pedidos  = []
ativo    = True


# ─── Solução 6: Linguagem consistente com o domínio ──────────────────────────
#
# Regra: escolha UMA língua e UMA convenção para o domínio e mantenha-as.
# Em Python, use snake_case. Se o domínio é em português, use português.
# Misturar idiomas ou convenções força o leitor a fazer tradução mental
# constante e quebra buscas por grep/IDE.

def obter_dados_usuario(usuario_id: str) -> dict:
    """Retorna os dados do usuário pelo ID."""
    return {"id": usuario_id}

def listar_clientes_ativos() -> list:
    """Retorna a lista de clientes com status ativo."""
    return []


# ─── Execução de demonstração ─────────────────────────────────────────────────

if __name__ == "__main__":
    todos_os_pedidos = [
        ("pendente", "Pedido A"),
        ("entregue", "Pedido B"),
        ("pendente", "Pedido C"),
    ]
    print("Pedidos pendentes:", filtrar_pedidos_por_status(todos_os_pedidos, "pendente"))
    print("Hipotenusa (3, 4):", calcular_hipotenusa(3, 4))
    registro = GerenciadorDeRegistros()
    print("Data de criação:", registro.data_criacao)

    # Solução 6: nomes em snake_case, em português, no idioma do domínio
    print("\nobter_dados_usuario('U001'):", obter_dados_usuario("U001"))
    print("listar_clientes_ativos():", listar_clientes_ativos())
