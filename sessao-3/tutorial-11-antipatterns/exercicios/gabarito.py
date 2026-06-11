"""
GABARITO 19 — Anti-patterns Clássicos
Referência: Clean Code Cap. 17 + Fowler Refactoring Cap. 3
Execute: python3 gabarito.py
"""
from typing import Optional
from dataclasses import dataclass


# ─── Passo 1: Magic Strings/Numbers → constantes nomeadas ────────────────────

CATEGORIA_CLT        = "C"
CATEGORIA_PJ         = "P"
CATEGORIA_ESTAGIARIO = "E"

SALARIO_MINIMO_2026      = 1412.0
LIMITE_FAIXA_INSS_2      = 2666.68
ALIQUOTA_INSS_FAIXA_1    = 0.075
ALIQUOTA_INSS_FAIXA_2    = 0.09
ALIQUOTA_INSS_FAIXA_3    = 0.12
ALIQUOTA_INSS_ESTAGIARIO = 0.03
ALIQUOTA_FGTS            = 0.08


# ─── Modelo de domínio ────────────────────────────────────────────────────────

@dataclass
class Funcionario:
    id:        str
    nome:      str
    email:     str
    categoria: str   # usa as constantes CATEGORIA_* acima
    salario:   float

    # Passo 2: Feature Envy → calcular_inss() pertence ao dono dos dados
    def calcular_inss(self) -> float:
        if self.categoria == CATEGORIA_CLT:
            if self.salario <= SALARIO_MINIMO_2026:
                return round(self.salario * ALIQUOTA_INSS_FAIXA_1, 2)
            elif self.salario <= LIMITE_FAIXA_INSS_2:
                return round(self.salario * ALIQUOTA_INSS_FAIXA_2, 2)
            else:
                return round(self.salario * ALIQUOTA_INSS_FAIXA_3, 2)
        if self.categoria == CATEGORIA_PJ:
            return 0.0
        return round(self.salario * ALIQUOTA_INSS_ESTAGIARIO, 2)


# ─── Passo 3: Copy-Paste → função livre compartilhada ────────────────────────

def _calcular_base(func: Funcionario) -> float:
    """Base de cálculo: garante piso de salário mínimo para CLT."""
    if func.categoria == CATEGORIA_CLT:
        return max(func.salario, SALARIO_MINIMO_2026)
    return func.salario


class CalculoNormal:
    def calcular_base(self, func: Funcionario) -> float:
        return _calcular_base(func)

    def calcular_liquido(self, func: Funcionario) -> float:
        return round(self.calcular_base(func) * 0.85, 2)


class CalculoTerceirizado:
    def calcular_base(self, func: Funcionario) -> float:
        return _calcular_base(func)

    def calcular_liquido(self, func: Funcionario) -> float:
        return round(self.calcular_base(func) * 0.80, 2)


# ─── Passo 4: God Object → 3 classes com responsabilidade única ──────────────

class RepositorioFuncionario:
    def buscar_funcionario(self, func_id: str) -> Funcionario:
        print(f"  [BD] buscar funcionário {func_id}")
        return Funcionario(func_id, "João Silva", "joao@empresa.com",
                           CATEGORIA_CLT, 3500.0)

    def salvar_funcionario(self, func: Funcionario) -> None:
        print(f"  [BD] salvar {func.id}")

    def calcular_fgts(self, func: Funcionario) -> float:
        if func.categoria == CATEGORIA_CLT:
            return round(func.salario * ALIQUOTA_FGTS, 2)
        return 0.0


class ServicoNotificacao:
    def enviar_contracheque(self, email: str, valor: float) -> None:
        print(f"  [Email] → {email}: contracheque R${valor:.2f}")

    def notificar_rh(self, msg: str) -> None:
        print(f"  [RH] {msg}")


class GeradorRelatorioRH:
    def gerar_relatorio(self, ano: int) -> str:
        return f"Relatório folha {ano}"

    def exportar_csv(self, dados: list) -> str:
        return "funcionario,salario\n" + "\n".join(str(d) for d in dados)

    def arquivar_folha(self, mes: int, ano: int) -> None:
        print(f"  [BD] arquivando folha {mes}/{ano}")


# ─── Verificação ──────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=== Gabarito 19 — Anti-patterns RH ===\n")

    # Passo 1: constantes no lugar de magic strings/numbers
    assert CATEGORIA_CLT        == "C"
    assert CATEGORIA_PJ         == "P"
    assert CATEGORIA_ESTAGIARIO == "E"
    assert SALARIO_MINIMO_2026  == 1412.0
    print("PASSO 1 OK: constantes CATEGORIA_* e SALARIO_MINIMO_2026 definidas")

    # Passo 2: calcular_inss() pertence a Funcionario
    func_clt     = Funcionario("F1", "João", "j@e.com", CATEGORIA_CLT,        3500.0)
    func_pj      = Funcionario("F2", "Ana",  "a@e.com", CATEGORIA_PJ,         8000.0)
    func_estag   = Funcionario("F3", "Leo",  "l@e.com", CATEGORIA_ESTAGIARIO,  900.0)
    assert func_clt.calcular_inss()   == round(3500.0 * ALIQUOTA_INSS_FAIXA_3, 2)
    assert func_pj.calcular_inss()    == 0.0
    assert func_estag.calcular_inss() == round(900.0 * ALIQUOTA_INSS_ESTAGIARIO, 2)
    print(f"PASSO 2 OK: calcular_inss() em Funcionario "
          f"(CLT=R${func_clt.calcular_inss():.2f}, PJ=R${func_pj.calcular_inss():.2f})")

    # Passo 3: _calcular_base() elimina duplicação
    n = CalculoNormal()
    t = CalculoTerceirizado()
    assert n.calcular_liquido(func_clt) == round(3500.0 * 0.85, 2)
    assert t.calcular_liquido(func_clt) == round(3500.0 * 0.80, 2)
    print(f"PASSO 3 OK: _calcular_base() sem duplicação "
          f"(CLT=R${n.calcular_liquido(func_clt):.2f}, Terc=R${t.calcular_liquido(func_clt):.2f})")

    # Passo 4: God Object separado em classes com responsabilidade única
    for cls in [RepositorioFuncionario, ServicoNotificacao, GeradorRelatorioRH]:
        metodos = [m for m in dir(cls()) if not m.startswith("_")]
        assert len(metodos) <= 5, f"{cls.__name__} ainda tem responsabilidades demais"
    print("PASSO 4 OK: RepositorioFuncionario / ServicoNotificacao / GeradorRelatorioRH")

    print("\n--- Demo completo ---")
    repo   = RepositorioFuncionario()
    notif  = ServicoNotificacao()
    func   = repo.buscar_funcionario("FUNC-001")
    inss   = func.calcular_inss()
    fgts   = repo.calcular_fgts(func)
    print(f"INSS: R${inss:.2f}, FGTS: R${fgts:.2f}")
    notif.enviar_contracheque(func.email, func.salario - inss)
