"""
EXERCÍCIO 22 — Idiom Patterns por Linguagem
Tempo estimado: 20 minutos

INSTRUÇÕES:
  O código abaixo é funcional mas não aproveita os idioms do Python.
  1. Funcionario usa __init__ manual sem validação — converta para @dataclass
     com __post_init__ que valide salario > 0 e nome não vazio.
  2. AbridorArquivo usa abrir()/fechar() com try/finally espalhados
     — implemente __enter__/__exit__ para uso com `with`.
  3. funcionarios_do_departamento() retorna uma lista completa
     — converta para generator com yield.
  4. calcular_total_folha() e calcular_media_salario() duplicam o timing
     — extraia um decorator @medir_tempo.
  Execute: python3 exercicio.py (deve rodar antes e depois)
"""
from typing import List
import time


class Funcionario:
    def __init__(self, id: str, nome: str, departamento: str, salario: float) -> None:
        self.id           = id
        self.nome         = nome
        self.departamento = departamento
        self.salario      = salario
        # sem validação: salario=-500 passa silenciosamente


class AbridorArquivo:
    def abrir(self, caminho: str) -> None:
        print(f"  [Arquivo] abrindo {caminho}")

    def fechar(self) -> None:
        print(f"  [Arquivo] fechado")


def processar_com_arquivo(caminho: str, funcionarios: List[Funcionario]) -> None:
    arq = AbridorArquivo()
    arq.abrir(caminho)
    try:
        for f in funcionarios:
            print(f"  processando {f.nome}")
    finally:
        arq.fechar()   # repetido em todo lugar que usa AbridorArquivo


def funcionarios_do_departamento(funcionarios: List[Funcionario], depto: str) -> List[Funcionario]:
    """Carrega todos antes de processar o primeiro."""
    resultado = []
    for f in funcionarios:
        if f.departamento == depto:
            resultado.append(f)
    return resultado


def calcular_total_folha(funcionarios: List[Funcionario]) -> float:
    inicio = time.time()
    total = sum(f.salario for f in funcionarios)
    fim = time.time()
    print(f"  calcular_total_folha: {(fim-inicio)*1000:.1f}ms")
    return total

def calcular_media_salario(funcionarios: List[Funcionario]) -> float:
    inicio = time.time()                # copiado
    media = sum(f.salario for f in funcionarios) / max(len(funcionarios), 1)
    fim = time.time()                   # copiado
    print(f"  calcular_media_salario: {(fim-inicio)*1000:.1f}ms")
    return media


if __name__ == "__main__":
    funcs = [
        Funcionario("F001", "Ana Silva", "TI", 5000.0),
        Funcionario("F002", "João Costa", "RH", 3500.0),
        Funcionario("F003", "Maria Lima", "TI", 6000.0),
    ]
    processar_com_arquivo("folha.csv", funcs)
    ti = funcionarios_do_departamento(funcs, "TI")
    print(f"TI: {len(ti)} funcionário(s)")
    print(f"Total folha: R${calcular_total_folha(funcs):.2f}")
