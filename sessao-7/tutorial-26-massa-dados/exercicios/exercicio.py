"""
EXERCÍCIO 26 — Massa de Dados para Testes
Tempo estimado: 15 minutos

INSTRUÇÕES:
  Os testes abaixo duplicam um literal gigante de NotaFiscal em cada teste,
  mudando só um campo por vez. Extraia um NotaFiscalBuilder com valores
  padrão sensatos e reduza cada teste ao que é relevante.
  Execute: pytest exercicio.py -v
"""


def calcular_imposto(nota_fiscal: dict) -> float:
    return sum(item["valor"] for item in nota_fiscal["itens"]) * nota_fiscal["aliquota"]


def test_calcula_imposto_com_aliquota_padrao():
    nota = {
        "numero": "NF-001",
        "emitente": {"cnpj": "11.111.111/0001-11", "razao_social": "Empresa A"},
        "destinatario": {"cpf": "111.111.111-11", "nome": "Cliente A"},
        "itens": [{"descricao": "Produto X", "valor": 1000.0}],
        "aliquota": 0.18,
        "chave_acesso": "35260100000000000000000000000000000000000000",
    }
    assert calcular_imposto(nota) == 180.0


def test_calcula_imposto_com_aliquota_reduzida():
    nota = {
        "numero": "NF-002",
        "emitente": {"cnpj": "11.111.111/0001-11", "razao_social": "Empresa A"},
        "destinatario": {"cpf": "111.111.111-11", "nome": "Cliente A"},
        "itens": [{"descricao": "Produto X", "valor": 1000.0}],
        "aliquota": 0.12,
        "chave_acesso": "35260100000000000000000000000000000000000001",
    }
    assert calcular_imposto(nota) == 120.0
