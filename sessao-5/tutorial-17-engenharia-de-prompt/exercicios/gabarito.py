"""
Gabarito — Cupom Progressivo (regra de negócio correta)
Referência: Tutorial 09 — Engenharia de contexto e prompt para gerar código
Execute: python3 gabarito.py

Correção aplicada em relação a exercicio.py:
  - determinar_faixa usava `>` (exclusivo) nos limiares de faixa —
    valores exatos de fronteira (R$ 200,00 e R$ 500,00) caíam na faixa abaixo.
  - Correto: `>=` (inclusivo), pois as faixas são definidas como "a partir de".
"""

from dataclasses import dataclass


# ─── Constantes de domínio ────────────────────────────────────────────────────

FAIXA_BRONZE_MIN  =   0.01   # R$ 0,01–199,99 → 5 %
FAIXA_PRATA_MIN   = 200.00   # R$ 200,00–499,99 → 10 %
FAIXA_OURO_MIN    = 500.00   # R$ 500,00+ → 20 %

DESCONTO_BRONZE   = 0.05
DESCONTO_PRATA    = 0.10
DESCONTO_OURO     = 0.20


# ─── Entidade ─────────────────────────────────────────────────────────────────

@dataclass
class ResultadoCupom:
    valor_original:   float
    percentual:       float
    valor_desconto:   float
    valor_final:      float
    faixa:            str


# ─── Lógica de cupom progressivo ─────────────────────────────────────────────

def determinar_faixa(valor: float) -> tuple[str, float]:
    """
    Determina a faixa e o percentual de desconto pelo valor da compra.

    Faixas:
      Bronze: R$ 0,01–R$ 199,99 → 5 %
      Prata:  R$ 200,00–R$ 499,99 → 10 %
      Ouro:   R$ 500,00+ → 20 %
    """
    if valor >= FAIXA_OURO_MIN:    # >= garante que R$500,00 exato entre em "ouro"
        return "ouro", DESCONTO_OURO
    if valor >= FAIXA_PRATA_MIN:   # >= garante que R$200,00 exato entre em "prata"
        return "prata", DESCONTO_PRATA
    if valor >= FAIXA_BRONZE_MIN:
        return "bronze", DESCONTO_BRONZE
    return "sem_faixa", 0.0


def calcular_cupom_progressivo(valor_compra: float) -> ResultadoCupom:
    """
    Calcula o desconto do cupom progressivo para o valor informado.
    Levanta ValueError se o valor for negativo.
    """
    if valor_compra < 0:
        raise ValueError("Valor da compra não pode ser negativo")

    faixa, percentual = determinar_faixa(valor_compra)
    valor_desconto    = valor_compra * percentual
    valor_final       = valor_compra - valor_desconto

    return ResultadoCupom(
        valor_original  = valor_compra,
        percentual      = percentual,
        valor_desconto  = valor_desconto,
        valor_final     = valor_final,
        faixa           = faixa,
    )


def formatar_cupom(resultado: ResultadoCupom) -> str:
    return (
        f"  faixa={resultado.faixa:<10}  "
        f"original=R${resultado.valor_original:>8.2f}  "
        f"desconto={resultado.percentual*100:.0f}%  "
        f"final=R${resultado.valor_final:>8.2f}"
    )


# ─── Execução de demonstração ─────────────────────────────────────────────────

if __name__ == "__main__":
    print("=== Cupom Progressivo (gabarito — regra de negócio correta) ===\n")

    casos = [50.00, 199.99, 200.00, 350.00, 499.99, 500.00, 750.00]

    for valor in casos:
        resultado = calcular_cupom_progressivo(valor)
        print(formatar_cupom(resultado))

    print()
    print("Casos de fronteira (confirmam a correção):")
    for valor in [200.00, 500.00]:
        resultado = calcular_cupom_progressivo(valor)
        print(f"  R${valor:.2f} → faixa={resultado.faixa}, desconto={resultado.percentual*100:.0f}%")
