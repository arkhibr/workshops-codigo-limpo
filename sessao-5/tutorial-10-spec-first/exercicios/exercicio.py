"""
Exercício — Cancelamento de Reserva (saída de IA sem spec firme)
Referência: Tutorial 10 — Spec-first: do requisito ao código verificável
Execute: python3 exercicio.py

Contexto:
  Este módulo foi gerado por um modelo de fronteira com boas práticas aplicadas:
  @dataclass, ValueError para entradas inválidas, repositório em memória,
  demo com stdout. O código é limpo e cobre o caminho principal de cancelamento.

  Mas foi gerado sem especificação de uma exigência implícita:
    "o cancelamento só é permitido com antecedência mínima de 2 horas."
  O código cancela qualquer reserva a qualquer momento — inclusive nos últimos
  minutos antes do horário agendado, o que viola a política da empresa.

Suas tarefas:
  (1) Execute o exercício e observe o resultado. Identifique qual caso demonstra
      o cancelamento que deveria ser rejeitado.
  (2) Escreva a spec que fixa a exigência implícita, incluindo:
      - A regra de antecedência mínima (2 horas)
      - Exemplos de contrato com entrada→saída esperada para os casos de fronteira
  (3) Corrija o código para respeitar a regra e compare com gabarito.py.
"""

from dataclasses import dataclass
from datetime import datetime


# ─── Exceção de domínio ───────────────────────────────────────────────────────

class ReservaNaoEncontradaError(Exception):
    """Levantada quando o id de reserva não existe no repositório."""


# ─── Entidade ─────────────────────────────────────────────────────────────────

@dataclass
class Reserva:
    id:           int
    sala:         str
    inicio:       datetime
    fim:          datetime
    responsavel:  str
    cancelada:    bool = False


# ─── Repositório em memória ───────────────────────────────────────────────────

_repositorio: list[Reserva] = []
_proximo_id: int = 1


# ─── Operações ────────────────────────────────────────────────────────────────

def criar_reserva(
    sala:        str,
    inicio:      datetime,
    fim:         datetime,
    responsavel: str,
) -> Reserva:
    """Cria uma nova reserva ativa no repositório."""
    global _proximo_id

    if not sala.strip():
        raise ValueError("O campo 'sala' não pode ser vazio")
    if not responsavel.strip():
        raise ValueError("O campo 'responsavel' não pode ser vazio")
    if fim <= inicio:
        raise ValueError(
            f"Horário de fim deve ser após o início "
            f"(início={inicio:%H:%M}, fim={fim:%H:%M})"
        )

    reserva = Reserva(
        id=_proximo_id,
        sala=sala,
        inicio=inicio,
        fim=fim,
        responsavel=responsavel,
    )
    _repositorio.append(reserva)
    _proximo_id += 1
    return reserva


def cancelar_reserva(id_reserva: int, agora: datetime) -> Reserva:
    """
    Cancela a reserva identificada por id_reserva.

    Levanta ReservaNaoEncontradaError se o id não existir ou a reserva já
    estiver cancelada.

    Regra de antecedência: [exigência implícita — não especificada no prompt]
    """
    reserva = next(
        (r for r in _repositorio if r.id == id_reserva and not r.cancelada),
        None,
    )
    if reserva is None:
        raise ReservaNaoEncontradaError(
            f"Reserva {id_reserva} não encontrada ou já cancelada"
        )

    # ⚠️  DEFEITO: cancela a qualquer momento sem verificar antecedência mínima.
    # A exigência implícita — "cancelamento apenas com 2h de antecedência" —
    # foi perdida porque o prompt informal descreveu apenas "cancelar reserva".
    # O caminho principal (cancelar reservas existentes) funciona corretamente;
    # o defeito só aparece quando o cancelamento ocorre muito próximo ao horário.
    reserva.cancelada = True
    return reserva


def listar_reservas_ativas() -> list[Reserva]:
    """Retorna apenas as reservas não canceladas."""
    return [r for r in _repositorio if not r.cancelada]


def formatar_reserva(reserva: Reserva) -> str:
    status = "cancelada" if reserva.cancelada else "ativa"
    return (
        f"  [{reserva.id}] {reserva.sala} | "
        f"{reserva.inicio:%d/%m %H:%M}–{reserva.fim:%H:%M} | "
        f"{reserva.responsavel} | {status}"
    )


# ─── Execução de demonstração ─────────────────────────────────────────────────

if __name__ == "__main__":
    print("=== Cancelamento de Reserva (exercício — exigência implícita perdida) ===\n")

    data = datetime(2026, 6, 10)

    def dt(hora: int, minuto: int) -> datetime:
        return data.replace(hour=hora, minute=minuto, second=0, microsecond=0)

    # Criar reservas para o dia
    r1 = criar_reserva("Sala A", dt(14, 0), dt(15, 0), "Ana")
    r2 = criar_reserva("Sala B", dt(15, 0), dt(16, 0), "Bob")
    r3 = criar_reserva("Sala C", dt(16, 0), dt(17, 0), "Carlos")

    print("Reservas criadas:")
    for r in listar_reservas_ativas():
        print(formatar_reserva(r))

    print()

    # Cancelamento com 3 horas de antecedência — OK em qualquer política
    agora_cedo = dt(11, 0)
    cancelar_reserva(r1.id, agora_cedo)
    print(f"Cancelamento às {agora_cedo:%H:%M} (3h antes de 14:00):")
    print(formatar_reserva(r1))

    # Cancelamento com 1 hora de antecedência — deveria ser rejeitado (exigência perdida)
    agora_tarde = dt(14, 0)  # exatamente no horário da reserva
    cancelar_reserva(r2.id, agora_tarde)
    print(f"\nCancelamento às {agora_tarde:%H:%M} (no horário da reserva 15:00):")
    print(formatar_reserva(r2))
    print("  ← ACEITO (defeito: deveria exigir 2h de antecedência)")

    # Cancelamento 30 minutos antes — deveria ser rejeitado
    agora_muito_tarde = dt(15, 30)
    cancelar_reserva(r3.id, agora_muito_tarde)
    print(f"\nCancelamento às {agora_muito_tarde:%H:%M} (30min antes de 16:00):")
    print(formatar_reserva(r3))
    print("  ← ACEITO (defeito: deveria exigir 2h de antecedência)")

    print()
    print("Reservas ativas após cancelamentos:")
    reservas = listar_reservas_ativas()
    if reservas:
        for r in reservas:
            print(formatar_reserva(r))
    else:
        print("  (nenhuma)")
