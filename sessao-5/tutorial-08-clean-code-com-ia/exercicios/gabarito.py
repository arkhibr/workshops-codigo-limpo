"""
GABARITO — Lista de espera da clínica (versão refatorada)
Referência: Clean Code, Cap. 2–3 aplicados a código assistido por IA

Problemas corrigidos em relação ao exercício:
  - Nomes descritivos em português para todos os identificadores
  - Estrutura de dados tipada (dataclass) em vez de dict com chaves vagas
  - Constante nomeada para a posição inicial do contador
  - Violação de CQS corrigida: adicionar não retorna o ID
  - Built-in `id` não mais sobrescrito
  - Remoção de paciente inexistente lança exceção com mensagem clara
  - Responsabilidade de "chamar próximo" separada em função coesa

Execute: python3 sessao-5/tutorial-08-clean-code-com-ia/exercicios/gabarito.py
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime

POSICAO_INICIAL = 1  # posição inicial do contador de entradas na fila


@dataclass
class EntradaFila:
    posicao: int
    nome_paciente: str
    tipo_atendimento: str
    registrado_em: str = field(default_factory=lambda: datetime.now().isoformat())
    atendido: bool = False


# repositório em memória
_lista_de_espera: list[EntradaFila] = []
_proximo_numero: int = POSICAO_INICIAL


def adicionar_na_fila(nome_paciente: str, tipo_atendimento: str) -> None:
    """Adiciona o paciente ao final da lista de espera."""
    global _proximo_numero
    entrada = EntradaFila(
        posicao=_proximo_numero,
        nome_paciente=nome_paciente,
        tipo_atendimento=tipo_atendimento,
    )
    _lista_de_espera.append(entrada)
    _proximo_numero += 1


def remover_da_fila(posicao: int) -> None:
    """Remove o paciente da lista de espera pela posição. Lança ValueError se não encontrado."""
    for i, entrada in enumerate(_lista_de_espera):
        if entrada.posicao == posicao:
            _lista_de_espera.pop(i)
            return
    raise ValueError(f"Nenhum paciente encontrado na posição {posicao}.")


def exibir_lista_de_espera() -> None:
    """Exibe o estado atual da lista de espera no console."""
    for entrada in _lista_de_espera:
        marcador = "✓" if entrada.atendido else "·"
        print(
            f"[{marcador}] #{entrada.posicao} "
            f"{entrada.nome_paciente} ({entrada.tipo_atendimento})"
        )


def _proxima_entrada_pendente() -> EntradaFila | None:
    """Retorna a primeira entrada ainda não atendida, ou None se a fila estiver vazia."""
    return next((e for e in _lista_de_espera if not e.atendido), None)


def chamar_proximo_paciente() -> EntradaFila:
    """
    Marca o próximo paciente pendente como atendido e o retorna.
    Lança RuntimeError se não houver pacientes aguardando.
    """
    entrada = _proxima_entrada_pendente()
    if entrada is None:
        raise RuntimeError("Não há pacientes aguardando na fila de espera.")
    entrada.atendido = True
    return entrada


# ─── Execução de demonstração ─────────────────────────────────────────────────

if __name__ == "__main__":
    adicionar_na_fila("Maria Oliveira", "retorno")
    adicionar_na_fila("João Costa", "primeira consulta")
    adicionar_na_fila("Beatriz Ferreira", "exame")

    print("=== Lista de espera ===")
    exibir_lista_de_espera()

    print("\nChamando próximo paciente...")
    proximo = chamar_proximo_paciente()
    print(f"Chamado: {proximo.nome_paciente} ({proximo.tipo_atendimento})")

    print("\n=== Lista atualizada ===")
    exibir_lista_de_espera()

    # remove um paciente da fila
    remover_da_fila(2)
    print("\n=== Após remover posição 2 ===")
    exibir_lista_de_espera()

    # tenta remover posição inexistente — deve lançar exceção
    try:
        remover_da_fila(99)
    except ValueError as erro:
        print(f"\nErro esperado: {erro}")
