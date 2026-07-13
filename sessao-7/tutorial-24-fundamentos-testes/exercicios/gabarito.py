"""
GABARITO 24 — Fundamentos de Testes de Unidade
Suíte refatorada: AAA explícito, nomes comportamentais, sem estado
compartilhado, sem dependência do relógio real.
Execute: pytest gabarito.py -v
"""
import pytest


def calcular_comissao(valor_venda: float, meta_batida: bool) -> float:
    return valor_venda * 0.08 if meta_batida else valor_venda * 0.03


class TestCalcularComissao:
    """Cada teste é rápido, independente e determinístico (F, I, R do FIRST)."""

    def test_paga_8_porcento_quando_bate_meta(self):
        # Arrange
        valor_venda = 1000.0
        # Act
        resultado = calcular_comissao(valor_venda, meta_batida=True)
        # Assert
        assert resultado == 80.0

    def test_paga_3_porcento_quando_nao_bate_meta(self):
        resultado = calcular_comissao(1000.0, meta_batida=False)
        assert resultado == 30.0

    @pytest.mark.parametrize("valor_venda,meta_batida,esperado", [
        (0.0, True, 0.0),
        (0.0, False, 0.0),
        (500.0, True, 40.0),
        (500.0, False, 15.0),
        (10_000.0, True, 800.0),
    ])
    def test_calcula_comissao_para_varios_valores(self, valor_venda, meta_batida, esperado):
        assert calcular_comissao(valor_venda, meta_batida) == esperado
