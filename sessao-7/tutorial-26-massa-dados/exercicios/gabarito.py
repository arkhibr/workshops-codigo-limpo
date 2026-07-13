"""
GABARITO 26 — Massa de Dados para Testes
Test Data Builder: NotaFiscalBuilder centraliza valores padrão sensatos
(emitente, destinatario, item e aliquota fixos) e expõe com_item(descricao,
valor) e com_aliquota(valor) para sobrescrever só o que cada teste precisa.
Os dois testes ficam reduzidos a poucas linhas, declarando apenas a alíquota
que varia entre eles.
Execute: pytest gabarito.py -v
"""
from dataclasses import dataclass, field


@dataclass
class NotaFiscal:
    numero: str = "NF-000"
    emitente: dict = field(default_factory=lambda: {"cnpj": "11.111.111/0001-11", "razao_social": "Empresa A"})
    destinatario: dict = field(default_factory=lambda: {"cpf": "111.111.111-11", "nome": "Cliente A"})
    itens: list = field(default_factory=lambda: [{"descricao": "Produto X", "valor": 1000.0}])
    aliquota: float = 0.18
    chave_acesso: str = "35260100000000000000000000000000000000000000"


class NotaFiscalBuilder:
    """Test Data Builder: valores padrão sensatos, sobrescreve só o relevante."""

    def __init__(self):
        self._nota = NotaFiscal()

    def com_item(self, descricao: str, valor: float) -> "NotaFiscalBuilder":
        self._nota.itens = [{"descricao": descricao, "valor": valor}]
        return self

    def com_aliquota(self, valor: float) -> "NotaFiscalBuilder":
        self._nota.aliquota = valor
        return self

    def construir(self) -> NotaFiscal:
        return self._nota


def calcular_imposto(nota_fiscal: NotaFiscal) -> float:
    return sum(item["valor"] for item in nota_fiscal.itens) * nota_fiscal.aliquota


def test_calcula_imposto_com_aliquota_padrao():
    nota = NotaFiscalBuilder().com_item("Produto X", valor=1000.0).construir()
    assert calcular_imposto(nota) == 180.0


def test_calcula_imposto_com_aliquota_reduzida():
    nota = NotaFiscalBuilder().com_item("Produto X", valor=1000.0).com_aliquota(0.12).construir()
    assert calcular_imposto(nota) == 120.0
