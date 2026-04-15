"""
GABARITO 01 — Nomes Significativos
Abra este arquivo apenas após tentar o exercício por conta própria.
"""

# ─── Solução 1 ────────────────────────────────────────────────────────────────

SEGUNDOS_POR_DIA  = 86400
DIAS_POR_SEMANA   = 7
SEGUNDOS_POR_SEMANA = SEGUNDOS_POR_DIA * DIAS_POR_SEMANA

def calcular_desconto(preco, percentual):
    return preco * percentual / 100


# ─── Solução 2 ────────────────────────────────────────────────────────────────

class CarrinhoDeCompras:
    def __init__(self):
        self.itens        = []
        self.quantidade   = 0
        self.total        = 0.0

    def adicionar_item(self, nome_produto, preco):
        self.itens.append({"produto": nome_produto, "preco": preco})
        self.quantidade += 1
        self.total      += preco

    def remover_item(self, nome_produto):
        self.itens    = [i for i in self.itens if i["produto"] != nome_produto]
        self.quantidade = len(self.itens)
        self.total    = sum(i["preco"] for i in self.itens)

    def listar_itens(self):
        return self.itens

    def obter_total(self):
        return self.total


# ─── Solução 3 ────────────────────────────────────────────────────────────────

def usuario_tem_acesso_ao_recurso(usuario, recurso, eh_administrador):
    if eh_administrador:
        return True
    return recurso in usuario.get("permissoes", [])


# ─── Verificação ──────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=== Solução 1 ===")
    print(f"Segundos por semana: {SEGUNDOS_POR_SEMANA}")
    print(f"Desconto de 10% em R$200: R${calcular_desconto(200, 10):.2f}")

    print("\n=== Solução 2 ===")
    carrinho = CarrinhoDeCompras()
    carrinho.adicionar_item("Camiseta", 89.90)
    carrinho.adicionar_item("Calça", 159.90)
    print(f"Itens: {carrinho.listar_itens()}")
    print(f"Total: R$ {carrinho.obter_total():.2f}")
    carrinho.remover_item("Camiseta")
    print(f"Após remover Camiseta: R$ {carrinho.obter_total():.2f}")

    print("\n=== Solução 3 ===")
    usuario = {"nome": "João", "permissoes": ["leitura", "escrita"]}
    print(f"Acesso leitura: {usuario_tem_acesso_ao_recurso(usuario, 'leitura', False)}")
    print(f"Acesso admin:   {usuario_tem_acesso_ao_recurso(usuario, 'exclusao', True)}")
