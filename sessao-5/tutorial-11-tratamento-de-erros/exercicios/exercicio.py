"""
EXERCÍCIO — cancelamento de assinatura (saída de IA com erros silenciados)
Referência: Clean Code, Cap. 7 (Error Handling)

⚠️  Este arquivo é INTENCIONALMENTE IMPERFEITO.
    A função mistura validação, cálculo e persistência EM UMA ÚNICA função
    E silencia os erros com except Exception: pass.
    Sua tarefa:

    (1) Torne cada falha visível com uma exceção específica.
    (2) Separe as responsabilidades (validação / cálculo / persistência).
    (3) Liste os erros que estavam sendo silenciados.

Execute: python3 sessao-5/tutorial-11-tratamento-de-erros/exercicios/exercicio.py
"""

# Prompt usado: "cria uma função que cancela uma assinatura e calcula o reembolso"

banco_assinaturas = {
    "ASS-001": {"plano": "mensal", "valor": 49.90, "dias_restantes": 18, "ativa": True},
    "ASS-002": {"plano": "anual",  "valor": 499.00, "dias_restantes": 0,  "ativa": False},
    "ASS-003": {"plano": "mensal", "valor": 29.90, "dias_restantes": 10, "ativa": True},
}

cancelamentos_registrados = []


def cancelar(id, motivo):  # faz tudo junto: busca, valida, calcula e persiste
    try:
        dados = banco_assinaturas.get(id)
        if not dados:
            return None  # assinatura não encontrada — falha silenciosa
        if not dados["ativa"]:
            return None  # já cancelada — falha silenciosa
        dias = dados["dias_restantes"]
        valor = dados["valor"]
        if dias <= 0:
            reembolso = 0.0
        else:
            # cálculo de reembolso proporcional ao plano
            if dados["plano"] == "mensal":
                reembolso = round(valor * (dias / 30), 2)
            else:
                reembolso = round(valor * (dias / 365), 2)
        dados["ativa"] = False  # persiste o cancelamento inline
        cancelamentos_registrados.append({
            "id": id,
            "motivo": motivo,
            "reembolso": reembolso,
        })
        return {"id": id, "reembolso": reembolso, "status": "cancelado"}
    except Exception:
        pass  # qualquer erro desaparece sem rastro


# ─── Execução de demonstração ─────────────────────────────────────────────────

if __name__ == "__main__":
    print("=== Demonstração: exercicio.py (cancelamento de assinatura) ===")
    print()

    # Caso 1: cancelamento válido
    r = cancelar("ASS-001", "cliente solicitou")
    print(f"ASS-001 (ativa, 18 dias restantes): {r}")

    # Caso 2: assinatura já cancelada
    r = cancelar("ASS-002", "cliente solicitou")
    print(f"ASS-002 (já cancelada): {r}")  # retorna None — falha invisível

    # Caso 3: ID inexistente
    r = cancelar("ASS-999", "cliente solicitou")
    print(f"ASS-999 (não existe): {r}")    # retorna None — falha invisível

    # Caso 4: motivo ausente — aceito sem validação (deveria falhar)
    r = cancelar("ASS-003", None)
    print(f"ASS-003 (motivo None): {r}")   # cancela mesmo sem motivo — falha silenciosa por omissão

    print()
    print("⚠ ASS-002 e ASS-999 sumiram como None; o motivo ausente foi aceito sem validação — três falhas sem erro.")
    print("  O chamador recebe None mas não sabe o que houve.")
