"""
EXERCÍCIO 01 — Nomes Significativos
Tempo estimado: 10 minutos
Referência: Clean Code, Cap. 2

INSTRUÇÕES:
  Renomeie todas as variáveis, parâmetros, funções e classes abaixo
  para que os nomes revelem claramente a intenção do código.
  Não altere a lógica — apenas os nomes.

Execute para verificar que o código funciona antes e depois:
  python exercicio.py
"""

# ─── Problema 1 ───────────────────────────────────────────────────────────────
# O que este código calcula? Renomeie para tornar óbvio.

x = 86400
y = 7
z = x * y

def calc(a, b):
    return a * b / 100


# ─── Problema 2 ───────────────────────────────────────────────────────────────
# Esta classe gerencia um carrinho de compras.
# Renomeie tudo para refletir isso.

class Mgr:
    def __init__(self):
        self.lst = []
        self.cnt = 0
        self.ttl = 0.0

    def add(self, itm, prc):
        self.lst.append({"itm": itm, "prc": prc})
        self.cnt += 1
        self.ttl += prc

    def rmv(self, itm):
        self.lst = [i for i in self.lst if i["itm"] != itm]
        self.cnt = len(self.lst)
        self.ttl = sum(i["prc"] for i in self.lst)

    def gt_all(self):
        return self.lst

    def gt_ttl(self):
        return self.ttl


# ─── Problema 3 ───────────────────────────────────────────────────────────────
# Esta função verifica se um usuário pode acessar um recurso.
# Renomeie os parâmetros e a função.

def proc(u, r, adm):
    if adm:
        return True
    return r in u.get("prms", [])


# ─── Verificação (não altere este bloco) ──────────────────────────────────────

if __name__ == "__main__":
    print("=== Problema 1 ===")
    print(f"x={x}, y={y}, z={z}")
    print(f"calc(200, 10) = {calc(200, 10)}")

    print("\n=== Problema 2 ===")
    m = Mgr()
    m.add("Camiseta", 89.90)
    m.add("Calça", 159.90)
    print(f"Itens: {m.gt_all()}")
    print(f"Total: R$ {m.gt_ttl():.2f}")
    m.rmv("Camiseta")
    print(f"Após remover Camiseta: R$ {m.gt_ttl():.2f}")

    print("\n=== Problema 3 ===")
    usuario = {"nome": "João", "prms": ["leitura", "escrita"]}
    print(f"Acesso leitura: {proc(usuario, 'leitura', False)}")
    print(f"Acesso admin:   {proc(usuario, 'exclusao', True)}")
