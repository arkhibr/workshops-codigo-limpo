"""
GABARITO 02 — Funções
Abra este arquivo apenas após tentar o exercício por conta própria.
"""

# ─── Solução 1: Quebrar função grande em responsabilidades únicas ─────────────

ALIQUOTA_INSS = 0.275

def calcular_salario_liquido(salario_bruto):
    return salario_bruto * (1 - ALIQUOTA_INSS)

def calcular_bonus(salario_bruto):
    if salario_bruto > 5000:
        return salario_bruto * 0.10
    return salario_bruto * 0.05

def calcular_remuneracao_total(salario_bruto):
    liquido = calcular_salario_liquido(salario_bruto)
    bonus   = calcular_bonus(salario_bruto)
    return liquido, bonus, liquido + bonus

def formatar_linha_resumida(funcionario, total):
    return f"{funcionario['nome']}: R${total:.2f}"

def formatar_linha_detalhada(funcionario, salario_liquido, bonus, total):
    return (
        f"Nome: {funcionario['nome']} | Salário bruto: R${funcionario['salario']:.2f} | "
        f"Líquido: R${salario_liquido:.2f} | Bônus: R${bonus:.2f} | Total: R${total:.2f}"
    )

def formatar_linha_funcionario(funcionario, formato):
    liquido, bonus, total = calcular_remuneracao_total(funcionario["salario"])
    if formato == "resumido":
        return formatar_linha_resumida(funcionario, total)
    return formatar_linha_detalhada(funcionario, liquido, bonus, total)

def filtrar_funcionarios(funcionarios, incluir_inativos):
    if incluir_inativos:
        return funcionarios
    return [f for f in funcionarios if f["ativo"]]

def gerar_relatorio(funcionarios, incluir_inativos, formato):
    selecionados = filtrar_funcionarios(funcionarios, incluir_inativos)
    return [formatar_linha_funcionario(f, formato) for f in selecionados]


# ─── Solução 2: Duas funções em vez de flag booleana ─────────────────────────

def enviar_notificacao_normal(usuario, mensagem):
    print(f"Para: {usuario['email']} | {mensagem}")

def enviar_notificacao_urgente(usuario, mensagem):
    print(f"[URGENTE] Para: {usuario['email']} | {mensagem}")


# ─── Solução 3: Efeito colateral explícito no retorno ────────────────────────

def adicionar_produto_ao_carrinho(carrinho, nome, preco, quantidade):
    """Retorna o carrinho atualizado — sem tocar em estado global."""
    subtotal      = preco * quantidade
    novos_itens   = carrinho["itens"] + [{"nome": nome, "preco": preco, "quantidade": quantidade}]
    novo_total    = carrinho["total"] + subtotal
    return {"itens": novos_itens, "total": novo_total}


# ─── Verificação ──────────────────────────────────────────────────────────────

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
    enviar_notificacao_normal(usuario, "Reunião amanhã às 9h")
    enviar_notificacao_urgente(usuario, "Servidor fora do ar!")

    print("\n=== Carrinho (sem estado global) ===")
    carrinho = {"itens": [], "total": 0.0}
    carrinho = adicionar_produto_ao_carrinho(carrinho, "Teclado", 250.0, 1)
    carrinho = adicionar_produto_ao_carrinho(carrinho, "Mouse", 80.0, 2)
    print(f"Total no carrinho: R${carrinho['total']:.2f}")
