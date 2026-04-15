"""
EXEMPLOS: Funções que seguem os princípios do Clean Code
Referência: Clean Code, Cap. 3 — Functions
Execute: python funcoes_boas.py
"""

from dataclasses import dataclass

# ─── Solução 1: Uma função, uma responsabilidade ──────────────────────────────

CUPONS = {
    "DESCONTO10": 0.90,
    "DESCONTO20": 0.80,
    "DESCONTO30": 0.70,
}

def validar_usuario(usuario_id):
    if not usuario_id:
        raise ValueError("ID de usuário não pode ser vazio")

def calcular_total_itens(itens):
    return sum(item["preco"] * item["quantidade"] for item in itens)

def aplicar_cupom(total, cupom):
    multiplicador = CUPONS.get(cupom, 1.0)
    return total * multiplicador

def formatar_endereco(endereco):
    return (
        f"{endereco['rua']}, {endereco['numero']}"
        f" - {endereco['bairro']}, {endereco['cidade']}/{endereco['uf']}"
    )

def salvar_pedido(pedido_id, usuario_id, total, endereco_formatado):
    print(f"[DB] Salvando pedido {pedido_id}...")
    print(f"[DB] Usuário: {usuario_id} | Total: R$ {total:.2f}")
    print(f"[DB] Entrega: {endereco_formatado}")

def processar_pedido(pedido_id, usuario_id, itens, cupom, endereco):
    validar_usuario(usuario_id)
    total             = calcular_total_itens(itens)
    total_com_desconto = aplicar_cupom(total, cupom)
    endereco_formatado = formatar_endereco(endereco)
    salvar_pedido(pedido_id, usuario_id, total_com_desconto, endereco_formatado)
    return {
        "pedido_id": pedido_id,
        "total":     total_com_desconto,
        "endereco":  endereco_formatado,
        "status":    "criado",
    }


# ─── Solução 2: Duas funções em vez de flag booleana ─────────────────────────

def formatar_nome_informal(nome):
    return nome

def formatar_nome_formal(nome):
    return f"Sr(a). {nome}"


# ─── Solução 3: Sem efeitos colaterais ocultos ────────────────────────────────

def senha_esta_correta(senha):
    return senha == "s3nh4S3gur4"

def autenticar_usuario(usuario, senha):
    """Retorna a sessão — sem tocar em estado global."""
    if not senha_esta_correta(senha):
        raise PermissionError("Credenciais inválidas")
    return {"usuario": usuario, "autenticado": True}


# ─── Solução 4: Dataclass em vez de lista longa de parâmetros ────────────────

@dataclass
class DadosUsuario:
    nome:            str
    email:           str
    senha:           str
    perfil:          str
    ativo:           bool
    data_nascimento: str
    telefone:        str
    cidade:          str

def criar_usuario(dados: DadosUsuario) -> dict:
    return {
        "nome":            dados.nome,
        "email":           dados.email,
        "perfil":          dados.perfil,
        "ativo":           dados.ativo,
        "data_nascimento": dados.data_nascimento,
        "telefone":        dados.telefone,
        "cidade":          dados.cidade,
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

    print("\nNome informal:", formatar_nome_informal("João"))
    print("Nome formal:", formatar_nome_formal("João"))

    sessao = autenticar_usuario("joao@ex.com", "s3nh4S3gur4")
    print("\nSessão retornada:", sessao)

    dados = DadosUsuario(
        nome="João", email="joao@ex.com", senha="hash",
        perfil="admin", ativo=True, data_nascimento="1990-01-01",
        telefone="11999999999", cidade="São Paulo",
    )
    print("\nUsuário criado:", criar_usuario(dados))
