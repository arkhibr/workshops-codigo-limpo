"""
EXERCÍCIO 21 — Observer e Command
Tempo estimado: 20 minutos

INSTRUÇÕES:
  O código abaixo tem dois problemas:
  1. ProcessadorPagamento.processar() conhece e chama 3 serviços diretamente
     (acoplamento). Adicionar notificação por SMS exige alterar processar().
  2. estornar_pagamento() não tem undo — uma vez executado, não há como reverter.

  1. Refatore para Observer: crie ObservadorPagamento com ao_aprovar()/ao_recusar(),
     e ProcessadorPagamento com registrar_observador().
  2. Refatore para Command: crie ComandoEstorno com executar()/desfazer(),
     e HistoricoComandos.
  3. Execute: python3 exercicio.py (deve rodar antes e depois)
"""
from typing import List, Optional
from dataclasses import dataclass


@dataclass
class Pagamento:
    id:        str
    valor:     float
    cliente_id: str
    status:    str = "pendente"


# ─── Serviços acoplados diretamente ──────────────────────────────────────────

class ServicoEmail:
    def notificar_aprovacao(self, cliente_id: str, valor: float) -> None:
        print(f"  [Email] → {cliente_id}: pagamento R${valor:.2f} aprovado")

class ServicoAuditoria:
    def registrar(self, evento: str, pagamento_id: str) -> None:
        print(f"  [Auditoria] {evento}: {pagamento_id}")

class ServicoFraude:
    def marcar_aprovado(self, pagamento_id: str) -> None:
        print(f"  [Fraude] aprovado: {pagamento_id}")


# ─── Sem Observer: ProcessadorPagamento conhece os 3 serviços ────────────────

class ProcessadorPagamento:
    def __init__(self) -> None:
        self.email    = ServicoEmail()
        self.auditoria = ServicoAuditoria()
        self.fraude   = ServicoFraude()

    def processar(self, pagamento: Pagamento) -> None:
        pagamento.status = "aprovado"
        # Adicionar SMS exige alterar processar()
        self.email.notificar_aprovacao(pagamento.cliente_id, pagamento.valor)
        self.auditoria.registrar("pagamento_aprovado", pagamento.id)
        self.fraude.marcar_aprovado(pagamento.id)


# ─── Sem Command: estornar sem undo ──────────────────────────────────────────

def estornar_pagamento(pagamento: Pagamento) -> None:
    """Sem estado anterior. Sem histórico. Sem desfazer."""
    pagamento.status = "estornado"
    print(f"  Crédito de R${pagamento.valor:.2f} devolvido a {pagamento.cliente_id}")
    print(f"  Pagamento {pagamento.id} marcado como estornado")


if __name__ == "__main__":
    pag = Pagamento("PAG-001", 500.0, "CLI-100")
    proc = ProcessadorPagamento()
    proc.processar(pag)
    print(f"Status: {pag.status}\n")

    estornar_pagamento(pag)
    print(f"Status: {pag.status}")
    print("(sem desfazer disponível)")
