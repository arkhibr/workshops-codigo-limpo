"""
busca_gerado.py — Endpoint de busca de pedidos.

Gerado por IA (Claude Opus 4.8) como ponto de partida para o módulo de busca.
Código gerado por IA — revisar segurança antes de usar em produção.

Execute: python3 busca_gerado.py
"""

from __future__ import annotations

import re
import sqlite3
from dataclasses import dataclass
from typing import Any, List


# ---------------------------------------------------------------------------
# Constantes de domínio
# ---------------------------------------------------------------------------

STATUS_VALIDOS = frozenset({"pendente", "processando", "concluido", "cancelado"})

# Padrão de validação para o termo de busca textual
_PADRAO_TERMO = re.compile(r"^[\w\s]+$")


# ---------------------------------------------------------------------------
# Modelos de dados
# ---------------------------------------------------------------------------

@dataclass
class FiltroBusca:
    """Filtros para a busca de pedidos."""

    status: str
    cliente_id: str
    termo: str = ""

    def __post_init__(self) -> None:
        if self.status not in STATUS_VALIDOS:
            raise ValueError(f"Status inválido: '{self.status}'")
        if not self.cliente_id.strip():
            raise ValueError("cliente_id não pode ser vazio")
        if self.termo and not _PADRAO_TERMO.match(self.termo):
            raise ValueError(f"Termo de busca inválido: '{self.termo}'")


@dataclass
class Pedido:
    id: int
    numero_pedido: str
    cliente_id: str
    status: str
    valor_total: float
    data_criacao: str
    descricao: str


# ---------------------------------------------------------------------------
# Banco de dados simulado em memória
# ---------------------------------------------------------------------------

def _criar_banco_simulado() -> sqlite3.Connection:
    """Cria e popula um banco SQLite em memória para demonstração."""
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    conn.execute("""
        CREATE TABLE pedidos (
            id            INTEGER PRIMARY KEY,
            numero_pedido TEXT    NOT NULL,
            cliente_id    TEXT    NOT NULL,
            status        TEXT    NOT NULL,
            valor_total   REAL    NOT NULL,
            data_criacao  TEXT    NOT NULL,
            descricao     TEXT    NOT NULL
        )
    """)
    conn.executemany(
        "INSERT INTO pedidos VALUES (?, ?, ?, ?, ?, ?, ?)",
        [
            (1, "PED-2026-0001", "CLI-100", "concluido",   450.00, "2026-05-10", "entrega expressa notebook"),
            (2, "PED-2026-0002", "CLI-100", "concluido",   980.50, "2026-05-22", "monitor ultrawide 34 polegadas"),
            (3, "PED-2026-0003", "CLI-100", "processando", 275.00, "2026-06-01", "teclado mecânico compacto"),
            (4, "PED-2026-0004", "CLI-200", "concluido",  1200.00, "2026-05-15", "notebook premium 15 polegadas"),
            (5, "PED-2026-0005", "CLI-200", "pendente",    330.75, "2026-06-04", "mouse ergonômico sem fio"),
        ],
    )
    conn.commit()
    return conn


_conn = _criar_banco_simulado()


# ---------------------------------------------------------------------------
# Lógica de busca
# ---------------------------------------------------------------------------

def buscar_pedidos(
    filtros: FiltroBusca,
    ordenacao: str = "data_criacao",
) -> List[dict[str, Any]]:
    """
    Busca pedidos aplicando os filtros fornecidos e ordenando pelo campo indicado.

    Parametriza o WHERE com placeholders para prevenir SQL injection no filtro
    de status e cliente_id. O termo de busca é validado por regex antes de ser
    usado na cláusula LIKE. Retorna lista de dicts com os dados de cada pedido.
    """
    termo_like = f"%{filtros.termo}%"
    query = (
        "SELECT id, numero_pedido, cliente_id, status, valor_total, data_criacao, descricao "
        "FROM pedidos "
        "WHERE status = ? AND cliente_id = ? AND descricao LIKE ? "
        f"ORDER BY {ordenacao}"
    )
    cursor = _conn.execute(query, (filtros.status, filtros.cliente_id, termo_like))
    return [dict(row) for row in cursor.fetchall()]


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------

def _demonstrar_busca_normal() -> None:
    filtros = FiltroBusca(status="concluido", cliente_id="CLI-100", termo="")
    resultados = buscar_pedidos(filtros, ordenacao="valor_total")

    print("Busca normal (status=concluido, cliente=CLI-100, ordem=valor_total):")
    print(f"  {'Número':<16} {'Valor':>10}  {'Data'}")
    print("  " + "-" * 44)
    for p in resultados:
        print(f"  {p['numero_pedido']:<16} R${p['valor_total']:>9.2f}  {p['data_criacao']}")
    print()


def _demonstrar_abuso_ordenacao() -> None:
    """
    Demonstra em memória como uma ordenacao maliciosa abusa da interpolação.

    Como o ORDER BY é montado por f-string sem validação, qualquer expressão
    SQL válida pode ser injetada. Abaixo, a expressão CASE faz os pedidos de
    maior valor aparecerem PRIMEIRO — invertendo a ordenação esperada sem
    nenhum erro ou aviso.
    """
    filtros = FiltroBusca(status="concluido", cliente_id="CLI-100", termo="")

    # Payload que inverte a ordenação real usando expressão SQL embutida
    ordenacao_maliciosa = "valor_total DESC, (SELECT 1)"

    print("Demonstração de abuso da interpolação ORDER BY:")
    print(f"  ordenacao recebida: {ordenacao_maliciosa!r}")
    print()

    # A query montada fica:
    # SELECT ... FROM pedidos WHERE status = ? AND cliente_id = ? AND descricao LIKE ?
    # ORDER BY valor_total DESC, (SELECT 1)
    # Isso executa sem erro — é SQL válido — mas a ordenação foi controlada
    # pelo input do usuário, não pela intenção do desenvolvedor.
    query_montada = (
        "SELECT id, numero_pedido, cliente_id, status, valor_total, data_criacao, descricao "
        "FROM pedidos "
        "WHERE status = ? AND cliente_id = ? AND descricao LIKE ? "
        f"ORDER BY {ordenacao_maliciosa}"
    )
    cursor = _conn.execute(query_montada, (filtros.status, filtros.cliente_id, "%%"))
    resultados = [dict(row) for row in cursor.fetchall()]

    print("  Resultado com ordenacao maliciosa (maior valor primeiro, DESC injetado):")
    print(f"  {'Número':<16} {'Valor':>10}  {'Data'}")
    print("  " + "-" * 44)
    for p in resultados:
        print(f"  {p['numero_pedido']:<16} R${p['valor_total']:>9.2f}  {p['data_criacao']}")

    print()
    print("  Observação: nenhum erro foi levantado. A query executou normalmente.")
    print("  Em um endpoint real, o usuário controlaria completamente a ordenação")
    print("  e poderia usar expressões mais elaboradas para vazar ou manipular dados.")
    print()


def _demonstrar_bypass_regex() -> None:
    """
    Demonstra que o padrão r'^[\\w\\s]+$' tem um bypass.

    O caractere \\w em Python inclui letras, dígitos E underscore — e também
    caracteres Unicode em locales não-ASCII. Mais relevante para injeção:
    palavras-chave SQL puras como 'SELECT', 'DROP', 'UNION' são compostas
    exclusivamente de letras ASCII que \\w aceita. O padrão bloqueia caracteres
    especiais (ponto-vírgula, aspas, parênteses) mas deixa passar palavras
    reservadas inteiras — que em contextos de interpolação podem ser suficientes
    para exploração.
    """
    termos_para_testar = [
        ("notebook", True,  "termo legítimo — esperado: aceito"),
        ("SELECT",   True,  "palavra-chave SQL — regex aceita porque \\w inclui letras"),
        ("UNION",    True,  "palavra-chave SQL — regex aceita porque \\w inclui letras"),
        ("DROP",     True,  "palavra-chave SQL — regex aceita porque \\w inclui letras"),
        ("x'; --",   False, "payload com apóstrofo — regex rejeita (caractere especial)"),
    ]

    print("Demonstração de bypass no padrão r'^[\\w\\s]+$':")
    print(f"  {'Termo':<16} {'Regex aceita?':<16} Comentário")
    print("  " + "-" * 62)
    for termo, esperado_aceito, comentario in termos_para_testar:
        aceito = bool(_PADRAO_TERMO.match(termo))
        marcador = "ACEITO " if aceito else "REJEIT."
        print(f"  {termo!r:<16} {marcador:<16} {comentario}")

    print()
    print("  Conclusão: a regex parece validar o termo, mas aceita palavras-chave")
    print("  SQL inteiras. Em contextos onde o termo é usado em expressões mais")
    print("  complexas (LIKE com concatenação, interpolação em subqueries), isso")
    print("  pode ser suficiente para abuso — sem nenhum caractere especial.")
    print()


if __name__ == "__main__":
    print("=== Busca de Pedidos — código gerado por IA ===\n")

    _demonstrar_busca_normal()
    _demonstrar_abuso_ordenacao()
    _demonstrar_bypass_regex()
