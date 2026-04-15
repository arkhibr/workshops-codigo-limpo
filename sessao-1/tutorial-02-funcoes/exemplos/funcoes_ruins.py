"""
EXEMPLOS: Funções que violam os princípios do Clean Code
Referência: Clean Code, Cap. 3 — Functions
Execute: python funcoes_ruins.py
"""

# ─── Problema 1: Função que faz muitas coisas (viola SRP) ────────────────────

def processar_pedido(pedido_id, usuario_id, itens, cupom, endereco):
    # Valida usuário
    if not usuario_id:
        return {"erro": "usuário inválido"}

    # Calcula total dos itens
    total = 0
    for item in itens:
        total += item["preco"] * item["quantidade"]

    # Aplica desconto do cupom
    if cupom == "DESCONTO10":
        total = total * 0.90
    elif cupom == "DESCONTO20":
        total = total * 0.80
    elif cupom == "DESCONTO30":
        total = total * 0.70

    # Formata endereço de entrega
    endereco_formatado = (
        f"{endereco['rua']}, {endereco['numero']}"
        f" - {endereco['bairro']}, {endereco['cidade']}/{endereco['uf']}"
    )

    # Simula salvamento no banco
    print(f"[DB] Salvando pedido {pedido_id}...")
    print(f"[DB] Usuário: {usuario_id}")
    print(f"[DB] Total: R$ {total:.2f}")
    print(f"[DB] Entrega: {endereco_formatado}")

    return {
        "pedido_id":  pedido_id,
        "total":      total,
        "endereco":   endereco_formatado,
        "status":     "criado",
    }


# ─── Problema 2: Flag booleana como parâmetro ─────────────────────────────────

def formatar_nome(nome, formal):
    """formal=True → "Sr(a). João", formal=False → "João" """
    if formal:
        return f"Sr(a). {nome}"
    return nome


# ─── Problema 3: Efeito colateral oculto ─────────────────────────────────────

sessao_ativa = {}

def verificar_credenciais(usuario, senha):
    """Verifica a senha — mas também modifica estado global sem avisar."""
    if senha == "s3nh4S3gur4":
        sessao_ativa["usuario"] = usuario   # efeito colateral oculto!
        sessao_ativa["autenticado"] = True
        return True
    return False


# ─── Problema 4: Muitos parâmetros ────────────────────────────────────────────

def criar_usuario(nome, email, senha, perfil, ativo, data_nascimento, telefone, cidade):
    return {
        "nome": nome, "email": email, "senha": senha,
        "perfil": perfil, "ativo": ativo,
        "data_nascimento": data_nascimento,
        "telefone": telefone, "cidade": cidade,
    }


# ─── Execução de demonstração ─────────────────────────────────────────────────

if __name__ == "__main__":
    itens = [
        {"preco": 50.0, "quantidade": 2},
        {"preco": 30.0, "quantidade": 1},
    ]
    endereco = {
        "rua": "Rua das Flores", "numero": "123",
        "bairro": "Centro", "cidade": "São Paulo", "uf": "SP",
    }
    resultado = processar_pedido("P001", "U001", itens, "DESCONTO10", endereco)
    print("\nResultado:", resultado)

    print("\nFormatar nome (informal):", formatar_nome("João", False))
    print("Formatar nome (formal):", formatar_nome("João", True))

    print("\nVerificar credenciais:", verificar_credenciais("joao@ex.com", "s3nh4S3gur4"))
    print("Sessão após verificação:", sessao_ativa)  # efeito colateral visível aqui
