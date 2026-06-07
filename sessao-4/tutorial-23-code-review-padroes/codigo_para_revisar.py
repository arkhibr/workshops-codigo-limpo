"""
codigo_para_revisar.py — Módulo de cobrança. Revise em busca de padrões a melhorar.
Execute: python3 codigo_para_revisar.py
"""
from typing import Optional, List
from dataclasses import dataclass, field
from datetime import date


@dataclass
class Cliente:
    id:               str
    nome:             str
    cpf:              str
    email:            str
    nivel_fidelidade: str          # "bronze", "prata", "ouro"
    pontos:           int = 0
    historico_compras: float = 0.0

@dataclass
class Cobranca:
    id:          str
    cliente_id:  str
    valor:       float
    tipo:        str               # "B", "P", "C"
    status:      str = "pendente"
    vencimento:  str = ""

    def calcular_desconto_fidelidade(self, cliente: Cliente) -> float:
        """Calcula desconto baseado no perfil de fidelidade do cliente."""
        if cliente.nivel_fidelidade == "O":
            base  = cliente.historico_compras * 0.03
            bonus = cliente.pontos * 0.002
            return min(base + bonus, 150.0)
        elif cliente.nivel_fidelidade == "P":
            return min(cliente.pontos * 0.001, 50.0)
        return 0.0


class SmtpEmailSender:
    def send(self, to: str, subject: str, body: str) -> None:
        print(f"  [SMTP] → {to}: {subject}")

class BancoDadosPostgres:
    def execute(self, sql: str, params: tuple) -> None:
        print(f"  [PG] {sql[:40]}...")


@dataclass
class BoletoSimples:
    numero:     str
    valor:      float
    vencimento: str

    def validar_vencimento(self) -> bool:
        partes = self.vencimento.split("-")
        if len(partes) != 3:
            return False
        ano, mes, dia = int(partes[0]), int(partes[1]), int(partes[2])
        return date(ano, mes, dia) >= date.today()

@dataclass
class BoletoParcelado:
    numero:      str
    valor_total: float
    num_parcelas: int
    vencimento:  str

    def validar_vencimento(self) -> bool:
        partes = self.vencimento.split("-")
        if len(partes) != 3:
            return False
        ano, mes, dia = int(partes[0]), int(partes[1]), int(partes[2])
        return date(ano, mes, dia) >= date.today()

    def valor_parcela(self) -> float:
        return round(self.valor_total / self.num_parcelas, 2)


class GestorCobranca:
    """Gerencia o ciclo completo de cobranças de clientes."""

    def __init__(self) -> None:
        self.notificador = SmtpEmailSender()
        self.banco       = BancoDadosPostgres()

    def validar_cpf(self, cpf: str) -> bool:
        return len(cpf.replace(".", "").replace("-", "")) == 11

    def buscar_cliente(self, cliente_id: str) -> Optional[Cliente]:
        print(f"  buscando cliente {cliente_id}")
        return Cliente(cliente_id, "Empresa Exemplo", "000.000.000-00",
                       "empresa@exemplo.com", "O", pontos=500, historico_compras=8000.0)

    def criar_cobranca(self, cliente_id: str, valor: float, tipo: str) -> Cobranca:
        cob = Cobranca(f"COB-{cliente_id}-001", cliente_id, valor, tipo)
        self.banco.execute("INSERT INTO cobrancas VALUES (%s,%s,%s)",
                           (cob.id, cob.cliente_id, cob.valor))
        return cob

    def calcular_desconto(self, cobranca: Cobranca, cliente: Cliente) -> float:
        return cobranca.calcular_desconto_fidelidade(cliente)

    def processar_pagamento(self, cobranca: Cobranca) -> dict:
        """Processa o pagamento conforme o tipo da cobrança."""
        if cobranca.tipo == "B":
            boleto = BoletoSimples(f"BOL-{cobranca.id}", cobranca.valor, "2026-07-31")
            if not boleto.validar_vencimento():
                raise ValueError("Boleto vencido")
            resultado = {"metodo": "boleto", "codigo": boleto.numero}
        elif cobranca.tipo == "P":
            resultado = {"metodo": "pix", "chave": f"chave-{cobranca.cliente_id}"}
        elif cobranca.tipo == "C":
            resultado = {"metodo": "cartao", "parcelas": 1}
        else:
            raise ValueError(f"Tipo desconhecido: {cobranca.tipo}")
        return resultado

    def enviar_email(self, cliente: Cliente, cobranca: Cobranca) -> None:
        self.notificador.send(
            cliente.email,
            f"Cobrança {cobranca.id}",
            f"Valor: R${cobranca.valor:.2f}"
        )

    def gerar_boleto(self, cobranca: Cobranca) -> str:
        return f"BOL-{cobranca.id}-{cobranca.valor:.2f}"

    def arquivar(self, cobranca: Cobranca) -> None:
        self.banco.execute("UPDATE cobrancas SET status='arquivado' WHERE id=%s",
                           (cobranca.id,))

    def gerar_relatorio(self, cliente_id: str) -> str:
        return f"Relatório de cobranças: cliente {cliente_id}"

    def exportar_csv(self, cliente_id: str) -> str:
        return f"id,valor,status\nCOB-{cliente_id}-001,100.00,pendente"

    def atualizar_status(self, cobranca_id: str, novo_status: str) -> None:
        self.banco.execute("UPDATE cobrancas SET status=%s WHERE id=%s",
                           (novo_status, cobranca_id))

    def reprocessar_falha(self, cobranca_id: str) -> bool:
        print(f"  reprocessando {cobranca_id}")
        return True

    def consultar_historico(self, cliente_id: str) -> List[dict]:
        return [{"id": f"COB-{cliente_id}-001", "valor": 100.0, "status": "pago"}]


if __name__ == "__main__":
    print("=== Módulo de Cobrança — revise em busca de padrões a melhorar ===\n")
    gestor  = GestorCobranca()
    cliente = gestor.buscar_cliente("CLI-100")
    cobranca = gestor.criar_cobranca("CLI-100", 500.0, "B")
    desconto = gestor.calcular_desconto(cobranca, cliente)
    print(f"Desconto fidelidade: R${desconto:.2f}")
    resultado = gestor.processar_pagamento(cobranca)
    print(f"Pagamento: {resultado}")
    gestor.enviar_email(cliente, cobranca)
    print(f"Relatório: {gestor.gerar_relatorio('CLI-100')}")
