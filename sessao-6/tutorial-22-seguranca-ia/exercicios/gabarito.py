"""
gabarito.py — Endpoint de busca de produtos (versão endurecida).

Corrige a brecha sutil de exercicio.py:
  - O LIKE era montado por concatenação: f"LIKE '%{filtros.termo_busca}%'"
  - Agora o termo vai como parâmetro posicional: execute(..., (f"%{termo}%",))
  - A validação de entrada bloqueia wildcards LIKE (%, _) antes da query.
  - ORDER BY continua via allow-list (já estava correto no exercício).

Execute: python3 gabarito.py
"""

from __future__ import annotations

import re
import sqlite3
from dataclasses import dataclass
from typing import Any, List


# ---------------------------------------------------------------------------
# Constantes de domínio
# ---------------------------------------------------------------------------

CATEGORIAS_VALIDAS = frozenset({"eletronicos", "vestuario", "alimentos", "livraria"})

COLUNAS_ORDENACAO_PERMITIDAS = frozenset({
    "preco",
    "nome_produto",
    "estoque_disponivel",
})

# Padrão restrito: apenas letras (incluindo acentuadas), dígitos e espaço.
# Bloqueia %, _, ;, aspas, parênteses — caracteres que tornariam o LIKE perigoso.
_PADRAO_TERMO_SEGURO = re.compile(r"^[a-zA-ZáàâãéêíóôõúüçÁÀÂÃÉÊÍÓÔÕÚÜÇ0-9 ]{1,50}$")


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
        if self.termo_busca and not _PADRAO_TERMO_SEGURO.match(self.termo_busca):
            raise ValueError(
                f"Termo de busca inválido: '{self.termo_busca}'. "
                "Use apenas letras, dígitos e espaços (máx. 50 caracteres)."
            )


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
            (3, "Camiseta Algodão", "vestuario",   "Camiseta 100% algodão lavada",         89.90, 80),
            (4, "Calça Jeans",      "vestuario",   "Calça jeans slim fit masculina",       199.00, 30),
            (5, "Café Especial",    "alimentos",   "Café arábica torrado médio 500g",       42.00, 200),
            (6, "Clean Code",       "livraria",    "Livro Clean Code Robert C. Martin",     95.00, 15),
        ],
    )
    conn.commit()
    return conn


_conn = _criar_banco_simulado()


# ---------------------------------------------------------------------------
# Validação de segurança
# ---------------------------------------------------------------------------

def _coluna_ordenacao_segura(ordenacao: str) -> str:
    """
    Valida que a coluna de ordenação pertence ao allow-list.

    ORDER BY não pode ser parametrizado com ? — mas deve ser validado antes
    de qualquer interpolação. Rejeita qualquer valor fora do conjunto permitido.
    """
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
) -> List[dict[str, Any]]:
    """
    Busca produtos por categoria e filtra por termo na descrição.

    Categoria e termo LIKE são parametrizados com ? — nunca concatenados.
    O % do LIKE é embutido no valor do parâmetro, não na string da query.
    Ordenação validada por allow-list antes de qualquer interpolação.
    Levanta ValueError para qualquer entrada fora dos critérios aceitos.
    """
    coluna = _coluna_ordenacao_segura(ordenacao)
    termo_like = f"%{filtros.termo_busca}%" if filtros.termo_busca else "%"
    query = (
        "SELECT id, nome_produto, categoria, descricao, preco, estoque_disponivel "
        "FROM produtos "
        f"WHERE categoria = ? AND descricao LIKE ? "
        f"ORDER BY {coluna}"
    )
    cursor = _conn.execute(query, (filtros.categoria, termo_like))
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


def _demonstrar_rejeicao_wildcard_like() -> None:
    print("Tentativa com wildcard LIKE como termo de busca:")
    for termo in ["%", "_%_", "x'; --"]:
        try:
            FiltroProduto(categoria="eletronicos", termo_busca=termo)
            print(f"  {termo!r:<20} Aceito (FALHOU — deveria rejeitar)")
        except ValueError as erro:
            print(f"  {termo!r:<20} Rejeitado: {erro}")
    print()


def _demonstrar_rejeicao_ordenacao_maliciosa() -> None:
    filtros = FiltroProduto(categoria="eletronicos", termo_busca="")
    print("Tentativa com ordenacao maliciosa:")
    try:
        buscar_produtos(filtros, ordenacao="preco DESC; DROP TABLE produtos--")
        print("  FALHOU: a query executou sem erro.")
    except ValueError as erro:
        print(f"  Bloqueado: {erro}")
    print()


def _demonstrar_busca_com_termo_seguro() -> None:
    filtros = FiltroProduto(categoria="vestuario", termo_busca="slim")
    resultados = buscar_produtos(filtros, ordenacao="preco")

    print("Busca com termo legítimo 'slim' (categoria=vestuario):")
    print(f"  {'Nome':<20} {'Preço':>10}")
    print("  " + "-" * 34)
    for p in resultados:
        print(f"  {p['nome_produto']:<20} R${p['preco']:>9.2f}")
    print()


if __name__ == "__main__":
    print("=== Busca de Produtos — gabarito (versão endurecida) ===\n")

    _demonstrar_busca_normal()
    _demonstrar_rejeicao_wildcard_like()
    _demonstrar_rejeicao_ordenacao_maliciosa()
    _demonstrar_busca_com_termo_seguro()
