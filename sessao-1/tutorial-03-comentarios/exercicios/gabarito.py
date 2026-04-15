"""
GABARITO — Tutorial 03: Comentários
Referência: Clean Code, Cap. 4
Execute: python gabarito.py
"""

# ════════════════════════════════════════════════════════════════════════════════
# PROBLEMA 1 — RESOLVIDO
# ════════════════════════════════════════════════════════════════════════════════
#
# O que foi feito:
#   - "chk" renomeado para "usuario_esta_ativo"; parâmetro "u" → "usuario";
#     campo "st" → "status". Sem comentário: o nome já diz tudo.
#   - "calc" renomeado para "calcular_preco_com_desconto"; parâmetros "p","d"
#     → "preco","desconto". Todos os comentários redundantes removidos.
#   - "registrar_acesso": TODO reescrito com rastreabilidade; código comentado
#     removido (fica no git history); diário de bordo removido de calcular_multa.

def usuario_esta_ativo(usuario: dict) -> bool:
    return usuario["status"] == 1


def calcular_preco_com_desconto(preco: float, desconto: float) -> float:
    return preco - desconto


def registrar_acesso(usuario_id: str, timestamp: str) -> int:
    # TODO [OPS-304]: persistir no banco de acessos.
    # Responsável: @carlos.lima  |  Prazo: Sprint 43
    contador = 1
    print(f"[LOG] Acesso registrado: {usuario_id} em {timestamp}")
    return contador


TAXA_MULTA_DIARIA = 0.02  # 2% ao dia — definido em contrato (cláusula 9.1, rev. 2024)

def calcular_multa(dias_atraso: int, valor_original: float) -> float:
    return valor_original * TAXA_MULTA_DIARIA * dias_atraso


# ════════════════════════════════════════════════════════════════════════════════
# PROBLEMA 2 — RESOLVIDO
# ════════════════════════════════════════════════════════════════════════════════
#
# O comentário adicionado explica o "porquê" (fórmula de Price / amortização
# constante) — algo que nunca ficaria óbvio só lendo o código.

def calcular_parcela_financiamento(
    valor_principal: float,
    taxa_mensal: float,
    numero_parcelas: int,
) -> float:
    if taxa_mensal == 0:
        return valor_principal / numero_parcelas

    # Fórmula de Price (Sistema Francês de Amortização):
    #   PMT = PV * (i * (1+i)^n) / ((1+i)^n - 1)
    # onde PV = valor principal, i = taxa mensal, n = número de parcelas.
    # Usamos Price porque o contrato prevê parcelas fixas — ao contrário do
    # SAC, onde as parcelas decrescem ao longo do tempo.
    fator = (1 + taxa_mensal) ** numero_parcelas
    parcela = valor_principal * (taxa_mensal * fator) / (fator - 1)
    return round(parcela, 2)


# ════════════════════════════════════════════════════════════════════════════════
# Bloco de verificação — saída idêntica ao exercício.py
# ════════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("=== Verificação do Gabarito ===\n")

    # As funções foram renomeadas no Problema 1 — ajustamos as chamadas:
    usuario_ativo = {"status": 1, "nome": "Maria"}
    usuario_inativo = {"status": 0, "nome": "João"}
    print("usuario_esta_ativo (ativo):", usuario_esta_ativo(usuario_ativo))      # True
    print("usuario_esta_ativo (inativo):", usuario_esta_ativo(usuario_inativo))  # False

    print("calcular_preco_com_desconto(100, 15):", calcular_preco_com_desconto(100.0, 15.0))  # 85.0

    registrar_acesso("U001", "2026-04-14 10:00:00")

    print("calcular_multa(5 dias, R$200):", calcular_multa(5, 200.0))  # 20.0

    print("\ncalcular_parcela_financiamento:")
    print("  R$10.000 / 12x / 1% a.m.:", calcular_parcela_financiamento(10000, 0.01, 12))
    print("  R$5.000 / 24x / 0.8% a.m.:", calcular_parcela_financiamento(5000, 0.008, 24))
    print("  R$3.000 / 10x / 0% (sem juros):", calcular_parcela_financiamento(3000, 0.0, 10))
