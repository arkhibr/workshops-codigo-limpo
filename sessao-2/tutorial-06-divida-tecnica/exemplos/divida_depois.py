"""
EXEMPLOS: Módulo de autenticação com as dívidas técnicas pagas
Referência: Clean Code, Cap. 17 — Smells and Heuristics
Execute: python divida_depois.py

Dívidas pagas:
  1. Nomes expressivos em todas as variáveis e funções
  2. Função gigante extraída em funções pequenas de responsabilidade única
  3. Duplicação eliminada: validações de credenciais centralizadas
  4. Magic numbers substituídos por constantes nomeadas
"""

import hashlib
import time

# ── Constantes ─────────────────────────────────────────────────────────────────
# Dívida 4 paga: magic numbers agora têm nomes que explicam o que representam

TAMANHO_MINIMO_USUARIO = 3
TAMANHO_MINIMO_SENHA = 8

EXPIRACAO_TOKEN_BASICO_SEGUNDOS = 3600    # 1 hora
EXPIRACAO_TOKEN_ADMIN_SEGUNDOS = 900      # 15 minutos
EXPIRACAO_TOKEN_PERMANENTE_SEGUNDOS = 86400  # 24 horas

TAMANHO_HASH_MD5 = 32


# ── Funções de validação ───────────────────────────────────────────────────────
# Dívida 3 paga: validações centralizadas em um único lugar

def _validar_credenciais(email: str, senha: str) -> dict:
    """Valida email e senha. Retorna dict com 'valido' e lista de 'erros'."""
    erros = []

    if not email or len(email) < TAMANHO_MINIMO_USUARIO:
        erros.append("e-mail muito curto")
    if email and "@" not in email:
        erros.append("e-mail inválido")
    if not senha or len(senha) < TAMANHO_MINIMO_SENHA:
        erros.append("senha deve ter ao menos 8 caracteres")
    if senha and senha.isdigit():
        erros.append("senha não pode conter apenas números")
    if senha and senha.isupper():
        erros.append("senha não pode conter apenas maiúsculas")

    return {"valido": len(erros) == 0, "erros": erros}


# ── Funções auxiliares de geração ──────────────────────────────────────────────
# Dívida 2 paga: funções pequenas com responsabilidade única

def _gerar_hash_senha(senha: str) -> str:
    return hashlib.sha256(senha.encode()).hexdigest()


def _gerar_token(email: str, hash_senha: str, sufixo: str = "") -> str:
    semente = f"{email}{hash_senha}{time.time()}{sufixo}"
    return hashlib.md5(semente.encode()).hexdigest()


def _calcular_expiracao(tipo_perfil: str) -> int:
    if tipo_perfil == "admin":
        return int(time.time()) + EXPIRACAO_TOKEN_ADMIN_SEGUNDOS
    if tipo_perfil == "permanente":
        return int(time.time()) + EXPIRACAO_TOKEN_PERMANENTE_SEGUNDOS
    return int(time.time()) + EXPIRACAO_TOKEN_BASICO_SEGUNDOS


# ── Funções públicas de autenticação ───────────────────────────────────────────
# Dívida 1 paga: nomes expressivos em parâmetros e variáveis locais

def autenticar_usuario(email: str, senha: str, tipo_perfil: str = "basico") -> dict:
    validacao = _validar_credenciais(email, senha)
    if not validacao["valido"]:
        return {"ok": False, "msg": validacao["erros"][0]}

    hash_senha = _gerar_hash_senha(senha)
    sufixo = tipo_perfil.upper() if tipo_perfil != "basico" else ""
    token = _gerar_token(email, hash_senha, sufixo)
    expiracao = _calcular_expiracao(tipo_perfil)

    return {
        "ok": True,
        "token": token,
        "expiracao": expiracao,
        "tipo_perfil": tipo_perfil,
    }


def renovar_token(email: str, senha: str, token_atual: str) -> dict:
    validacao = _validar_credenciais(email, senha)
    if not validacao["valido"]:
        return {"ok": False, "msg": validacao["erros"][0]}

    if not token_atual or len(token_atual) != TAMANHO_HASH_MD5:
        return {"ok": False, "msg": "token atual inválido"}

    hash_senha = _gerar_hash_senha(senha)
    novo_token = _gerar_token(email, hash_senha)
    nova_expiracao = _calcular_expiracao("basico")

    return {"ok": True, "token": novo_token, "expiracao": nova_expiracao}


# ── Execução de demonstração ───────────────────────────────────────────────────

if __name__ == "__main__":
    print("=== Demonstração: Dívida Técnica Paga — Autenticação ===\n")

    resultado1 = autenticar_usuario("jo", "abc")
    print("Login usuário curto:", resultado1)

    resultado2 = autenticar_usuario("joao@empresa.com", "1234567")
    print("Login senha fraca:", resultado2)

    resultado3 = autenticar_usuario("joao@empresa.com", "Senha@2026")
    print("Login válido (básico):", resultado3)

    resultado4 = autenticar_usuario("admin@empresa.com", "Admin@2026", "admin")
    print("Login admin:", resultado4)

    if resultado3["ok"]:
        resultado5 = renovar_token("joao@empresa.com", "Senha@2026", resultado3["token"])
        print("\nRenovação de token:", resultado5)
