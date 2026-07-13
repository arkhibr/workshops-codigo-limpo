"""
EXERCÍCIO 24 — Fundamentos de Testes de Unidade
Tempo estimado: 15 minutos

INSTRUÇÕES:
  A suíte abaixo testa calcular_comissao() mas tem 4 problemas:
    1. Nomes que não dizem o que é testado (test1, test2, test_comissao)
    2. Um teste verificando comportamentos não relacionados
    3. Estado global compartilhado entre testes (ordem importa)
    4. Dependência do relógio real (não-determinístico)

  Refatore aplicando AAA, FIRST e nomes comportamentais. Use
  @pytest.mark.parametrize para as variações de valor/meta.
  Execute: pytest exercicio.py -v (deve passar antes e depois da refatoração)
"""
from datetime import datetime

_ultima_comissao = None


def calcular_comissao(valor_venda: float, meta_batida: bool) -> float:
    return valor_venda * 0.08 if meta_batida else valor_venda * 0.03


def test1():
    assert calcular_comissao(1000.0, True) == 80.0
    assert calcular_comissao(1000.0, False) == 30.0


def test2():
    global _ultima_comissao
    _ultima_comissao = calcular_comissao(500.0, True)
    assert _ultima_comissao == 40.0


def test_comissao():
    hoje = datetime.now()
    resultado = calcular_comissao(1000.0, hoje.weekday() == 0)
    assert resultado >= 0
