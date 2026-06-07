"""
idioms_bons.py — Python com dataclass, context manager, generator e decorator.
Execute: python3 idioms_bons.py
"""
from typing import List, Generator
from dataclasses import dataclass
import time
import functools


# ─── Idiom 1: @dataclass com __post_init__ ───────────────────────────────────

@dataclass
class ItemVenda:
    produto_id:     str
    descricao:      str
    preco_unitario: float
    quantidade:     int
    mes:            int

    def __post_init__(self) -> None:
        if self.preco_unitario <= 0:
            raise ValueError(f"preco_unitario deve ser positivo, recebido: {self.preco_unitario}")
        if self.quantidade <= 0:
            raise ValueError(f"quantidade deve ser positiva, recebida: {self.quantidade}")


# ─── Idiom 2: Context manager ────────────────────────────────────────────────

class ConexaoBanco:
    def __enter__(self) -> "ConexaoBanco":
        print("  [BD] conexão aberta")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        print("  [BD] conexão fechada (garantido pelo context manager)")
        return False   # não suprime exceções

    def processar(self, produto_id: str) -> None:
        print(f"  processando {produto_id}")


# ─── Idiom 3: Generator com yield ────────────────────────────────────────────

def vendas_do_mes(dados: List[ItemVenda], mes: int) -> Generator[ItemVenda, None, None]:
    """Processa sob demanda — não carrega tudo na memória."""
    for item in dados:
        if item.mes == mes:
            yield item


# ─── Idiom 4: Decorator ───────────────────────────────────────────────────────

def medir_tempo(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        inicio = time.perf_counter()
        resultado = func(*args, **kwargs)
        elapsed = (time.perf_counter() - inicio) * 1000
        print(f"  {func.__name__}: {elapsed:.2f}ms")
        return resultado
    return wrapper

@medir_tempo
def calcular_total_vendas(itens: List[ItemVenda]) -> float:
    return sum(i.preco_unitario * i.quantidade for i in itens)

@medir_tempo
def calcular_receita_liquida(itens: List[ItemVenda], taxa: float) -> float:
    return sum(i.preco_unitario * i.quantidade * (1 - taxa) for i in itens)


# ─── Verificação ──────────────────────────────────────────────────────────────

def verificar_idioms() -> None:
    # Dataclass com validação
    item = ItemVenda("P001", "Webcam HD", 299.90, 2, 6)
    assert item.preco_unitario == 299.90
    print("OK: @dataclass — ItemVenda criado com validação em __post_init__")

    try:
        ItemVenda("P999", "Inválido", -1.0, 1, 6)
        print("FALHOU: @dataclass — deveria rejeitar preco negativo")
    except ValueError:
        print("OK: @dataclass — rejeita preco_unitario negativo")

    # Context manager
    dados = [ItemVenda("P001", "Webcam", 299.90, 2, 6)]
    with ConexaoBanco() as conn:
        conn.processar("P001")
    print("OK: Context manager — ConexaoBanco fechado automaticamente")

    # Generator
    todos = [
        ItemVenda("P001", "Webcam", 299.90, 2, 6),
        ItemVenda("P002", "Teclado", 189.90, 1, 5),
        ItemVenda("P003", "Mouse", 99.90, 3, 6),
    ]
    mes6 = list(vendas_do_mes(todos, 6))
    assert len(mes6) == 2
    print(f"OK: Generator — vendas_do_mes(6) retornou {len(mes6)} item(ns) sob demanda")

    # Decorator
    total = calcular_total_vendas(dados)
    assert total > 0
    print(f"OK: @medir_tempo — calcular_total_vendas decorado sem alterar assinatura")


if __name__ == "__main__":
    print("=== Idioms _bons — Python idiomático ===\n")
    verificar_idioms()
