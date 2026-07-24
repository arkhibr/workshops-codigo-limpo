"""Repositório de pedidos sobre sqlite3 — SUT do tutorial de integração de banco.

Testa a camada de persistência de verdade: SQL, constraints e transações reais.
"""
import sqlite3


def criar_schema(conn: sqlite3.Connection) -> None:
    conn.execute("PRAGMA foreign_keys = ON")
    conn.executescript(
        """
        CREATE TABLE clientes (
            id   INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT    NOT NULL,
            vip  INTEGER NOT NULL DEFAULT 0
        );
        CREATE TABLE pedidos (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente_id INTEGER NOT NULL REFERENCES clientes(id),
            total      REAL    NOT NULL CHECK (total >= 0),
            status     TEXT    NOT NULL DEFAULT 'aberto'
        );
        """
    )


def inserir_cliente(conn: sqlite3.Connection, nome: str, vip: bool = False) -> int:
    cur = conn.execute(
        "INSERT INTO clientes (nome, vip) VALUES (?, ?)", (nome, int(vip))
    )
    return cur.lastrowid


def inserir_pedido(conn: sqlite3.Connection, cliente_id: int, total: float) -> int:
    cur = conn.execute(
        "INSERT INTO pedidos (cliente_id, total) VALUES (?, ?)",
        (cliente_id, total),
    )
    return cur.lastrowid


def buscar_pedido(conn: sqlite3.Connection, pedido_id: int) -> dict | None:
    conn.row_factory = sqlite3.Row
    linha = conn.execute(
        "SELECT id, cliente_id, total, status FROM pedidos WHERE id = ?",
        (pedido_id,),
    ).fetchone()
    return dict(linha) if linha else None


def listar_pedidos_do_cliente(conn: sqlite3.Connection, cliente_id: int) -> list[dict]:
    conn.row_factory = sqlite3.Row
    linhas = conn.execute(
        "SELECT id, cliente_id, total, status FROM pedidos WHERE cliente_id = ?",
        (cliente_id,),
    ).fetchall()
    return [dict(l) for l in linhas]
