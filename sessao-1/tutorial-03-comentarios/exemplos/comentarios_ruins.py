"""
EXEMPLOS: Comentários que violam os princípios do Clean Code
Referência: Clean Code, Cap. 4 — Comments
Execute: python comentarios_ruins.py
"""

# ─── Problema 1: Comentário redundante — repete o que o código já diz ─────────

# incrementa i em 1
i = i + 1 if False else 0  # linha só para ilustrar a redundância

def calcular_total(preco, quantidade):
    # multiplica preço pela quantidade
    total = preco * quantidade
    # retorna o total
    return total


# ─── Problema 2: Comentário enganoso ──────────────────────────────────────────

def esta_disponivel(produto):
    # retorna True se o produto NÃO estiver disponível
    return produto["estoque"] > 0   # na verdade retorna True quando ESTÁ disponível


def aplicar_desconto(total, percentual):
    # desconto é aplicado apenas para clientes VIP
    return total * (1 - percentual / 100)  # na verdade aplica para qualquer chamada


# ─── Problema 3: Código comentado sem explicação ──────────────────────────────

def processar_pagamento(valor, metodo):
    # if metodo == "pix":
    #     taxa = 0.0
    # if metodo == "debito":
    #     taxa = 0.5
    # valor_final = valor + taxa

    # valor_com_taxa = valor * 1.035
    # enviar_para_gateway_antigo(valor_com_taxa)

    if metodo == "credito":
        taxa = 2.5
    else:
        taxa = 0.0
    return valor * (1 + taxa / 100)


# ─── Problema 4: TODO sem rastreabilidade ─────────────────────────────────────

def buscar_usuario(usuario_id):
    # TODO: adicionar cache
    # TODO: tratar erro quando banco estiver fora
    # TODO: melhorar isso depois
    return {"id": usuario_id, "nome": "Usuário Mockado"}


def calcular_frete(cep_destino, peso_kg):
    # FIXME: bugado pra CEPs fora de SP
    # TODO: integrar com API dos Correios
    return 15.0


# ─── Problema 5: Diário de bordo inline (log de mudanças no código) ───────────

def calcular_imposto(valor_bruto):
    # 12/03/2023 - João alterou a alíquota de 12% para 15%
    # 05/07/2023 - Maria reverteu para 12% a pedido do fiscal
    # 01/11/2023 - Pedro ajustou para 13% conforme nova lei
    # 14/04/2024 - Carlos adicionou isenção para valores abaixo de 100
    aliquota = 0.13
    if valor_bruto < 100:
        return 0.0
    return valor_bruto * aliquota


# ─── Problema 6: Comentário de fechamento de bloco (sem necessidade) ──────────

def gerar_relatorio(pedidos):
    resultado = []
    for pedido in pedidos:
        if pedido["status"] == "entregue":
            linha = {
                "id": pedido["id"],
                "total": pedido["total"],
            }
            resultado.append(linha)
        # fim do if status == entregue
    # fim do for pedido in pedidos
    return resultado
# fim da função gerar_relatorio


# ─── Execução de demonstração ─────────────────────────────────────────────────

if __name__ == "__main__":
    print("=== Demonstração: Comentários Ruins ===\n")

    print("calcular_total(50.0, 3):", calcular_total(50.0, 3))

    produto_em_estoque = {"nome": "Café", "estoque": 10}
    produto_sem_estoque = {"nome": "Açúcar", "estoque": 0}
    print("\nesta_disponivel (com estoque):", esta_disponivel(produto_em_estoque))
    print("esta_disponivel (sem estoque):", esta_disponivel(produto_sem_estoque))
    # Nota: o comentário dizia "retorna True se NÃO disponível" — enganoso!

    print("\nprocessar_pagamento (crédito, R$100):", processar_pagamento(100.0, "credito"))
    print("processar_pagamento (pix, R$100):", processar_pagamento(100.0, "pix"))

    print("\nbuscar_usuario('U42'):", buscar_usuario("U42"))

    print("\ncalcular_imposto(R$500):", calcular_imposto(500.0))
    print("calcular_imposto(R$80) [isento]:", calcular_imposto(80.0))

    pedidos = [
        {"id": "P01", "status": "entregue", "total": 120.0},
        {"id": "P02", "status": "pendente", "total": 80.0},
        {"id": "P03", "status": "entregue", "total": 55.0},
    ]
    print("\ngerar_relatorio:", gerar_relatorio(pedidos))
