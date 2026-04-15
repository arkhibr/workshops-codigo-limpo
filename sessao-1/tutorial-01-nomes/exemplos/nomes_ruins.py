"""
EXEMPLOS: Nomes que violam os princípios do Clean Code
Referência: Clean Code, Cap. 2 — Meaningful Names
Execute: python nomes_ruins.py
"""

# ─── Problema 1: Nomes que não revelam intenção ──────────────────────────────

d = 0  # o que é "d"? dias? distância? dados?

def get(l, s):
    r = []
    for i in l:
        if i[0] == s:
            r.append(i)
    return r


# ─── Problema 2: Desinformação ────────────────────────────────────────────────

# "lista_de_contas" sugere uma list Python — mas é um dict!
lista_de_contas = {"joao": 1500.0, "maria": 3200.0}

# "hp" poderia ser hipotenusa, hit points, Hewlett-Packard...
def calc_hp(a, b):
    return (a ** 2 + b ** 2) ** 0.5


# ─── Problema 3: Distinções sem significado ───────────────────────────────────

def get_dados():
    return {"nome": "João"}

def get_dados2():
    return {"nome": "João", "idade": 30}

def get_dados_processados():
    return {"nome": "JOÃO"}  # o que muda exatamente?


# ─── Problema 4: Nomes impronunciáveis ────────────────────────────────────────

class DtRcrdMgr:
    def __init__(self):
        self.gnrtn_ymdhms = "2026-01-01 10:00:00"
        self.mdfy_ymdhms  = "2026-01-02 15:30:00"
        self.pszqint       = 10


# ─── Problema 5: Notação húngara e prefixos ───────────────────────────────────

str_nome     = "João Silva"
int_idade    = 30
lst_pedidos  = []
b_ativo      = True


# ─── Execução de demonstração ─────────────────────────────────────────────────

if __name__ == "__main__":
    pedidos = [
        ("pendente", "Pedido A"),
        ("entregue", "Pedido B"),
        ("pendente", "Pedido C"),
    ]
    print("Resultado de get(pedidos, 'pendente'):", get(pedidos, "pendente"))
    print("Resultado de calc_hp(3, 4):", calc_hp(3, 4))
    rec = DtRcrdMgr()
    print("gnrtn_ymdhms:", rec.gnrtn_ymdhms)
