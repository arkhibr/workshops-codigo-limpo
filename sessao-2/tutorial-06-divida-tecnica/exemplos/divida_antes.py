"""
EXEMPLOS: Módulo de autenticação com dívida técnica acumulada
Referência: Clean Code, Cap. 17 — Smells and Heuristics
Execute: python divida_antes.py

Tipos de dívida presentes:
  1. Dívida de nomes (variáveis obscuras)
  2. Dívida de funções (função gigante que faz tudo)
  3. Dívida de duplicação (mesma validação em dois lugares)
  4. Dívida de magic numbers (valores numéricos sem constante)
"""

import hashlib
import time


def login(u, s, t="basico"):
    # valida usuario
    if not u or len(u) < 3:
        return {"ok": False, "msg": "usuario invalido"}
    if "@" not in u:
        return {"ok": False, "msg": "usuario invalido"}

    # valida senha
    if not s or len(s) < 8:
        return {"ok": False, "msg": "senha fraca"}
    if s.isdigit():
        return {"ok": False, "msg": "senha so numeros"}
    if s.isupper():
        return {"ok": False, "msg": "senha invalida"}

    # gera hash
    h = hashlib.sha256(s.encode()).hexdigest()

    # gera token
    if t == "basico":
        tk = hashlib.md5(f"{u}{h}{time.time()}".encode()).hexdigest()
        exp = int(time.time()) + 3600
    elif t == "admin":
        tk = hashlib.md5(f"{u}{h}{time.time()}ADMIN".encode()).hexdigest()
        exp = int(time.time()) + 900
    else:
        tk = hashlib.md5(f"{u}{h}{time.time()}".encode()).hexdigest()
        exp = int(time.time()) + 86400

    return {"ok": True, "tk": tk, "exp": exp, "tp": t}


def renovar_token(u, s, tk_atual):
    # valida usuario — DUPLICADO de login()
    if not u or len(u) < 3:
        return {"ok": False, "msg": "usuario invalido"}
    if "@" not in u:
        return {"ok": False, "msg": "usuario invalido"}

    # valida senha — DUPLICADO de login()
    if not s or len(s) < 8:
        return {"ok": False, "msg": "senha fraca"}
    if s.isdigit():
        return {"ok": False, "msg": "senha so numeros"}
    if s.isupper():
        return {"ok": False, "msg": "senha invalida"}

    if not tk_atual or len(tk_atual) != 32:
        return {"ok": False, "msg": "token invalido"}

    # gera novo token
    h = hashlib.sha256(s.encode()).hexdigest()
    novo_tk = hashlib.md5(f"{u}{h}{time.time()}".encode()).hexdigest()
    exp = int(time.time()) + 3600

    return {"ok": True, "tk": novo_tk, "exp": exp}


if __name__ == "__main__":
    print("=== Demonstração: Dívida Técnica — Autenticação ===\n")

    r1 = login("jo", "abc")
    print("Login usuário curto:", r1)

    r2 = login("joao@empresa.com", "1234567")
    print("Login senha fraca:", r2)

    r3 = login("joao@empresa.com", "Senha@2026")
    print("Login válido (básico):", r3)

    r4 = login("admin@empresa.com", "Admin@2026", "admin")
    print("Login admin:", r4)

    if r3["ok"]:
        r5 = renovar_token("joao@empresa.com", "Senha@2026", r3["tk"])
        print("\nRenovação de token:", r5)
