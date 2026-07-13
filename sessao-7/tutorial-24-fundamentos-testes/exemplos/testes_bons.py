"""
testes_bons.py — Testes de unidade com AAA, FIRST e nomes comportamentais.
Execute: pytest testes_bons.py -v
"""
import pytest


def calcular_desconto(valor: float, cliente_vip: bool) -> float:
    return valor * 0.9 if cliente_vip else valor


def calcular_frete(valor: float) -> float:
    return 0.0 if valor > 200 else 25.0


class TestCalcularDesconto:
    """Cada teste é rápido, independente e determinístico (F, I, R do FIRST)."""

    def test_aplica_10_porcento_para_cliente_vip(self):
        # Arrange
        valor = 100.0
        # Act
        resultado = calcular_desconto(valor, cliente_vip=True)
        # Assert
        assert resultado == 90.0

    def test_nao_aplica_desconto_para_cliente_comum(self):
        resultado = calcular_desconto(100.0, cliente_vip=False)
        assert resultado == 100.0

    @pytest.mark.parametrize("valor,vip,esperado", [
        (0.0, True, 0.0),
        (100.0, False, 100.0),
        (200.0, True, 180.0),
    ])
    def test_calcula_desconto_para_varios_valores(self, valor, vip, esperado):
        assert calcular_desconto(valor, vip) == esperado


class TestCalcularFrete:
    def test_frete_gratis_acima_de_200(self):
        assert calcular_frete(201.0) == 0.0

    def test_cobra_frete_fixo_ate_200(self):
        assert calcular_frete(200.0) == 25.0
