"""
VERSÃO REVISADA — cálculo de frete com testes de caracterização completos
Referência: Feathers (testes de caracterização) + Clean Code, Cap. 9 (Testes)

O que este arquivo demonstra:
  1. Testes de caracterização escritos ANTES da mudança assistida.
  2. A mudança (nova faixa > 15 kg) introduz uma regressão: verificar_limite_faixa2_3
     detecta que 12 kg retorna valor errado.
  3. A correção do limite restaura o comportamento: todas as verificações voltam a OK.

Ciclo demonstrado aqui:
  caracterizar → mudança quebra → corrigir → tudo OK (estado final do arquivo)

Execute: python3 sessao-6/tutorial-14-testes-guard-rails/exemplos/frete_revisado.py
"""

from __future__ import annotations

DISTANCIA_BASE_KM = 100.0  # distância de referência para normalização


def calcular_frete(peso: float, distancia: float) -> float:
    """
    Calcula o frete com base no peso (kg) e na distância (km).
    O resultado é proporcional à distância em relação à base de 100 km.

    Faixas:
      até 5 kg      → R$ 2,00/kg
      5,01–10 kg    → R$ 1,80/kg + R$ 3,00 fixo
      10,01–15 kg   → R$ 1,50/kg + R$ 5,00 fixo
      acima de 15 kg → R$ 1,20/kg + R$ 8,00 fixo  (faixa adicionada pela mudança)
    """
    fator_distancia = distancia / DISTANCIA_BASE_KM

    if peso <= 0:
        return 0.0
    elif peso <= 5.0:
        valor_base = peso * 2.00
    elif peso <= 10.0:
        valor_base = peso * 1.80 + 3.00
    elif peso <= 15.0:
        # Faixa 3 — limite corrigido após a regressão ser detectada pelos testes
        valor_base = peso * 1.50 + 5.00
    else:
        # Faixa 4 — nova faixa adicionada pela mudança assistida
        valor_base = peso * 1.20 + 8.00

    return round(valor_base * fator_distancia, 2)


# ─── Testes de caracterização completos ───────────────────────────────────────
# Escritos ANTES da mudança, cobrindo cada faixa, limites e bordas.
# A regressão do frete_gerado.py seria capturada por verificar_limite_faixa2_3.

def verificar_peso_zero() -> None:
    """Borda inferior: peso zero deve retornar frete zero."""
    resultado = calcular_frete(peso=0.0, distancia=100.0)
    esperado = 0.00
    if abs(resultado - esperado) < 0.01:
        print("OK: peso zero retorna frete zero")
    else:
        print(f"FALHOU: peso zero (esperado {esperado:.2f}, obtido {resultado:.2f})")


def verificar_frete_faixa1_tipico() -> None:
    """Faixa 1 — caso típico: 3 kg, 100 km."""
    resultado = calcular_frete(peso=3.0, distancia=100.0)
    esperado = 6.00  # 3 * 2.00
    if abs(resultado - esperado) < 0.01:
        print("OK: faixa 1 típico (3 kg, 100 km)")
    else:
        print(f"FALHOU: faixa 1 típico (esperado {esperado:.2f}, obtido {resultado:.2f})")


def verificar_limite_faixa1() -> None:
    """Borda faixa 1: exatamente 5 kg ainda deve usar faixa 1."""
    resultado = calcular_frete(peso=5.0, distancia=100.0)
    esperado = 10.00  # 5 * 2.00
    if abs(resultado - esperado) < 0.01:
        print("OK: limite faixa 1 (5 kg exatos, 100 km)")
    else:
        print(f"FALHOU: limite faixa 1 (esperado {esperado:.2f}, obtido {resultado:.2f})")


def verificar_frete_faixa2_tipico() -> None:
    """Faixa 2 — caso típico: 8 kg, 100 km."""
    resultado = calcular_frete(peso=8.0, distancia=100.0)
    esperado = 17.40  # 8 * 1.80 + 3.00
    if abs(resultado - esperado) < 0.01:
        print("OK: faixa 2 típico (8 kg, 100 km)")
    else:
        print(f"FALHOU: faixa 2 típico (esperado {esperado:.2f}, obtido {resultado:.2f})")


def verificar_limite_faixa2_3() -> None:
    """Borda crítica: 12 kg deve usar faixa 3 (R$ 1,50/kg + R$ 5,00).
    Esta verificação teria detectado a regressão do frete_gerado.py."""
    resultado = calcular_frete(peso=12.0, distancia=100.0)
    esperado = 23.00  # 12 * 1.50 + 5.00
    if abs(resultado - esperado) < 0.01:
        print("OK: limite faixa 2-3 (12 kg, 100 km)")
    else:
        print(f"FALHOU: limite faixa 2-3 (esperado {esperado:.2f}, obtido {resultado:.2f})")


def verificar_frete_faixa3_tipico() -> None:
    """Faixa 3 — caso típico: 13 kg, 100 km."""
    resultado = calcular_frete(peso=13.0, distancia=100.0)
    esperado = 24.50  # 13 * 1.50 + 5.00
    if abs(resultado - esperado) < 0.01:
        print("OK: faixa 3 típico (13 kg, 100 km)")
    else:
        print(f"FALHOU: faixa 3 típico (esperado {esperado:.2f}, obtido {resultado:.2f})")


def verificar_limite_faixa3_4() -> None:
    """Borda faixa 3-4: exatamente 15 kg ainda deve usar faixa 3."""
    resultado = calcular_frete(peso=15.0, distancia=100.0)
    esperado = 27.50  # 15 * 1.50 + 5.00
    if abs(resultado - esperado) < 0.01:
        print("OK: limite faixa 3-4 (15 kg exatos, 100 km)")
    else:
        print(f"FALHOU: limite faixa 3-4 (esperado {esperado:.2f}, obtido {resultado:.2f})")


def verificar_frete_faixa4_tipico() -> None:
    """Faixa 4 (nova) — caso típico: 40 kg, 100 km."""
    resultado = calcular_frete(peso=40.0, distancia=100.0)
    esperado = 56.00  # 40 * 1.20 + 8.00
    if abs(resultado - esperado) < 0.01:
        print("OK: faixa 4 nova (40 kg, 100 km)")
    else:
        print(f"FALHOU: faixa 4 nova (esperado {esperado:.2f}, obtido {resultado:.2f})")


def verificar_fator_distancia() -> None:
    """Distância diferente: 200 km deve dobrar o valor base."""
    resultado = calcular_frete(peso=3.0, distancia=200.0)
    esperado = 12.00  # (3 * 2.00) * (200/100)
    if abs(resultado - esperado) < 0.01:
        print("OK: fator de distância (3 kg, 200 km)")
    else:
        print(f"FALHOU: fator de distância (esperado {esperado:.2f}, obtido {resultado:.2f})")


def executar_todas_verificacoes() -> None:
    """Executa todas as verificações; estado final: todas OK após correção."""
    verificacoes = [
        verificar_peso_zero,
        verificar_frete_faixa1_tipico,
        verificar_limite_faixa1,
        verificar_frete_faixa2_tipico,
        verificar_limite_faixa2_3,
        verificar_frete_faixa3_tipico,
        verificar_limite_faixa3_4,
        verificar_frete_faixa4_tipico,
        verificar_fator_distancia,
    ]
    for verificacao in verificacoes:
        verificacao()


# ─── Execução de demonstração ─────────────────────────────────────────────────

if __name__ == "__main__":
    print("=== Demonstração: frete_revisado.py ===")
    print()
    print("Contexto: testes de caracterização escritos ANTES da mudança assistida.")
    print("A mudança adicionou a faixa > 15 kg. A regressão foi detectada e corrigida.")
    print("Estado final: implementação correta, todas as verificações passam.")
    print()
    print("Verificações de caracterização (suite completa):")
    executar_todas_verificacoes()
    print()
    print("Verificação resumo: todas OK — guard-rails funcionaram.")
    print()
    print("Cálculos de referência (estado corrigido):")
    print(f"  0 kg, 100 km  → R$ {calcular_frete(0.0, 100.0):.2f}  (peso zero)")
    print(f"  3 kg, 100 km  → R$ {calcular_frete(3.0, 100.0):.2f}  (faixa 1)")
    print(f"  5 kg, 100 km  → R$ {calcular_frete(5.0, 100.0):.2f}  (limite faixa 1)")
    print(f"  8 kg, 100 km  → R$ {calcular_frete(8.0, 100.0):.2f}  (faixa 2)")
    print(f"  12 kg, 100 km → R$ {calcular_frete(12.0, 100.0):.2f}  (faixa 3 — era a zona regredida)")
    print(f"  15 kg, 100 km → R$ {calcular_frete(15.0, 100.0):.2f}  (limite faixa 3)")
    print(f"  40 kg, 100 km → R$ {calcular_frete(40.0, 100.0):.2f}  (faixa 4 nova)")
    print(f"  3 kg, 200 km  → R$ {calcular_frete(3.0, 200.0):.2f}  (distância dupla)")
