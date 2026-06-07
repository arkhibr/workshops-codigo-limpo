"""
idioms_ruins.py — Python funcional mas sem aproveitar os idioms da linguagem.
Execute: python3 idioms_ruins.py
"""
from typing import List
import time


# ─── Sem dataclass: __init__ manual sem validação ────────────────────────────

class ItemVenda:
    def __init__(self, produto_id: str, descricao: str,
                 preco_unitario: float, quantidade: int, mes: int) -> None:
        self.produto_id     = produto_id
        self.descricao      = descricao
        self.preco_unitario = preco_unitario
        self.quantidade     = quantidade
        self.mes            = mes
        # sem validação: preco_unitario=-1 passa silenciosamente


# ─── Sem context manager: try/finally manual ──────────────────────────────────

class ConexaoBanco:
    def abrir(self) -> None:
        print("  [BD] conexão aberta")

    def fechar(self) -> None:
        print("  [BD] conexão fechada")

def processar_com_conexao_manual(dados: List) -> None:
    conn = ConexaoBanco()
    conn.abrir()
    try:
        for item in dados:
            print(f"  processando {item.produto_id}")
    finally:
        conn.fechar()   # repetido em todo lugar que usa ConexaoBanco


# ─── Sem generator: carrega tudo na memória ───────────────────────────────────

def vendas_do_mes_lista(dados: List[ItemVenda], mes: int) -> List[ItemVenda]:
    """Carrega todos os resultados antes de processar o primeiro."""
    resultado = []
    for item in dados:
        if item.mes == mes:
            resultado.append(item)
    return resultado


# ─── Sem decorator: código de timing copiado ─────────────────────────────────

def calcular_total_vendas(itens: List[ItemVenda]) -> float:
    inicio = time.time()
    total = sum(i.preco_unitario * i.quantidade for i in itens)
    fim = time.time()
    print(f"  calcular_total_vendas: {(fim-inicio)*1000:.1f}ms")
    return total

def calcular_receita_liquida(itens: List[ItemVenda], taxa: float) -> float:
    inicio = time.time()                 # copiado
    receita = sum(i.preco_unitario * i.quantidade * (1 - taxa) for i in itens)
    fim = time.time()                    # copiado
    print(f"  calcular_receita_liquida: {(fim-inicio)*1000:.1f}ms")
    return receita


if __name__ == "__main__":
    print("=== Idioms _ruins ===\n")
    dados = [
        ItemVenda("P001", "Webcam", 299.90, 2, 6),
        ItemVenda("P002", "Teclado", 189.90, 1, 5),
    ]
    processar_com_conexao_manual(dados)
    mes6 = vendas_do_mes_lista(dados, 6)
    print(f"  Vendas de junho: {len(mes6)} item(ns)")
    print(f"  Total: R${calcular_total_vendas(dados):.2f}")
