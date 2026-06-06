"""
MÓDULO DE RELATÓRIO DE VENDAS — versão consolidada após revisão de deriva
Referência: Clean Code, Cap. 1 e 17; Regra do Escoteiro

Sinais de deriva eliminados em relação à versão gerada:
  - Duplicação removida: calcTotal() e calcular_total_geral() eliminadas;
    calcular_total_vendas() é a única função de cálculo de total.
  - Estilo unificado: todos os nomes em snake_case português com type hints.
  - Dependência desnecessária removida: _formatador_externo substituído por
    f-string nativa com :,.2f (stdlib resolve sem dependência externa).
  - Formatação unificada: espaçamento e assinaturas consistentes em todas
    as funções.

Execute: python3 sessao-6/tutorial-15-manutenibilidade-agentes/exemplos/relatorio_revisado.py
"""

from __future__ import annotations


# ── Funções de cálculo ────────────────────────────────────────────────────────

def calcular_total_vendas(vendas: list[dict]) -> float:
    """Retorna a soma dos valores de todas as vendas da lista."""
    return sum(v["valor"] for v in vendas)


def calcular_media_vendas(vendas: list[dict]) -> float:
    """Retorna o valor médio das vendas da lista."""
    if not vendas:
        return 0.0
    return calcular_total_vendas(vendas) / len(vendas)


# ── Formatação ────────────────────────────────────────────────────────────────

def formatar_valor_reais(valor: float) -> str:
    """Formata um número como moeda brasileira usando a stdlib."""
    # f-string com :,.2f produz "1,234.56"; ajuste de separadores abaixo.
    formatado = f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return f"R$ {formatado}"


# ── Relatório ─────────────────────────────────────────────────────────────────

def gerar_resumo(vendas: list[dict], titulo: str = "Resumo de Vendas") -> None:
    """Imprime um resumo de vendas com total e média."""
    total = calcular_total_vendas(vendas)
    media = calcular_media_vendas(vendas)

    print(titulo)
    print("-" * 40)
    for v in vendas:
        print(f"{v['descricao']}: {formatar_valor_reais(v['valor'])}")
    print("-" * 40)
    print(f"Total: {formatar_valor_reais(total)}")
    print(f"Média: {formatar_valor_reais(media)}")


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
