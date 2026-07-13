"""
massa_ruins.py — Massa de dados duplicada e irrelevante ("Mystery Guest").
Execute: pytest massa_ruins.py -v
"""


def aplicar_cupom(pedido: dict, codigo) -> dict:
    if codigo == "PROMO10":
        for item in pedido["itens"]:
            item["preco"] = item["preco"] * 0.9
    return pedido


def test_cupom_aplica_desconto():
    # literal gigante — só o cupom importa para este teste, mas repete tudo
    pedido = {
        "id": "P001",
        "cliente": {"id": "C1", "nome": "Maria Silva", "email": "maria@teste.com", "cpf": "111.111.111-11"},
        "itens": [{"produto": "Notebook", "preco": 3000.0, "quantidade": 1}],
        "endereco_entrega": {"rua": "Rua A", "numero": "100", "cidade": "SP", "cep": "01000-000"},
        "forma_pagamento": "cartao",
        "cupom_desconto": "PROMO10",
        "data_criacao": "2026-01-01",
        "status": "pendente",
    }
    resultado = aplicar_cupom(pedido, "PROMO10")
    assert resultado["itens"][0]["preco"] == 2700.0


def test_pedido_sem_cupom_mantem_preco():
    # o mesmo literal gigante duplicado, mudando só o campo do cupom
    pedido = {
        "id": "P002",
        "cliente": {"id": "C1", "nome": "Maria Silva", "email": "maria@teste.com", "cpf": "111.111.111-11"},
        "itens": [{"produto": "Notebook", "preco": 3000.0, "quantidade": 1}],
        "endereco_entrega": {"rua": "Rua A", "numero": "100", "cidade": "SP", "cep": "01000-000"},
        "forma_pagamento": "cartao",
        "cupom_desconto": None,
        "data_criacao": "2026-01-01",
        "status": "pendente",
    }
    resultado = aplicar_cupom(pedido, None)
    assert resultado["itens"][0]["preco"] == 3000.0
