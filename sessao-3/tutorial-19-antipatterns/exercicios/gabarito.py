"""
GABARITO 19 — Anti-patterns Clássicos
Referência: Clean Code Cap. 17 + Fowler Refactoring Cap. 3
Execute: python3 gabarito.py
"""
from typing import List, Optional
from dataclasses import dataclass
from enum import Enum


# ─── Correção 2: Magic Strings → enum + constantes nomeadas ──────────────────

class CategoriaCargo(str, Enum):
    CLT        = "clt"
    PJ         = "pj"
    ESTAGIARIO = "estagiario"

SALARIO_MINIMO_2026:     float = 1412.0
LIMITE_FAIXA_INSS_1:     float = 2666.68
ALIQUOTA_INSS_FAIXA_1:   float = 0.075
ALIQUOTA_INSS_FAIXA_2:   float = 0.09
ALIQUOTA_INSS_FAIXA_3:   float = 0.12
ALIQUOTA_INSS_ESTAGIARIO: float = 0.03
ALIQUOTA_FGTS:           float = 0.08


# ─── Modelo de domínio ────────────────────────────────────────────────────────

@dataclass
class Funcionario:
    id:        str
    nome:      str
    email:     str
    categoria: CategoriaCargo
    salario:   float


# ─── Correção 1: God Object → classes com responsabilidade única ──────────────

class RepositorioFuncionario:
    def buscar(self, func_id: str) -> Optional[Funcionario]:
        print(f"  [BD] buscar funcionário {func_id}")
        return Funcionario(func_id, "João Silva", "joao@empresa.com",
                           CategoriaCargo.CLT, 3500.0)

    def salvar(self, func: Funcionario) -> None:
        print(f"  [BD] salvar {func.id}")


class CalculadorInss:
    def calcular(self, salario: float, categoria: CategoriaCargo) -> float:
        if categoria == CategoriaCargo.CLT:
            if salario <= SALARIO_MINIMO_2026:
                return round(salario * ALIQUOTA_INSS_FAIXA_1, 2)
            elif salario <= LIMITE_FAIXA_INSS_1:
                return round(salario * ALIQUOTA_INSS_FAIXA_2, 2)
            else:
                return round(salario * ALIQUOTA_INSS_FAIXA_3, 2)
        if categoria == CategoriaCargo.PJ:
            return 0.0
        return round(salario * ALIQUOTA_INSS_ESTAGIARIO, 2)


class CalculadorFgts:
    def calcular(self, salario: float, categoria: CategoriaCargo) -> float:
        if categoria == CategoriaCargo.CLT:
            return round(salario * ALIQUOTA_FGTS, 2)
        return 0.0


class ServicoNotificacao:
    def enviar_contracheque(self, email: str, valor: float) -> None:
        print(f"  [Email] → {email}: contracheque R${valor:.2f}")

    def notificar_rh(self, msg: str) -> None:
        print(f"  [RH] {msg}")


class GeradorRelatorioRH:
    def gerar(self, ano: int) -> str:
        return f"Relatório folha {ano}"

    def exportar_csv(self, dados: list) -> str:
        return "funcionario,salario\n" + "\n".join(str(d) for d in dados)

    def arquivar_folha(self, mes: int, ano: int) -> None:
        print(f"  [BD] arquivando folha {mes}/{ano}")


# ─── Verificação ──────────────────────────────────────────────────────────────

def verificar_antipatterns() -> None:
    # God Object corrigido
    for cls in [RepositorioFuncionario, CalculadorInss, CalculadorFgts,
                ServicoNotificacao, GeradorRelatorioRH]:
        metodos = [m for m in dir(cls()) if not m.startswith("_")]
        assert len(metodos) <= 5, f"{cls.__name__} ainda tem responsabilidades demais"
    print("OK: God Object — responsabilidades separadas em 5 classes especializadas")

    # Enums no lugar de strings mágicas
    assert CategoriaCargo.CLT.value        == "clt"
    assert CategoriaCargo.PJ.value         == "pj"
    assert CategoriaCargo.ESTAGIARIO.value == "estagiario"
    print("OK: Magic Strings — CategoriaCargo como enum (CLT, PJ, ESTAGIARIO)")

    # Constantes no lugar de números mágicos
    assert SALARIO_MINIMO_2026 == 1412.0
    print("OK: Magic Numbers — SALARIO_MINIMO_2026 e alíquotas como constantes nomeadas")

    # CalculadorInss com enum
    calc_inss = CalculadorInss()
    assert calc_inss.calcular(1000.0, CategoriaCargo.CLT)   == round(1000.0 * 0.075, 2)
    assert calc_inss.calcular(3500.0, CategoriaCargo.CLT)   == round(3500.0 * 0.12, 2)
    assert calc_inss.calcular(5000.0, CategoriaCargo.PJ)    == 0.0
    assert calc_inss.calcular(1500.0, CategoriaCargo.ESTAGIARIO) == round(1500.0 * 0.03, 2)
    print("OK: CalculadorInss — faixas corretas para CLT, PJ e Estagiário")

    # CalculadorFgts com enum
    calc_fgts = CalculadorFgts()
    assert calc_fgts.calcular(3500.0, CategoriaCargo.CLT) == round(3500.0 * 0.08, 2)
    assert calc_fgts.calcular(5000.0, CategoriaCargo.PJ)  == 0.0
    print("OK: CalculadorFgts — 8% para CLT, zero para PJ")


if __name__ == "__main__":
    print("=== Gabarito 19 — Anti-patterns RH ===\n")
    verificar_antipatterns()

    print("\n--- Demo completo ---")
    repo        = RepositorioFuncionario()
    calc_inss   = CalculadorInss()
    calc_fgts   = CalculadorFgts()
    notificacao = ServicoNotificacao()

    func = repo.buscar("FUNC-001")
    inss = calc_inss.calcular(func.salario, func.categoria)
    fgts = calc_fgts.calcular(func.salario, func.categoria)
    print(f"INSS: R${inss:.2f}, FGTS: R${fgts:.2f}")
    notificacao.enviar_contracheque(func.email, func.salario - inss)
