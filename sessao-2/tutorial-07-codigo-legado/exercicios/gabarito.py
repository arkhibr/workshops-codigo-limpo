# ============================================================================
# GABARITO — Tutorial 07: Código Legado
# Execute: python3 gabarito.py
#
# Quatro passos aplicados em sequência sobre o código original:
#   Passo 1: testes de caracterização escritos e validados
#   Passo 2: smells anotados no código
#   Passo 3: magic numbers → constantes; s/r/t/m → nomes descritivos
#   Passo 4: _cache para instância; batch_calc chama calc_comm
# ============================================================================

# ── Passo 3: constantes nomeadas (substituem os magic numbers) ───────────────

ALIQUOTA_SR_META_ATINGIDA  = 0.08
ALIQUOTA_SR_BONUS          = 0.03
ALIQUOTA_SR_PARCIAL        = 0.05
ALIQUOTA_SR_ABAIXO         = 0.03

ALIQUOTA_JR_META_ATINGIDA  = 0.05
ALIQUOTA_JR_BONUS          = 0.02
ALIQUOTA_JR_ABAIXO         = 0.03

MULTIPLICADOR_AGR          = 1.1
MULTIPLICADOR_BONUS_META   = 1.2
MULTIPLICADOR_PARCIAL_META = 0.8
RECEITA_MINIMA             = 5000.0

# Tabela de vendedores (simulando banco de dados)
_vendedores = {
    "V001": {"nome": "Ana Paula",   "tipo": "SR", "regiao": "SP"},
    "V002": {"nome": "Carlos Lima", "tipo": "JR", "regiao": "RJ"},
    "V003": {"nome": "Maria Costa", "tipo": "SR", "regiao": "MG"},
}


class CommissionCalc:
    # Passo 2 — smells identificados:
    # SMELL: parâmetros s, r, t, m obscuros → renomeados no Passo 3
    # SMELL: magic numbers (0.08, 0.05, 0.03 etc.) → constantes no Passo 3
    # SMELL: _cache global modificado dentro de método → movido para instância no Passo 4
    # SMELL: lógica idêntica duplicada em batch_calc → eliminada no Passo 4
    # SMELL: comentário "atualizado em jan/2020" desatualizado

    # Passo 4: cache movido de variável global para instância
    def __init__(self) -> None:
        self._cache: dict = {}

    def calc_comm(self, vendedor_id: str, receita: float, tipo_meta: str, meta: float) -> float:
        # Passo 3: s, r, t, m → vendedor_id, receita, tipo_meta, meta
        if vendedor_id in self._cache:      # Passo 4: self._cache em vez de _cache global
            return self._cache[vendedor_id]

        v = _vendedores.get(vendedor_id)
        if not v:
            return 0

        if v["tipo"] == "SR":
            if receita >= meta:
                comissao = receita * ALIQUOTA_SR_META_ATINGIDA
                if receita > meta * MULTIPLICADOR_BONUS_META:
                    comissao += (receita - meta * MULTIPLICADOR_BONUS_META) * ALIQUOTA_SR_BONUS
            elif receita >= meta * MULTIPLICADOR_PARCIAL_META:
                comissao = receita * ALIQUOTA_SR_PARCIAL
            else:
                comissao = receita * ALIQUOTA_SR_ABAIXO
            if tipo_meta == "AGR":
                comissao *= MULTIPLICADOR_AGR
            if receita < RECEITA_MINIMA:
                comissao = 0
        else:
            if receita >= meta:
                comissao = receita * ALIQUOTA_JR_META_ATINGIDA
                if receita > meta * MULTIPLICADOR_BONUS_META:
                    comissao += (receita - meta * MULTIPLICADOR_BONUS_META) * ALIQUOTA_JR_BONUS
            else:
                # Nota: no original, as duas ramificações (parcial e abaixo) usam a
                # mesma alíquota para JR — comportamento preservado intencionalmente.
                comissao = receita * ALIQUOTA_JR_ABAIXO
            if tipo_meta == "AGR":
                comissao *= MULTIPLICADOR_AGR
            if receita < RECEITA_MINIMA:
                comissao = 0

        self._cache[vendedor_id] = round(comissao, 2)
        return self._cache[vendedor_id]

    def batch_calc(self, vendas: list) -> dict:
        # Passo 4: chama calc_comm em vez de duplicar a lógica
        return {
            venda["id"]: self.calc_comm(
                venda["id"], venda["receita"], venda["tipo_meta"], venda["meta"]
            )
            for venda in vendas
        }


if __name__ == "__main__":
    # ── Passo 1: testes de caracterização (com valores preenchidos) ──────────
    print("=== Passo 1: testes de caracterização ===")

    # SR, receita > 120% da meta → bônus de excedente
    # 10000*0.08 + (10000 - 9600)*0.03 = 800 + 12 = 812
    assert CommissionCalc().calc_comm("V001", 10000, "STD", 8000) == 812.0

    # SR, receita < 5000 → comissão zerada
    assert CommissionCalc().calc_comm("V003", 4000, "STD", 8000) == 0.0

    # SR, entre 80%-100% da meta → 7000*0.05 = 350
    assert CommissionCalc().calc_comm("V003", 7000, "STD", 8000) == 350.0

    # JR, meta atingida → 6000*0.05 = 300
    assert CommissionCalc().calc_comm("V002", 6000, "STD", 5000) == 300.0

    # JR, tipo AGR → 300 * 1.1 = 330
    assert CommissionCalc().calc_comm("V002", 6000, "AGR", 5000) == 330.0

    # JR, receita < 5000 → comissão zerada
    assert CommissionCalc().calc_comm("V002", 4000, "STD", 5000) == 0.0

    # Vendedor inexistente → 0
    assert CommissionCalc().calc_comm("V999", 10000, "STD", 8000) == 0

    print("[OK] todos os testes de caracterização passaram")
    print()

    # ── Passo 4: verificação — batch_calc usa calc_comm ──────────────────────
    print("=== Passo 4: batch_calc sem duplicação ===")
    calc = CommissionCalc()
    resultado = calc.batch_calc([
        {"id": "V001", "receita": 10000, "tipo_meta": "STD", "meta": 8000},
        {"id": "V002", "receita": 6000,  "tipo_meta": "AGR", "meta": 5000},
        {"id": "V003", "receita": 7000,  "tipo_meta": "STD", "meta": 8000},
    ])
    assert resultado == {"V001": 812.0, "V002": 330.0, "V003": 350.0}
    print(f"  Resultado: {resultado}")
    print("[OK] batch_calc chama calc_comm, sem lógica duplicada")
