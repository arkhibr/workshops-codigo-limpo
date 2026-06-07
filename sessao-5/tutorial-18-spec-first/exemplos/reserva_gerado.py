"""
Saída do modelo de IA (sem spec firme) — Sistema de Reservas de Sala
Referência: Tutorial 10 — Spec-first: do requisito ao código verificável
Execute: python3 reserva_gerado.py

ATENÇÃO: saída de IA sem spec firme — exigência implícita perdida.
O código é limpo, tipado e idiomático: @dataclass, ValueError para entradas
inválidas, repositório em memória, demo com stdout. Cobre o caminho principal
(criar e listar reservas) sem nenhum problema aparente.

Mas a exigência implícita crítica foi perdida: o sistema aceita silenciosamente
duas reservas sobrepostas na mesma sala. O prompt pediu "criar e listar reservas"
— e o modelo fez exatamente isso, sem inferir que sobreposição deveria ser
bloqueada. O defeito não aparece nos casos normais; só quando duas reservas
compartilham sala e horário.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


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


# ─── Operações ────────────────────────────────────────────────────────────────

def criar_reserva(
    sala:        str,
    inicio:      datetime,
    fim:         datetime,
    responsavel: str,
) -> Reserva:
    """
    Cria uma nova reserva e a adiciona ao repositório.

    Levanta ValueError se os campos obrigatórios forem inválidos ou se
    o horário de fim não for após o início.
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

    # ⚠️  DEFEITO: não verifica sobreposição de horário na mesma sala.
    # A exigência implícita — "não permitir reservas sobrepostas" — foi perdida
    # porque o prompt informal não a mencionava explicitamente. O modelo gerou
    # o caminho principal (criar → salvar) sem inferir a restrição de negócio.
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
    print("=== Reservas de Sala (saída do modelo — exigência implícita perdida) ===\n")

    data = datetime(2026, 6, 10)

    def dt(hora: int, minuto: int) -> datetime:
        return data.replace(hour=hora, minute=minuto, second=0, microsecond=0)

    # Reserva normal — OK
    r1 = criar_reserva("Sala A", dt(10, 0), dt(11, 0), "Ana")
    print(f"Criada: {formatar_reserva(r1)}")

    # Reserva sobreposta — deveria ser rejeitada, mas é aceita silenciosamente
    r2 = criar_reserva("Sala A", dt(10, 30), dt(11, 30), "Bob")
    print(f"Criada: {formatar_reserva(r2)}  ← SOBREPOSIÇÃO ACEITA (defeito)")

    # Reserva em sala diferente — OK
    r3 = criar_reserva("Sala B", dt(10, 0), dt(11, 0), "Carlos")
    print(f"Criada: {formatar_reserva(r3)}")

    print()
    print("Reservas em Sala A:")
    for r in listar_reservas("Sala A"):
        print(formatar_reserva(r))

    print()
    print("Caso crítico — sobreposição aceita silenciosamente:")
    print("  Sala A 10:00–11:00 (Ana) e Sala A 10:30–11:30 (Bob)")
    print("  Ambas estão no repositório — conflito não detectado.")
    print("  Um participante chegará à Sala A e encontrará outra reunião.")
