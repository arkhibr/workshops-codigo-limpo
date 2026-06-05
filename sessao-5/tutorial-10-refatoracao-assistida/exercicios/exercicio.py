"""
EXERCÍCIO — importação de catálogo de produtos (saída de IA com baixa coesão)
Referência: Clean Code, Cap. 3 (Funções)

⚠️  Este arquivo é INTENCIONALMENTE IMPERFEITO.
    Representa o tipo de código monolítico que uma IA gera a partir de um prompt aberto.
    Sua tarefa:

    (1) Refatore em passos pequenos, extraindo uma responsabilidade por vez.
    (2) Rode o arquivo após cada passo para confirmar que a saída é preservada.
    (3) Liste as responsabilidades que você separou.

Execute: python3 sessao-5/tutorial-10-refatoracao-assistida/exercicios/exercicio.py
"""

# Prompt usado: "importa produtos de um CSV"


def processar(data):  # lê, valida, converte, filtra e acumula tudo junto
    res = []
    rows = data.strip().split("\n")[1:]  # descarta cabeçalho inline
    for r in rows:
        cols = r.split(",")
        if len(cols) != 4:  # validação misturada com leitura
            continue
        nm, cat, pr, qt = cols[0].strip(), cols[1].strip(), cols[2].strip(), cols[3].strip()
        if not nm or not cat:  # validação de campos obrigatórios inline
            continue
        try:
            preco = float(pr)  # conversão de tipo inline
            qtd = int(qt)
        except ValueError:
            continue
        if preco <= 0 or qtd < 0:  # regra de negócio inline
            continue
        res.append({"nome": nm, "categoria": cat, "preco": preco, "quantidade": qtd})  # conversão inline
    return res


# ─── Execução de demonstração ─────────────────────────────────────────────────

if __name__ == "__main__":
    catalogo_csv = (
        "nome,categoria,preco,quantidade\n"
        "Teclado Mecânico,Periféricos,350.00,15\n"
        "Mouse Sem Fio,Periféricos,120.00,30\n"
        "Monitor 24pol,Monitores,-50.00,5\n"
        "Headset Gamer,Periféricos,280.00,0\n"
        "Webcam HD,,90.00,12\n"
        "Hub USB,Acessórios,abc,8\n"
        "SSD 1TB,Armazenamento,450.00,20\n"
    )

    produtos = processar(catalogo_csv)
    print(f"Produtos importados: {len(produtos)}")
    for p in produtos:
        print(f"  [{p['categoria']}] {p['nome']} — R$ {p['preco']:.2f} ({p['quantidade']} un.)")
