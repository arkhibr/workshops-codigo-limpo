"""
EXEMPLOS: Formatação seguindo os princípios do Clean Code
Referência: Clean Code, Cap. 5 — Formatting
Execute: python formatacao_boa.py

Configuração de referência: black --line-length 88 / flake8 --max-line-length 88
"""

# ── Stdlib ────────────────────────────────────────────────────────────────────
import math
import os
import sys
from datetime import datetime
from typing import Optional

# ── Terceiros (nenhum neste módulo) ──────────────────────────────────────────
# import requests

# ── Locais (nenhum neste módulo) ──────────────────────────────────────────────
# from .repositorio import RepositorioDeProdutos

# ── Constantes ────────────────────────────────────────────────────────────────

DESCONTO_PADRAO = 0.05
ALIQUOTA_IMPOSTO_PADRAO = 0.12
CAPACIDADE_MAXIMA_PADRAO = 100


# ── Classes ───────────────────────────────────────────────────────────────────

class GerenciadorDeEstoque:
    """Gerencia o ciclo de vida de produtos em um estoque físico."""

    def __init__(self, nome_loja: str, capacidade_maxima: int = CAPACIDADE_MAXIMA_PADRAO):
        self.nome_loja = nome_loja
        self.capacidade_maxima = capacidade_maxima
        self._produtos: dict = {}
        self._log: list[str] = []
        self._ultima_atualizacao: Optional[str] = None

    # ── Operações públicas ─────────────────────────────────────────────────

    def adicionar_produto(
        self,
        codigo: str,
        nome: str,
        preco: float,
        quantidade: int,
        categoria: str = "geral",
        fornecedor: Optional[str] = None,
        data_validade: Optional[str] = None,
        peso_kg: float = 0.0,
        ativo: bool = True,
    ) -> None:
        self._validar_produto_novo(codigo, preco, quantidade)

        self._produtos[codigo] = {
            "codigo": codigo,
            "nome": nome,
            "preco": preco,
            "quantidade": quantidade,
            "categoria": categoria,
            "fornecedor": fornecedor,
            "data_validade": data_validade,
            "peso_kg": peso_kg,
            "ativo": ativo,
        }
        self._registrar_evento("ADICIONADO", f"{codigo} - {nome} (qtd: {quantidade})")

    def buscar_produto(self, codigo: str) -> Optional[dict]:
        return self._produtos.get(codigo)

    def remover_produto(self, codigo: str, motivo: str = "não informado") -> dict:
        if codigo not in self._produtos:
            raise KeyError(f"Produto {codigo} não encontrado")

        produto = self._produtos.pop(codigo)
        self._registrar_evento("REMOVIDO", f"{codigo} - {produto['nome']} (motivo: {motivo})")
        return produto

    def calcular_valor_total_estoque(
        self,
        apenas_ativos: bool = True,
        aplicar_desconto: bool = False,
        percentual_desconto: float = DESCONTO_PADRAO,
        incluir_impostos: bool = False,
        aliquota_imposto: float = ALIQUOTA_IMPOSTO_PADRAO,
    ) -> float:
        total = 0.0

        for produto in self._produtos.values():
            if apenas_ativos and not produto["ativo"]:
                continue

            valor_item = produto["preco"] * produto["quantidade"]

            if aplicar_desconto:
                valor_item *= 1 - percentual_desconto

            if incluir_impostos:
                valor_item *= 1 + aliquota_imposto

            total += valor_item

        return round(total, 2)

    def listar_produtos(self, apenas_ativos: bool = True) -> list[dict]:
        return [
            produto
            for produto in self._produtos.values()
            if not apenas_ativos or produto["ativo"]
        ]

    def exportar_log(self) -> list[str]:
        return list(self._log)

    # ── Operações privadas ─────────────────────────────────────────────────

    def _validar_produto_novo(self, codigo: str, preco: float, quantidade: int) -> None:
        if codigo in self._produtos:
            raise ValueError(f"Produto {codigo} já existe no estoque")
        if preco <= 0:
            raise ValueError("Preço deve ser positivo")
        if quantidade < 0:
            raise ValueError("Quantidade não pode ser negativa")
        if len(self._produtos) >= self.capacidade_maxima:
            raise RuntimeError(
                f"Estoque cheio. Capacidade máxima: {self.capacidade_maxima}"
            )

    def _registrar_evento(self, tipo: str, descricao: str) -> None:
        entrada = f"{datetime.now().isoformat()} [{tipo}] {descricao}"
        self._log.append(entrada)
        self._ultima_atualizacao = datetime.now().isoformat()


# ── Execução de demonstração ──────────────────────────────────────────────────

if __name__ == "__main__":
    gerenciador = GerenciadorDeEstoque("Loja Central", capacidade_maxima=50)

    gerenciador.adicionar_produto(
        codigo="C001",
        nome="Café Especial",
        preco=45.90,
        quantidade=100,
        categoria="bebidas",
        fornecedor="Fazenda Boa Vista",
        data_validade="2026-12-31",
        peso_kg=0.5,
    )
    gerenciador.adicionar_produto("A001", "Açúcar Cristal", 3.50, 200, "alimentos")
    gerenciador.adicionar_produto("C002", "Chá Verde", 12.00, 50, "bebidas")

    print("Produto C001:", gerenciador.buscar_produto("C001"))
    print("Valor total (sem desconto):", gerenciador.calcular_valor_total_estoque())
    print("Valor total (com desconto 5%):", gerenciador.calcular_valor_total_estoque(aplicar_desconto=True))
    print("Valor total (com imposto 12%):", gerenciador.calcular_valor_total_estoque(incluir_impostos=True))

    removido = gerenciador.remover_produto("C002", motivo="produto vencendo")
    print("Removido:", removido["nome"])
    print("Produtos restantes:", len(gerenciador.listar_produtos()))
    print("Log:", gerenciador.exportar_log())
