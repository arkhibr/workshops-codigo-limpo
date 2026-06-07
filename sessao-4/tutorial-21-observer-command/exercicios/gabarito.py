"""
gabarito.py — Solução do Exercício 21: Observer e Command
Execute: python3 gabarito.py
"""
from typing import List, Optional, Protocol
from dataclasses import dataclass


@dataclass
class Pagamento:
    id:         str
    valor:      float
    cliente_id: str
    status:     str = "pendente"


# ─── Observer ─────────────────────────────────────────────────────────────────

class ObservadorPagamento(Protocol):
    def ao_aprovar(self, pagamento: Pagamento) -> None: ...
    def ao_recusar(self, pagamento: Pagamento) -> None: ...

class NotificadorEmailPag:
    def ao_aprovar(self, pag: Pagamento) -> None:
        print(f"  [Email] → {pag.cliente_id}: pagamento R${pag.valor:.2f} aprovado")
    def ao_recusar(self, pag: Pagamento) -> None:
        print(f"  [Email] → {pag.cliente_id}: pagamento R${pag.valor:.2f} recusado")

class AuditoriaPag:
    def ao_aprovar(self, pag: Pagamento) -> None:
        print(f"  [Auditoria] pagamento_aprovado: {pag.id}")
    def ao_recusar(self, pag: Pagamento) -> None:
        print(f"  [Auditoria] pagamento_recusado: {pag.id}")

class FraudePag:
    def ao_aprovar(self, pag: Pagamento) -> None:
        print(f"  [Fraude] aprovado: {pag.id}")
    def ao_recusar(self, pag: Pagamento) -> None:
        print(f"  [Fraude] recusado: {pag.id}")


class ProcessadorPagamento:
    def __init__(self) -> None:
        self._observadores: List[ObservadorPagamento] = []

    def registrar_observador(self, obs: ObservadorPagamento) -> None:
        self._observadores.append(obs)

    def aprovar(self, pagamento: Pagamento) -> None:
        pagamento.status = "aprovado"
        for obs in self._observadores:
            obs.ao_aprovar(pagamento)

    def recusar(self, pagamento: Pagamento) -> None:
        pagamento.status = "recusado"
        for obs in self._observadores:
            obs.ao_recusar(pagamento)


# ─── Command ──────────────────────────────────────────────────────────────────

class ComandoEstorno:
    def __init__(self, pagamento: Pagamento, processador: ProcessadorPagamento) -> None:
        self._pagamento       = pagamento
        self._processador     = processador
        self._status_anterior: Optional[str] = None

    def executar(self) -> None:
        self._status_anterior = self._pagamento.status
        self._pagamento.status = "estornado"
        print(f"  Crédito de R${self._pagamento.valor:.2f} devolvido a {self._pagamento.cliente_id}")
        print(f"  Pagamento {self._pagamento.id} marcado como estornado")

    def desfazer(self) -> None:
        if self._status_anterior is None:
            raise RuntimeError("desfazer() chamado antes de executar()")
        self._pagamento.status = self._status_anterior
        print(f"  Pagamento {self._pagamento.id} restaurado para '{self._status_anterior}'")


class HistoricoComandos:
    def __init__(self) -> None:
        self._historico: List[ComandoEstorno] = []

    def executar(self, cmd: ComandoEstorno) -> None:
        cmd.executar()
        self._historico.append(cmd)

    def desfazer_ultimo(self) -> None:
        if not self._historico:
            print("  Nada para desfazer")
            return
        self._historico.pop().desfazer()


# ─── Verificação ──────────────────────────────────────────────────────────────

def verificar_gabarito() -> None:
    # Observer
    pag  = Pagamento("PAG-001", 500.0, "CLI-100")
    proc = ProcessadorPagamento()
    proc.registrar_observador(NotificadorEmailPag())
    proc.registrar_observador(AuditoriaPag())
    proc.registrar_observador(FraudePag())

    proc.aprovar(pag)
    assert pag.status == "aprovado"
    print("OK: Observer — 3 observadores notificados em aprovar()")
    print("OK: Observer — adicionar SMS não altera ProcessadorPagamento")

    # Command
    historico = HistoricoComandos()
    cmd = ComandoEstorno(pag, proc)
    historico.executar(cmd)
    assert pag.status == "estornado"
    print("OK: Command — estorno executado")

    historico.desfazer_ultimo()
    assert pag.status == "aprovado"
    print("OK: Command — estorno desfeito, pagamento restaurado para 'aprovado'")


if __name__ == "__main__":
    print("=== Gabarito 21 — Observer e Command: Pagamentos ===\n")
    verificar_gabarito()
