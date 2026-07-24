"""API de Pedidos — SUT dos tutoriais de integração (Sessão 8).

`criar_app()` é uma factory: cada chamada devolve um app com estado próprio.
Isso é o que permite isolamento real entre testes (cada teste, um app novo).
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, field_validator


class ItemPedido(BaseModel):
    produto: str
    quantidade: int
    preco_unitario: float

    @field_validator("quantidade")
    @classmethod
    def _quantidade_positiva(cls, v: int) -> int:
        if v <= 0:
            raise ValueError("quantidade deve ser positiva")
        return v


class NovoPedido(BaseModel):
    cliente: str
    itens: list[ItemPedido]

    @field_validator("itens")
    @classmethod
    def _itens_nao_vazio(cls, v: list) -> list:
        if not v:
            raise ValueError("pedido precisa de ao menos um item")
        return v


def criar_app() -> FastAPI:
    app = FastAPI()
    pedidos: dict[int, dict] = {}
    sequencia = {"proximo_id": 1}

    @app.post("/pedidos", status_code=201)
    def criar_pedido(novo: NovoPedido) -> dict:
        total = sum(i.quantidade * i.preco_unitario for i in novo.itens)
        pedido_id = sequencia["proximo_id"]
        sequencia["proximo_id"] += 1
        pedido = {"id": pedido_id, "cliente": novo.cliente,
                  "total": total, "status": "aberto"}
        pedidos[pedido_id] = pedido
        return pedido

    @app.get("/pedidos/{pedido_id}")
    def buscar_pedido(pedido_id: int) -> dict:
        if pedido_id not in pedidos:
            raise HTTPException(status_code=404, detail="pedido não encontrado")
        return pedidos[pedido_id]

    @app.post("/pedidos/{pedido_id}/pagar")
    def pagar_pedido(pedido_id: int) -> dict:
        if pedido_id not in pedidos:
            raise HTTPException(status_code=404, detail="pedido não encontrado")
        pedido = pedidos[pedido_id]
        if pedido["status"] == "pago":
            raise HTTPException(status_code=409, detail="pedido já pago")
        pedido["status"] = "pago"
        return pedido

    return app
