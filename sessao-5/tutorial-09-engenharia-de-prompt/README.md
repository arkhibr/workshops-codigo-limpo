# Tutorial 09 — Engenharia de contexto e prompt para gerar código

> Referência: engenharia de contexto/prompt para geração de código com modelos de fronteira

---

## 1. Contexto e Motivação

Em 2026, os modelos de fronteira — Claude Opus 4.8, OpenAI Codex, Gemini — geram código
limpo, tipado e idiomático por padrão. `@dataclass`, constantes nomeadas, tratamento de
exceções correto: tudo isso sai sem pedir. O problema deixou de ser técnico e passou a
ser semântico: *o modelo não conhece a regra de negócio que você tem na cabeça*.

Um modelo sem contexto de regra gera código que parece correto. Ele usa as melhores
práticas que aprendeu no treinamento — mas infere a lógica de negócio a partir do padrão
estatístico mais comum, não da especificação da sua empresa. O resultado é código polido
com um defeito silencioso: a função calcula, compila, passa no lint, e devolve o número
errado.

> *"The ratio of time spent reading versus writing is well over 10 to 1."*
> — Robert C. Martin, *Clean Code*, Cap. 1

Quando a IA amplifica esse padrão — gerando centenas de linhas por minuto — um defeito
de regra de negócio se espalha na mesma velocidade. Código limpo importa *mais* na era
da IA, não menos: se você não dá a regra, o modelo inventa uma plausível. E plausível
não é correto.

O papel do desenvolvedor sênior mudou: de **escritor** para **engenheiro de contexto**.
Você define o contexto, a regra crítica, a assinatura-alvo — e o modelo gera. A revisão
passa a ser verificação de aderência à regra, não apenas correção sintática.

---

## 2. Conceito Central

### O toolkit robusto para gerar código com modelos de fronteira

Sete técnicas que, juntas, transformam prompts genéricos em código alinhado ao projeto:

#### (1) Dar contexto de arquitetura e módulo-alvo

Diga ao modelo onde o código vai viver e o que existe em volta dele.

```
# Fraco — sem contexto
"Crie uma função de desconto."

# Robusto — com contexto
"Gere a função calcular_preco_final para o módulo de precificação
 do workshop (sessao-5/). Ela recebe um ItemPedido e retorna float."
```

#### (2) Linguagem de domínio

Dê os nomes do domínio explicitamente. O modelo usa inglês por padrão.

```
# Com linguagem de domínio:
"Identificadores obrigatórios: item_pedido, preco_unit, desconto_volume,
 desconto_categoria, melhor_desconto, calcular_preco_final."
```

#### (3) Few-shot do padrão real

Cole um trecho de código existente do repositório. Descrição textual é ambígua;
código real é inequívoco.

```
# Few-shot de padrão:
"Siga este padrão de funcoes_boas.py:

@dataclass
class DadosUsuario:
    nome:  str
    email: str

Use @dataclass para entidades. Levante ValueError para entradas inválidas."
```

#### (4) Assinaturas e tipos-alvo

Declare as assinaturas exatas das funções públicas. Isso ancora a interface
antes de o modelo inventar a própria.

```
# Assinatura-alvo:
"A função deve ter exatamente esta assinatura:
   def calcular_preco_final(item: ItemPedido) -> float"
```

#### (5) Restrições

Diga o que o modelo **não** deve fazer. Isso é tão importante quanto o que deve.

```
# Restrições:
"Sem novas dependências externas. Responsabilidade única por função.
 Módulo plano — sem classes Repository ou Service separadas."
```

#### (6) Pedir o plano antes do código

Antes de gerar código, peça que o modelo declare a estratégia para os pontos
críticos. Se a estratégia estiver errada, você corrige no prompt — não no código.

```
# Plano antes do código:
"Antes de gerar o código, descreva em uma frase como você vai combinar
 desconto_volume e desconto_categoria em calcular_preco_final."
```

#### (7) Iterar em vez de aceitar a primeira resposta

A primeira saída é um rascunho. Compare com a regra de negócio, refine o prompt,
regenere. Três iterações com prompt melhorado valem mais do que dez revisões manuais.

```
# Iteração:
"O desconto_volume e desconto_categoria estão sendo acumulados (multiplicados).
 A regra é: vale apenas o MAIOR. Corrija usando max() e regenere."
```

---

### O mesmo pedido pobre e o mesmo pedido rico — ambos produzem código polido

**Prompt pobre:**

```
Crie uma função Python que calcula o preço final de um item com desconto.
O item tem preço unitário, quantidade e categoria. Aplique desconto de
volume para pedidos grandes e desconto especial para a categoria "premium".
```

**Saída típica (polida, mas errada):**

```python
desconto_total = desconto_volume + desconto_categoria   # ou versão multiplicativa
return subtotal * (1.0 - desconto_total)
```

O código tem constantes nomeadas, `@dataclass`, sem magic values. Mas acumula os dois
descontos porque "acumular" é a inferência mais natural para "aplique os dois descontos".

**Prompt rico (com regra explícita):**

```
[...contexto, few-shot, assinatura-alvo, restrições...]

REGRA DE NEGÓCIO CRÍTICA:
  Vale APENAS o MAIOR desconto disponível — os descontos NÃO se acumulam.
  melhor_desconto = max(desconto_volume, desconto_categoria)
```

**Saída típica (polida e correta):**

```python
melhor_desconto = max(desconto_volume, desconto_categoria)
return subtotal * (1.0 - melhor_desconto)
```

A diferença não está no modelo — está em quem o dirige. Ambas as saídas são polidas.
Só a segunda acerta a regra de negócio porque a regra estava no prompt.

---

## 3. Exercício

**Contexto:** o arquivo `exercicios/exercicio.py` (e `.ts`) contém um módulo de cupom
progressivo gerado por um modelo de fronteira com contexto de convenção, mas **sem a
regra de limiar explícita**. O código é limpo e tipado — mas usa `>` onde devia `>=`
nos limiares de faixa, fazendo valores exatos de fronteira caírem na faixa errada.

**Tarefas:**

1. Execute o exercício e observe os casos de fronteira:
   ```bash
   python3 sessao-5/tutorial-09-engenharia-de-prompt/exercicios/exercicio.py
   ```

2. Identifique qual caso revela o defeito (dica: tente `R$200,00` e `R$500,00` exatos).

3. Escreva o prompt contextualizado que deveria ter gerado o código correto — use o
   template da equipe em `exercicios/gabarito_revisao.md`.

4. Corrija o código (ou use o prompt revisado em um modelo) e compare com `gabarito.py`.

**Referência:** `exercicios/gabarito_revisao.md` tem o caso que revela o defeito,
o prompt contextualizado sugerido e o template de prompt da equipe.

---

## 4. Checklist — Engenharia de prompt para geração de código

Use estas perguntas antes de enviar qualquer prompt de geração:

- [ ] Dei o **contexto** do módulo — onde ele vive na arquitetura e o que existe em volta?
- [ ] Forneci a **linguagem de domínio** — os nomes em português que devem aparecer no código?
- [ ] Colei um **few-shot do padrão real** — um trecho de código existente do repositório?
- [ ] Declarei a **assinatura-alvo** — tipos de parâmetros e retorno das funções públicas?
- [ ] Listei as **restrições** — o que o modelo não deve fazer (deps, camadas, mecanismo de erro)?
- [ ] Pedi o **plano antes do código** — especialmente para os pontos de regra crítica?
- [ ] Estou pronto para **iterar** — comparar a saída com a regra e refinar o prompt?

---

## 5. Referências

- Martin, Robert C. *Clean Code: A Handbook of Agile Software Craftsmanship*. Cap. 1–3.
- Documentação Claude Code: [Claude Code e CLAUDE.md](https://docs.anthropic.com/claude-code)
- OpenAI Codex: [AGENTS.md e system instructions](https://platform.openai.com/docs/agents)
- Gemini CLI: [GEMINI.md e system instructions](https://cloud.google.com/vertex-ai/docs/generative-ai/model-reference/gemini)
- Exemplos do repositório:
  - `sessao-1/tutorial-02-funcoes/exemplos/funcoes_boas.py`
  - `sessao-5/tutorial-08-novo-fluxo-ia/exemplos/catalogo_revisado.py`
  - `sessao-5/tutorial-09-engenharia-de-prompt/exemplos/preco_revisado.py`
