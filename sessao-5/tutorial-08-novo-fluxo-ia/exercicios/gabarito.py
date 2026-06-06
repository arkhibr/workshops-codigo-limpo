"""
GABARITO — Tutorial 08: O novo fluxo: dirigir e revisar
Referência: Tutorial 08 — O novo fluxo: dirigir e revisar
Execute: python3 gabarito.py

Versão alinhada às convenções do projeto. Consulte gabarito_revisao.md para
a tabela de divergências e o prompt com contexto de convenção sugerido.

Divergências corrigidas:
  - @dataclass em vez de dicionários crus para modelar a entidade
  - Exceções explícitas (ValueError, KeyError) em vez de objetos de resultado
  - Constantes nomeadas para limites e valores de domínio
  - Identificadores 100 % em português (categoria, id_categoria, etc.)
  - Sem classe de serviço separada — funções planas no módulo
"""

from dataclasses import dataclass
from typing import Optional


# ─── Constantes de domínio ────────────────────────────────────────────────────

TAMANHO_MINIMO_ID = 3
TAMANHO_MINIMO_NOME = 2


# ─── Entidade ─────────────────────────────────────────────────────────────────

@dataclass
class Categoria:
    id:         str
    nome:       str
    id_pai:     Optional[str]
    ativa:      bool = True


# ─── Estado em memória ────────────────────────────────────────────────────────

_categorias: dict[str, Categoria] = {}


# ─── Operações de categorias ──────────────────────────────────────────────────

def criar_categoria(
    id: str,
    nome: str,
    id_pai: Optional[str] = None,
) -> Categoria:
    """Cria e registra uma categoria. Levanta ValueError ou KeyError conforme o caso."""
    if not id or len(id) < TAMANHO_MINIMO_ID:
        raise ValueError(f"ID da categoria deve ter ao menos {TAMANHO_MINIMO_ID} caracteres")
    if not nome or len(nome) < TAMANHO_MINIMO_NOME:
        raise ValueError(f"Nome da categoria deve ter ao menos {TAMANHO_MINIMO_NOME} caracteres")
    if id in _categorias:
        raise ValueError(f"Categoria '{id}' já existe")
    if id_pai and id_pai not in _categorias:
        raise KeyError(f"Categoria pai '{id_pai}' não encontrada")

    categoria = Categoria(id=id, nome=nome, id_pai=id_pai)
    _categorias[id] = categoria
    return categoria


def buscar_categoria(id: str) -> Categoria:
    """Retorna a categoria pelo ID. Levanta KeyError se não encontrada."""
    if id not in _categorias:
        raise KeyError(f"Categoria '{id}' não encontrada")
    return _categorias[id]


def listar_categorias(apenas_ativas: bool = False) -> list[Categoria]:
    """Lista todas as categorias, com opção de filtrar apenas as ativas."""
    todas = list(_categorias.values())
    if apenas_ativas:
        return [c for c in todas if c.ativa]
    return todas


def desativar_categoria(id: str) -> Categoria:
    """Desativa uma categoria. Levanta KeyError se não encontrada."""
    categoria = buscar_categoria(id)
    categoria.ativa = False
    return categoria


# ─── Execução de demonstração ─────────────────────────────────────────────────

if __name__ == "__main__":
    print("=== Módulo de Categorias (gabarito — alinhado às convenções do projeto) ===\n")

    c1 = criar_categoria("CAT01", "Eletrônicos")
    print("Categoria criada:", c1)

    c2 = criar_categoria("CAT02", "Informática", id_pai="CAT01")
    print("Categoria criada (filha):", c2)

    try:
        criar_categoria("", "Sem ID")
    except ValueError as erro:
        print(f"\nErro esperado no cadastro: {erro}")

    encontrada = buscar_categoria("CAT01")
    print("\nBusca por CAT01:", encontrada)

    try:
        buscar_categoria("X999")
    except KeyError as erro:
        print(f"Erro esperado na busca: {erro}")

    todas = listar_categorias()
    print(f"\nTodas as categorias ({len(todas)}):", todas)

    desativada = desativar_categoria("CAT02")
    print("\nCategoria desativada:", desativada)

    ativas = listar_categorias(apenas_ativas=True)
    print(f"Apenas ativas ({len(ativas)}):", ativas)
