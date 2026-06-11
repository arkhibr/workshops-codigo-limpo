"""
EXERCÍCIO 19 — Anti-patterns Clássicos
Tempo estimado: 34 minutos (4 micro-passos)
Referência: Clean Code Cap. 17 + Fowler Refactoring Cap. 3

INSTRUÇÕES GERAIS:
  O código abaixo demonstra 4 anti-patterns.
  Siga os 4 passos em ordem — cada passo é independente e verificável.
  Execute: python3 exercicio.py (deve rodar sem erro antes e depois de cada passo)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PASSO 1 — MAGIC STRINGS/NUMBERS  (8 min)
  Extraia as strings e números mágicos para constantes nomeadas:
    SALARIO_MINIMO_2026 = 1412.0
    CATEGORIA_CLT = "C"  /  CATEGORIA_PJ = "P"  /  CATEGORIA_ESTAGIARIO = "E"
  Substitua todas as ocorrências nos lugares onde estão usados.
  Verifique que o demo ainda roda.

PASSO 2 — FEATURE ENVY  (8 min)
  Mova calcular_inss() da classe Pagamento para a classe Funcionario.
  Funcionario.calcular_inss(self) — sem parâmetro, usa self.salario/self.categoria.
  Atualize os chamadores.
  Verifique que o demo ainda roda.

PASSO 3 — COPY-PASTE  (8 min)
  Extraia calcular_base() como função de módulo:
    def _calcular_base(func: Funcionario) -> float: ...
  Faça CalculoNormal.calcular_base() e CalculoTerceirizado.calcular_base()
  chamarem _calcular_base().
  Verifique que o demo ainda roda.

PASSO 4 — GOD OBJECT  (10 min)
  Separe GestorFolhaPagamento em 3 classes com responsabilidade única:
    RepositorioFuncionario  — buscar_funcionario, salvar_funcionario
    ServicoNotificacao      — enviar_contracheque, notificar_rh
    GeradorRelatorioRH      — gerar_relatorio, exportar_csv, arquivar_folha
  Deixe calcular_fgts() em RepositorioFuncionario ou crie CalculadorFolha separado.
  Verifique que o demo ainda roda.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
from typing import List, Optional
from dataclasses import dataclass


@dataclass
class Funcionario:
    id:        str
    nome:      str
    email:     str
    categoria: str   # "C" = CLT, "P" = PJ, "E" = Estagiário
    salario:   float


# ─── Anti-pattern 3 — Feature Envy ───────────────────────────────────────────

@dataclass
class Pagamento:
    id:  str
    mes: int
    ano: int

    def calcular_inss(self, funcionario: Funcionario) -> float:
        """Feature Envy: este método sabe mais sobre Funcionario do que sobre Pagamento."""
        salario_base = 1412          # magic number — salário mínimo 2026
        if funcionario.categoria == "C":        # magic string
            if funcionario.salario <= salario_base:
                return round(funcionario.salario * 0.075, 2)
            elif funcionario.salario <= 2666.68:
                return round(funcionario.salario * 0.09, 2)
            else:
                return round(funcionario.salario * 0.12, 2)
        elif funcionario.categoria == "P":      # magic string
            return 0.0
        return round(funcionario.salario * 0.03, 2)


# ─── Anti-pattern 1 — God Object ─────────────────────────────────────────────

class GestorFolhaPagamento:
    """Faz tudo: busca, calcula, notifica, arquiva, gera relatório."""

    def buscar_funcionario(self, func_id: str) -> Optional[Funcionario]:
        print(f"  [BD] buscar funcionário {func_id}")
        return Funcionario(func_id, "João Silva", "joao@empresa.com", "C", 3500.0)

    def salvar_funcionario(self, func: Funcionario) -> None:
        print(f"  [BD] salvar {func.id}")

    def calcular_fgts(self, func: Funcionario) -> float:
        if func.categoria == "C":
            return round(func.salario * 0.08, 2)
        return 0.0

    def enviar_contracheque(self, email: str, valor: float) -> None:
        print(f"  [Email] → {email}: contracheque R${valor:.2f}")

    def arquivar_folha(self, mes: int, ano: int) -> None:
        print(f"  [BD] arquivando folha {mes}/{ano}")

    def gerar_relatorio(self, ano: int) -> str:
        return f"Relatório folha {ano}"

    def exportar_csv(self, dados: list) -> str:
        return "funcionario,salario\n"

    def reprocessar_folha(self, mes: int) -> bool:
        print(f"  reprocessando folha {mes}")
        return True

    def notificar_rh(self, msg: str) -> None:
        print(f"  [RH] {msg}")

    def validar_cpf(self, cpf: str) -> bool:
        return len(cpf.replace(".", "").replace("-", "")) == 11

    def calcular_ferias(self, func: Funcionario) -> float:
        return round(func.salario / 3, 2)

    def calcular_horas_extras(self, func_id: str, horas: float) -> float:
        return round(horas * 1.5, 2)


# ─── Anti-pattern 4 — Copy-Paste ─────────────────────────────────────────────

class CalculoNormal:
    def calcular_base(self, func: Funcionario) -> float:
        salario_base = 1412          # magic number — copiado em CalculoTerceirizado
        if func.categoria == "C":
            return max(func.salario, salario_base)
        return func.salario

    def calcular_liquido(self, func: Funcionario) -> float:
        return round(self.calcular_base(func) * 0.85, 2)  # desconta 15%


class CalculoTerceirizado:
    def calcular_base(self, func: Funcionario) -> float:  # idêntico a CalculoNormal
        salario_base = 1412          # magic number — copiado de CalculoNormal
        if func.categoria == "C":
            return max(func.salario, salario_base)
        return func.salario

    def calcular_liquido(self, func: Funcionario) -> float:
        return round(self.calcular_base(func) * 0.80, 2)  # desconta 20%


if __name__ == "__main__":
    gestor = GestorFolhaPagamento()
    func   = gestor.buscar_funcionario("FUNC-001")

    # God Object em ação
    metodos = [m for m in dir(gestor) if not m.startswith("_")]
    print(f"GestorFolhaPagamento tem {len(metodos)} métodos")

    # Feature Envy em ação
    pag  = Pagamento("PAG-001", 6, 2026)
    inss = pag.calcular_inss(func)
    fgts = gestor.calcular_fgts(func)
    print(f"INSS (Feature Envy): R${inss:.2f}, FGTS: R${fgts:.2f}")
    gestor.enviar_contracheque(func.email, func.salario - inss)

    # Copy-Paste em ação
    normal       = CalculoNormal()
    terceirizado = CalculoTerceirizado()
    print(f"Líquido CLT: R${normal.calcular_liquido(func):.2f}")
    print(f"Líquido Terc: R${terceirizado.calcular_liquido(func):.2f}")

    # ── Stubs de verificação — descomente após cada passo ─────────────────────

    # PASSO 1 — descomente para verificar:
    # assert CATEGORIA_CLT == "C"
    # assert CATEGORIA_PJ == "P"
    # assert CATEGORIA_ESTAGIARIO == "E"
    # assert SALARIO_MINIMO_2026 == 1412.0
    # print("PASSO 1 OK: constantes definidas e usadas")

    # PASSO 2 — descomente para verificar (requer Passo 1 feito):
    # func_clt = Funcionario("F1", "João", "j@e.com", CATEGORIA_CLT, 3500.0)
    # assert func_clt.calcular_inss() == round(3500.0 * 0.12, 2)
    # func_pj = Funcionario("F2", "Ana", "a@e.com", CATEGORIA_PJ, 8000.0)
    # assert func_pj.calcular_inss() == 0.0
    # print("PASSO 2 OK: calcular_inss() pertence a Funcionario")

    # PASSO 3 — descomente para verificar (requer Passo 1 feito):
    # func_teste = Funcionario("F3", "Leo", "l@e.com", CATEGORIA_CLT, 3500.0)
    # n = CalculoNormal()
    # t = CalculoTerceirizado()
    # assert n.calcular_liquido(func_teste) == round(3500.0 * 0.85, 2)
    # assert t.calcular_liquido(func_teste) == round(3500.0 * 0.80, 2)
    # print("PASSO 3 OK: _calcular_base() sem duplicação")

    # PASSO 4 — descomente para verificar:
    # repo = RepositorioFuncionario()
    # notif = ServicoNotificacao()
    # rel = GeradorRelatorioRH()
    # for cls in [RepositorioFuncionario, ServicoNotificacao, GeradorRelatorioRH]:
    #     metodos_cls = [m for m in dir(cls()) if not m.startswith("_")]
    #     assert len(metodos_cls) <= 5, f"{cls.__name__} ainda tem responsabilidades demais"
    # print("PASSO 4 OK: God Object separado em 3 classes")
