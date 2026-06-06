"""
MÓDULO DE DASHBOARD DE VENDAS — acumulou deriva por contribuições de IA
Referência: Clean Code, Cap. 1 e 17; Regra do Escoteiro

⚠️  Este arquivo é INTENCIONALMENTE IMPERFEITO.
    Representa um módulo que cresceu com contribuições de IA sem contexto.

Sua tarefa:
  (1) Identifique os sinais de deriva (duplicação, estilo divergente,
      dependência supérflua, formatação inconsistente).
  (2) Consolide o módulo mantendo o comportamento observável.
  (3) Liste o que foi unificado.

Execute: python3 sessao-6/tutorial-15-manutenibilidade-agentes/exercicios/exercicio.py
"""

# Dependência desnecessária — reimplementada localmente para rodar sem instalação.
# Em um projeto real, a IA teria feito: from util_percentual import UtilPercentual
class UtilPercentual:  # noqa: N801  (nome intencional, simula lib de terceiro)
    @staticmethod
    def formatar(valor: float) -> str:
        return f"{valor * 100:.1f}%"


# ── Contribuição 1 — estilo original ─────────────────────────────────────────

META_MENSAL = 10_000.0  # valor-alvo de vendas por mês

def calcular_total_periodo(vendas: list) -> float:
    """Retorna a soma dos valores das vendas no período."""
    return sum(v["valor"] for v in vendas)


def calcular_percentual_meta(total: float) -> float:
    """Retorna o percentual atingido em relação à meta mensal."""
    if META_MENSAL == 0:
        return 0.0
    return total / META_MENSAL


# ── Contribuição 2 — IA duplicou sem saber que a função já existia ────────────

def getTotal(sales):  # inglês; sem type hints; duplica calcular_total_periodo
    t = 0
    for s in sales:
        t += s["valor"]
    return t


def calcular_soma_vendas(lista):  # terceiro nome para a mesma operação
    soma = 0.0
    for item in lista:
        soma = soma + item["valor"]
    return soma


# ── Contribuição 3 — IA usou UtilPercentual em vez de f-string ───────────────

def formatar_percentual_dashboard(valor: float) -> str:
    # Usa UtilPercentual em vez de f-string nativa
    return UtilPercentual.formatar(valor)


# ── Contribuição 4 — estilo e formatação divergentes ─────────────────────────
def exibir_dashboard(vendas,periodo="Período Atual"): # sem espaços, sem type hints
    total=getTotal(vendas)  # usa duplicata em vez da função original
    pct=calcular_percentual_meta(total)
    print(f"=== Dashboard: {periodo} ===")
    print(f"Vendas registradas: {len(vendas)}")
    print(f"Total: R$ {total:,.2f}".replace(",","X").replace(".",",").replace("X","."))
    print("Meta atingida:",formatar_percentual_dashboard(pct))
    if total>=META_MENSAL:
        print("STATUS: META ATINGIDA")
    else:
        faltam=META_MENSAL-total
        print(f"STATUS: faltam R$ {faltam:,.2f}".replace(",","X").replace(".",",").replace("X","."))


# ── Execução de demonstração ──────────────────────────────────────────────────

if __name__ == "__main__":
    vendas_fevereiro = [
        {"descricao": "Produto A", "valor": 3200.00},
        {"descricao": "Produto B", "valor": 1750.00},
        {"descricao": "Produto C", "valor": 4100.00},
    ]

    exibir_dashboard(vendas_fevereiro, "Fevereiro/2026")
    print()
    print("calcular_total_periodo:", calcular_total_periodo(vendas_fevereiro))
    print("getTotal (duplicata):", getTotal(vendas_fevereiro))
    print("calcular_soma_vendas (duplicata):", calcular_soma_vendas(vendas_fevereiro))
