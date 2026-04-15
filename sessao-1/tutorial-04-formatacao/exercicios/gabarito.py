"""
GABARITO — Tutorial 04: Formatação
Referência: Clean Code, Cap. 5
Execute: python gabarito.py

Formatação: black --line-length 88 / flake8 --max-line-length 88
Lógica: idêntica ao exercicio.py — apenas formatação alterada.
"""

# ── Stdlib ────────────────────────────────────────────────────────────────────
import json
import math
import os
import sys
from datetime import datetime
from typing import Optional

# ── Constantes ────────────────────────────────────────────────────────────────

STATUS_APROVADO = "aprovado"
STATUS_RECUSADO = "recusado"
STATUS_PENDENTE = "pendente"

TAXA_PROCESSAMENTO = 0.025
LIMITE_DIARIO = 10_000.0
VALOR_MINIMO_PAGAMENTO = 1.0


# ── Classes ───────────────────────────────────────────────────────────────────

class ProcessadorDePagamentos:
    """Processa pagamentos para um comerciante, aplicando validações e taxas."""

    def __init__(self, nome_comerciante: str, limite_diario: float = LIMITE_DIARIO):
        self.nome_comerciante = nome_comerciante
        self.limite_diario = limite_diario
        self._total_processado_hoje: float = 0.0
        self._historico: list[dict] = []
        self._ultima_transacao: Optional[dict] = None

    # ── Operações públicas ─────────────────────────────────────────────────

    def validar_pagamento(
        self,
        valor: float,
        metodo_pagamento: str,
        dados_cartao: Optional[dict] = None,
        cpf_titular: Optional[str] = None,
        descricao: str = "",
    ) -> dict:
        erros = []

        if valor < VALOR_MINIMO_PAGAMENTO:
            erros.append(f"Valor mínimo é R$ {VALOR_MINIMO_PAGAMENTO:.2f}")

        if self._total_processado_hoje + valor > self.limite_diario:
            erros.append(
                f"Limite diário de R$ {self.limite_diario:.2f} seria excedido"
            )

        if metodo_pagamento not in ["credito", "debito", "pix", "boleto"]:
            erros.append(f"Método de pagamento inválido: {metodo_pagamento}")

        if metodo_pagamento in ["credito", "debito"] and not dados_cartao:
            erros.append("Dados do cartão são obrigatórios para pagamento com cartão")

        return {"valido": len(erros) == 0, "erros": erros}

    def processar_pagamento(
        self,
        valor: float,
        metodo_pagamento: str,
        dados_cartao: Optional[dict] = None,
        cpf_titular: Optional[str] = None,
        descricao: str = "",
    ) -> dict:
        validacao = self.validar_pagamento(
            valor, metodo_pagamento, dados_cartao, cpf_titular, descricao
        )

        if not validacao["valido"]:
            return {
                "status": STATUS_RECUSADO,
                "motivos": validacao["erros"],
                "valor": valor,
            }

        taxa = valor * TAXA_PROCESSAMENTO if metodo_pagamento == "credito" else 0.0
        valor_liquido = valor - taxa

        self._total_processado_hoje += valor
        id_transacao = f"TRX-{datetime.now().strftime('%Y%m%d%H%M%S%f')}"

        registro = {
            "id": id_transacao,
            "valor_bruto": valor,
            "taxa": round(taxa, 2),
            "valor_liquido": round(valor_liquido, 2),
            "metodo": metodo_pagamento,
            "status": STATUS_APROVADO,
            "timestamp": datetime.now().isoformat(),
            "descricao": descricao,
        }

        self._historico.append(registro)
        self._ultima_transacao = registro

        return {
            "status": STATUS_APROVADO,
            "transacao_id": id_transacao,
            "valor_liquido": round(valor_liquido, 2),
            "taxa": round(taxa, 2),
        }

    def gerar_comprovante(self, transacao_id: str) -> Optional[str]:
        transacao = next(
            (t for t in self._historico if t["id"] == transacao_id), None
        )

        if not transacao:
            return None

        linhas = [
            "=" * 50,
            "COMPROVANTE DE PAGAMENTO",
            f"Comerciante: {self.nome_comerciante}",
            "=" * 50,
            f"ID Transação : {transacao['id']}",
            f"Data/Hora    : {transacao['timestamp']}",
            f"Método       : {transacao['metodo'].upper()}",
            f"Valor Bruto  : R$ {transacao['valor_bruto']:.2f}",
            f"Taxa         : R$ {transacao['taxa']:.2f}",
            f"Valor Líquido: R$ {transacao['valor_liquido']:.2f}",
            f"Status       : {transacao['status'].upper()}",
            "=" * 50,
        ]

        if transacao["descricao"]:
            linhas.insert(-1, f"Descrição    : {transacao['descricao']}")

        return "\n".join(linhas)

    def obter_resumo_do_dia(self) -> dict:
        return {
            "total_processado": self._total_processado_hoje,
            "numero_transacoes": len(self._historico),
            "total_taxas": self._calcular_total_taxas(),
            "limite_disponivel": self.limite_diario - self._total_processado_hoje,
        }

    # ── Operações privadas ─────────────────────────────────────────────────

    def _calcular_total_taxas(self) -> float:
        return sum(t["taxa"] for t in self._historico)


# ── Execução de demonstração ──────────────────────────────────────────────────

if __name__ == "__main__":
    processador = ProcessadorDePagamentos("Restaurante do Zé", limite_diario=5000.0)

    resultado1 = processador.processar_pagamento(
        150.0,
        "credito",
        dados_cartao={"numero": "****1234"},
        descricao="Almoço executivo",
    )
    print("Transação 1:", resultado1)

    resultado2 = processador.processar_pagamento(
        0.50, "pix", descricao="Teste abaixo do mínimo"
    )
    print("Transação 2 (inválida):", resultado2)

    resultado3 = processador.processar_pagamento(80.0, "pix", descricao="Sobremesa")
    print("Transação 3:", resultado3)

    if resultado1["status"] == STATUS_APROVADO:
        comprovante = processador.gerar_comprovante(resultado1["transacao_id"])
        print("\n" + comprovante)

    print("\nResumo do dia:", processador.obter_resumo_do_dia())
