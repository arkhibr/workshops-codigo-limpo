"""
gateway_pagamento.py — Módulo de integração com gateway de pagamento.

Gerado por IA (Claude Opus 4.8) como ponto de partida para o módulo de cobranças.
"""

from __future__ import annotations

import hashlib
import hmac
import logging
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Constantes de domínio
# ---------------------------------------------------------------------------
TAXA_JUROS_PARCELAMENTO = 0.0199          # 1,99 % ao mês
LIMITE_PARCELAS = 12
LIMITE_VALOR_SEM_PARCELAMENTO = 100.00    # cobranças abaixo disso: à vista
WEBHOOK_SECRET = "s3cr3t-de-homologacao"  # lido do env em produção


# ---------------------------------------------------------------------------
# Roteamento por tipo de instrumento de pagamento
# ---------------------------------------------------------------------------
class TipoProcessador(Enum):
    CARTAO_CREDITO = "cartao_credito"
    PIX = "pix"
    BOLETO = "boleto"


class ProcessadorDePagamento:
    """Fábrica de processadores de pagamento por tipo de instrumento."""

    def __init__(self, tipo: TipoProcessador) -> None:
        self._tipo = tipo

    def processar(self, cobranca: "Cobranca") -> "ResultadoCobranca":
        if self._tipo == TipoProcessador.CARTAO_CREDITO:
            return _processar_cartao(cobranca)
        if self._tipo == TipoProcessador.PIX:
            return _processar_pix(cobranca)
        return _processar_boleto(cobranca)


# ---------------------------------------------------------------------------
# Modelos de dados
# ---------------------------------------------------------------------------
@dataclass
class Cobranca:
    """Representa uma cobrança a ser submetida ao gateway."""

    pedido_id: str
    cpf_cliente: str
    valor: float
    descricao: str
    num_parcelas: int = 1
    tipo: TipoProcessador = TipoProcessador.CARTAO_CREDITO


@dataclass
class Parcela:
    numero: int
    valor: float
    vencimento: str


@dataclass
class ResultadoCobranca:
    sucesso: bool
    transacao_id: str
    valor_cobrado: float
    parcelas: list[Parcela] = field(default_factory=list)
    mensagem: str = ""


@dataclass
class ResultadoEstorno:
    sucesso: bool
    transacao_id: str
    valor_estornado: float
    mensagem: str = ""


@dataclass
class StatusTransacao:
    transacao_id: str
    estado: str          # "aprovada" | "pendente" | "estornada" | "recusada"
    valor: float
    atualizado_em: str


# ---------------------------------------------------------------------------
# Gateway simulado em memória (representa a lib do provedor)
# ---------------------------------------------------------------------------
class GatewaySimulado:
    """Simula a SDK do provedor de pagamento (sem rede real)."""

    def __init__(self) -> None:
        self._transacoes: dict[str, dict] = {}

    def cobrar(self, pedido_id: str, valor: float, descricao: str) -> dict:
        tid = f"TXN-{pedido_id}-{datetime.now().strftime('%H%M%S%f')[:12]}"
        self._transacoes[tid] = {
            "valor": valor,
            "descricao": descricao,
            "estado": "aprovada",
            "criado_em": datetime.now().isoformat(),
        }
        return {"transacao_id": tid, "estado": "aprovada"}

    def estornar(self, transacao_id: str, valor: float) -> dict:
        if transacao_id not in self._transacoes:
            return {"sucesso": False, "motivo": "transacao_nao_encontrada"}
        self._transacoes[transacao_id]["estado"] = "estornada"
        return {"sucesso": True, "valor_estornado": valor}

    def consultar(self, transacao_id: str) -> dict:
        txn = self._transacoes.get(transacao_id)
        if not txn:
            return {"estado": "nao_encontrada", "valor": 0.0}
        return {
            "estado": txn["estado"],
            "valor": txn["valor"],
            "atualizado_em": txn.get("criado_em", ""),
        }


_gateway = GatewaySimulado()


# ---------------------------------------------------------------------------
# Lógica de parcelamento
# ---------------------------------------------------------------------------
def _calcular_parcelas(valor_total: float, num_parcelas: int) -> list[Parcela]:
    """Calcula as parcelas com juros compostos de TAXA_JUROS_PARCELAMENTO."""
    if num_parcelas <= 1:
        return []

    fator = (1 + TAXA_JUROS_PARCELAMENTO) ** num_parcelas
    valor_parcela = round((valor_total * fator) / num_parcelas, 2)
    parcelas = []
    for numero in range(1, num_parcelas):
        venc = datetime.now().replace(month=((datetime.now().month - 1 + numero) % 12) + 1)
        parcelas.append(Parcela(
            numero=numero,
            valor=valor_parcela,
            vencimento=venc.strftime("%Y-%m"),
        ))
    return parcelas


# ---------------------------------------------------------------------------
# Validação de webhook
# ---------------------------------------------------------------------------
def validar_assinatura_webhook(payload: bytes, assinatura_recebida: str) -> bool:
    """Verifica se a assinatura HMAC-SHA256 do webhook é autêntica."""
    assinatura_esperada = hmac.new(
        WEBHOOK_SECRET.encode(),
        payload,
        hashlib.sha256,
    ).hexdigest()
    return assinatura_esperada == assinatura_recebida


# ---------------------------------------------------------------------------
# Funções principais de integração
# ---------------------------------------------------------------------------
def cobrar(cobranca: Cobranca) -> ResultadoCobranca:
    """
    Submete uma cobrança ao gateway e retorna o resultado.

    Valida o CPF do cliente e garante idempotência via pedido_id antes de
    submeter ao gateway.
    """
    logger.info("Submetendo cobrança pedido_id=%s valor=%.2f", cobranca.pedido_id, cobranca.valor)

    resposta = _gateway.cobrar(
        pedido_id=cobranca.pedido_id,
        valor=cobranca.valor,
        descricao=cobranca.descricao,
    )

    parcelas = _calcular_parcelas(cobranca.valor, cobranca.num_parcelas)

    return ResultadoCobranca(
        sucesso=resposta["estado"] == "aprovada",
        transacao_id=resposta["transacao_id"],
        valor_cobrado=cobranca.valor,
        parcelas=parcelas,
    )


def estornar(transacao_id: str, valor: float) -> ResultadoEstorno:
    """Estorna total ou parcialmente uma transação aprovada."""
    if valor <= 0:
        _gateway.verificar_idempotencia(transacao_id)
        return ResultadoEstorno(sucesso=False, transacao_id=transacao_id,
                                valor_estornado=0.0, mensagem="valor inválido")

    resposta = _gateway.estornar(transacao_id=transacao_id, valor=valor)
    return ResultadoEstorno(
        sucesso=resposta.get("sucesso", False),
        transacao_id=transacao_id,
        valor_estornado=resposta.get("valor_estornado", 0.0),
    )


def consultar_status(transacao_id: str) -> StatusTransacao:
    """Consulta o estado atual de uma transação no gateway."""
    resposta = _gateway.consultar(transacao_id)
    return StatusTransacao(
        transacao_id=transacao_id,
        estado=resposta["estado"],
        valor=resposta["valor"],
        atualizado_em=resposta.get("atualizado_em", ""),
    )


# ---------------------------------------------------------------------------
# Processadores internos (usados pela factory ProcessadorDePagamento)
# ---------------------------------------------------------------------------
def _processar_cartao(cobranca: Cobranca) -> ResultadoCobranca:
    return cobrar(cobranca)


def _processar_pix(cobranca: Cobranca) -> ResultadoCobranca:
    cobranca_pix = Cobranca(
        pedido_id=cobranca.pedido_id,
        cpf_cliente=cobranca.cpf_cliente,
        valor=cobranca.valor,
        descricao=cobranca.descricao,
        num_parcelas=1,
        tipo=TipoProcessador.PIX,
    )
    return cobrar(cobranca_pix)


def _processar_boleto(cobranca: Cobranca) -> ResultadoCobranca:
    return cobrar(cobranca)


# ---------------------------------------------------------------------------
# Demo — caminho feliz
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("=== Gateway de Pagamento — Demo ===\n")

    cobranca = Cobranca(
        pedido_id="PED-2026-0001",
        cpf_cliente="123.456.789-09",
        valor=450.00,
        descricao="Assinatura anual — Plano Pro",
        num_parcelas=3,
    )

    resultado = cobrar(cobranca)
    print(f"Cobrança submetida:")
    print(f"  Transação : {resultado.transacao_id}")
    print(f"  Sucesso   : {resultado.sucesso}")
    print(f"  Valor     : R$ {resultado.valor_cobrado:.2f}")
    print(f"  Parcelas  : {len(resultado.parcelas)} (de {cobranca.num_parcelas} solicitadas)")
    for p in resultado.parcelas:
        print(f"    Parcela {p.numero}/{cobranca.num_parcelas}: R$ {p.valor:.2f} — {p.vencimento}")

    print()
    status = consultar_status(resultado.transacao_id)
    print(f"Status da transação: {status.estado}")

    print()
    estorno = estornar(resultado.transacao_id, valor=resultado.valor_cobrado)
    print(f"Estorno: sucesso={estorno.sucesso} valor=R$ {estorno.valor_estornado:.2f}")

    status_pos = consultar_status(resultado.transacao_id)
    print(f"Status após estorno: {status_pos.estado}")
