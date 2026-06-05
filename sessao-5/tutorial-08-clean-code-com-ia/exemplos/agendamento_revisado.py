"""
VERSÃO REVISADA — agendamento de consultas após revisão de código gerado por IA
Referência: Clean Code, Cap. 2–3

Problemas corrigidos em relação à versão gerada:
  - Nomes descritivos em português para todos os identificadores
  - Parâmetros soltos substituídos por dataclass
  - Número mágico extraído como constante nomeada
  - Validação de conflito de horário em função própria
  - Código de erro substituído por exceção com mensagem clara
  - Idioma consistente (sem mistura PT/EN)

Execute: python3 sessao-5/tutorial-08-clean-code-com-ia/exemplos/agendamento_revisado.py
"""

from __future__ import annotations

from dataclasses import dataclass

DURACAO_PADRAO_MIN = 30  # duração padrão de consulta em minutos


@dataclass
class Consulta:
    data: str          # formato "AAAA-MM-DD"
    horario: str       # formato "HH:MM"
    nome_paciente: str
    duracao_min: int = DURACAO_PADRAO_MIN
    status: str = "confirmada"


# repositório em memória (simula banco de dados)
_consultas_agendadas: list[Consulta] = []


def _existe_conflito(data: str, nome_paciente: str) -> bool:
    """Verifica se o paciente já tem consulta agendada na data informada."""
    return any(
        c.data == data and c.nome_paciente == nome_paciente
        for c in _consultas_agendadas
    )


def agendar_consulta(data: str, horario: str, nome_paciente: str) -> Consulta:
    """
    Agenda uma consulta para o paciente na data e horário indicados.

    Lança ValueError se o paciente já tiver consulta agendada na mesma data.
    """
    if _existe_conflito(data, nome_paciente):
        raise ValueError(
            f"Paciente '{nome_paciente}' já possui consulta agendada em {data}."
        )

    nova_consulta = Consulta(
        data=data,
        horario=horario,
        nome_paciente=nome_paciente,
    )
    _consultas_agendadas.append(nova_consulta)
    return nova_consulta


def consultas_do_paciente(nome_paciente: str) -> list[Consulta]:
    """Retorna todas as consultas agendadas para o paciente informado."""
    return [c for c in _consultas_agendadas if c.nome_paciente == nome_paciente]


# ─── Execução de demonstração ─────────────────────────────────────────────────

if __name__ == "__main__":
    c1 = agendar_consulta("2026-07-10", "09:00", "Ana Lima")
    print("Agendamento 1:", c1)

    # tenta agendar o mesmo paciente no mesmo dia — deve lançar exceção
    try:
        c2 = agendar_consulta("2026-07-10", "14:00", "Ana Lima")
    except ValueError as erro:
        print(f"Conflito detectado: {erro}")

    # agendamento em dia diferente — deve funcionar
    c3 = agendar_consulta("2026-07-11", "10:30", "Carlos Souza")
    print("Agendamento 3:", c3)

    print("\nConsultas de Ana Lima:", consultas_do_paciente("Ana Lima"))
