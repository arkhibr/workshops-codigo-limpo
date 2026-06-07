"""
antipatterns_bons.py — Correção dos 4 anti-patterns: SRP, enums, method moved, herança correta.
Execute: python3 antipatterns_bons.py
"""
from typing import List, Optional
from dataclasses import dataclass, field
from enum import Enum
from abc import ABC, abstractmethod


# ─── Correção 1: God Object → classes com responsabilidade única ──────────────

class NivelFidelidade(str, Enum):
    BRONZE = "bronze"
    PRATA  = "prata"
    OURO   = "ouro"

@dataclass
class Cliente:
    id:               str
    nome:             str
    email:            str
    nivel_fidelidade: NivelFidelidade
    historico_compras: float = 0.0
    pontos_acumulados: int   = 0
    data_cadastro:    str   = "2020-01-01"

    # Correção 3: método movido para onde os dados vivem (Feature Envy)
    def calcular_desconto_fidelidade(self) -> float:
        if self.nivel_fidelidade == NivelFidelidade.OURO:
            base  = self.historico_compras * 0.05
            bonus = self.pontos_acumulados * 0.001
            anos  = (2026 - int(self.data_cadastro[:4]))
            return min(base + bonus + anos * 2.0, 200.0)
        elif self.nivel_fidelidade == NivelFidelidade.PRATA:
            return min(self.pontos_acumulados * 0.001, 50.0)
        return 0.0


class RepositorioCliente:
    def buscar(self, cliente_id: str) -> Optional[Cliente]:
        print(f"  [BD] buscar cliente {cliente_id}")
        return Cliente(cliente_id, "Empresa X", "x@x.com",
                       NivelFidelidade.OURO, 5000.0, 200)
    def salvar(self, cliente: Cliente) -> None:
        print(f"  [BD] salvar cliente {cliente.id}")

class ValidadorDocumento:
    def validar_cpf(self, cpf: str) -> bool:
        return len(cpf.replace(".", "").replace("-", "")) == 11

class ServicoNotificacao:
    def enviar_email(self, email: str, assunto: str) -> None:
        print(f"  [Email] → {email}: {assunto}")

class ServicoCobranca:
    def gerar_boleto(self, valor: float, vencimento: str) -> str:
        return f"BOL-{int(valor)}-{vencimento}"

class GeradorRelatorio:
    def gerar(self, cliente_id: str) -> str:
        return f"Relatório do cliente {cliente_id}"
    def exportar_csv(self, dados: list) -> str:
        return "id,valor\n" + "\n".join(str(d) for d in dados)


# ─── Correção 2: Magic Strings/Numbers → enums e constantes nomeadas ─────────

class StatusPedido(str, Enum):
    ATIVO   = "ativo"
    INATIVO = "inativo"

class TipoPedido(str, Enum):
    PREMIUM = "premium"
    NORMAL  = "normal"

LIMITE_FRETE_GRATIS:  float = 1500.0
PRAZO_PAGAMENTO_DIAS: int   = 30
TAXA_PREMIUM:         float = 0.02

def processar_por_status(
    status: StatusPedido,
    tipo:   TipoPedido,
    valor:  float,
    prazo:  int,
) -> dict:
    resultado: dict = {}
    if status == StatusPedido.ATIVO:
        resultado["ativo"] = True
        if tipo == TipoPedido.PREMIUM and valor > LIMITE_FRETE_GRATIS:
            prazo = PRAZO_PAGAMENTO_DIAS
            resultado["taxa_extra"] = round(valor * TAXA_PREMIUM, 2)
        else:
            resultado["taxa_extra"] = 0.0
    else:
        resultado["ativo"] = False
    resultado["prazo"] = prazo
    resultado["tipo"]  = tipo.value
    return resultado


# ─── Correção 4: Copy-Paste → herança com variação mínima ────────────────────

@dataclass
class ItemPedido:
    produto_id: str
    preco:      float
    quantidade: int

class PedidoBase(ABC):
    def calcular_total(self, itens: List[ItemPedido]) -> float:
        base = sum(i.preco * i.quantidade for i in itens)
        return round(base + self._adicional(base), 2)

    @abstractmethod
    def _adicional(self, base: float) -> float: ...

class PedidoNormal(PedidoBase):
    def _adicional(self, base: float) -> float:
        return 0.0

class PedidoUrgente(PedidoBase):
    def _adicional(self, base: float) -> float:
        return base * 0.15   # +15% taxa urgência

class PedidoAgendado(PedidoBase):
    def _adicional(self, base: float) -> float:
        return 5.0           # +R$5 taxa agendamento


# ─── Verificação ──────────────────────────────────────────────────────────────

def verificar_antipatterns() -> None:
    # God Object
    for cls in [RepositorioCliente, ValidadorDocumento, ServicoNotificacao,
                ServicoCobranca, GeradorRelatorio]:
        metodos = [m for m in dir(cls()) if not m.startswith("_")]
        assert len(metodos) <= 4, f"{cls.__name__} ainda tem responsabilidades demais"
    print("OK: God Object — responsabilidades separadas em 5 classes especializadas")

    # Magic Strings/Numbers
    resultado = processar_por_status(StatusPedido.ATIVO, TipoPedido.PREMIUM, 2000.0, 15)
    assert resultado["ativo"] is True
    assert resultado["prazo"] == PRAZO_PAGAMENTO_DIAS
    print("OK: Magic Strings — StatusPedido e TipoPedido como enums")
    print("OK: Magic Numbers — LIMITE_FRETE_GRATIS e PRAZO_PAGAMENTO_DIAS como constantes")

    # Feature Envy
    cliente = Cliente("CLI-100", "X", "x@x.com", NivelFidelidade.OURO, 5000.0, 200)
    desconto = cliente.calcular_desconto_fidelidade()
    assert desconto > 0
    print("OK: Feature Envy — calcular_desconto_fidelidade() movido para Cliente")

    # Copy-Paste
    itens = [ItemPedido("P001", 100.0, 2)]
    assert PedidoNormal().calcular_total(itens)   == 200.0
    assert PedidoUrgente().calcular_total(itens)  == 230.0
    assert PedidoAgendado().calcular_total(itens) == 205.0
    print("OK: Copy-Paste — calcular_total() na base PedidoBase, _adicional() nas subclasses")


if __name__ == "__main__":
    print("=== Anti-patterns _bons — 4 correções ===\n")
    verificar_antipatterns()
