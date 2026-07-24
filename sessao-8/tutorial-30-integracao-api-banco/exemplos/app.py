"""API de Pedidos com persistência sqlite — SUT do tutorial-âncora (T30).

A conexão é injetada em criar_app(conn) para o teste poder passar um
sqlite ':memory:' e verificar a stack inteira: HTTP -> app -> banco.
"""
import sqlite3
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, field_validator


class ItemPedido(BaseModel):
    produto: str
    quantidade: int
    preco_unitario: float

    @field_validator("quantidade")
    @classmethod
    def _pos(cls, v: int) -> int:
        if v <= 0:
            raise ValueError("quantidade deve ser positiva")
        return v


class NovoPedido(BaseModel):
    cliente: str
    itens: list[ItemPedido]

    @field_validator("itens")
    @classmethod
    def _nao_vazio(cls, v: list) -> list:
        if not v:
            raise ValueError("pedido precisa de ao menos um item")
        return v


def criar_schema(conn: sqlite3.Connection) -> None:
    conn.executescript(
        """
        CREATE TABLE IF NOT EXISTS pedidos (
            id     INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente TEXT NOT NULL,
            total  REAL NOT NULL CHECK (total >= 0),
            status TEXT NOT NULL DEFAULT 'aberto'
        );
        """
    )


def criar_app(conn: sqlite3.Connection) -> FastAPI:
    criar_schema(conn)
    conn.row_factory = sqlite3.Row
    app = FastAPI()

    @app.post("/pedidos", status_code=201)
    def criar_pedido(novo: NovoPedido) -> dict:
        total = sum(i.quantidade * i.preco_unitario for i in novo.itens)
        cur = conn.execute(
            "INSERT INTO pedidos (cliente, total) VALUES (?, ?)",
            (novo.cliente, total),
        )
        conn.commit()
        return {"id": cur.lastrowid, "cliente": novo.cliente,
                "total": total, "status": "aberto"}

    @app.get("/pedidos/{pedido_id}")
    def buscar_pedido(pedido_id: int) -> dict:
        linha = conn.execute(
            "SELECT id, cliente, total, status FROM pedidos WHERE id = ?",
            (pedido_id,),
        ).fetchone()
        if linha is None:
            raise HTTPException(status_code=404, detail="pedido não encontrado")
        return dict(linha)

    return app
