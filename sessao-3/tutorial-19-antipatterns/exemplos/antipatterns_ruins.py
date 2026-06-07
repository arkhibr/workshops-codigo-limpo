"""
antipatterns_ruins.py — God Object, Magic Strings/Numbers, Feature Envy, Copy-Paste Inheritance.
Execute: python3 antipatterns_ruins.py
"""
from typing import List, Optional
from dataclasses import dataclass, field


# ─── Modelos de domínio ───────────────────────────────────────────────────────

@dataclass
class Cliente:
    id:               str
    nome:             str
    email:            str
    nivel_fidelidade: str
    historico_compras: float = 0.0
    pontos_acumulados: int   = 0
    data_cadastro:    str   = "2020-01-01"

@dataclass
class ItemPedido:
    produto_id: str
    preco:      float
    quantidade: int


# ─── Anti-pattern 1: God Object ──────────────────────────────────────────────

class GestorClientePedido:
    """Uma classe que faz tudo — CRUD, validação, email, boleto, estoque, relatório."""

    def buscar_cliente(self, cliente_id: str) -> Optional[Cliente]:
        print(f"  [BD] buscar cliente {cliente_id}")
        return Cliente(cliente_id, "Empresa X", "x@x.com", "ouro", 5000.0, 200)

    def salvar_cliente(self, cliente: Cliente) -> None:
        print(f"  [BD] salvar cliente {cliente.id}")

    def validar_cpf(self, cpf: str) -> bool:
        return len(cpf.replace(".", "").replace("-", "")) == 11

    def calcular_total(self, itens: List[ItemPedido]) -> float:
        return sum(i.preco * i.quantidade for i in itens)

    def aplicar_desconto(self, total: float, percentual: float) -> float:
        return round(total * (1 - percentual), 2)

    def enviar_email(self, email: str, assunto: str, corpo: str) -> None:
        print(f"  [Email] → {email}: {assunto}")

    def gerar_boleto(self, valor: float, vencimento: str) -> str:
        return f"BOL-{int(valor)}-{vencimento}"

    def atualizar_estoque(self, produto_id: str, quantidade: int) -> None:
        print(f"  [Estoque] {produto_id}: -{quantidade}")

    def gerar_relatorio(self, cliente_id: str) -> str:
        return f"Relatório do cliente {cliente_id}"

    def exportar_csv(self, dados: list) -> str:
        return "id,valor\n" + "\n".join(str(d) for d in dados)

    def arquivar_pedido(self, pedido_id: str) -> None:
        print(f"  [BD] arquivar pedido {pedido_id}")

    def reprocessar_falha(self, pedido_id: str) -> bool:
        print(f"  [Fila] reprocessar {pedido_id}")
        return True


# ─── Anti-pattern 2: Magic Strings e Magic Numbers ───────────────────────────

def processar_por_status(status: str, tipo: str, valor: float, prazo: int) -> dict:
    resultado: dict = {}
    if status == "A":            # "A" = Ativo? Aprovado? Aberto?
        resultado["ativo"] = True
        if tipo == "P":          # "P" = Premium? Prioritário? Parcial?
            if valor > 1500:     # por que 1500? qual regra de negócio?
                prazo = 30       # 30 dias? horas? úteis? corridos?
            resultado["taxa_extra"] = valor * 0.02
        elif tipo == "N":
            resultado["taxa_extra"] = 0.0
    elif status == "I":
        resultado["ativo"] = False
    resultado["prazo"] = prazo
    resultado["tipo"]  = tipo
    return resultado


# ─── Anti-pattern 3: Feature Envy ────────────────────────────────────────────

@dataclass
class Pedido:
    id:    str
    itens: List[ItemPedido] = field(default_factory=list)

    def calcular_desconto_fidelidade(self, cliente: Cliente) -> float:
        """Este método sabe mais sobre Cliente do que sobre Pedido."""
        if cliente.nivel_fidelidade == "ouro":
            base  = cliente.historico_compras * 0.05
            bonus = cliente.pontos_acumulados * 0.001
            anos  = (2026 - int(cliente.data_cadastro[:4]))
            return min(base + bonus + anos * 2.0, 200.0)
        elif cliente.nivel_fidelidade == "prata":
            return min(cliente.pontos_acumulados * 0.001, 50.0)
        return 0.0


# ─── Anti-pattern 4: Copy-Paste Inheritance ──────────────────────────────────

class PedidoNormal:
    def calcular_total(self, itens: List[ItemPedido]) -> float:
        return round(sum(i.preco * i.quantidade for i in itens), 2)

class PedidoUrgente:
    def calcular_total(self, itens: List[ItemPedido]) -> float:       # copiado
        base = sum(i.preco * i.quantidade for i in itens)
        return round(base * 1.15, 2)                                  # +15% urgência

class PedidoAgendado:
    def calcular_total(self, itens: List[ItemPedido]) -> float:       # copiado
        base = sum(i.preco * i.quantidade for i in itens)
        return round(base + 5.0, 2)                                   # +R$5 agendamento


# ─── Demo ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=== Anti-patterns _ruins ===\n")

    print("1. God Object:")
    gestor = GestorClientePedido()
    cliente = gestor.buscar_cliente("CLI-100")
    metodos = [m for m in dir(gestor) if not m.startswith("_")]
    print(f"  GestorClientePedido tem {len(metodos)} métodos públicos")

    print("\n2. Magic Strings/Numbers:")
    resultado = processar_por_status("A", "P", 2000.0, 15)
    print(f"  status='A', tipo='P', valor=2000 → {resultado}")

    print("\n3. Feature Envy:")
    pedido = Pedido("PED-001")
    desconto = pedido.calcular_desconto_fidelidade(cliente)
    print(f"  Pedido.calcular_desconto_fidelidade usa dados de Cliente: R${desconto:.2f}")

    print("\n4. Copy-Paste Inheritance:")
    itens = [ItemPedido("P001", 100.0, 2)]
    print(f"  Normal:   R${PedidoNormal().calcular_total(itens):.2f}")
    print(f"  Urgente:  R${PedidoUrgente().calcular_total(itens):.2f}")
    print(f"  Agendado: R${PedidoAgendado().calcular_total(itens):.2f}")
