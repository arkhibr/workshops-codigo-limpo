"""
SAÍDA TÍPICA DE IA — agendamento de consultas (a partir de prompt fraco)
Referência: Clean Code, Cap. 2–3

⚠️  Este arquivo é INTENCIONALMENTE IMPERFEITO.
    Representa o tipo de código que uma IA gera a partir de um prompt vago.
    Analise os problemas antes de ver a versão revisada.

Execute: python3 sessao-5/tutorial-08-clean-code-com-ia/exemplos/agendamento_gerado.py
"""

# Prompt usado: "faz uma função de agendar consulta"

from datetime import datetime

# lista global de consultas agendadas
data = []


def processar(d, p, h):  # o que é d? p? h?
    # checa se pode agendar
    ok = True
    for item in data:
        if item["date"] == d and item["p"] == p:  # mistura de idioma
            ok = False
    if not ok:
        return -1  # código de erro em vez de exceção

    # cria o registro
    consulta = {
        "date": d,       # "date" em inglês
        "p": p,          # "p" — o que significa?
        "h": h,          # "h" — horário? hora? hospital?
        "dur": 30,       # número mágico — por que 30?
        "status": "ok",  # "ok" — aprovado? confirmado? ativo?
    }
    data.append(consulta)
    return consulta


def get_consultas(p):  # mistura de idioma no nome
    result = []
    for item in data:
        if item["p"] == p:
            result.append(item)
    return result


# ─── Execução de demonstração ─────────────────────────────────────────────────

if __name__ == "__main__":
    c1 = processar("2026-07-10", "Ana Lima", "09:00")
    print("Agendamento 1:", c1)

    # tenta agendar o mesmo paciente no mesmo dia
    c2 = processar("2026-07-10", "Ana Lima", "14:00")
    print("Agendamento 2 (mesmo dia):", c2)

    # agendamento diferente
    c3 = processar("2026-07-11", "Carlos Souza", "10:30")
    print("Agendamento 3:", c3)

    print("\nConsultas de Ana Lima:", get_consultas("Ana Lima"))
