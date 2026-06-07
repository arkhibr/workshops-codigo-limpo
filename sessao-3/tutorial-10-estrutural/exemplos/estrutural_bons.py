"""
estrutural_bons.py — Adapter isola o ERP legado; Facade simplifica a orquestração.
Execute: python3 estrutural_bons.py
"""
from typing import Protocol, Optional
from dataclasses import dataclass


# ─── ERP legado (imutável) ────────────────────────────────────────────────────

def erp_buscar_cliente(cliente_id: str) -> dict:
    print(f"  [ERP] buscarCliente({cliente_id})")
    return {
        "nCodCliente":   int(cliente_id.split("-")[1]),
        "cNomeCliente":  "Empresa Exemplo Ltda",
        "cEmailCliente": "contato@exemplo.com",
    }

def erp_salvar_pedido(dados: dict) -> str:
    print(f"  [ERP] salvarPedido({dados.get('cNroPedido', '?')})")
    return "PED-ERP-001"

def erp_atualizar_estoque(cProduto: str, nQtd: int) -> bool:
    print(f"  [ERP] atualizarEstoque({cProduto}, {nQtd})")
    return True

def erp_gerar_nf(cNroPedido: str) -> str:
    print(f"  [ERP] gerarNF({cNroPedido})")
    return "NF-000042"


# ─── Modelos de domínio modernos ─────────────────────────────────────────────

@dataclass
class Cliente:
    id:    str
    nome:  str
    email: str

@dataclass
class ResultadoPedido:
    numero_pedido: str
    nota_fiscal:   str
    cliente_nome:  str


# ─── Adapter: isola nomenclatura ADVPL do código moderno ─────────────────────

class IRepositorioCliente(Protocol):
    def buscar(self, cliente_id: str) -> Optional[Cliente]: ...

class IRepositorioPedido(Protocol):
    def salvar(self, cliente_id: str, produto_id: str, quantidade: int) -> str: ...
    def atualizar_estoque(self, produto_id: str, quantidade: int) -> bool: ...
    def gerar_nota_fiscal(self, nro_pedido: str) -> str: ...


class ERPClienteAdapter:
    """Traduz a API ADVPL (nCod*, cNome*) para o contrato IRepositorioCliente."""
    def buscar(self, cliente_id: str) -> Optional[Cliente]:
        raw = erp_buscar_cliente(cliente_id)
        return Cliente(
            id=str(raw["nCodCliente"]),
            nome=raw["cNomeCliente"],
            email=raw["cEmailCliente"],
        )


class ERPPedidoAdapter:
    """Isola os detalhes de nomenclatura ADVPL da lógica de negócio."""
    def salvar(self, cliente_id: str, produto_id: str, quantidade: int) -> str:
        return erp_salvar_pedido({
            "cNroPedido":  "PED-TEMP",
            "nCodCliente": int(cliente_id.split("-")[1]),
            "cCodProduto": produto_id,
            "nQtdPedida":  quantidade,
        })

    def atualizar_estoque(self, produto_id: str, quantidade: int) -> bool:
        return erp_atualizar_estoque(produto_id, -quantidade)

    def gerar_nota_fiscal(self, nro_pedido: str) -> str:
        return erp_gerar_nf(nro_pedido)


# ─── Facade: simplifica os subsistemas em uma chamada ────────────────────────

class FachadaProcessamentoPedido:
    """Quem chama passa apenas os dados — não conhece os subsistemas internos."""
    def __init__(
        self,
        repo_cliente: IRepositorioCliente,
        repo_pedido:  IRepositorioPedido,
    ) -> None:
        self._repo_cliente = repo_cliente
        self._repo_pedido  = repo_pedido

    def processar(
        self,
        cliente_id: str,
        produto_id: str,
        quantidade: int,
    ) -> ResultadoPedido:
        cliente = self._repo_cliente.buscar(cliente_id)
        if cliente is None:
            raise ValueError(f"Cliente não encontrado: {cliente_id}")
        nro_pedido = self._repo_pedido.salvar(cliente_id, produto_id, quantidade)
        self._repo_pedido.atualizar_estoque(produto_id, quantidade)
        nf = self._repo_pedido.gerar_nota_fiscal(nro_pedido)
        print(f"  [Email] → {cliente.email}: pedido {nro_pedido} confirmado")
        return ResultadoPedido(nro_pedido, nf, cliente.nome)


# ─── Verificação ──────────────────────────────────────────────────────────────

def verificar_adapter() -> None:
    adapter_cliente = ERPClienteAdapter()
    cliente = adapter_cliente.buscar("CLI-100")
    assert cliente is not None
    assert cliente.nome == "Empresa Exemplo Ltda"
    assert not hasattr(cliente, "nCodCliente")
    print("OK: Adapter — ERPClienteAdapter traduz nomenclatura ADVPL para Cliente")

    adapter_pedido = ERPPedidoAdapter()
    nro = adapter_pedido.salvar("CLI-100", "PROD-001", 3)
    assert nro.startswith("PED")
    print("OK: Adapter — ERPPedidoAdapter salva pedido sem expor campos ADVPL")


def verificar_facade() -> None:
    fachada = FachadaProcessamentoPedido(ERPClienteAdapter(), ERPPedidoAdapter())
    resultado = fachada.processar("CLI-100", "PROD-001", 5)
    assert resultado.numero_pedido.startswith("PED")
    assert resultado.nota_fiscal.startswith("NF")
    assert resultado.cliente_nome == "Empresa Exemplo Ltda"
    print("OK: Facade — 5 subsistemas orquestrados em uma chamada processar()")
    print("OK: Facade — chamador não conhece ERP, adapters ou sequência de etapas")


if __name__ == "__main__":
    print("=== Estrutural _bons — Adapter + Facade ===\n")
    verificar_adapter()
    print()
    verificar_facade()
