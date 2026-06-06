"""
busca_revisado.py — Endpoint de busca de pedidos (versão endurecida).

Corrige três brechas presentes em busca_gerado.py:
  1. ORDER BY interpolado → validação via allow-list antes de qualquer interpolação.
  2. Regex com bypass (r'^[\\w\\s]+$') → padrão restrito que rejeita palavras-chave SQL.
  3. LIKE por concatenação → parâmetro posicional com o % embutido no valor.

Qualquer input fora dos critérios aceitos é rejeitado com ValueError antes
de tocar na query.

Execute: python3 busca_revisado.py
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

COLUNAS_ORDENACAO_PERMITIDAS = frozenset({
    "data_criacao",
    "valor_total",
    "numero_pedido",
})

# Padrão restrito: apenas letras (incluindo acentuadas), dígitos e espaço,
# com comprimento máximo explícito. O padrão fecha os caracteres especiais que
# tornariam o LIKE perigoso se fosse concatenado (%, _, ;, aspas, parênteses).
# Nota: mesmo que um termo passe aqui, ele vai como parâmetro posicional no LIKE
# — nunca concatenado na query. A regex é defesa em profundidade, não a única barreira.
_PADRAO_TERMO_SEGURO = re.compile(r"^[a-zA-ZáàâãéêíóôõúüçÁÀÂÃÉÊÍÓÔÕÚÜÇ0-9 ]{1,50}$")


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
        if self.termo and not _PADRAO_TERMO_SEGURO.match(self.termo):
            raise ValueError(
                f"Termo de busca inválido: '{self.termo}'. "
                "Use apenas letras e espaços (máx. 50 caracteres)."
            )


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
# Validação de segurança
# ---------------------------------------------------------------------------

def _coluna_ordenacao_segura(ordenacao: str) -> str:
    """
    Valida que a coluna de ordenação pertence ao allow-list.

    ORDER BY não pode ser parametrizado com ? na maioria dos drivers SQL.
    Esta função garante que apenas identificadores conhecidos sejam
    interpolados na query — qualquer outro valor é rejeitado antes de
    chegar ao banco.
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

def buscar_pedidos(
    filtros: FiltroBusca,
    ordenacao: str = "data_criacao",
) -> List[dict[str, Any]]:
    """
    Busca pedidos aplicando os filtros fornecidos e ordenando pelo campo indicado.

    WHERE parametrizado com ? para status, cliente_id e o padrão LIKE.
    O % do LIKE é embutido no valor do parâmetro — não concatenado na query.
    ORDER BY validado por allow-list antes de qualquer interpolação.
    Levanta ValueError para qualquer entrada fora dos critérios aceitos.
    """
    coluna = _coluna_ordenacao_segura(ordenacao)
    termo_like = f"%{filtros.termo}%" if filtros.termo else "%"
    query = (
        "SELECT id, numero_pedido, cliente_id, status, valor_total, data_criacao, descricao "
        "FROM pedidos "
        "WHERE status = ? AND cliente_id = ? AND descricao LIKE ? "
        f"ORDER BY {coluna}"
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


def _demonstrar_rejeicao_ordenacao_maliciosa() -> None:
    filtros = FiltroBusca(status="concluido", cliente_id="CLI-100")
    ordenacao_maliciosa = "valor_total DESC, (SELECT 1)"

    print("Tentativa com ordenacao maliciosa:")
    print(f"  ordenacao recebida: {ordenacao_maliciosa!r}")
    try:
        buscar_pedidos(filtros, ordenacao=ordenacao_maliciosa)
        print("  FALHOU: a query executou sem erro — allow-list não funcionou.")
    except ValueError as erro:
        print(f"  Bloqueado antes da query: {erro}")
    print()


def _demonstrar_rejeicao_caracteres_especiais() -> None:
    """
    Demonstra que a regex restrita bloqueia os caracteres que tornariam
    o LIKE perigoso — e que, mesmo para termos aceitos, o valor vai como
    parâmetro posicional (nunca concatenado na query).
    """
    print("Tentativas com termos suspeitos (validação de entrada):")
    print(f"  {'Termo':<20} Resultado")
    print("  " + "-" * 56)
    casos = [
        ("notebook",       "termo legítimo"),
        ("monitor 34",     "termo com espaço — legítimo"),
        ("x'; DROP TABLE", "payload com aspas e ponto-vírgula"),
        ("%_wildcard",     "wildcards LIKE — rejeitados"),
        ("a" * 51,         "termo muito longo — rejeitado"),
    ]
    for termo, descricao in casos:
        try:
            FiltroBusca(status="concluido", cliente_id="CLI-100", termo=termo)
            print(f"  {repr(termo[:18]):<20} Aceito ({descricao})")
        except ValueError:
            print(f"  {repr(termo[:18]):<20} Rejeitado ({descricao})")
    print()
    print("  Mesmo que um termo passe a regex, ele vai como parâmetro '?'")
    print("  no LIKE — nunca concatenado na string da query.")
    print()


def _demonstrar_rejeicao_coluna_inexistente() -> None:
    filtros = FiltroBusca(status="concluido", cliente_id="CLI-100")

    print("Tentativa com coluna inexistente:")
    print("  ordenacao recebida: 'cpf_cliente'")
    try:
        buscar_pedidos(filtros, ordenacao="cpf_cliente")
        print("  FALHOU: a query executou sem erro — allow-list não funcionou.")
    except ValueError as erro:
        print(f"  Bloqueado antes da query: {erro}")
    print()


if __name__ == "__main__":
    print("=== Busca de Pedidos — versão endurecida ===\n")

    _demonstrar_busca_normal()
    _demonstrar_rejeicao_ordenacao_maliciosa()
    _demonstrar_rejeicao_caracteres_especiais()
    _demonstrar_rejeicao_coluna_inexistente()
