"""
EXERCÍCIO 16 — SOLID na Prática
Tempo estimado: 15 minutos
Referência: Clean Code + SOLID papers

INSTRUÇÕES:
  A classe GeradorFatura abaixo viola SRP (valida, calcula, persiste e envia
  email) e DIP (instancia EmailSMTP diretamente).

  1. Separe em classes com responsabilidade única.
  2. Inverta a dependência de email: GeradorFatura deve receber um INotificador.
  3. Execute: python3 exercicio.py (deve rodar antes e depois da refatoração)
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
