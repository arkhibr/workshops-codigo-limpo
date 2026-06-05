"""
VERSÃO REVISADA — importação de clientes a partir de CSV após refatoração assistida
Referência: Clean Code, Cap. 3 (Funções)

Problemas corrigidos em relação à versão gerada:
  - Função monolítica dividida em responsabilidades únicas
  - ler_linhas: lê e descarta o cabeçalho
  - validar_cliente: verifica campos obrigatórios e formato de e-mail
  - converter_cliente: monta o dicionário com campos normalizados
  - importar_clientes: orquestra as três funções acima
  - Nomes descritivos em português para todos os identificadores

Nota didática: o comportamento é idêntico ao da versão gerada — apenas
a estrutura interna foi reorganizada em passos pequenos e verificáveis.

Execute: python3 sessao-5/tutorial-10-refatoracao-assistida/exemplos/importacao_revisado.py
"""

from __future__ import annotations

SEPARADOR_CSV = ","
INDICE_NOME = 0
INDICE_EMAIL = 1
INDICE_CIDADE = 2
TOTAL_CAMPOS_ESPERADO = 3


def ler_linhas(conteudo_csv: str) -> list[str]:
    """Retorna as linhas de dados do CSV, descartando o cabeçalho."""
    linhas = conteudo_csv.strip().split("\n")
    return linhas[1:]


def validar_cliente(campos: list[str]) -> bool:
    """Retorna True se os campos contiverem nome, e-mail válido e cidade."""
    if len(campos) != TOTAL_CAMPOS_ESPERADO:
        return False
    nome = campos[INDICE_NOME].strip()
    email = campos[INDICE_EMAIL].strip()
    return bool(nome) and bool(email) and "@" in email


def converter_cliente(campos: list[str]) -> dict:
    """Converte campos CSV em dicionário de cliente normalizado."""
    return {
        "nome": campos[INDICE_NOME].strip(),
        "email": campos[INDICE_EMAIL].strip(),
        "cidade": campos[INDICE_CIDADE].strip(),
    }


def importar_clientes(conteudo_csv: str) -> list[dict]:
    """Lê, valida e converte cada linha do CSV em dicionário de cliente."""
    clientes = []
    for linha in ler_linhas(conteudo_csv):
        campos = linha.split(SEPARADOR_CSV)
        if validar_cliente(campos):
            clientes.append(converter_cliente(campos))
    return clientes


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

    clientes = importar_clientes(dados)
    print(f"Clientes importados: {len(clientes)}")
    for cliente in clientes:
        print(f"  {cliente['nome']} <{cliente['email']}> — {cliente['cidade']}")
