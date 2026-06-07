"""
Revisão alinhada às convenções do projeto — Catálogo de Produtos
Referência: Tutorial 08 — O novo fluxo: dirigir e revisar
Execute: python3 catalogo_revisado.py

Divergências corrigidas em relação a catalogo_gerado.py:
  - Exceções explícitas (ValueError, KeyError) em vez de dicionários de erro
  - @dataclass para modelagem de entidade, seguindo o estilo de funcoes_boas.py
  - Constantes nomeadas para limites de negócio
  - Identificadores 100 % em português (produto, catalogo, preco, categoria)
  - Sem camadas Repository/Service separadas — único módulo plano como no repo
"""

from dataclasses import dataclass
from typing import Optional


# ─── Constantes de domínio ────────────────────────────────────────────────────

PRECO_MINIMO = 0.0
TAMANHO_MINIMO_NOME = 2
TAMANHO_MINIMO_ID = 3


# ─── Entidade ─────────────────────────────────────────────────────────────────

@dataclass
class Produto:
    id:        str
    nome:      str
    preco:     float
    categoria: str


# ─── Catálogo (estado em memória) ─────────────────────────────────────────────

_produtos: dict[str, Produto] = {}


# ─── Operações do catálogo ────────────────────────────────────────────────────

def cadastrar_produto(id: str, nome: str, preco: float, categoria: str) -> Produto:
    """Cadastra um produto. Levanta ValueError se os dados forem inválidos."""
    if not id or len(id) < TAMANHO_MINIMO_ID:
        raise ValueError(f"ID do produto deve ter ao menos {TAMANHO_MINIMO_ID} caracteres")
    if not nome or len(nome) < TAMANHO_MINIMO_NOME:
        raise ValueError(f"Nome do produto deve ter ao menos {TAMANHO_MINIMO_NOME} caracteres")
    if preco < PRECO_MINIMO:
        raise ValueError("Preço não pode ser negativo")

    produto = Produto(id=id, nome=nome, preco=preco, categoria=categoria)
    _produtos[id] = produto
    return produto


def buscar_produto(id: str) -> Produto:
    """Retorna o produto pelo ID. Levanta KeyError se não encontrado."""
    if id not in _produtos:
        raise KeyError(f"Produto '{id}' não encontrado no catálogo")
    return _produtos[id]


def listar_produtos(categoria: Optional[str] = None) -> list[Produto]:
    """Lista todos os produtos ou filtra por categoria."""
    todos = list(_produtos.values())
    if categoria:
        return [p for p in todos if p.categoria == categoria]
    return todos


def atualizar_preco(id: str, novo_preco: float) -> Produto:
    """Atualiza o preço de um produto. Levanta ValueError ou KeyError conforme o caso."""
    if novo_preco < PRECO_MINIMO:
        raise ValueError("Preço não pode ser negativo")
    produto = buscar_produto(id)
    produto.preco = novo_preco
    return produto


# ─── Execução de demonstração ─────────────────────────────────────────────────

if __name__ == "__main__":
    print("=== Catálogo de Produtos (revisado — alinhado às convenções do projeto) ===\n")

    p1 = cadastrar_produto("P001", "Notebook Pro 15", 4_500.00, "informatica")
    print("Produto cadastrado:", p1)

    p2 = cadastrar_produto("P002", "Mouse Sem Fio", 89.90, "perifericos")
    print("Produto cadastrado:", p2)

    try:
        cadastrar_produto("", "Sem ID", 10.0, "geral")
    except ValueError as erro:
        print(f"\nErro esperado no cadastro: {erro}")

    encontrado = buscar_produto("P001")
    print("\nBusca por P001:", encontrado)

    try:
        buscar_produto("X999")
    except KeyError as erro:
        print(f"Erro esperado na busca: {erro}")

    todos = listar_produtos()
    print(f"\nTodos os produtos ({len(todos)}):", todos)

    filtrados = listar_produtos(categoria="informatica")
    print(f"Categoria 'informatica' ({len(filtrados)}):", filtrados)

    atualizado = atualizar_preco("P001", 3_999.00)
    print("\nPreço atualizado:", atualizado)
