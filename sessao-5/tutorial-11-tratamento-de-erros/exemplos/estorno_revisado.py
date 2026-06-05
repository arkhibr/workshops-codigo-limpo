"""
VERSÃO REVISADA — processamento de estornos com tratamento de erro explícito
Referência: Clean Code, Cap. 7 (Error Handling)

Problemas corrigidos em relação à versão gerada:
  - except Exception: pass substituído por exceções específicas nomeadas
  - EstornoInvalidoError: campo obrigatório ausente ou tipo incorreto
  - ValorEstornoExcedidoError: valor do estorno excede o original
  - Mensagens de erro incluem os valores que causaram o problema
  - Falhas são propagadas — o chamador decide o que fazer

Execute: python3 sessao-5/tutorial-11-tratamento-de-erros/exemplos/estorno_revisado.py
"""

from __future__ import annotations


class EstornoInvalidoError(Exception):
    """Levantada quando os dados do estorno estão incompletos ou malformados."""


class ValorEstornoExcedidoError(Exception):
    """Levantada quando o valor do estorno excede o valor original da compra."""


def validar_campos_estorno(estorno: dict) -> None:
    """Verifica se os campos obrigatórios estão presentes e com tipos corretos."""
    for campo in ("id", "valor", "valor_original"):
        if campo not in estorno:
            raise EstornoInvalidoError(
                f"Campo obrigatório ausente no estorno: '{campo}'."
            )
    if not isinstance(estorno["valor"], (int, float)):
        raise EstornoInvalidoError(
            f"Campo 'valor' deve ser numérico; recebido: {type(estorno['valor']).__name__}."
        )
    if estorno["valor"] <= 0:
        raise EstornoInvalidoError(
            f"Campo 'valor' deve ser positivo; recebido: {estorno['valor']:.2f}."
        )


def verificar_limite_estorno(valor: float, valor_original: float) -> None:
    """Verifica se o valor do estorno não excede o valor original da compra."""
    if valor > valor_original:
        raise ValorEstornoExcedidoError(
            f"Estorno de R$ {valor:.2f} excede o valor original de R$ {valor_original:.2f}."
        )


def processar_estorno(estorno: dict) -> dict:
    """
    Processa um estorno após validação completa.

    Levanta:
        EstornoInvalidoError: se campos obrigatórios estiverem ausentes ou inválidos.
        ValorEstornoExcedidoError: se o valor exceder o original.
    """
    validar_campos_estorno(estorno)
    verificar_limite_estorno(estorno["valor"], estorno["valor_original"])
    return {
        "id": estorno["id"],
        "status": "aprovado",
        "valor": estorno["valor"],
    }


# ─── Execução de demonstração ─────────────────────────────────────────────────

if __name__ == "__main__":
    estornos = [
        {"id": "EST-001", "valor": 150.00, "valor_original": 300.00},
        {"id": "EST-002", "valor": 80.00},                            # campo ausente
        {"id": "EST-003", "valor": 500.00, "valor_original": 300.00}, # excede original
    ]

    print("=== Demonstração: estorno_revisado.py ===")
    print()

    sucessos = []
    falhas = []

    for estorno in estornos:
        try:
            resultado = processar_estorno(estorno)
            sucessos.append(resultado)
        except (EstornoInvalidoError, ValorEstornoExcedidoError) as erro:
            falhas.append({"id": estorno.get("id", "?"), "erro": str(erro)})

    print(f"Estornos aprovados: {len(sucessos)}")
    for s in sucessos:
        print(f"  [{s['id']}] R$ {s['valor']:.2f} — {s['status']}")

    print()
    print(f"Estornos com falha: {len(falhas)}")
    for f in falhas:
        print(f"  [{f['id']}] {f['erro']}")

    print()
    print("Cada falha agora é visível com tipo e mensagem descritiva.")
