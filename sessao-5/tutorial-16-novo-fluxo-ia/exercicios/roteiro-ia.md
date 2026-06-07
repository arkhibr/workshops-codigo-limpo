# Roteiro Hands-On — Dirigir e Revisar com IA

**Duração estimada:** 25 minutos  
**Objetivo:** comparar a aderência às convenções do projeto ao usar Claude, OpenAI e Gemini,
com e sem o contexto de convenção explícito.

---

## Preparação (5 min)

Antes de usar qualquer modelo, leia rapidamente:

- `CLAUDE.md` (raiz do repositório) — as 5 convenções críticas
- `sessao-1/tutorial-02-funcoes/exemplos/funcoes_boas.py` — padrão de @dataclass e exceções
- `sessao-2/tutorial-06-divida-tecnica/exemplos/divida_depois.py` — constantes nomeadas

Você usará trechos desses arquivos como contexto nos prompts abaixo.

---

## Etapa 1 — Sem contexto de convenção (5 min)

Envie o mesmo pedido genérico para cada modelo:

```
Crie um módulo Python de gerenciamento de categorias de produtos com as operações:
criar, buscar, listar e desativar. O módulo deve rodar e imprimir exemplos de uso.
```

**Anote:** quais convenções o modelo violou? (idioma, estrutura de erro, @dataclass, constantes?)

---

## Etapa 2 — Com contexto de convenção (15 min)

### Claude (Opus 4.8 / Claude Code)

O `CLAUDE.md` já está no contexto automático ao usar Claude Code. Reforce com:

```
Gere um módulo de categorias de produtos em Python seguindo EXATAMENTE o padrão
do repositório definido no CLAUDE.md. Regras que devem aparecer no código:

1. Identificadores em português: variáveis, funções, classes, parâmetros.
2. @dataclass para modelar entidades — não use dicts crus.
3. Exceções explícitas: ValueError para dados inválidos, KeyError para não-encontrado.
   NUNCA retorne {"ok": False} ou {"status": "error"}.
4. Constantes nomeadas no topo: TAMANHO_MINIMO_ID, TAMANHO_MINIMO_NOME, etc.
5. Funções planas no módulo — sem classes Repository ou Service separadas.
6. Bloco if __name__ == "__main__": com demo completo via print.

Operações: criar_categoria, buscar_categoria, listar_categorias, desativar_categoria.
```

Vantagens de Claude Code aqui: `CLAUDE.md` já está no contexto de 1M tokens junto com
todo o código das sessões anteriores. O modelo pode ver os exemplos reais e inferir o padrão.

---

### OpenAI (Codex / ChatGPT com AGENTS.md)

Crie ou edite um arquivo `AGENTS.md` na raiz do projeto com a seção de convenções.
No prompt use a estrutura de mensagens do sistema:

```
[developer/system message]
You are a Python code generator for a Clean Code workshop project.
Follow the project conventions in AGENTS.md exactly.
Key rules:
- All identifiers in Brazilian Portuguese (not English)
- @dataclass for entities, never raw dicts
- Raise ValueError for invalid data, KeyError for not-found
  — NEVER return {"ok": False} or {"status": "error"}
- Named constants at module top for business limits
- Flat module functions, no Repository/Service class layers
- if __name__ == "__main__": block with print demo

[user message]
Generate a categories module: criar_categoria, buscar_categoria,
listar_categorias, desativar_categoria.
Show a complete demo in __main__.
```

Diferença relevante: no Codex, o contexto de convenção vai na mensagem de sistema (`developer`).
Sem esse contexto, o Codex tende ao padrão inglês + classes de serviço.

---

### Gemini (Gemini CLI com GEMINI.md)

Configure o arquivo `GEMINI.md` na raiz com as convenções do projeto.
Use `gemini -p` ou inclua as instruções de sistema:

```
# system_instruction (em GEMINI.md ou --system_instruction):
Você é um gerador de código para um projeto de workshop de Clean Code.
Siga estas convenções do repositório:
- Identificadores em português brasileiro (nunca inglês)
- @dataclass para entidades — nunca dicts crus
- Levante ValueError para dados inválidos e KeyError para não-encontrado
  — nunca retorne objetos de resultado com campos "ok" ou "status"
- Constantes nomeadas no topo para limites de negócio
- Funções planas no módulo — sem camadas Repository/Service
- Bloco __main__ com demo de print ao final

# prompt:
Crie o módulo categorias.py com:
criar_categoria(id, nome, id_pai=None) -> Categoria
buscar_categoria(id) -> Categoria
listar_categorias(apenas_ativas=False) -> list[Categoria]
desativar_categoria(id) -> Categoria
Demo completo em __main__.
```

Vantagem do Gemini: janela de contexto muito ampla — você pode colar múltiplos arquivos
de exemplo completos sem se preocupar com limite de tokens.

---

## Etapa 3 — Comparação e revisão (5 min)

Para cada saída gerada, responda:

| Pergunta de revisão | Claude | OpenAI | Gemini |
|---|---|---|---|
| Identificadores em português? | | | |
| Usa @dataclass? | | | |
| Levanta exceções (não retorna erros)? | | | |
| Tem constantes nomeadas? | | | |
| Módulo plano (sem layers)? | | | |
| Demo em __main__ com print? | | | |

**Reflexão:** o que mudou mais ao dar o contexto de convenção?
Qual modelo aderiu melhor ao padrão do projeto?

---

## Fallback — sem acesso a IA

Se não tiver acesso a nenhum modelo no momento, use o exercício e o gabarito
já prontos:

```bash
python3 sessao-5/tutorial-16-novo-fluxo-ia/exercicios/exercicio.py
python3 sessao-5/tutorial-16-novo-fluxo-ia/exercicios/gabarito.py
```

Compare os dois arquivos e preencha a tabela de revisão acima como se você fosse
o revisor da saída do modelo. As divergências estão documentadas em `gabarito_revisao.md`.
