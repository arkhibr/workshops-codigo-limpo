# Prompt — Gerar serviço de catálogo de produtos

Este arquivo demonstra **o mesmo objetivo de geração** expresso para os três modelos
de fronteira, mostrando como dar o contexto de convenção em cada plataforma.

**Objetivo:** gerar um serviço de catálogo de produtos seguindo o padrão do projeto.

---

## Sem contexto de convenção (o problema)

```
Crie um serviço Python de catálogo de produtos com operações de cadastro,
busca e listagem. Use boas práticas.
```

**Saída típica:** classes `ProductRepository` e `CatalogService`, identificadores
em inglês, retorno de dicionários `{"success": True, "data": ...}`.
O código é limpo — mas fora do padrão do projeto. É o que está em `catalogo_gerado.py`.

---

## Com contexto de convenção (a solução)

### Claude (Opus 4.8 / Claude Code)

O `CLAUDE.md` já está no contexto permanente ao usar Claude Code. Complemente o prompt
com um trecho dos exemplos existentes para ancorar o padrão:

```
Gere um módulo de catálogo de produtos em Python seguindo EXATAMENTE o padrão
do repositório definido no CLAUDE.md. Aplique as convenções que vejo em
funcoes_boas.py e divida_depois.py:

1. Identificadores em português: produto, preco, categoria, cadastrar_produto, etc.
2. @dataclass para modelar entidades — como DadosUsuario em funcoes_boas.py.
3. Levante exceções: ValueError para dados inválidos, KeyError para não-encontrado.
   NUNCA retorne dicionários {"ok": False} ou {"success": False, "error": ...}.
4. Constantes nomeadas no topo para limites: PRECO_MINIMO, TAMANHO_MINIMO_NOME.
5. Funções planas no módulo — sem classes Repository ou Service separadas.
6. Bloco if __name__ == "__main__": com demo de stdout.

Operações: cadastrar_produto, buscar_produto, listar_produtos, atualizar_preco.
```

**Por que funciona:** Claude Code lê o `CLAUDE.md` e todo o código das sessões
anteriores no contexto de 1M tokens. O trecho de exemplo ancora o padrão de forma
concreta — o modelo vê o código real, não uma descrição abstrata.

---

### OpenAI (Codex com AGENTS.md)

O Codex usa `AGENTS.md` como arquivo de instrução permanente. Crie ou edite
`AGENTS.md` na raiz com as convenções do projeto. No prompt:

```
[developer message — instrução de sistema para o agente]
You are a code generator for a Brazilian Portuguese Clean Code workshop project.
Follow the conventions in AGENTS.md:
- All identifiers in Brazilian Portuguese: produto, preco, categoria
- @dataclass for entities — never raw dicts or plain classes without dataclass
- Raise ValueError for invalid inputs, KeyError for not-found errors
  — NEVER return {"success": False} or {"status": "error"} objects
- Named constants at module top: PRECO_MINIMO, TAMANHO_MINIMO_NOME
- Flat module with free functions, no Repository/Service class hierarchy
- if __name__ == "__main__": block that prints a complete demo

[user message]
Generate a product catalog module: cadastrar_produto, buscar_produto,
listar_produtos, atualizar_preco. Full __main__ demo with print output.
```

**Diferença relevante:** o contexto de convenção vai na mensagem `developer` (system),
não no `user`. Isso dá mais peso ao padrão e reduz a chance de o modelo "esquecer"
as regras quando o pedido concreto aparecer. Sem `AGENTS.md`, o Codex tende a gerar
o padrão inglês + classes de serviço.

---

### Gemini (Gemini CLI com GEMINI.md)

O Gemini CLI usa `GEMINI.md` como arquivo de instrução de sistema. Configure-o
na raiz do projeto. No prompt ou como `--system_instruction`:

```
# Em GEMINI.md (system_instruction):
Você é um gerador de código para um workshop de Clean Code em português.
Siga estas convenções antes de gerar qualquer código:
- Identificadores em português: produto, preco, categoria, cadastrar, buscar
- @dataclass para entidades em Python — nunca dicts crus
- Levante ValueError para dados inválidos, KeyError para não-encontrado
  — nunca retorne {"ok": False} ou {"status": "error"}
- Constantes nomeadas no topo do arquivo para limites de negócio
- Funções livres no módulo — sem hierarquia Repository/Service
- Bloco __main__ com demo de print ao final

# Prompt do usuário:
Crie o módulo catalogo.py com:
  cadastrar_produto(id, nome, preco, categoria) -> Produto
  buscar_produto(id) -> Produto
  listar_produtos(categoria=None) -> list[Produto]
  atualizar_preco(id, novo_preco) -> Produto
Demo completo em __main__ que exercita todos os fluxos, incluindo erros.
```

**Vantagem:** a janela de contexto do Gemini é muito ampla — você pode colar
múltiplos arquivos de exemplo completos (`funcoes_boas.py`, `divida_depois.py`)
diretamente no prompt sem se preocupar com limite de tokens. Isso ancora o padrão
de forma ainda mais concreta do que uma descrição textual.

---

## O que muda na aderência

| Aspecto | Sem contexto | Com contexto (qualquer modelo) |
|---|---|---|
| Idioma dos identificadores | Inglês (padrão da internet) | Português (domínio do projeto) |
| Mecanismo de erro | Objetos de resultado (`{"ok": False}`) | Exceções explícitas |
| Modelagem de entidade | Classe com `__init__` manual ou dict | `@dataclass` |
| Limites de negócio | Magic values inline | Constantes nomeadas |
| Estrutura | Repository + Service layers | Funções planas no módulo |

**Conclusão:** a qualidade da saída não depende só do modelo — depende de quem o dirige.
Dar o contexto de convenção é a diferença entre código limpo genérico e código alinhado
ao projeto.
