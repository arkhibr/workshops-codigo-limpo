"""
gabarito.py — Solução do Exercício 22: Idiom Patterns
Execute: python3 gabarito.py
"""
from typing import List, Generator
from dataclasses import dataclass
import time
import functools


# ─── Idiom 1: @dataclass com __post_init__ ───────────────────────────────────

@dataclass
class Funcionario:
    id:            str
    nome:          str
    departamento:  str
    salario:       float

    def __post_init__(self) -> None:
        if self.salario <= 0:
            raise ValueError(f"salario deve ser positivo, recebido: {self.salario}")
        if not self.nome.strip():
            raise ValueError("nome não pode ser vazio")


# ─── Idiom 2: Context manager ────────────────────────────────────────────────

class AbridorArquivo:
    def __init__(self, caminho: str) -> None:
        self._caminho = caminho

    def __enter__(self) -> "AbridorArquivo":
        print(f"  [Arquivo] abrindo {self._caminho}")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        print(f"  [Arquivo] fechado (garantido)")
        return False


# ─── Idiom 3: Generator ───────────────────────────────────────────────────────

def funcionarios_do_departamento(funcionarios: List[Funcionario], depto: str) -> Generator[Funcionario, None, None]:
    for f in funcionarios:
        if f.departamento == depto:
            yield f


# ─── Idiom 4: Decorator ───────────────────────────────────────────────────────

def medir_tempo(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        inicio = time.perf_counter()
        resultado = func(*args, **kwargs)
        elapsed = (time.perf_counter() - inicio) * 1000
        print(f"  {func.__name__}: {elapsed:.2f}ms")
        return resultado
    return wrapper

@medir_tempo
def calcular_total_folha(funcionarios: List[Funcionario]) -> float:
    return sum(f.salario for f in funcionarios)

@medir_tempo
def calcular_media_salario(funcionarios: List[Funcionario]) -> float:
    return sum(f.salario for f in funcionarios) / max(len(funcionarios), 1)


# ─── Verificação ──────────────────────────────────────────────────────────────

def verificar_gabarito() -> None:
    # @dataclass com validação
    f = Funcionario("F001", "Ana Silva", "TI", 5000.0)
    assert f.salario == 5000.0
    print("OK: @dataclass — Funcionario criado com validação em __post_init__")

    try:
        Funcionario("F999", "Inválido", "RH", -100.0)
        print("FALHOU: @dataclass — deveria rejeitar salario negativo")
    except ValueError:
        print("OK: @dataclass — rejeita salario negativo")

    # Context manager
    funcs = [Funcionario("F001", "Ana Silva", "TI", 5000.0)]
    with AbridorArquivo("folha.csv") as arq:
        for f in funcs:
            print(f"  processando {f.nome}")
    print("OK: Context manager — AbridorArquivo fechado automaticamente")

    # Generator
    todos = [
        Funcionario("F001", "Ana Silva", "TI", 5000.0),
        Funcionario("F002", "João Costa", "RH", 3500.0),
        Funcionario("F003", "Maria Lima", "TI", 6000.0),
    ]
    ti = list(funcionarios_do_departamento(todos, "TI"))
    assert len(ti) == 2
    print(f"OK: Generator — funcionarios_do_departamento('TI') retornou {len(ti)} sob demanda")

    # Decorator
    total = calcular_total_folha(todos)
    assert total == 14500.0
    print(f"OK: @medir_tempo — calcular_total_folha decorado sem alterar assinatura (total=R${total:.2f})")

    media = calcular_media_salario(todos)
    assert abs(media - 14500.0 / 3) < 0.01
    print(f"OK: @medir_tempo — calcular_media_salario decorado (média=R${media:.2f})")


if __name__ == "__main__":
    print("=== Gabarito 22 — Idiom Patterns: Folha de Pagamento ===\n")
    verificar_gabarito()
