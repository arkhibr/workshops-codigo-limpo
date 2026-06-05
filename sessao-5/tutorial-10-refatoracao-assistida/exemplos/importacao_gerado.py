"""
SAÍDA TÍPICA DE IA — importação de clientes a partir de CSV (a partir de prompt aberto)
Referência: Clean Code, Cap. 3 (Funções)

⚠️  Este arquivo é INTENCIONALMENTE IMPERFEITO.
    Representa o tipo de código monolítico que uma IA gera a partir de um prompt aberto.
    Analise os problemas de coesão antes de ver a versão revisada.

Execute: python3 sessao-5/tutorial-10-refatoracao-assistida/exemplos/importacao_gerado.py
"""

# Prompt usado: "importa clientes de um CSV"


def importar(csv):  # faz tudo: lê, valida, converte e acumula
    r = []
    for l in csv.strip().split("\n")[1:]:  # descarta cabeçalho inline
        p = l.split(",")
        if len(p) != 3:  # validação misturada com leitura
            continue
        n, e, c = p[0].strip(), p[1].strip(), p[2].strip()
        if not n or not e or "@" not in e:  # mais validação no mesmo loop
            continue
        r.append({"nome": n, "email": e, "cidade": c})  # conversão inline
    return r


# ─── Execução de demonstração ─────────────────────────────────────────────────

if __name__ == "__main__":
    dados = (
        "nome,email,cidade\n"
        "Ana Silva,ana@exemplo.com,São Paulo\n"
        "Carlos,carlos-invalido,Rio de Janeiro\n"
        "Beatriz Santos,beatriz@exemplo.com,Curitiba\n"
        ",email@vazio.com,Belo Horizonte\n"
        "Diego Lima,diego@exemplo.com,Porto Alegre\n"
    )

    clientes = importar(dados)
    print(f"Clientes importados: {len(clientes)}")
    for c in clientes:
        print(f"  {c['nome']} <{c['email']}> — {c['cidade']}")
