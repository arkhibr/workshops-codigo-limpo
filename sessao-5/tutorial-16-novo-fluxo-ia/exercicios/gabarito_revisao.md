# Gabarito — Revisão de Convenção do Projeto

## Divergências encontradas no exercício (tabela)

| # | Divergência | No exercício (`exercicio.py/.ts`) | Padrão do projeto |
|---|---|---|---|
| 1 | **Mecanismo de erro** | Retorna `{"status": "error", "message": ...}` | Levanta exceções (`ValueError`, `KeyError` / `Error`) |
| 2 | **Modelagem de entidade** | Dicionário cru (`dict`) ou interface anônima | `@dataclass` em Python; `interface` nomeada em PT no TS |
| 3 | **Identificadores** | Inglês: `id`, `name`, `parentId`, `active`, `CategoryService` | Português: `id`, `nome`, `id_pai`/`idPai`, `ativa`, funções planas |
| 4 | **Constantes nomeadas** | Magic values inline (`True`, `False`, comprimentos hardcoded) | Constantes no topo: `TAMANHO_MINIMO_ID`, `TAMANHO_MINIMO_NOME` |
| 5 | **Estrutura do módulo** | Classe `CategoryService` com estado privado | Funções planas + estado global em memória no módulo |
| 6 | **Nomes de funções** | `create`, `get`, `listAll`, `deactivate` (inglês) | `criar_categoria`, `buscar_categoria`, `listar_categorias`, `desativar_categoria` (PT) |

---

## Prompt com contexto de convenção (sugerido)

### Para Claude (Opus 4.8 / Claude Code)

O arquivo `CLAUDE.md` já está no contexto. Complemente o prompt com um trecho de exemplo:

```
Gere um módulo de categorias de produtos em Python seguindo EXATAMENTE o padrão
do repositório. Regras obrigatórias extraídas do CLAUDE.md e dos exemplos:

1. Identificadores em português: variáveis, funções, classes, parâmetros.
2. Use @dataclass para modelar entidades (exemplo em funcoes_boas.py:
   @dataclass class DadosUsuario).
3. Levante exceções explícitas (ValueError, KeyError) — NUNCA retorne
   dicionários de erro como {"ok": False, "msg": ...}.
4. Defina constantes nomeadas no topo do arquivo para qualquer limite
   de negócio (exemplo: TAMANHO_MINIMO_SENHA = 8).
5. Módulo plano com funções livres e estado em dicionário — sem camadas
   Repository/Service separadas.
6. Bloco if __name__ == "__main__": ao final com demo de stdout.

Objetivo: módulo de categorias com criar_categoria, buscar_categoria,
listar_categorias e desativar_categoria.
```

### Para OpenAI (Codex / ChatGPT com AGENTS.md)

```
System (developer message):
You are a Python code generator. Follow the project conventions in AGENTS.md exactly.
Key rules from AGENTS.md:
- All identifiers in Brazilian Portuguese
- Use @dataclass for entities, never raw dicts
- Raise ValueError/KeyError for errors — never return error dicts
- Named constants at module top for any business limit
- Flat module functions, no Repository/Service layers

User:
Generate a categories module with: criar_categoria, buscar_categoria,
listar_categorias, desativar_categoria.
Include a __main__ block that demos all operations with print output.
```

### Para Gemini (Gemini CLI com GEMINI.md)

```
# system_instruction (em GEMINI.md):
Este projeto segue convenções estritas definidas no repositório.
Identifique e aplique cada uma antes de gerar código:
- Identificadores em português brasileiro
- @dataclass para entidades
- Exceções (ValueError, KeyError) para erros, nunca objetos de resultado
- Constantes nomeadas para limites de negócio
- Funções planas no módulo, sem classes de serviço separadas

# prompt:
Crie o módulo `categorias.py` com as operações:
criar_categoria(id, nome, id_pai=None) -> Categoria
buscar_categoria(id) -> Categoria
listar_categorias(apenas_ativas=False) -> list[Categoria]
desativar_categoria(id) -> Categoria

Inclua bloco __main__ que demonstra todas as operações via print.
```

---

## O que muda na aderência com o contexto de convenção

Sem o contexto de convenção, os três modelos tendem a:
- Usar inglês nos identificadores (padrão global da internet)
- Retornar objetos de resultado (padrão "Railway-Oriented")
- Criar classes de serviço (padrão enterprise popular em exemplos de treinamento)

Com o contexto de convenção explícito, a saída converge para o padrão do projeto.
A diferença não está no modelo — está em **quem dirige o modelo**.
