"""
exercicio.py — Endpoint de busca de produtos por descrição.

Gerado por IA como ponto de partida. O código parece seguro — inspecione
toda a construção da query antes de concluir.

Exercício:
  (1) Ache a brecha sutil — toda a query é realmente segura?
  (2) Endureça o código corrigindo a brecha encontrada.
  (3) Liste o que faltava no código original.

Execute: python3 exercicio.py
"""

from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from typing import Any


# ---------------------------------------------------------------------------
# Constantes de domínio
# ---------------------------------------------------------------------------

CATEGORIAS_VALIDAS = frozenset({"eletronicos", "vestuario", "alimentos", "livraria"})

COLUNAS_ORDENACAO_PERMITIDAS = frozenset({
    "preco",
    "nome_produto",
    "estoque_disponivel",
})


# ---------------------------------------------------------------------------
# Modelos de dados
# ---------------------------------------------------------------------------

@dataclass
class FiltroProduto:
    """Filtros para busca de produtos por categoria e descrição."""

    categoria: str
    termo_busca: str

    def __post_init__(self) -> None:
        if self.categoria not in CATEGORIAS_VALIDAS:
            raise ValueError(f"Categoria inválida: '{self.categoria}'")


@dataclass
class Produto:
    id: int
    nome_produto: str
    categoria: str
    descricao: str
    preco: float
    estoque_disponivel: int


# ---------------------------------------------------------------------------
# Banco de dados simulado em memória
# ---------------------------------------------------------------------------

def _criar_banco_simulado() -> sqlite3.Connection:
    """Cria e popula um banco SQLite em memória para demonstração."""
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    conn.execute("""
        CREATE TABLE produtos (
            id                  INTEGER PRIMARY KEY,
            nome_produto        TEXT    NOT NULL,
            categoria           TEXT    NOT NULL,
            descricao           TEXT    NOT NULL,
            preco               REAL    NOT NULL,
            estoque_disponivel  INTEGER NOT NULL
        )
    """)
    conn.executemany(
        "INSERT INTO produtos VALUES (?, ?, ?, ?, ?, ?)",
        [
            (1, "Notebook Pro",     "eletronicos", "Notebook 15 polegadas Intel i7",    4500.00, 12),
            (2, "Fone Bluetooth",   "eletronicos", "Fone sem fio cancelamento de ruído",  350.00, 45),
            (3, "Camiseta Algodão", "vestuario",   "Camiseta 100% algodão lavada",         89.90,  80),
            (4, "Calça Jeans",      "vestuario",   "Calça jeans slim fit masculina",       199.00, 30),
            (5, "Café Especial",    "alimentos",   "Café arábica torrado médio 500g",       42.00, 200),
            (6, "Clean Code",       "livraria",    "Livro Clean Code Robert C. Martin",     95.00, 15),
        ],
    )
    conn.commit()
    return conn


_conn = _criar_banco_simulado()


# ---------------------------------------------------------------------------
# Validação de segurança (parcial)
# ---------------------------------------------------------------------------

def _coluna_ordenacao_segura(ordenacao: str) -> str:
    """Valida que a coluna de ordenação pertence ao allow-list."""
    coluna = ordenacao.strip().lower()
    if coluna not in COLUNAS_ORDENACAO_PERMITIDAS:
        raise ValueError(
            f"Coluna de ordenação inválida: '{ordenacao}'. "
            f"Permitidas: {sorted(COLUNAS_ORDENACAO_PERMITIDAS)}"
        )
    return coluna


# ---------------------------------------------------------------------------
# Lógica de busca
# ---------------------------------------------------------------------------

def buscar_produtos(
    filtros: FiltroProduto,
    ordenacao: str = "nome_produto",
) -> list[dict[str, Any]]:
    """
    Busca produtos por categoria e filtra por termo na descrição.

    Categoria é parametrizada com ? para prevenir injeção no filtro principal.
    Ordenação é validada por allow-list antes de ser interpolada.
    Retorna lista de dicts com os produtos encontrados.
    """
    coluna = _coluna_ordenacao_segura(ordenacao)
    query = (
        "SELECT id, nome_produto, categoria, descricao, preco, estoque_disponivel "
        "FROM produtos "
        f"WHERE categoria = ? AND descricao LIKE '%{filtros.termo_busca}%' "
        f"ORDER BY {coluna}"
    )
    cursor = _conn.execute(query, (filtros.categoria,))
    return [dict(row) for row in cursor.fetchall()]


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------

def _demonstrar_busca_normal() -> None:
    filtros = FiltroProduto(categoria="eletronicos", termo_busca="fio")
    resultados = buscar_produtos(filtros, ordenacao="preco")

    print("Busca normal (categoria=eletronicos, termo=fio, ordem=preco):")
    print(f"  {'Nome':<20} {'Preço':>10}  {'Estoque':>8}")
    print("  " + "-" * 44)
    for p in resultados:
        print(f"  {p['nome_produto']:<20} R${p['preco']:>9.2f}  {p['estoque_disponivel']:>8}")
    print()


def _demonstrar_busca_sem_filtro_termo() -> None:
    filtros = FiltroProduto(categoria="vestuario", termo_busca="")
    resultados = buscar_produtos(filtros)

    print("Busca sem filtro de termo (categoria=vestuario, termo=''):")
    print(f"  {'Nome':<20} {'Preço':>10}  {'Estoque':>8}")
    print("  " + "-" * 44)
    for p in resultados:
        print(f"  {p['nome_produto']:<20} R${p['preco']:>9.2f}  {p['estoque_disponivel']:>8}")
    print()


def _demonstrar_brecha_like() -> None:
    """
    Demonstra a brecha no LIKE por concatenação.

    A query monta: WHERE categoria = ? AND descricao LIKE '%{termo_busca}%'
    O categoria vai como parâmetro — seguro. O termo_busca é concatenado
    diretamente na string da query — vulnerável.

    Um termo com % ou _ abusa dos wildcards LIKE sem nenhum erro.
    O SQLite interpreta como padrão de busca estendido, não como texto literal.
    """
    # Payload com wildcard que casa com tudo — ignora o filtro de categoria implicitamente
    # e retorna registros que não deveriam aparecer com aquele termo
    termo_wildcard = "%"  # retorna todos — o % do código + % do usuario = %% = qualquer coisa
    filtros = FiltroProduto(categoria="eletronicos", termo_busca=termo_wildcard)

    # A query montada fica: ... LIKE '%%%' — o duplo % é tratado como % pelo SQLite
    # efetivamente retornando todos os produtos da categoria, não apenas os com '%' no texto
    resultados = buscar_produtos(filtros, ordenacao="preco")

    print("Demonstração da brecha no LIKE por concatenação:")
    print(f"  termo_busca recebido: {termo_wildcard!r}")
    print(f"  Query montada (trecho): LIKE '%{termo_wildcard}%'  ← wildcard não escapado")
    print()
    print("  Resultado: retornou TODOS os produtos de eletronicos")
    print("  (o % do usuário foi tratado como wildcard LIKE, não como texto literal):")
    print(f"  {'Nome':<20} {'Preço':>10}")
    print("  " + "-" * 34)
    for p in resultados:
        print(f"  {p['nome_produto']:<20} R${p['preco']:>9.2f}")
    print()
    print("  Questão: o código usa allow-list para ORDER BY e parâmetros para categoria —")
    print("  mas o termo_busca é concatenado diretamente no LIKE. Essa é a brecha sutil.")
    print()


if __name__ == "__main__":
    print("=== Busca de Produtos — exercício de segurança ===\n")

    _demonstrar_busca_normal()
    _demonstrar_busca_sem_filtro_termo()
    _demonstrar_brecha_like()
