"""
EXERCÍCIO 19 — Anti-patterns Clássicos
Tempo estimado: 15 minutos
Referência: Clean Code Cap. 17 + Fowler Refactoring Cap. 3

INSTRUÇÕES:
  O código abaixo demonstra dois anti-patterns:
  1. God Object: GestorFolhaPagamento faz tudo — CRUD, cálculo, relatório, email.
  2. Magic Strings/Numbers: if categoria == "C", salario_base = 1412.

  1. Quebre o God Object em classes com responsabilidade única.
  2. Substitua as strings/números mágicos por enums e constantes.
  3. Execute: python3 exercicio.py (deve rodar antes e depois)
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


class GestorFolhaPagamento:
    """Faz tudo: busca, calcula, notifica, arquiva, gera relatório."""

    def buscar_funcionario(self, func_id: str) -> Optional[Funcionario]:
        print(f"  [BD] buscar funcionário {func_id}")
        return Funcionario(func_id, "João Silva", "joao@empresa.com", "C", 3500.0)

    def salvar_funcionario(self, func: Funcionario) -> None:
        print(f"  [BD] salvar {func.id}")

    def calcular_inss(self, salario: float, categoria: str) -> float:
        if categoria == "C":      # magic string
            if salario <= 1412:   # magic number — salário mínimo 2026
                return salario * 0.075
            elif salario <= 2666.68:
                return salario * 0.09
            else:
                return salario * 0.12
        elif categoria == "P":    # magic string
            return 0.0
        return salario * 0.03    # estagiário

    def calcular_fgts(self, salario: float, categoria: str) -> float:
        if categoria == "C":
            return round(salario * 0.08, 2)
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

    def calcular_ferias(self, salario: float) -> float:
        return round(salario / 3, 2)


if __name__ == "__main__":
    gestor = GestorFolhaPagamento()
    func   = gestor.buscar_funcionario("FUNC-001")
    inss   = gestor.calcular_inss(func.salario, func.categoria)
    fgts   = gestor.calcular_fgts(func.salario, func.categoria)
    print(f"INSS: R${inss:.2f}, FGTS: R${fgts:.2f}")
    gestor.enviar_contracheque(func.email, func.salario - inss)
    metodos = [m for m in dir(gestor) if not m.startswith("_")]
    print(f"GestorFolhaPagamento tem {len(metodos)} métodos")
