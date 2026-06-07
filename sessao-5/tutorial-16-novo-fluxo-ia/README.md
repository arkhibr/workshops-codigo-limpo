# Tutorial 16 — O novo fluxo: dirigir e revisar

> Referência: *Clean Code*, Cap. 1–2; engenharia de contexto com modelos de fronteira

---

## 1. Contexto e Motivação

Em 2026, os modelos de fronteira — Claude Opus 4.8, OpenAI Codex, Gemini — geram código
limpo, tipado e idiomático por padrão. O problema deixou de ser "o modelo sabe escrever
código bom?" e passou a ser "o modelo sabe escrever código bom *para este projeto*?"

Um modelo sem contexto inventa suas próprias convenções. Ele usa inglês porque a maioria
do código na internet está em inglês. Ele retorna objetos de resultado `{"ok": False}`
porque esse padrão aparece em milhares de tutoriais. Ele cria camadas `Repository` e
`Service` porque é um padrão popular em exemplos enterprise. O código resultante é limpo
em isolamento — mas inconsistente com a base existente.

> *"The ratio of time spent reading versus writing is well over 10 to 1."*
> — Robert C. Martin, *Clean Code*, Cap. 1

Quando a IA amplifica esse padrão — gerando centenas de linhas por minuto — a inconsistência
se multiplica na mesma velocidade. Código limpo importa *mais* na era da IA, não menos:
se você não dá a convenção, o modelo inventa uma, e cada dev na equipe recebe uma versão
diferente do mesmo padrão.

O papel do desenvolvedor sênior mudou: de **escritor** para **diretor e revisor**. Você
define o contexto, dirige a geração e revisa em altitude — verificando aderência ao padrão
do projeto, não apenas correção sintática.

---

## 2. Conceito Central

### Arquivos de convenção como contexto permanente

Cada plataforma de IA tem um arquivo que funciona como instrução permanente para o modelo:

| Plataforma | Arquivo de convenção |
|---|---|
| Claude Code | `CLAUDE.md` (lido automaticamente em toda sessão) |
| OpenAI Codex | `AGENTS.md` (instrução de sistema do agente) |
| Gemini CLI | `GEMINI.md` (system instruction) |

Esses arquivos transformam o modelo de um gerador genérico em um colaborador que conhece
o seu projeto. Sem eles, o modelo gera código limpo por padrão mundial. Com eles, gera
código alinhado ao padrão da sua base.

### O mesmo pedido, dois resultados diferentes

**Sem contexto de convenção:**

```python
# Prompt: "Crie um serviço de catálogo de produtos com boas práticas."
# Saída típica do modelo (limpa, mas fora do padrão):

class CatalogService:
    def add_product(self, id: str, name: str, price: float) -> dict:
        if price < 0:
            return {"success": False, "error": "Price cannot be negative"}
        product = {"id": id, "name": name, "price": price}
        self._store[id] = product
        return {"success": True, "data": product}
```

O código é idiomático. Mas viola quatro convenções do repositório de uma vez:
identificadores em inglês, retorno de dicionários de erro, classe de serviço,
ausência de `@dataclass`.

**Com contexto de convenção:**

```python
# Prompt com CLAUDE.md no contexto + trecho de funcoes_boas.py como âncora:
# "Siga o padrão do CLAUDE.md: PT, @dataclass, ValueError, constantes nomeadas."

@dataclass
class Produto:
    id:        str
    nome:      str
    preco:     float
    categoria: str

def cadastrar_produto(id: str, nome: str, preco: float, categoria: str) -> Produto:
    if preco < PRECO_MINIMO:
        raise ValueError("Preço não pode ser negativo")
    produto = Produto(id=id, nome=nome, preco=preco, categoria=categoria)
    _produtos[id] = produto
    return produto
```

Mesmo objetivo, output alinhado ao projeto. A diferença está no contexto dado ao modelo,
não no modelo em si.

### Revisão em altitude

Revisar saída de IA não é revisar linha a linha — é verificar aderência ao padrão em
três perguntas de altitude:

1. **Idioma:** todos os identificadores estão em português?
2. **Estrutura de erro:** o módulo levanta exceções ou retorna objetos de resultado?
3. **Modelagem:** usa `@dataclass` para entidades? Constantes nomeadas para limites?

Se a resposta for "não" em qualquer uma, o prompt precisava de mais contexto de convenção
— não de correção manual linha a linha. Corrija o prompt, regenere.

---

## 3. Exercício

**Contexto:** o arquivo `exercicios/exercicio.py` (e `.ts`) contém um módulo de categorias
gerado por um modelo de fronteira sem contexto de convenção. O código funciona e é limpo
em si — mas diverge do padrão do repositório.

**Tarefas:**

1. Execute o exercício e leia o código:
   ```bash
   python3 sessao-5/tutorial-16-novo-fluxo-ia/exercicios/exercicio.py
   ```

2. Liste as divergências de convenção que você encontrar. Use o checklist abaixo.

3. Reescreva o prompt que originou esse código, adicionando o contexto de convenção
   do projeto (`CLAUDE.md`, trecho de `funcoes_boas.py`).

4. Alinhe o código ao padrão do repositório — ou use o prompt revisado em um modelo
   e compare com `gabarito.py`.

**Referência:** `exercicios/gabarito_revisao.md` tem a tabela de divergências e o
prompt com contexto sugerido para os três modelos.

---

## 4. Checklist de revisão de saída do modelo

Use estas perguntas ao revisar qualquer código gerado por IA:

- [ ] Dei ao modelo os arquivos de convenção do projeto (`CLAUDE.md` / `AGENTS.md` / `GEMINI.md`)?
- [ ] Forneci um trecho de código existente como âncora do padrão (não só descrição textual)?
- [ ] Todos os identificadores estão em português (variáveis, funções, classes, parâmetros)?
- [ ] A estrutura de erro segue o padrão do repositório (exceções, não dicionários de resultado)?
- [ ] Entidades usam `@dataclass` e limites de negócio têm constantes nomeadas?
- [ ] A estrutura do módulo (plana vs. layered) é consistente com as sessões anteriores?

---

## 5. Referências

- Martin, Robert C. *Clean Code: A Handbook of Agile Software Craftsmanship*. Cap. 1–2.
- Documentação Claude Code: [CLAUDE.md como contexto permanente](https://docs.anthropic.com/claude-code)
- OpenAI Codex: [AGENTS.md e system instructions](https://platform.openai.com/docs/agents)
- Gemini CLI: [GEMINI.md e system instructions](https://cloud.google.com/vertex-ai/docs/generative-ai/model-reference/gemini)
- Exemplos do repositório:
  - `sessao-1/tutorial-02-funcoes/exemplos/funcoes_boas.py`
  - `sessao-2/tutorial-06-divida-tecnica/exemplos/divida_depois.py`
