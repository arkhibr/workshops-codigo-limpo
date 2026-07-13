"""
testes_ruins.py — Testes de unidade mal estruturados sobre desconto e frete.
Execute: pytest testes_ruins.py -v
"""
from datetime import datetime

_ultimo_valor = None  # estado global mutável compartilhado entre testes


def calcular_desconto(valor: float, cliente_vip: bool) -> float:
    return valor * 0.9 if cliente_vip else valor


def calcular_frete(valor: float) -> float:
    return 0.0 if valor > 200 else 25.0


def test1():
    # nome não descreve comportamento; testa desconto e frete juntos
    assert calcular_desconto(100.0, True) == 90.0
    assert calcular_frete(100.0) == 25.0
    assert calcular_desconto(300.0, False) == 300.0


def test2():
    # depende de estado deixado por outro teste — ordem de execução importa
    global _ultimo_valor
    _ultimo_valor = calcular_desconto(50.0, True)
    assert _ultimo_valor == 45.0


def test_desconto():
    # nome genérico; não-determinístico: depende do dia real da execução
    hoje = datetime.now()
    resultado = calcular_desconto(100.0, hoje.weekday() == 0)
    assert resultado >= 0
