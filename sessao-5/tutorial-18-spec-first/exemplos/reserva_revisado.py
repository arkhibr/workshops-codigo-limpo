"""
Revisão corrigida — Sistema de Reservas de Sala (gerado a partir da spec.md)
Referência: Tutorial 10 — Spec-first: do requisito ao código verificável
Execute: python3 reserva_revisado.py

Correção em relação a reserva_gerado.py:
  - Regra R1 implementada: sobreposição de horário na mesma sala é detectada e
    rejeitada com ReservaSobrepostaError antes de salvar a reserva.
  - Fórmula de sobreposição: inicio_nova < fim_existente AND fim_nova > inicio_existente
  - Reservas adjacentes (fim == início) não são consideradas sobrepostas.
  - Reservas em salas diferentes são independentes.
  - Demo exercita todos os 6 casos do contrato definido em spec.md.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


# ─── Exceção de domínio ───────────────────────────────────────────────────────

class ReservaSobrepostaError(Exception):
    """Levantada quando uma nova reserva sobrepõe uma reserva existente."""


# ─── Entidade ─────────────────────────────────────────────────────────────────

@dataclass
class Reserva:
    id:           int
    sala:         str
    inicio:       datetime
    fim:          datetime
    responsavel:  str


# ─── Repositório em memória ───────────────────────────────────────────────────

_repositorio: list[Reserva] = []
_proximo_id: int = 1


# ─── Lógica de sobreposição ───────────────────────────────────────────────────

def _reservas_sobrepostas(existente: Reserva, inicio: datetime, fim: datetime) -> bool:
    """
    Retorna True se o intervalo [inicio, fim] se sobrepõe ao intervalo da reserva.

    Fórmula: inicio_nova < fim_existente AND fim_nova > inicio_existente
    Reservas adjacentes (fim_nova == inicio_existente ou vice-versa) não se sobrepõem.
    """
    return inicio < existente.fim and fim > existente.inicio


# ─── Operações ────────────────────────────────────────────────────────────────

def criar_reserva(
    sala:        str,
    inicio:      datetime,
    fim:         datetime,
    responsavel: str,
) -> Reserva:
    """
    Cria uma nova reserva, verificando sobreposição na mesma sala (Regra R1).

    Levanta ReservaSobrepostaError se a sala já estiver reservada no horário.
    Levanta ValueError para campos inválidos ou horário de fim anterior ao início.
    """
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

    # Regra R1: verificar sobreposição de horário na mesma sala
    for reserva in _repositorio:
        if reserva.sala == sala and _reservas_sobrepostas(reserva, inicio, fim):
            raise ReservaSobrepostaError(
                f"{sala} já está reservada das {reserva.inicio:%H:%M} "
                f"às {reserva.fim:%H:%M} por {reserva.responsavel}"
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


def listar_reservas(sala: Optional[str] = None) -> list[Reserva]:
    """
    Retorna as reservas existentes, opcionalmente filtradas por sala.
    """
    if sala is None:
        return list(_repositorio)
    return [r for r in _repositorio if r.sala == sala]


def formatar_reserva(reserva: Reserva) -> str:
    return (
        f"  [{reserva.id}] {reserva.sala} | "
        f"{reserva.inicio:%d/%m %H:%M}–{reserva.fim:%H:%M} | "
        f"{reserva.responsavel}"
    )


# ─── Execução de demonstração ─────────────────────────────────────────────────

if __name__ == "__main__":
    print("=== Reservas de Sala (revisado — spec completa, sobreposição detectada) ===\n")

    data = datetime(2026, 6, 10)

    def dt(hora: int, minuto: int) -> datetime:
        return data.replace(hour=hora, minute=minuto, second=0, microsecond=0)

    # Caso 1 — criação normal (OK)
    r1 = criar_reserva("Sala A", dt(10, 0), dt(11, 0), "Ana")
    print(f"Caso 1 — OK:    {formatar_reserva(r1)}")

    # Caso 2 — sobreposição total (ERRO esperado)
    try:
        criar_reserva("Sala A", dt(10, 30), dt(11, 30), "Bob")
        print("Caso 2 — FALHA: sobreposição deveria ter sido detectada")
    except ReservaSobrepostaError as erro:
        print(f"Caso 2 — OK:    ReservaSobrepostaError: {erro}")

    # Caso 3 — sobreposição parcial no fim (ERRO esperado)
    try:
        criar_reserva("Sala A", dt(9, 30), dt(10, 30), "Carlos")
        print("Caso 3 — FALHA: sobreposição deveria ter sido detectada")
    except ReservaSobrepostaError as erro:
        print(f"Caso 3 — OK:    ReservaSobrepostaError: {erro}")

    # Caso 4 — reserva adjacente após (OK — não sobrepõe)
    r4 = criar_reserva("Sala A", dt(11, 0), dt(12, 0), "Dana")
    print(f"Caso 4 — OK:    {formatar_reserva(r4)}  (adjacente, não sobrepõe)")

    # Caso 5 — sala diferente no mesmo horário (OK)
    r5 = criar_reserva("Sala B", dt(10, 0), dt(11, 0), "Eva")
    print(f"Caso 5 — OK:    {formatar_reserva(r5)}  (sala diferente)")

    # Caso 6 — fim antes do início (ERRO esperado)
    try:
        criar_reserva("Sala A", dt(14, 0), dt(13, 0), "Felipe")
        print("Caso 6 — FALHA: ValueError deveria ter sido levantado")
    except ValueError as erro:
        print(f"Caso 6 — OK:    ValueError: {erro}")

    print()
    print("Reservas confirmadas:")
    for r in listar_reservas():
        print(formatar_reserva(r))
