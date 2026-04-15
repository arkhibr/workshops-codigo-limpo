"""
EXERCÍCIO 02 — Funções
Tempo estimado: 15 minutos
Referência: Clean Code, Cap. 3

INSTRUÇÕES:
  Refatore as funções abaixo aplicando os princípios do Clean Code:
  - Cada função deve fazer UMA coisa
  - Extraia funções auxiliares com nomes descritivos
  - Elimine flags booleanas (crie funções separadas)
  - Elimine efeitos colaterais ocultos

  Não mude o comportamento externo — apenas a organização interna.

Execute para verificar que o código funciona antes e depois:
  python exercicio.py
"""

# ─── Problema 1 ───────────────────────────────────────────────────────────────
# Esta função faz pelo menos 4 coisas diferentes. Quebre-a.

def gerar_relatorio(funcionarios, incluir_inativos, formato):
    resultado = []
    for f in funcionarios:
        if not incluir_inativos and not f["ativo"]:
            continue
        salario_liquido = f["salario"] - (f["salario"] * 0.275)
        if f["salario"] > 5000:
            bonus = f["salario"] * 0.10
        else:
            bonus = f["salario"] * 0.05
        total = salario_liquido + bonus
        if formato == "resumido":
            linha = f"{f['nome']}: R${total:.2f}"
        else:
            linha = (
                f"Nome: {f['nome']} | Salário bruto: R${f['salario']:.2f} | "
                f"Líquido: R${salario_liquido:.2f} | Bônus: R${bonus:.2f} | "
                f"Total: R${total:.2f}"
            )
        resultado.append(linha)
    return resultado


# ─── Problema 2 ───────────────────────────────────────────────────────────────
# Flag booleana — crie duas funções distintas.

def enviar_notificacao(usuario, mensagem, urgente):
    if urgente:
        print(f"[URGENTE] Para: {usuario['email']} | {mensagem}")
    else:
        print(f"Para: {usuario['email']} | {mensagem}")


# ─── Problema 3 ───────────────────────────────────────────────────────────────
# Efeito colateral oculto — torne o efeito explícito no retorno.

carrinho_global = {"itens": [], "total": 0.0}

def adicionar_produto(nome, preco, quantidade):
    subtotal = preco * quantidade
    carrinho_global["itens"].append({
        "nome": nome, "preco": preco, "quantidade": quantidade
    })
    carrinho_global["total"] += subtotal   # efeito colateral oculto!
    return subtotal


# ─── Verificação (não altere este bloco) ──────────────────────────────────────

if __name__ == "__main__":
    funcionarios = [
        {"nome": "Ana",   "salario": 6000.0, "ativo": True},
        {"nome": "Bruno", "salario": 4000.0, "ativo": False},
        {"nome": "Carla", "salario": 3500.0, "ativo": True},
    ]

    print("=== Relatório resumido (todos) ===")
    for linha in gerar_relatorio(funcionarios, True, "resumido"):
        print(linha)

    print("\n=== Relatório detalhado (apenas ativos) ===")
    for linha in gerar_relatorio(funcionarios, False, "detalhado"):
        print(linha)

    print("\n=== Notificações ===")
    usuario = {"email": "ana@empresa.com"}
    enviar_notificacao(usuario, "Reunião amanhã às 9h", False)
    enviar_notificacao(usuario, "Servidor fora do ar!", True)

    print("\n=== Carrinho ===")
    adicionar_produto("Teclado", 250.0, 1)
    adicionar_produto("Mouse", 80.0, 2)
    print(f"Total no carrinho: R${carrinho_global['total']:.2f}")
