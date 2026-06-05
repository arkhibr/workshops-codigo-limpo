"""
GABARITO — importação de catálogo de produtos após refatoração assistida
Referência: Clean Code, Cap. 3 (Funções)

Responsabilidades separadas:
  - ler_linhas: lê e descarta o cabeçalho do CSV
  - validar_produto: verifica campos obrigatórios e formatos
  - converter_produto: converte tipos e monta o dicionário
  - filtrar_produto: aplica regras de negócio (preço e estoque)
  - importar_produtos: orquestra as quatro funções acima

Execute: python3 sessao-5/tutorial-10-refatoracao-assistida/exercicios/gabarito.py
"""

from __future__ import annotations

SEPARADOR_CSV = ","
INDICE_NOME = 0
INDICE_CATEGORIA = 1
INDICE_PRECO = 2
INDICE_QUANTIDADE = 3
TOTAL_CAMPOS_ESPERADO = 4
PRECO_MINIMO = 0.0
QUANTIDADE_MINIMA = 0


def ler_linhas(conteudo_csv: str) -> list[str]:
    """Retorna as linhas de dados do CSV, descartando o cabeçalho."""
    linhas = conteudo_csv.strip().split("\n")
    return linhas[1:]


def validar_produto(campos: list[str]) -> bool:
    """Retorna True se os campos contiverem nome, categoria e valores convertíveis."""
    if len(campos) != TOTAL_CAMPOS_ESPERADO:
        return False
    nome = campos[INDICE_NOME].strip()
    categoria = campos[INDICE_CATEGORIA].strip()
    if not nome or not categoria:
        return False
    try:
        float(campos[INDICE_PRECO].strip())
        int(campos[INDICE_QUANTIDADE].strip())
    except ValueError:
        return False
    return True


def converter_produto(campos: list[str]) -> dict:
    """Converte campos CSV em dicionário de produto com tipos corretos."""
    return {
        "nome": campos[INDICE_NOME].strip(),
        "categoria": campos[INDICE_CATEGORIA].strip(),
        "preco": float(campos[INDICE_PRECO].strip()),
        "quantidade": int(campos[INDICE_QUANTIDADE].strip()),
    }


def filtrar_produto(produto: dict) -> bool:
    """Retorna True se o produto atender às regras de negócio (preço e estoque)."""
    return produto["preco"] > PRECO_MINIMO and produto["quantidade"] >= QUANTIDADE_MINIMA


def importar_produtos(conteudo_csv: str) -> list[dict]:
    """Lê, valida, converte e filtra cada linha do CSV em dicionário de produto."""
    produtos = []
    for linha in ler_linhas(conteudo_csv):
        campos = linha.split(SEPARADOR_CSV)
        if not validar_produto(campos):
            continue
        produto = converter_produto(campos)
        if filtrar_produto(produto):
            produtos.append(produto)
    return produtos


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

    produtos = importar_produtos(catalogo_csv)
    print(f"Produtos importados: {len(produtos)}")
    for produto in produtos:
        print(f"  [{produto['categoria']}] {produto['nome']} — R$ {produto['preco']:.2f} ({produto['quantidade']} un.)")
