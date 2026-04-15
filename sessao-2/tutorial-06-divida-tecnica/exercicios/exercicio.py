"""
EXERCÍCIO — Tutorial 06: Dívida Técnica
Referência: Clean Code, Cap. 17
Execute: python exercicio.py

Este módulo calcula fretes para uma transportadora fictícia.
Ele está funcional, mas tem pelo menos 4 tipos de dívida técnica.

TAREFA:
  Parte 1 — IDENTIFICAR: leia o código abaixo e adicione um comentário
  antes de cada dívida encontrada no formato:
      # DÍVIDA [TIPO]: <descrição do problema>
  Onde TIPO pode ser: NOMES, FUNÇÕES, DUPLICAÇÃO, MAGIC_NUMBER

  Parte 2 — REFATORAR: implemente a versão refatorada na seção
  marcada ao final deste arquivo. A saída do bloco __main__ deve
  ser idêntica antes e depois da refatoração.

Tipos de dívida para encontrar (pelo menos 3 dos 4):
  - Magic numbers (valores sem constante nomeada)
  - Duplicação (lógica repetida em dois ou mais lugares)
  - Funções longas (função que faz mais de uma coisa)
  - Nomes obscuros (variáveis/funções que não revelam intenção)
"""

# ════════════════════════════════════════════════════════════════════════════════
# CÓDIGO COM DÍVIDA TÉCNICA — identifique e anote as dívidas
# ════════════════════════════════════════════════════════════════════════════════

def calc_frete(tp, kg, km, urg=False):
    t = 0.0
    if tp == "A":
        if kg <= 5:
            t = 15.0
        elif kg <= 20:
            t = 15.0 + (kg - 5) * 2.5
        else:
            t = 15.0 + (20 - 5) * 2.5 + (kg - 20) * 1.8
        t += km * 0.12
    elif tp == "B":
        if kg <= 5:
            t = 25.0
        elif kg <= 20:
            t = 25.0 + (kg - 5) * 3.2
        else:
            t = 25.0 + (20 - 5) * 3.2 + (kg - 20) * 2.1
        t += km * 0.18
    elif tp == "C":
        if kg <= 5:
            t = 40.0
        elif kg <= 20:
            t = 40.0 + (kg - 5) * 4.0
        else:
            t = 40.0 + (20 - 5) * 4.0 + (kg - 20) * 2.8
        t += km * 0.25
    if urg:
        t = t * 1.3
    return round(t, 2)


def estimar(tp, kg, km):
    t = 0.0
    if tp == "A":
        if kg <= 5:
            t = 15.0
        elif kg <= 20:
            t = 15.0 + (kg - 5) * 2.5
        else:
            t = 15.0 + (20 - 5) * 2.5 + (kg - 20) * 1.8
        t += km * 0.12
    elif tp == "B":
        if kg <= 5:
            t = 25.0
        elif kg <= 20:
            t = 25.0 + (kg - 5) * 3.2
        else:
            t = 25.0 + (20 - 5) * 3.2 + (kg - 20) * 2.1
        t += km * 0.18
    elif tp == "C":
        if kg <= 5:
            t = 40.0
        elif kg <= 20:
            t = 40.0 + (kg - 5) * 4.0
        else:
            t = 40.0 + (20 - 5) * 4.0 + (kg - 20) * 2.8
        t += km * 0.25
    return round(t, 2)


# ════════════════════════════════════════════════════════════════════════════════
# IMPLEMENTE AQUI A VERSÃO REFATORADA
# ════════════════════════════════════════════════════════════════════════════════

# Dica: comece pelas constantes, depois extraia funções pequenas.

# def calcular_frete_por_modalidade(...):
#     ...

# def calcular_frete(modalidade, peso_kg, distancia_km, urgente=False):
#     ...

# def estimar_frete(modalidade, peso_kg, distancia_km):
#     ...


# ════════════════════════════════════════════════════════════════════════════════
# Bloco de verificação — não altere
# ════════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("=== Verificação: Cálculo de Frete ===\n")

    # Usando funções originais (com dívida)
    print("Frete A, 3kg, 100km:", calc_frete("A", 3, 100))
    print("Frete A, 15kg, 200km:", calc_frete("A", 15, 200))
    print("Frete A, 30kg, 300km:", calc_frete("A", 30, 300))
    print("Frete B, 10kg, 150km:", calc_frete("B", 10, 150))
    print("Frete C, 25kg, 400km:", calc_frete("C", 25, 400))
    print("Frete A urgente, 5kg, 100km:", calc_frete("A", 5, 100, urg=True))
    print("Estimativa A, 3kg, 100km:", estimar("A", 3, 100))

    # Após implementar, descomente e verifique que os valores batem:
    # print("\n--- Versão Refatorada ---")
    # print("Frete A, 3kg, 100km:", calcular_frete("A", 3, 100))
    # print("Frete A, 15kg, 200km:", calcular_frete("A", 15, 200))
    # print("Frete A, 30kg, 300km:", calcular_frete("A", 30, 300))
    # print("Frete B, 10kg, 150km:", calcular_frete("B", 10, 150))
    # print("Frete C, 25kg, 400km:", calcular_frete("C", 25, 400))
    # print("Frete A urgente, 5kg, 100km:", calcular_frete("A", 5, 100, urgente=True))
    # print("Estimativa A, 3kg, 100km:", estimar_frete("A", 3, 100))
