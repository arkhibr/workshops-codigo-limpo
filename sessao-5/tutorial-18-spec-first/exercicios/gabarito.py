"""
Gabarito — Cancelamento de Reserva (gerado a partir da spec com exigência fixada)
Referência: Tutorial 10 — Spec-first: do requisito ao código verificável
Execute: python3 gabarito.py

Correção em relação a exercicio.py:
  - Regra de antecedência mínima implementada: cancelamento só permitido com
    pelo menos 2 horas de antecedência em relação ao início da reserva.
  - Se antecedência < 2 horas, levanta CancelamentoForaDoPrazoError com mensagem
    descritiva informando o tempo restante e o prazo exigido.
  - Demo exercita os casos de fronteira: exatamente 2h (OK), menos de 2h (ERRO).
"""

from dataclasses import dataclass
from datetime import datetime, timedelta


# ─── Constantes de domínio ────────────────────────────────────────────────────

ANTECEDENCIA_MINIMA_CANCELAMENTO = timedelta(hours=2)


# ─── Exceções de domínio ─────────────────────────────────────────────────────

class ReservaNaoEncontradaError(Exception):
    """Levantada quando o id de reserva não existe ou já foi cancelada."""


class CancelamentoForaDoPrazoError(Exception):
    """Levantada quando o cancelamento ocorre com menos de 2h de antecedência."""


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
    Cancela a reserva, respeitando a antecedência mínima de 2 horas.

    Levanta ReservaNaoEncontradaError se o id não existir ou já cancelada.
    Levanta CancelamentoForaDoPrazoError se antecedência < 2 horas.
    """
    reserva = next(
        (r for r in _repositorio if r.id == id_reserva and not r.cancelada),
        None,
    )
    if reserva is None:
        raise ReservaNaoEncontradaError(
            f"Reserva {id_reserva} não encontrada ou já cancelada"
        )

    antecedencia = reserva.inicio - agora
    if antecedencia < ANTECEDENCIA_MINIMA_CANCELAMENTO:
        horas_restantes = antecedencia.total_seconds() / 3600
        raise CancelamentoForaDoPrazoError(
            f"Cancelamento não permitido: faltam {horas_restantes:.1f}h para o início "
            f"da reserva (mínimo exigido: "
            f"{int(ANTECEDENCIA_MINIMA_CANCELAMENTO.total_seconds() // 3600)}h)"
        )

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
    print("=== Cancelamento de Reserva (gabarito — exigência de antecedência fixada) ===\n")

    data = datetime(2026, 6, 10)

    def dt(hora: int, minuto: int) -> datetime:
        return data.replace(hour=hora, minute=minuto, second=0, microsecond=0)

    # Criar reservas para o dia
    r1 = criar_reserva("Sala A", dt(14, 0), dt(15, 0), "Ana")
    r2 = criar_reserva("Sala B", dt(15, 0), dt(16, 0), "Bob")
    r3 = criar_reserva("Sala C", dt(16, 0), dt(17, 0), "Carlos")
    r4 = criar_reserva("Sala D", dt(17, 0), dt(18, 0), "Dana")

    print("Reservas criadas:")
    for r in listar_reservas_ativas():
        print(formatar_reserva(r))
    print()

    # Caso 1 — cancelamento com 3h de antecedência (OK)
    agora = dt(11, 0)
    cancelar_reserva(r1.id, agora)
    print(f"Caso 1 — OK: cancelamento às {agora:%H:%M} (3h antes de 14:00)")
    print(formatar_reserva(r1))

    # Caso 2 — cancelamento exatamente com 2h de antecedência (OK — no limite)
    agora = dt(13, 0)
    cancelar_reserva(r2.id, agora)
    print(f"\nCaso 2 — OK: cancelamento às {agora:%H:%M} (exatamente 2h antes de 15:00)")
    print(formatar_reserva(r2))

    # Caso 3 — cancelamento com 1h30min de antecedência (ERRO — fora do prazo)
    agora = dt(14, 30)
    try:
        cancelar_reserva(r3.id, agora)
        print(f"\nCaso 3 — FALHA: deveria ter sido rejeitado")
    except CancelamentoForaDoPrazoError as erro:
        print(f"\nCaso 3 — OK: CancelamentoForaDoPrazoError: {erro}")

    # Caso 4 — cancelamento no próprio horário (ERRO — fora do prazo)
    agora = dt(17, 0)
    try:
        cancelar_reserva(r4.id, agora)
        print(f"\nCaso 4 — FALHA: deveria ter sido rejeitado")
    except CancelamentoForaDoPrazoError as erro:
        print(f"\nCaso 4 — OK: CancelamentoForaDoPrazoError: {erro}")

    print()
    print("Reservas ativas após cancelamentos:")
    reservas = listar_reservas_ativas()
    if reservas:
        for r in reservas:
            print(formatar_reserva(r))
    else:
        print("  (nenhuma)")
