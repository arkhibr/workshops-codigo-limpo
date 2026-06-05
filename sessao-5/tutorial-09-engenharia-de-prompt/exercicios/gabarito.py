"""
GABARITO — Cupom de desconto progressivo (versão aderente ao prompt estruturado)
Referência: Clean Code, Cap. 2–3; engenharia de contexto em prompts de código

Problemas corrigidos em relação ao exercício:
  - Nomes descritivos em português para todos os identificadores
  - Estrutura de dados tipada substituindo dict solto
  - Números mágicos extraídos como constantes nomeadas
  - Regras de desconto separadas em funções próprias
  - Falha silenciosa substituída por exceção descritiva
  - Funções com nomes que revelam intenção no domínio

Execute: python3 sessao-5/tutorial-09-engenharia-de-prompt/exercicios/gabarito.py
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

MULTIPLICADOR_PROGRESSIVO = 1.5   # bônus de desconto para compras acima do limiar
LIMIAR_DESCONTO_PROGRESSIVO = 200.0  # valor mínimo para ativar o desconto progressivo
PRECO_MINIMO = 0.0               # preço final nunca pode ser negativo


class TipoCupom(Enum):
    PERCENTUAL = "percentual"
    VALOR_FIXO = "valor_fixo"


@dataclass
class Cupom:
    codigo: str
    tipo: TipoCupom
    valor: float  # percentual (0–1) ou valor fixo em reais


_cupons_cadastrados: dict[str, Cupom] = {}


def _calcular_desconto_percentual(cupom: Cupom, valor_compra: float) -> float:
    """Retorna o desconto em reais, com bônus progressivo para compras acima do limiar."""
    if valor_compra >= LIMIAR_DESCONTO_PROGRESSIVO:
        return valor_compra * cupom.valor * MULTIPLICADOR_PROGRESSIVO
    return valor_compra * cupom.valor


def _calcular_desconto_fixo(cupom: Cupom, valor_compra: float) -> float:
    """Retorna o desconto em reais limitado ao valor da compra."""
    return min(cupom.valor, valor_compra)


def _calcular_desconto(cupom: Cupom, valor_compra: float) -> float:
    """Despacha o cálculo de desconto conforme o tipo do cupom."""
    if cupom.tipo == TipoCupom.PERCENTUAL:
        return _calcular_desconto_percentual(cupom, valor_compra)
    return _calcular_desconto_fixo(cupom, valor_compra)


def aplicar_cupom(codigo: str, valor_compra: float) -> float:
    """
    Aplica o cupom ao valor da compra e retorna o preço final.

    Lança ValueError se o cupom não estiver cadastrado.
    """
    if codigo not in _cupons_cadastrados:
        raise ValueError(f"Cupom '{codigo}' não encontrado.")

    cupom = _cupons_cadastrados[codigo]
    desconto = _calcular_desconto(cupom, valor_compra)
    return round(max(valor_compra - desconto, PRECO_MINIMO), 2)


def cadastrar_cupom(codigo: str, tipo: TipoCupom, valor: float) -> None:
    """Cadastra um novo cupom no repositório em memória."""
    _cupons_cadastrados[codigo] = Cupom(codigo=codigo, tipo=tipo, valor=valor)


def remover_cupom(codigo: str) -> None:
    """
    Remove o cupom do repositório.

    Lança ValueError se o cupom não estiver cadastrado.
    """
    if codigo not in _cupons_cadastrados:
        raise ValueError(f"Cupom '{codigo}' não encontrado para remoção.")
    del _cupons_cadastrados[codigo]


def exibir_cupons_cadastrados() -> None:
    """Exibe todos os cupons cadastrados com seus detalhes."""
    for cupom in _cupons_cadastrados.values():
        valor_display = f"{cupom.valor * 100:.0f}%" if cupom.tipo == TipoCupom.PERCENTUAL else f"R${cupom.valor:.2f}"
        print(f"  [{cupom.codigo}] {cupom.tipo.value}: {valor_display}")


# ─── Execução de demonstração ─────────────────────────────────────────────────

if __name__ == "__main__":
    cadastrar_cupom("VERAO10", TipoCupom.PERCENTUAL, 0.10)
    cadastrar_cupom("FRETE", TipoCupom.VALOR_FIXO, 15.0)
    cadastrar_cupom("VIP20", TipoCupom.PERCENTUAL, 0.20)

    print("=== Cupons cadastrados ===")
    exibir_cupons_cadastrados()

    print("\n--- Aplicando cupons ---")
    # compra de R$ 150 com cupom percentual (sem bônus progressivo)
    print("Compra R$150 + VERAO10:", aplicar_cupom("VERAO10", 150.0))

    # compra de R$ 300 com cupom percentual (com bônus progressivo)
    print("Compra R$300 + VERAO10:", aplicar_cupom("VERAO10", 300.0))

    # cupom de valor fixo
    print("Compra R$50 + FRETE:", aplicar_cupom("FRETE", 50.0))

    # cupom inexistente — deve lançar exceção
    try:
        aplicar_cupom("INVALIDO", 100.0)
    except ValueError as erro:
        print(f"Erro esperado: {erro}")
