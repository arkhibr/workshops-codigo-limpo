"""
EXERCÍCIO — Testes de Caracterização Antes de Mudanças Assistidas
Referência: Feathers (testes de caracterização) + Clean Code, Cap. 9 (Testes)

Domínio: cálculo de desconto de fidelidade por faixas de pontos acumulados.

Sua tarefa (em três etapas):
  (1) Escreva testes de caracterização do comportamento atual usando a
      convenção verificar_*: funções que imprimem "OK: <caso>" ou
      "FALHOU: <caso> (esperado X, obtido Y)". Cubra cada faixa e os
      valores-limite.
  (2) Só depois que todos os testes passarem com o código intocado,
      peça à IA a mudança: adicionar uma nova faixa para clientes com
      mais de 2.000 pontos (desconto de 25%).
  (3) Rode os testes antes e depois da mudança. Se algum falhar,
      encontre e corrija a regressão antes de aceitar o código gerado.

Execute: python3 sessao-6/tutorial-14-testes-guard-rails/exercicios/exercicio.py
"""


# Tabela de faixas de desconto por pontos acumulados:
#   0–499 pontos    → 0% de desconto
#   500–999 pontos  → 5% de desconto
#   1.000–1.999 pts → 10% de desconto
#   2.000+ pontos   → (sem faixa definida — será adicionada pela mudança)

DESCONTO_SEM_PONTOS = 0.00
DESCONTO_BRONZE = 0.05
DESCONTO_PRATA = 0.10


def calcular_desconto_fidelidade(pontos: int, valor_compra: float) -> float:
    """
    Calcula o desconto de fidelidade com base nos pontos acumulados.

    Retorna o valor do desconto (não o valor final da compra).
    """
    if pontos < 500:
        percentual = DESCONTO_SEM_PONTOS
    elif pontos < 1000:
        percentual = DESCONTO_BRONZE
    else:
        percentual = DESCONTO_PRATA

    return round(valor_compra * percentual, 2)


# ─── TODO: escreva suas verificações verificar_* aqui ─────────────────────────
#
# Exemplo de estrutura:
#
# def verificar_desconto_sem_pontos() -> None:
#     resultado = calcular_desconto_fidelidade(pontos=100, valor_compra=200.00)
#     esperado = 0.00
#     if abs(resultado - esperado) < 0.01:
#         print("OK: desconto sem pontos")
#     else:
#         print(f"FALHOU: desconto sem pontos (esperado {esperado}, obtido {resultado})")
#
# Lembre-se de cobrir:
#   - cada faixa com um caso típico
#   - os valores exatos de limite (499, 500, 999, 1.000)
#   - valor_compra variado (0.00, valor pequeno, valor grande)


# ─── Execução de demonstração ─────────────────────────────────────────────────

if __name__ == "__main__":
    print("=== Exercício: exercicio.py ===")
    print()
    print("Comportamento atual da função calcular_desconto_fidelidade:")
    print()

    casos = [
        (100,  200.00, "sem pontos (faixa 0%)"),
        (499,  200.00, "limite inferior bronze (499 pts)"),
        (500,  200.00, "bronze (500 pts, 5%)"),
        (999,  200.00, "limite inferior prata (999 pts)"),
        (1000, 200.00, "prata (1.000 pts, 10%)"),
        (1500, 200.00, "prata alto (1.500 pts, 10%)"),
    ]

    for pontos, valor, descricao in casos:
        desconto = calcular_desconto_fidelidade(pontos, valor)
        print(f"  {pontos:5d} pts, R$ {valor:.2f} → desconto R$ {desconto:.2f}  ({descricao})")

    print()
    print("Escreva os testes de caracterização ANTES de pedir a mudança à IA.")
