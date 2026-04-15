"""
EXEMPLOS: Formatação que viola os princípios do Clean Code
Referência: Clean Code, Cap. 5 — Formatting
Execute: python formatacao_ruim.py
"""
import os
import json
from datetime import datetime
import sys
from typing import Optional
import math

LIMITE_ITENS=100
DESCONTO_PADRAO=0.05
TAX_RATE=0.12
MAX_NOME_LENGTH=200
_DB_HOST="localhost"

class GerenciadorDeEstoque:
    def __init__(self,nome_loja,capacidade_maxima):
        self.nome_loja=nome_loja
        self.capacidade_maxima=capacidade_maxima
        self._produtos={}
        self._log=[]
        self._ultima_atualizacao=None
    def adicionar_produto(self,codigo,nome,preco,quantidade,categoria="geral",fornecedor=None,data_validade=None,peso_kg=0.0,ativo=True):
        if codigo in self._produtos:
            raise ValueError(f"Produto {codigo} já existe no estoque")
        if preco<=0:
            raise ValueError("Preço deve ser positivo")
        if quantidade<0:
            raise ValueError("Quantidade não pode ser negativa")
        if len(self._produtos)>=self.capacidade_maxima:
            raise RuntimeError(f"Estoque cheio. Capacidade máxima: {self.capacidade_maxima}")
        self._produtos[codigo]={"codigo":codigo,"nome":nome,"preco":preco,"quantidade":quantidade,"categoria":categoria,"fornecedor":fornecedor,"data_validade":data_validade,"peso_kg":peso_kg,"ativo":ativo}
        self._ultima_atualizacao=datetime.now().isoformat()
        self._log.append(f"ADICIONADO: {codigo} - {nome} (qtd: {quantidade})")
    def buscar_produto(self,codigo):
        if codigo not in self._produtos:
            return None
        return self._produtos[codigo]
    def remover_produto(self,codigo,motivo="não informado"):
        if codigo not in self._produtos:
            raise KeyError(f"Produto {codigo} não encontrado")
        produto=self._produtos.pop(codigo)
        self._ultima_atualizacao=datetime.now().isoformat()
        self._log.append(f"REMOVIDO: {codigo} - {produto['nome']} (motivo: {motivo})")
        return produto
    def calcular_valor_total_estoque(self,apenas_ativos=True,aplicar_desconto=False,percentual_desconto=DESCONTO_PADRAO,incluir_impostos=False,aliquota_imposto=TAX_RATE):
        total=0.0
        for codigo,produto in self._produtos.items():
            if apenas_ativos and not produto["ativo"]:
                continue
            valor_item=produto["preco"]*produto["quantidade"]
            if aplicar_desconto:
                valor_item=valor_item*(1-percentual_desconto)
            if incluir_impostos:
                valor_item=valor_item*(1+aliquota_imposto)
            total+=valor_item
        return round(total,2)
    def listar_produtos(self,apenas_ativos=True):
        return [p for p in self._produtos.values() if not apenas_ativos or p["ativo"]]
    def _registrar_evento(self,tipo,descricao):
        self._log.append(f"{datetime.now().isoformat()} [{tipo}] {descricao}")
    def exportar_log(self):
        return list(self._log)


if __name__ == "__main__":
    g=GerenciadorDeEstoque("Loja Central",50)
    g.adicionar_produto("C001","Café Especial",45.90,100,"bebidas","Fazenda Boa Vista","2026-12-31",0.5)
    g.adicionar_produto("A001","Açúcar Cristal",3.50,200,"alimentos")
    g.adicionar_produto("C002","Chá Verde",12.00,50,"bebidas")
    print("Produto C001:",g.buscar_produto("C001"))
    print("Valor total (sem desconto):",g.calcular_valor_total_estoque())
    print("Valor total (com desconto 5%):",g.calcular_valor_total_estoque(aplicar_desconto=True))
    print("Valor total (com imposto 12%):",g.calcular_valor_total_estoque(incluir_impostos=True))
    removido=g.remover_produto("C002","produto vencendo")
    print("Removido:",removido["nome"])
    print("Produtos restantes:",len(g.listar_produtos()))
    print("Log:",g.exportar_log())
