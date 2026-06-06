# Prompt — Gerar endpoint de busca de pedidos com segurança

Este arquivo demonstra **o mesmo objetivo de geração** expresso de dois modos —
sem requisitos de segurança e com requisitos explícitos — para os três modelos
de fronteira.

**Objetivo:** gerar um endpoint `buscar_pedidos(filtros, ordenacao)` que consulta
pedidos por status e cliente, com ordenação configurável pelo chamador.

---

## Sem requisitos de segurança (o problema)

```
Crie uma função Python buscar_pedidos(filtros, ordenacao) que busca pedidos
em um banco SQLite. filtros é um dict com chaves "status" e "cliente_id".
ordenacao é uma string com o nome da coluna para ORDER BY.
Parametrize a query com sqlite3. Retorne lista de dicts.
Use boas práticas e tipagem.
```

**Saída típica:** código limpo, tipado, com `@dataclass` para os filtros,
`sqlite3.connect` com `row_factory`, `cursor.execute` com `?` no `WHERE` —
e `ORDER BY {ordenacao}` por interpolação direta, porque o modelo sabe que
`ORDER BY` não aceita parâmetro posicional na maioria dos drivers.

O `WHERE` parametrizado cria uma falsa sensação de segurança. A linha do
`ORDER BY` fica no mesmo bloco de montagem de query, parecer correta — e
não é. É o que está em `busca_gerado.py`.

---

## Com requisitos de segurança (a solução)

### Claude (Claude Code / Opus 4.8)

O `CLAUDE.md` já está no contexto permanente ao usar Claude Code. Complemente
o prompt com os requisitos de segurança e o padrão esperado:

```
Gere um módulo Python de busca de pedidos, seguindo o padrão do repositório
definido no CLAUDE.md. Use as mesmas convenções de busca_revisado.py (sessão 6):

1. @dataclass FiltroBusca com campos: status, cliente_id (strings).
2. Constante COLUNAS_ORDENACAO_PERMITIDAS com o allow-list de colunas válidas.
3. Função _coluna_ordenacao_segura(ordenacao) que valida contra o allow-list
   e levanta ValueError para qualquer valor fora do conjunto.
4. Função buscar_pedidos(filtros, ordenacao) que parametriza o WHERE com ?
   e usa _coluna_ordenacao_segura antes de qualquer interpolação no ORDER BY.
5. Banco em memória simulado (sem arquivo em disco). Demo com __main__.

REQUISITO DE SEGURANÇA CRÍTICO — não pode ser inferido do contexto:
  ORDER BY não pode ser parametrizado com ? — mas DEVE ser validado por allow-list
  antes de qualquer interpolação. O campo ordenacao vem do usuário externo.
  Nunca interpole ordenacao diretamente na query sem passar por allow-list.
  Se a coluna não estiver no allow-list, levante ValueError imediatamente.

Inclua no demo uma tentativa com ordenacao maliciosa para confirmar que o
ValueError é levantado antes de qualquer interpolação.
```

**Por que funciona:** o requisito de segurança está explícito e separado das
convenções de estilo. O modelo vê o padrão real do repositório e a regra crítica
na mesma mensagem — não precisa inferir que `ordenacao` vem do usuário.

---

### OpenAI (Codex com AGENTS.md)

Configure `AGENTS.md` com as convenções do projeto. Use o turno de declaração
de estratégia antes da geração, da mesma forma que no Tutorial 13:

```
[developer/system message — vai em AGENTS.md ou como system instruction]
You are a Python code generator for a Clean Code workshop (Brazilian Portuguese).
Conventions:
- All identifiers in Brazilian Portuguese (pedido, filtro, status, ordenacao)
- @dataclass for entities — never raw dicts
- Raise ValueError for invalid inputs — never return error objects
- Named constants at module top for all allow-lists and thresholds
- Flat module with free functions, no Repository/Service class layers
- if __name__ == "__main__": block with full print demo

[turno 1 — estratégia de segurança]
Before writing any code, answer in one sentence each:
  a) Can ORDER BY be parameterized with ? in sqlite3?
  b) If ordenacao comes from an external user, what must happen before it is
     interpolated into the query string?
  c) What Python construct will enforce the allow-list?

[turno 2 — implementação]
Now generate buscar_pedidos(filtros, ordenacao) with:
  @dataclass FiltroBusca: status, cliente_id
  COLUNAS_ORDENACAO_PERMITIDAS: frozenset of valid column names
  _coluna_ordenacao_segura(ordenacao: str) -> str  — raises ValueError if invalid
  buscar_pedidos(filtros: FiltroBusca, ordenacao: str) -> list[dict]

CRITICAL: WHERE uses ? parameters. ORDER BY uses _coluna_ordenacao_segura result.
Demo must include a malicious ordenacao to confirm ValueError is raised.
```

**Diferença relevante:** pedir a declaração de estratégia antes do código força
o modelo a explicitar que `ORDER BY` precisa do allow-list. Se o modelo disser
"interpolo diretamente porque ORDER BY não aceita ?", você corrige no turno 1,
antes de receber o código.

---

### Gemini (Gemini CLI com GEMINI.md)

Configure `GEMINI.md` com as convenções. Cole `busca_revisado.py` completo como
few-shot antes do prompt — o Gemini usa a janela de contexto ampla para inferir
o padrão real:

```
# system_instruction (em GEMINI.md):
Você é um gerador de código para um workshop de Clean Code em português.
Siga estas convenções antes de gerar qualquer código:
- Identificadores em português (pedido, filtro, busca, ordenacao)
- @dataclass para entidades — nunca dicts crus
- ValueError para dados inválidos — nunca objetos de resultado
- Constantes nomeadas para allow-lists e limiares
- Funções planas no módulo — sem camadas Repository/Service
- Bloco __main__ com demo de print

# prompt (cole busca_revisado.py inteiro como few-shot antes deste bloco):
Antes de gerar o código, responda em uma frase:
  Qual função valida o campo ordenacao antes de ele ser interpolado na query?

Depois gere buscar_pedidos com:
  @dataclass FiltroBusca: status, cliente_id
  COLUNAS_ORDENACAO_PERMITIDAS: frozenset com colunas válidas
  _coluna_ordenacao_segura(ordenacao) — ValueError se inválida
  buscar_pedidos(filtros, ordenacao) — WHERE com ?, ORDER BY com allow-list

REQUISITO: nenhuma string de usuário toca a query sem passar por allow-list.
Demo com ordenacao maliciosa para confirmar rejeição.
```

**Vantagem:** colar `busca_revisado.py` como few-shot ancora o padrão de allow-list
de forma concreta. O Gemini vê o `_coluna_ordenacao_segura` no código real e
reproduz a estrutura — não precisa inferir o padrão de segurança a partir de
uma descrição textual.

---

## O que muda na aderência

| Aspecto | Sem requisito de segurança | Com requisito explícito |
|---|---|---|
| WHERE parametrizado | Sim (`?`) | Sim (`?`) |
| ORDER BY | Interpolação direta | Allow-list + interpolação |
| Valor malicioso em ordenacao | Chega à query | ValueError antes da query |
| Detecção do defeito | Só com teste focado em ordenacao | Imediata — requisito declarado |
| Iterações para acertar | 2–3 (descoberta + correção) | 1 (correto de primeira) |

**Conclusão:** ambos os prompts produzem código polido e tipado. O `WHERE`
parametrizado aparece nos dois casos — o modelo sabe que `WHERE` precisa de `?`.
A diferença está no `ORDER BY`: sem o requisito explícito, o modelo interpola
porque é o que funciona tecnicamente e é o padrão mais comum na internet.
Com o requisito, ele adiciona o allow-list porque foi instruído a fazê-lo.
