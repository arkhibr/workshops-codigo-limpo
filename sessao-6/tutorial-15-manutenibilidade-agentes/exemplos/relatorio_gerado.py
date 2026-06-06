"""
MÓDULO DE RELATÓRIO DE VENDAS — acumulou deriva por contribuições de IA inconsistentes
Referência: Clean Code, Cap. 1 e 17; Regra do Escoteiro

⚠️  Este arquivo é INTENCIONALMENTE IMPERFEITO.
    Representa um módulo real que "cresceu" com várias sessões de IA sem contexto.
    Analise os quatro sinais de deriva antes de ver a versão revisada.

Cenário: o módulo começou com calcular_total_vendas() (contribuição 1).
  Contribuição 2: IA adicionou calcTotal() sem saber que a função já existia.
  Contribuição 3: IA adicionou formatação de moeda via _formatador_externo,
                  sem saber que f-string com :,.2f resolve o problema.
  Contribuição 4: IA adicionou gerar_resumo() com estilo de nome e formatação
                  divergentes das funções anteriores.

Execute: python3 sessao-6/tutorial-15-manutenibilidade-agentes/exemplos/relatorio_gerado.py
"""

# Dependência desnecessária — reimplementada localmente para o módulo rodar
# sem instalação. Em um projeto real, a IA teria feito: import formatador_externo
class _formatador_externo:  # noqa: N801  (nome intencional, simula lib de terceiro)
    @staticmethod
    def formatar_moeda(valor: float) -> str:
        """Formata um número como moeda brasileira."""
        inteiro = int(valor)
        centavos = round((valor - inteiro) * 100)
        s = f"{inteiro:,}".replace(",", "X").replace(".", ",").replace("X", ".")
        return f"R$ {s},{centavos:02d}"


# ── Contribuição 1 — estilo original do módulo ────────────────────────────────

def calcular_total_vendas(vendas: list) -> float:
    """Retorna a soma dos valores de todas as vendas da lista."""
    return sum(v["valor"] for v in vendas)


def calcular_media_vendas(vendas: list) -> float:
    """Retorna o valor médio das vendas da lista."""
    if not vendas:
        return 0.0
    return calcular_total_vendas(vendas) / len(vendas)


# ── Contribuição 2 — IA não recebeu contexto; duplicou com estilo diferente ───

def calcTotal(vendas):  # camelCase; sem type hints; duplica calcular_total_vendas
    total = 0
    for v in vendas:
        total = total + v["valor"]  # loop manual em vez de sum()
    return total


def calcular_total_geral(lista_de_vendas):  # terceiro nome para a mesma operação
    soma = 0.0
    for venda in lista_de_vendas:
        soma += venda["valor"]
    return soma


# ── Contribuição 3 — IA puxou "dependência" para formatar moeda ───────────────

def formatar_valor_relatorio(valor: float) -> str:
    # Usa _formatador_externo em vez de f-string nativa
    return _formatador_externo.formatar_moeda(valor)


# ── Contribuição 4 — estilo e formatação divergentes ─────────────────────────
def gerar_resumo(vendas,titulo="Resumo de Vendas"): # sem espaços, sem type hints
    total=calcTotal(vendas)  # usa a função duplicada em vez da original
    media=calcular_media_vendas(vendas)
    print(titulo)
    print("-"*40)
    for v in vendas:
        print(v["descricao"],":",formatar_valor_relatorio(v["valor"]))
    print("-"*40)
    print("Total:",formatar_valor_relatorio(total))
    print("Média:",formatar_valor_relatorio(media))


# ── Execução de demonstração ──────────────────────────────────────────────────

if __name__ == "__main__":
    vendas_janeiro = [
        {"descricao": "Produto A", "valor": 1200.00},
        {"descricao": "Produto B", "valor": 850.50},
        {"descricao": "Produto C", "valor": 3400.00},
    ]

    gerar_resumo(vendas_janeiro, "Relatório de Janeiro")
    print()
    print("calcular_total_vendas:", calcular_total_vendas(vendas_janeiro))
    print("calcTotal (duplicata):", calcTotal(vendas_janeiro))
    print("calcular_total_geral (duplicata):", calcular_total_geral(vendas_janeiro))
