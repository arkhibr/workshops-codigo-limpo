"""
EXERCÍCIO — Tutorial 03: Comentários
Referência: Clean Code, Cap. 4
Execute: python exercicio.py

Este exercício tem dois problemas independentes.

PROBLEMA 1 — REMOVER / REESCREVER
    O código abaixo tem comentários ruins: redundantes, enganosos e código comentado.
    Sua tarefa:
      a) Remova os comentários que não agregam nada.
      b) Reescreva os enganosos como comentário de intenção (se houver algo a dizer).
      c) Remova o código comentado.
      d) Quando necessário, renomeie funções/variáveis para tornar o código autodocumentado.

PROBLEMA 2 — ADICIONAR O COMENTÁRIO CORRETO
    O código abaixo tem uma lógica não óbvia sem nenhum comentário.
    Sua tarefa: adicione APENAS o comentário necessário para explicar o "porquê".
    Não reescreva o código — apenas comente.
"""

# ════════════════════════════════════════════════════════════════════════════════
# PROBLEMA 1: Código com comentários ruins — remova/reescreva/renomeie
# ════════════════════════════════════════════════════════════════════════════════

# verifica se o usuário está ativo
def chk(u):
    # retorna True se o campo "st" for igual a 1
    return u["st"] == 1


# calcula o preço com desconto
def calc(p, d):
    # subtrai o desconto do preço
    r = p - d
    # retorna o resultado
    return r


def registrar_acesso(usuario_id, timestamp):
    # TODO: melhorar isso
    # TODO: adicionar log

    # incrementa o contador
    contador = 0
    contador = contador + 1  # soma 1

    # insere no banco
    # db.insert("acessos", {"usuario": usuario_id, "ts": timestamp})
    # db_antigo.log(usuario_id)
    # enviar_email_boas_vindas(usuario_id)  # não era necessário

    print(f"[LOG] Acesso registrado: {usuario_id} em {timestamp}")
    return contador


def calcular_multa(dias_atraso, valor_original):
    # 15/01/2024 - Pedro mudou a multa de 1% para 2%
    # 03/03/2024 - Ana reverteu para 1% a pedido do jurídico
    # 10/04/2024 - Carlos subiu para 2% novamente
    taxa_multa = 0.02
    return valor_original * taxa_multa * dias_atraso


# ════════════════════════════════════════════════════════════════════════════════
# PROBLEMA 2: Lógica não óbvia sem comentário — adicione o comentário correto
# ════════════════════════════════════════════════════════════════════════════════

def calcular_parcela_financiamento(
    valor_principal: float,
    taxa_mensal: float,
    numero_parcelas: int,
) -> float:
    if taxa_mensal == 0:
        return valor_principal / numero_parcelas

    fator = (1 + taxa_mensal) ** numero_parcelas
    parcela = valor_principal * (taxa_mensal * fator) / (fator - 1)
    return round(parcela, 2)


# ════════════════════════════════════════════════════════════════════════════════
# Bloco de verificação — NÃO altere este bloco
# ════════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("=== Verificação do Exercício ===\n")

    # Problema 1
    usuario_ativo = {"st": 1, "nome": "Maria"}
    usuario_inativo = {"st": 0, "nome": "João"}
    print("chk (ativo):", chk(usuario_ativo))        # esperado: True
    print("chk (inativo):", chk(usuario_inativo))    # esperado: False

    print("calc(100, 15):", calc(100.0, 15.0))        # esperado: 85.0

    registrar_acesso("U001", "2026-04-14 10:00:00")

    print("calcular_multa(5 dias, R$200):", calcular_multa(5, 200.0))  # esperado: 20.0

    # Problema 2
    print("\ncalcular_parcela_financiamento:")
    print("  R$10.000 / 12x / 1% a.m.:", calcular_parcela_financiamento(10000, 0.01, 12))
    print("  R$5.000 / 24x / 0.8% a.m.:", calcular_parcela_financiamento(5000, 0.008, 24))
    print("  R$3.000 / 10x / 0% (sem juros):", calcular_parcela_financiamento(3000, 0.0, 10))
