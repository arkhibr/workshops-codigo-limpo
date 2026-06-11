"""
EXERCÍCIO — Tutorial 06: Dívida Técnica
Referência: Clean Code, Cap. 17
Execute: python3 exercicio.py

Este módulo calcula fretes para uma transportadora fictícia.
Ele está funcional, mas carrega 4 tipos de dívida técnica.

PASSOS (faça um de cada vez, em ordem):

  PASSO 1 — IDENTIFICAR (5 min)
    Leia o código abaixo. Antes de cada dívida, adicione um comentário:
        # DÍVIDA [TIPO]: <descrição>
    Tipos: MAGIC_NUMBER, NOMES, DUPLICAÇÃO, FUNÇÕES
    Meta: encontrar pelo menos 3 das 4 antes de avançar.

  PASSO 2 — CONSTANTES (5 min)
    Extraia os magic numbers para constantes nomeadas acima das funções.
    Substitua os literais numéricos pelas constantes no corpo das funções.
    Verifique: python3 exercicio.py deve imprimir os mesmos valores.

  PASSO 3 — NOMES (5 min)
    Renomeie os parâmetros obscuros em calc_frete e estimar:
      tp  → modalidade
      kg  → peso_kg
      km  → distancia_km
      urg → urgente
    Renomeie a função estimar para estimar_frete.
    Verifique que o arquivo ainda executa sem erros.

  PASSO 4 — ELIMINAR DUPLICAÇÃO (10 min)
    calc_frete e estimar têm exatamente o mesmo corpo de cálculo.
    Extraia a lógica compartilhada para _calcular_por_modalidade.
    Faça calcular_frete e estimar_frete chamarem essa função.
    Verifique que a saída continua idêntica.
"""

# ════════════════════════════════════════════════════════════════════════════════
# CÓDIGO COM DÍVIDA TÉCNICA — trabalhe aqui nos Passos 1, 2 e 3
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
# PASSO 2 — adicione as constantes nomeadas aqui
# ════════════════════════════════════════════════════════════════════════════════

# LIMITE_FAIXA_1_KG = ...
# LIMITE_FAIXA_2_KG = ...
# FATOR_URGENCIA    = ...
# TARIFAS = {
#     "A": {"taxa_base": ..., "custo_faixa_2": ..., "custo_faixa_3": ..., "custo_km": ...},
#     ...
# }


# ════════════════════════════════════════════════════════════════════════════════
# PASSO 4 — extraia aqui a função auxiliar e redefina as funções públicas
# ════════════════════════════════════════════════════════════════════════════════

# Dica: mova a lógica duplicada para _calcular_por_modalidade; as funções
# públicas ficam com 2-3 linhas cada.

# def _calcular_por_modalidade(modalidade, peso_kg, distancia_km):
#     ...

# def calcular_frete(modalidade, peso_kg, distancia_km, urgente=False):
#     valor = _calcular_por_modalidade(...)
#     ...

# def estimar_frete(modalidade, peso_kg, distancia_km):
#     return calcular_frete(...)


# ════════════════════════════════════════════════════════════════════════════════
# Bloco de verificação — não altere
# ════════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("=== Verificação: Cálculo de Frete ===\n")

    print("Frete A, 3kg, 100km:",          calc_frete("A",  3, 100))        # 27.0
    print("Frete A, 15kg, 200km:",         calc_frete("A", 15, 200))        # 64.0
    print("Frete A, 30kg, 300km:",         calc_frete("A", 30, 300))        # 106.5
    print("Frete B, 10kg, 150km:",         calc_frete("B", 10, 150))        # 68.0
    print("Frete C, 25kg, 400km:",         calc_frete("C", 25, 400))        # 214.0
    print("Frete A urgente, 5kg, 100km:",  calc_frete("A",  5, 100, True))  # 35.1
    print("Estimativa A, 3kg, 100km:",     estimar("A", 3, 100))            # 27.0

    # Após o Passo 4, descomente e verifique que os valores batem:
    # print("\n--- Versão refatorada (Passo 4) ---")
    # print("Frete A, 3kg, 100km:",         calcular_frete("A",  3, 100))
    # print("Frete A, 15kg, 200km:",        calcular_frete("A", 15, 200))
    # print("Frete A, 30kg, 300km:",        calcular_frete("A", 30, 300))
    # print("Frete B, 10kg, 150km:",        calcular_frete("B", 10, 150))
    # print("Frete C, 25kg, 400km:",        calcular_frete("C", 25, 400))
    # print("Frete A urgente, 5kg, 100km:", calcular_frete("A",  5, 100, urgente=True))
    # print("Estimativa A, 3kg, 100km:",    estimar_frete("A", 3, 100))
