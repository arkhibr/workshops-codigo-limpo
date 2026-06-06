"""
GABARITO 16 — SOLID na Prática
Referência: Clean Code + SOLID papers

Correções aplicadas:
  SRP — ValidadorFatura, CalculadorFatura, RepositorioFatura separados
  DIP — GeradorFatura recebe INotificador no construtor, não instancia EmailSMTP
Execute: python3 gabarito.py
"""
from dataclasses import dataclass
from typing import List, Protocol, runtime_checkable


@dataclass
class ItemFatura:
    descricao: str
    valor:     float

@dataclass
class Fatura:
    id:         str
    cliente_id: str
    itens:      List[ItemFatura]
    status:     str = "pendente"


# ─── Abstrações (DIP) ────────────────────────────────────────────────────────

@runtime_checkable
class INotificador(Protocol):
    def notificar(self, destinatario: str, mensagem: str) -> None: ...

class IRepositorioFatura(Protocol):
    def salvar(self, fatura: "Fatura") -> None: ...


# ─── Classes com responsabilidade única (SRP) ────────────────────────────────

class ValidadorFatura:
    def validar(self, fatura: Fatura) -> bool:
        return bool(fatura.itens) and bool(fatura.cliente_id)

class CalculadorFatura:
    def calcular_total(self, fatura: Fatura) -> float:
        return round(sum(i.valor for i in fatura.itens), 2)

class RepositorioFatura:
    def salvar(self, fatura: Fatura) -> None:
        print(f"  [BD] fatura {fatura.id} salva ({fatura.status})")

class NotificadorEmail:
    def notificar(self, destinatario: str, mensagem: str) -> None:
        print(f"  [SMTP] → {destinatario}: {mensagem}")


# ─── GeradorFatura: orquestra, não executa (DIP + SRP) ───────────────────────

class GeradorFatura:
    def __init__(
        self,
        validador:   ValidadorFatura,
        calculador:  CalculadorFatura,
        repositorio: IRepositorioFatura,
        notificador: INotificador,
    ) -> None:
        self._validador   = validador
        self._calculador  = calculador
        self._repositorio = repositorio
        self._notificador = notificador

    def processar(self, fatura: Fatura) -> float:
        if not self._validador.validar(fatura):
            raise ValueError("Fatura inválida")
        total = self._calculador.calcular_total(fatura)
        self._repositorio.salvar(fatura)
        self._notificador.notificar(fatura.cliente_id, f"Fatura {fatura.id}: R${total:.2f}")
        return total


# ─── Verificação ─────────────────────────────────────────────────────────────

def verificar_solid() -> None:
    itens  = [ItemFatura("Consultoria", 1500.0), ItemFatura("Suporte", 300.0)]
    fatura = Fatura("FAT-001", "CLI-200", itens)

    validador   = ValidadorFatura()
    calculador  = CalculadorFatura()
    repositorio = RepositorioFatura()
    notificador = NotificadorEmail()

    gerador = GeradorFatura(validador, calculador, repositorio, notificador)
    total   = gerador.processar(fatura)

    if total == 1800.0:
        print("OK: SRP — ValidadorFatura, CalculadorFatura, RepositorioFatura separados")
    else:
        print(f"FALHOU: SRP — total calculado incorretamente (esperado 1800.0, obtido {total})")

    # Substituição de notificador sem alterar GeradorFatura (DIP)
    class NotificadorLog:
        def __init__(self) -> None:
            self.chamado = False
        def notificar(self, destinatario: str, mensagem: str) -> None:
            self.chamado = True

    notif_log = NotificadorLog()
    gerador2  = GeradorFatura(validador, calculador, repositorio, notif_log)
    gerador2.processar(fatura)

    if notif_log.chamado:
        print("OK: DIP — GeradorFatura aceita qualquer INotificador sem ser alterado")
    else:
        print("FALHOU: DIP — notificador substituto não foi chamado")

    # Fatura inválida
    fatura_vazia = Fatura("FAT-000", "", [])
    try:
        gerador.processar(fatura_vazia)
        print("FALHOU: validação — deveria ter lançado ValueError")
    except ValueError:
        print("OK: validação — ValueError lançado para fatura inválida")


if __name__ == "__main__":
    print("=== GABARITO 16 — SOLID na Prática ===\n")
    verificar_solid()
