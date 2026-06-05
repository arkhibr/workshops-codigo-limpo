"""
EXERCÍCIO — Lista de espera da clínica (saída típica de IA, a partir de prompt fraco)
Referência: Clean Code, Cap. 2–3 aplicados a código assistido por IA

Prompt usado para gerar este código:
    "cria um módulo de lista de espera pra clínica"

Sua tarefa:
    (1) Reescreva o prompt acima para ser mais forte (veja o modelo em exemplos/prompt.md).
    (2) Refatore o código abaixo aplicando os princípios de Clean Code.
    (3) Liste os problemas que você encontrou (nomes, coesão, idioma, etc.).

Execute: python3 sessao-5/tutorial-08-clean-code-com-ia/exercicios/exercicio.py
"""

# ⚠️  Código gerado por IA — INTENCIONALMENTE IMPERFEITO. Não corrija antes de listar os problemas.

queue = []  # nome em inglês — o que representa?
_id = 0     # variável global sem contexto


def add(n, t):  # o que é n? o que é t?
    global _id
    _id += 1
    entry = {
        "id": _id,
        "n": n,       # "n" — nome? número? nível?
        "t": t,       # "t" — tipo? tempo? turno?
        "ts": __import__("datetime").datetime.now().isoformat(),  # "ts" — timestamp? tipo serviço?
        "done": False,  # mistura de idioma
    }
    queue.append(entry)
    return _id  # retorna id E adiciona (viola CQS)


def remove(id):  # sobrescreve built-in `id` do Python
    for i, entry in enumerate(queue):
        if entry["id"] == id:
            queue.pop(i)
            return True
    return False  # código de retorno sem exceção


def show():  # o que "show" mostra? de quem?
    for entry in queue:
        s = "✓" if entry["done"] else "·"
        print(f"[{s}] #{entry['id']} {entry['n']} ({entry['t']})")


def next_p():  # mistura de idioma ("next" + "p")
    for entry in queue:
        if not entry["done"]:
            entry["done"] = True  # modifica E implica retorno
            return entry
    return None


# ─── Execução de demonstração ─────────────────────────────────────────────────

if __name__ == "__main__":
    add("Maria Oliveira", "retorno")
    add("João Costa", "primeira consulta")
    add("Beatriz Ferreira", "exame")

    print("=== Lista de espera ===")
    show()

    print("\nChamando próximo paciente...")
    proximo = next_p()
    print(f"Chamado: {proximo}")

    print("\n=== Lista atualizada ===")
    show()
