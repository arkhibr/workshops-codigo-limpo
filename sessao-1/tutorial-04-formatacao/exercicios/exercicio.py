"""
EXERCÍCIO — Tutorial 04: Formatação
Referência: Clean Code, Cap. 5
Execute: python exercicio.py

TAREFA: Formate o código abaixo seguindo as convenções do Clean Code e PEP 8
(black --line-length 88). Não altere a lógica — apenas a formatação.

O que corrigir:
  1. Imports desorganizados (ordene: stdlib, depois terceiros, depois locais)
  2. Constantes misturadas com lógica — mova para o topo do módulo
  3. Sem espaços entre operadores e após vírgulas
  4. Linhas muito longas (>88 chars) — quebre com parênteses
  5. Métodos sem linha em branco de separação
  6. Argumentos e lógica num único bloco sem respiração visual
  7. Métodos privados misturados com públicos sem separação clara
"""
import json
import os
from datetime import datetime
import sys
from typing import Optional
import math

STATUS_APROVADO="aprovado"
STATUS_RECUSADO="recusado"
STATUS_PENDENTE="pendente"
TAXA_PROCESSAMENTO=0.025
LIMITE_DIARIO=10000.0
VALOR_MINIMO_PAGAMENTO=1.0

class ProcessadorDePagamentos:
    def __init__(self,nome_comerciante,limite_diario=LIMITE_DIARIO):
        self.nome_comerciante=nome_comerciante
        self.limite_diario=limite_diario
        self._total_processado_hoje=0.0
        self._historico=[]
        self._ultima_transacao=None
    def validar_pagamento(self,valor,metodo_pagamento,dados_cartao=None,cpf_titular=None,descricao=""):
        erros=[]
        if valor<VALOR_MINIMO_PAGAMENTO:
            erros.append(f"Valor mínimo é R$ {VALOR_MINIMO_PAGAMENTO:.2f}")
        if self._total_processado_hoje+valor>self.limite_diario:
            erros.append(f"Limite diário de R$ {self.limite_diario:.2f} seria excedido")
        if metodo_pagamento not in ["credito","debito","pix","boleto"]:
            erros.append(f"Método de pagamento inválido: {metodo_pagamento}")
        if metodo_pagamento in ["credito","debito"] and not dados_cartao:
            erros.append("Dados do cartão são obrigatórios para pagamento com cartão")
        return {"valido":len(erros)==0,"erros":erros}
    def processar_pagamento(self,valor,metodo_pagamento,dados_cartao=None,cpf_titular=None,descricao=""):
        validacao=self.validar_pagamento(valor,metodo_pagamento,dados_cartao,cpf_titular,descricao)
        if not validacao["valido"]:
            return {"status":STATUS_RECUSADO,"motivos":validacao["erros"],"valor":valor}
        taxa=valor*TAXA_PROCESSAMENTO if metodo_pagamento=="credito" else 0.0
        valor_liquido=valor-taxa
        self._total_processado_hoje+=valor
        id_transacao=f"TRX-{datetime.now().strftime('%Y%m%d%H%M%S%f')}"
        registro={"id":id_transacao,"valor_bruto":valor,"taxa":round(taxa,2),"valor_liquido":round(valor_liquido,2),"metodo":metodo_pagamento,"status":STATUS_APROVADO,"timestamp":datetime.now().isoformat(),"descricao":descricao}
        self._historico.append(registro)
        self._ultima_transacao=registro
        return {"status":STATUS_APROVADO,"transacao_id":id_transacao,"valor_liquido":round(valor_liquido,2),"taxa":round(taxa,2)}
    def gerar_comprovante(self,transacao_id):
        transacao=next((t for t in self._historico if t["id"]==transacao_id),None)
        if not transacao:
            return None
        linhas=["="*50,f"COMPROVANTE DE PAGAMENTO",f"Comerciante: {self.nome_comerciante}","="*50,f"ID Transação : {transacao['id']}",f"Data/Hora    : {transacao['timestamp']}",f"Método       : {transacao['metodo'].upper()}",f"Valor Bruto  : R$ {transacao['valor_bruto']:.2f}",f"Taxa         : R$ {transacao['taxa']:.2f}",f"Valor Líquido: R$ {transacao['valor_liquido']:.2f}",f"Status       : {transacao['status'].upper()}","="*50]
        if transacao["descricao"]:
            linhas.insert(-1,f"Descrição    : {transacao['descricao']}")
        return "\n".join(linhas)
    def _calcular_total_taxas(self):
        return sum(t["taxa"] for t in self._historico)
    def obter_resumo_do_dia(self):
        return {"total_processado":self._total_processado_hoje,"numero_transacoes":len(self._historico),"total_taxas":self._calcular_total_taxas(),"limite_disponivel":self.limite_diario-self._total_processado_hoje}


if __name__ == "__main__":
    proc=ProcessadorDePagamentos("Restaurante do Zé",limite_diario=5000.0)
    v1=proc.processar_pagamento(150.0,"credito",dados_cartao={"numero":"****1234"},descricao="Almoço executivo")
    print("Transação 1:",v1)
    v2=proc.processar_pagamento(0.50,"pix",descricao="Teste abaixo do mínimo")
    print("Transação 2 (inválida):",v2)
    v3=proc.processar_pagamento(80.0,"pix",descricao="Sobremesa")
    print("Transação 3:",v3)
    if v1["status"]==STATUS_APROVADO:
        comprovante=proc.gerar_comprovante(v1["transacao_id"])
        print("\n"+comprovante)
    print("\nResumo do dia:",proc.obter_resumo_do_dia())
