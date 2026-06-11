"""
EXERCÍCIO 16 — SOLID na Prática
Tempo estimado: 29 minutos (4 micro-passos)
Referência: Clean Code + SOLID papers

PASSOS (faça um de cada vez, em ordem):

  PASSO 1 — IDENTIFICAR (5 min)
    Leia GeradorFatura e adicione comentários # SRP: e # DIP: antes de
    cada trecho problemático.
    Meta: encontrar pelo menos 4 violações antes de alterar código.

  PASSO 2 — EXTRAIR ValidadorFatura (8 min)
    Mova validar() para uma nova classe ValidadorFatura.
    GeradorFatura passa a receber ValidadorFatura no construtor.
    Verifique que o demo ainda roda: python3 exercicio.py

  PASSO 3 — EXTRAIR CalculadorFatura + RepositorioFatura (8 min)
    Repita para calcular_total() e salvar().
    GeradorFatura.processar() delega para os colaboradores injetados.
    Verifique que o demo ainda roda: python3 exercicio.py

  PASSO 4 — INVERTER DEPENDÊNCIA DE EMAIL (8 min)
    Crie Protocol INotificador com notificar(destinatario, mensagem).
    Substitua self.email = EmailSMTP() por injeção no construtor.
    Verifique que o demo ainda roda: python3 exercicio.py

Para rodar: python3 exercicio.py
"""
from dataclasses import dataclass
from typing import List


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


class EmailSMTP:
    def enviar(self, dest: str, msg: str) -> None:
        print(f"  [SMTP] → {dest}: {msg}")


class GeradorFatura:
    def __init__(self) -> None:
        self.email = EmailSMTP()   # DIP violation

    def validar(self, fatura: Fatura) -> bool:   # SRP violation
        return bool(fatura.itens) and bool(fatura.cliente_id)

    def calcular_total(self, fatura: Fatura) -> float:   # SRP violation
        return sum(i.valor for i in fatura.itens)

    def salvar(self, fatura: Fatura) -> None:   # SRP violation
        print(f"  [BD] fatura {fatura.id} salva")

    def processar(self, fatura: Fatura) -> float:
        if not self.validar(fatura):
            raise ValueError("Fatura inválida")
        total = self.calcular_total(fatura)
        self.salvar(fatura)
        self.email.enviar(fatura.cliente_id, f"Fatura {fatura.id}: R${total:.2f}")
        return total


if __name__ == "__main__":
    itens  = [ItemFatura("Consultoria", 1500.0), ItemFatura("Suporte", 300.0)]
    fatura = Fatura("FAT-001", "CLI-200", itens)
    gerador = GeradorFatura()
    total = gerador.processar(fatura)
    print(f"Total: R${total:.2f}")

    # -----------------------------------------------------------------------
    # PASSO 4 — stub para verificar a injeção de dependência.
    # Após criar INotificador, descomente e rode python3 exercicio.py.
    # -----------------------------------------------------------------------
    # class NotificadorLog:
    #     def __init__(self):
    #         self.chamado = False
    #     def notificar(self, destinatario: str, mensagem: str) -> None:
    #         self.chamado = True
    #
    # notif_log = NotificadorLog()
    # gerador2  = GeradorFatura(
    #     ValidadorFatura(), CalculadorFatura(), RepositorioFatura(), notif_log
    # )
    # gerador2.processar(fatura)
    # assert notif_log.chamado, "FALHOU: notificador substituto não foi chamado"
    # print("[OK] DIP — GeradorFatura aceita qualquer INotificador")
