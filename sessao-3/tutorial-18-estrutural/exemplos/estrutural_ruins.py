"""
estrutural_ruins.py — Código de negócio acoplado a ERP legado; orquestração exposta.
Execute: python3 estrutural_ruins.py
"""
from typing import Optional
from dataclasses import dataclass


# ─── ERP legado (funções procedurais — sistema externo imutável) ──────────────

def erp_buscar_cliente(cliente_id: str) -> dict:
    print(f"  [ERP] buscarCliente({cliente_id})")
    return {
        "nCodCliente":   int(cliente_id.split("-")[1]),
        "cNomeCliente":  "Empresa Exemplo Ltda",
        "cEmailCliente": "contato@exemplo.com",
    }

def erp_salvar_pedido(dados_pedido: dict) -> str:
    print(f"  [ERP] salvarPedido({dados_pedido.get('cNroPedido', '?')})")
    return "PED-ERP-001"

def erp_atualizar_estoque(cProduto: str, nQtd: int) -> bool:
    print(f"  [ERP] atualizarEstoque({cProduto}, {nQtd})")
    return True

def erp_gerar_nf(cNroPedido: str) -> str:
    print(f"  [ERP] gerarNF({cNroPedido})")
    return "NF-000042"


# ─── Sem Adapter: negócio chama ERP diretamente em múltiplas funções ─────────

def buscar_dados_cliente(cliente_id: str) -> dict:
    raw = erp_buscar_cliente(cliente_id)     # acoplamento direto — nomenclatura ADVPL exposta
    return {
        "id":    str(raw["nCodCliente"]),
        "nome":  raw["cNomeCliente"],
        "email": raw["cEmailCliente"],
    }

def registrar_pedido(cliente_id: str, produto_id: str, quantidade: int) -> str:
    erp_buscar_cliente(cliente_id)            # chamada duplicada ao ERP
    nro = erp_salvar_pedido({
        "cNroPedido":  "PED-TEMP",
        "nCodCliente": int(cliente_id.split("-")[1]),
        "cCodProduto": produto_id,
        "nQtdPedida":  quantidade,
    })
    erp_atualizar_estoque(produto_id, -quantidade)
    return nro

def emitir_nota_fiscal(nro_pedido: str) -> str:
    return erp_gerar_nf(nro_pedido)


# ─── Sem Facade: chamador precisa orquestrar 5 etapas ────────────────────────

def processar_pedido_completo(cliente_id: str, produto_id: str, qtd: int) -> dict:
    """Quem chama conhece e orquestra os 5 subsistemas — alto acoplamento."""
    cliente = buscar_dados_cliente(cliente_id)
    if not cliente:
        raise ValueError("Cliente não encontrado")
    nro_pedido = registrar_pedido(cliente_id, produto_id, qtd)
    nf = emitir_nota_fiscal(nro_pedido)
    print(f"  [Email] → {cliente['email']}: pedido {nro_pedido} confirmado")
    return {"pedido": nro_pedido, "nf": nf, "cliente": cliente["nome"]}


if __name__ == "__main__":
    print("=== Estrutural _ruins — sem Adapter, sem Facade ===\n")
    resultado = processar_pedido_completo("CLI-100", "PROD-001", 5)
    print(f"\nResultado: {resultado}")
