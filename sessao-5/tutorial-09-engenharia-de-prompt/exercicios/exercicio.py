"""
EXERCÍCIO — Cupom de desconto progressivo (saída típica de IA, a partir de prompt fraco)
Referência: Clean Code, Cap. 2–3; engenharia de contexto em prompts de código

Prompt usado para gerar este código:
    "cria um módulo de cupom de desconto pra loja"

Sua tarefa:
    (1) Reescreva o prompt acima para ser mais forte (veja o modelo em exemplos/prompt.md).
    (2) Refatore o código abaixo aplicando os princípios de Clean Code.
    (3) Liste os problemas que você encontrou (nomes, coesão, idioma, números mágicos, etc.).

Execute: python3 sessao-5/tutorial-09-engenharia-de-prompt/exercicios/exercicio.py
"""

# ⚠️  Código gerado por IA — INTENCIONALMENTE IMPERFEITO. Não corrija antes de listar os problemas.

cupons = {}  # nome vago; o que guarda?


def apply(code, val):  # nome em inglês; "val" — valor do quê?
    if code not in cupons:
        return val  # sem exceção — falha silenciosa
    c = cupons[code]  # "c" — o que é?
    if c["type"] == "pct":  # "pct" — abreviação obscura; "type" em inglês
        if val >= 200:
            d = val * c["amt"] * 1.5  # número mágico 1.5 — bônus? progressivo?
        else:
            d = val * c["amt"]
        return round(val - d, 2)
    elif c["type"] == "fixed":  # inglês misturado
        return round(max(val - c["amt"], 0), 2)  # max sem comentário — por quê?
    return val


def add(code, tp, amt):  # "tp" — tipo? temperatura? turno?
    cupons[code] = {"type": tp, "amt": amt}


def rm(code):  # "rm" — nome de comando Unix, não de domínio
    if code in cupons:
        del cupons[code]
    # sem aviso se não existir


def show_all():  # mistura de idioma; "show" vago
    for k, v in cupons.items():
        print(f"  {k}: {v}")


# ─── Execução de demonstração ─────────────────────────────────────────────────

if __name__ == "__main__":
    add("VERAO10", "pct", 0.10)
    add("FRETE", "fixed", 15.0)
    add("VIP20", "pct", 0.20)

    print("=== Cupons cadastrados ===")
    show_all()

    print("\n--- Aplicando cupons ---")
    # compra de R$ 150 com cupom percentual (sem bônus progressivo)
    print("Compra R$150 + VERAO10:", apply("VERAO10", 150.0))

    # compra de R$ 300 com cupom percentual (com bônus progressivo)
    print("Compra R$300 + VERAO10:", apply("VERAO10", 300.0))

    # cupom de valor fixo
    print("Compra R$50 + FRETE:", apply("FRETE", 50.0))

    # cupom inexistente — falha silenciosa
    print("Compra R$100 + INVALIDO:", apply("INVALIDO", 100.0))
