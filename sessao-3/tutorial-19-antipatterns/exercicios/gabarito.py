"""
GABARITO 19 — Anti-patterns Clássicos
Referência: Clean Code Cap. 17 + Fowler Refactoring Cap. 3
Execute: python3 gabarito.py
"""
from typing import List, Optional
from dataclasses import dataclass
from abc import ABC, abstractmethod
from enum import Enum


# ─── Correção 2: Magic Strings → enum + constantes nomeadas ──────────────────

class CategoriaFuncionario(str, Enum):
    CLT        = "clt"
    PJ         = "pj"
    ESTAGIARIO = "estagiario"

SALARIO_MINIMO_2026:     float = 1412.0
LIMITE_FAIXA_INSS_2:     float = 2666.68
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
    categoria: CategoriaFuncionario
    salario:   float

    def calcular_inss(self) -> float:
        """Correção 3 (Feature Envy): método movido para o dono dos dados."""
        if self.categoria == CategoriaFuncionario.CLT:
            if self.salario <= SALARIO_MINIMO_2026:
                return round(self.salario * ALIQUOTA_INSS_FAIXA_1, 2)
            elif self.salario <= LIMITE_FAIXA_INSS_2:
                return round(self.salario * ALIQUOTA_INSS_FAIXA_2, 2)
            else:
                return round(self.salario * ALIQUOTA_INSS_FAIXA_3, 2)
        if self.categoria == CategoriaFuncionario.PJ:
            return 0.0
        return round(self.salario * ALIQUOTA_INSS_ESTAGIARIO, 2)


# ─── Correção 1: God Object → classes com responsabilidade única ──────────────

class RepositorioFuncionario:
    def buscar(self, func_id: str) -> Optional[Funcionario]:
        print(f"  [BD] buscar funcionário {func_id}")
        return Funcionario(func_id, "João Silva", "joao@empresa.com",
                           CategoriaFuncionario.CLT, 3500.0)

    def salvar(self, func: Funcionario) -> None:
        print(f"  [BD] salvar {func.id}")


class CalculadorFgts:
    def calcular(self, func: Funcionario) -> float:
        if func.categoria == CategoriaFuncionario.CLT:
            return round(func.salario * ALIQUOTA_FGTS, 2)
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


# ─── Correção 4: Copy-Paste → CalculoBase com Template Method ────────────────

class CalculoBase(ABC):
    def calcular_base(self, func: Funcionario) -> float:
        if func.categoria == CategoriaFuncionario.CLT:
            return max(func.salario, SALARIO_MINIMO_2026)
        return func.salario

    def calcular_liquido(self, func: Funcionario) -> float:
        return round(self.calcular_base(func) * self._fator_desconto(), 2)

    @abstractmethod
    def _fator_desconto(self) -> float: ...


class CalculoCLT(CalculoBase):
    def _fator_desconto(self) -> float:
        return 0.85


class CalculoTerceirizado(CalculoBase):
    def _fator_desconto(self) -> float:
        return 0.80


# ─── Verificação ──────────────────────────────────────────────────────────────

def verificar_gabarito() -> None:
    # God Object corrigido
    for cls in [RepositorioFuncionario, CalculadorFgts, ServicoNotificacao, GeradorRelatorioRH]:
        metodos = [m for m in dir(cls()) if not m.startswith("_")]
        assert len(metodos) <= 5, f"{cls.__name__} ainda tem responsabilidades demais"
    print("OK: God Object — responsabilidades separadas em 4 classes especializadas")

    # Enums no lugar de strings mágicas
    assert CategoriaFuncionario.CLT.value        == "clt"
    assert CategoriaFuncionario.PJ.value         == "pj"
    assert CategoriaFuncionario.ESTAGIARIO.value == "estagiario"
    print("OK: Magic Strings — CategoriaFuncionario como enum (CLT, PJ, ESTAGIARIO)")

    # Constantes no lugar de números mágicos
    assert SALARIO_MINIMO_2026 == 1412.0
    print("OK: Magic Numbers — SALARIO_MINIMO_2026 e alíquotas como constantes nomeadas")

    # Feature Envy corrigido: calcular_inss() pertence ao Funcionario
    func_clt   = Funcionario("F1", "João", "j@e.com", CategoriaFuncionario.CLT, 3500.0)
    func_pj    = Funcionario("F2", "Ana",  "a@e.com", CategoriaFuncionario.PJ,  8000.0)
    func_estagio = Funcionario("F3", "Leo", "l@e.com", CategoriaFuncionario.ESTAGIARIO, 900.0)
    assert func_clt.calcular_inss()     == round(3500.0 * 0.12, 2)
    assert func_pj.calcular_inss()      == 0.0
    assert func_estagio.calcular_inss() == round(900.0 * 0.03, 2)
    print(f"OK: Feature Envy — calcular_inss() movido para Funcionario "
          f"(CLT=R${func_clt.calcular_inss():.2f}, PJ=R${func_pj.calcular_inss():.2f})")

    # Copy-Paste corrigido: CalculoBase elimina calcular_base() duplicado
    clt_calc  = CalculoCLT()
    terc_calc = CalculoTerceirizado()
    assert clt_calc.calcular_liquido(func_clt)  == round(3500.0 * 0.85, 2)
    assert terc_calc.calcular_liquido(func_clt) == round(3500.0 * 0.80, 2)
    print(f"OK: Copy-Paste — CalculoBase._fator_desconto() elimina calcular_base() duplicado "
          f"(CLT=R${clt_calc.calcular_liquido(func_clt):.2f}, Terc=R${terc_calc.calcular_liquido(func_clt):.2f})")


if __name__ == "__main__":
    print("=== Gabarito 19 — Anti-patterns RH ===\n")
    verificar_gabarito()

    print("\n--- Demo completo ---")
    repo        = RepositorioFuncionario()
    calc_fgts   = CalculadorFgts()
    notificacao = ServicoNotificacao()

    func = repo.buscar("FUNC-001")
    inss = func.calcular_inss()
    fgts = calc_fgts.calcular(func)
    print(f"INSS: R${inss:.2f}, FGTS: R${fgts:.2f}")
    notificacao.enviar_contracheque(func.email, func.salario - inss)
