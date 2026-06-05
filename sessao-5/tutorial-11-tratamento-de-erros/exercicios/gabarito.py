"""
GABARITO — cancelamento de assinatura com erros tratados explicitamente
Referência: Clean Code, Cap. 7 (Error Handling)

Problemas corrigidos em relação ao exercício:
  - AssinaturaNaoEncontradaError: ID inexistente levanta exceção específica
  - AssinaturaJaCanceladaError: estado inválido levanta exceção específica
  - MotivoAusenteError: motivo obrigatório validado explicitamente
  - Responsabilidades separadas: buscar / validar / calcular / persistir / cancelar
  - Falhas agora são visíveis — o chamador coleta e reporta cada uma

Execute: python3 sessao-5/tutorial-11-tratamento-de-erros/exercicios/gabarito.py
"""

from __future__ import annotations


# ─── Exceções específicas ──────────────────────────────────────────────────────

class AssinaturaNaoEncontradaError(Exception):
    """Levantada quando o ID da assinatura não existe no banco."""


class AssinaturaJaCanceladaError(Exception):
    """Levantada quando a assinatura já foi cancelada anteriormente."""


class MotivoAusenteError(Exception):
    """Levantada quando o motivo do cancelamento não foi informado."""


# ─── Dados em memória ─────────────────────────────────────────────────────────

DIAS_MES = 30
DIAS_ANO = 365

banco_assinaturas: dict[str, dict] = {
    "ASS-001": {"plano": "mensal", "valor": 49.90, "dias_restantes": 18, "ativa": True},
    "ASS-002": {"plano": "anual",  "valor": 499.00, "dias_restantes": 0,  "ativa": False},
    "ASS-003": {"plano": "mensal", "valor": 29.90, "dias_restantes": 10, "ativa": True},
}

cancelamentos_registrados: list[dict] = []


# ─── Funções com responsabilidade única ───────────────────────────────────────

def buscar_assinatura(id_assinatura: str) -> dict:
    """Retorna os dados da assinatura ou levanta AssinaturaNaoEncontradaError."""
    dados = banco_assinaturas.get(id_assinatura)
    if dados is None:
        raise AssinaturaNaoEncontradaError(
            f"Assinatura '{id_assinatura}' não encontrada."
        )
    return dados


def validar_cancelamento(id_assinatura: str, dados: dict, motivo: str | None) -> None:
    """Verifica pré-condições do cancelamento; levanta exceção específica se inválido."""
    if not dados["ativa"]:
        raise AssinaturaJaCanceladaError(
            f"Assinatura '{id_assinatura}' já foi cancelada anteriormente."
        )
    if not motivo or not motivo.strip():
        raise MotivoAusenteError(
            "O motivo do cancelamento é obrigatório e não pode ser vazio."
        )


def calcular_reembolso(dados: dict) -> float:
    """Calcula o reembolso proporcional aos dias restantes do plano."""
    if dados["dias_restantes"] <= 0:
        return 0.0
    total_dias = DIAS_MES if dados["plano"] == "mensal" else DIAS_ANO
    return round(dados["valor"] * (dados["dias_restantes"] / total_dias), 2)


def registrar_cancelamento(id_assinatura: str, motivo: str, reembolso: float) -> None:
    """Persiste o cancelamento no banco em memória."""
    banco_assinaturas[id_assinatura]["ativa"] = False
    cancelamentos_registrados.append({
        "id": id_assinatura,
        "motivo": motivo,
        "reembolso": reembolso,
    })


def cancelar_assinatura(id_assinatura: str, motivo: str | None) -> dict:
    """
    Cancela a assinatura e retorna o resultado com o valor de reembolso.

    Levanta:
        AssinaturaNaoEncontradaError: se o ID não existir.
        AssinaturaJaCanceladaError: se a assinatura já estiver cancelada.
        MotivoAusenteError: se o motivo for None ou vazio.
    """
    dados = buscar_assinatura(id_assinatura)
    validar_cancelamento(id_assinatura, dados, motivo)
    reembolso = calcular_reembolso(dados)
    registrar_cancelamento(id_assinatura, motivo, reembolso)  # type: ignore[arg-type]
    return {"id": id_assinatura, "reembolso": reembolso, "status": "cancelado"}


# ─── Execução de demonstração ─────────────────────────────────────────────────

if __name__ == "__main__":
    tentativas = [
        ("ASS-001", "cliente solicitou"),
        ("ASS-002", "cliente solicitou"),  # já cancelada
        ("ASS-999", "cliente solicitou"),  # não existe
        ("ASS-003", None),                 # motivo ausente
    ]

    print("=== Demonstração: gabarito.py (cancelamento de assinatura) ===")
    print()

    sucessos = []
    falhas = []

    for id_assinatura, motivo in tentativas:
        try:
            resultado = cancelar_assinatura(id_assinatura, motivo)
            sucessos.append(resultado)
        except (AssinaturaNaoEncontradaError, AssinaturaJaCanceladaError, MotivoAusenteError) as erro:
            falhas.append({"id": id_assinatura, "tipo": type(erro).__name__, "erro": str(erro)})

    print(f"Cancelamentos aprovados: {len(sucessos)}")
    for s in sucessos:
        print(f"  [{s['id']}] reembolso R$ {s['reembolso']:.2f} — {s['status']}")

    print()
    print(f"Cancelamentos com falha: {len(falhas)}")
    for f in falhas:
        print(f"  [{f['id']}] {f['tipo']}: {f['erro']}")

    print()
    print("Cada falha agora é visível com tipo específico e mensagem descritiva.")
