# Roteiro Hands-On — Engenharia de Prompt para Gerar Código

**Duração estimada:** 25 minutos  
**Objetivo:** montar o template de prompt da equipe e gerar a função de cupom progressivo
nos três modelos de fronteira, comparando se cada um acerta a regra de negócio crítica.

---

## Preparação (5 min)

Antes de abrir qualquer modelo, leia:

- `sessao-5/tutorial-09-engenharia-de-prompt/exemplos/preco_gerado.py` — veja o defeito de regra de negócio em código polido
- `sessao-5/tutorial-09-engenharia-de-prompt/exercicios/exercicio.py` — o módulo que você vai analisar e corrigir
- `exercicios/gabarito_revisao.md` — template de prompt da equipe (seção final)

Você usará o template para construir o prompt antes de gerar código.

---

## Etapa 1 — Montar o prompt contextualizado (10 min)

Usando o template de prompt da equipe (em `gabarito_revisao.md`), preencha cada seção
para o módulo de cupom progressivo:

```
## Contexto
[Módulo de desconto progressivo por valor de compra — workshop de Clean Code,
 sessão 5. Arquivos de convenção: CLAUDE.md / AGENTS.md / GEMINI.md]

## Domínio
[cupom, faixa, valor_compra, desconto, ResultadoCupom, determinar_faixa,
 calcular_cupom_progressivo, bronze, prata, ouro]

## Few-shot (padrão real)
[Cole o trecho de preco_revisado.py: @dataclass ItemPedido + calcular_preco_final]

## Assinatura-alvo
  def determinar_faixa(valor: float) -> tuple[str, float]
  def calcular_cupom_progressivo(valor_compra: float) -> ResultadoCupom

## Regras de negócio críticas
  - Faixas INCLUSIVAS nos limites inferiores (use >=, não >):
      Bronze: valor >= R$0,01 e valor < R$200,00 → 5%
      Prata:  valor >= R$200,00 e valor < R$500,00 → 10%
      Ouro:   valor >= R$500,00 → 20%
  - R$200,00 exato → Prata. R$500,00 exato → Ouro.
  - Exemplo de caso-limite: calcular_cupom_progressivo(200.00).faixa == "prata"

## Restrições
  Sem dependências externas. ValueError para valor negativo. Módulo plano.
  Bloco __main__ com demo incluindo: 199.99, 200.00, 499.99, 500.00.

## Pedir o plano antes do código
  "Antes de gerar o código, descreva como vai implementar determinar_faixa
   — especialmente os operadores de comparação nos limiares."
```

---

## Etapa 2 — Gerar e comparar nos três modelos (10 min)

### Claude (Opus 4.8 / Claude Code)

O `CLAUDE.md` já está no contexto ao usar Claude Code. Envie o prompt completo acima.

```
[use o prompt montado na Etapa 1 no terminal do Claude Code]
```

**Vantagem:** o contexto de 1M tokens inclui todo o código das sessões anteriores.
O modelo pode ver os exemplos reais de `preco_revisado.py` e inferir o padrão
sem precisar do few-shot colado — mas colá-lo ainda reduz ambiguidade.

**Verifique:** peça que o modelo explique o operador usado em `determinar_faixa`
antes de aceitar o código. Se disser `>`, corrija no prompt e peça regeneração.

---

### OpenAI (Codex com AGENTS.md)

Crie ou edite `AGENTS.md` na raiz com as convenções do projeto. No prompt use a
estrutura de mensagens do sistema:

```
[developer/system message]
You are a Python code generator for a Clean Code workshop (Brazilian Portuguese).
Follow conventions from AGENTS.md:
- All identifiers in Brazilian Portuguese
- @dataclass for result entities, raise ValueError for errors
- Named constants for all thresholds; flat module; __main__ demo

CRITICAL: discount tiers use INCLUSIVE lower bounds (>=):
  Bronze: valor >= 0.01 and valor < 200.00 → 5%
  Prata:  valor >= 200.00 and valor < 500.00 → 10%
  Ouro:   valor >= 500.00 → 20%
R$200.00 → Prata. R$500.00 → Ouro.

[user message]
Before generating code, describe in 2 sentences how you will implement
determinar_faixa — especially the comparison operators at the thresholds.
Then generate the module with the signatures:
  def determinar_faixa(valor: float) -> tuple[str, float]
  def calcular_cupom_progressivo(valor_compra: float) -> ResultadoCupom
Demo must test: 199.99, 200.00, 499.99, 500.00.
```

---

### Gemini (Gemini CLI com GEMINI.md)

Configure `GEMINI.md` na raiz com as convenções. Use `gemini -p` ou inclua as
instruções de sistema:

```
# system_instruction (em GEMINI.md):
Você é um gerador de código para um workshop de Clean Code em português.
Siga as convenções: identificadores em PT, @dataclass, ValueError, constantes
nomeadas, módulo plano, bloco __main__.

# prompt:
Antes de gerar o código, explique em 2 frases como vai implementar
determinar_faixa, especialmente os operadores de comparação nos limiares.

Depois, crie o módulo de cupom progressivo com estas regras OBRIGATÓRIAS:
  - Faixas com limiares INCLUSIVOS (>=):
      Bronze: valor >= R$0,01 e valor < R$200,00 → 5%
      Prata:  valor >= R$200,00 e valor < R$500,00 → 10%
      Ouro:   valor >= R$500,00 → 20%

Assinaturas:
  def determinar_faixa(valor: float) -> tuple[str, float]
  def calcular_cupom_progressivo(valor_compra: float) -> ResultadoCupom

Demo com: 199.99, 200.00, 499.99, 500.00 (confirmar faixas corretas).
```

**Vantagem do Gemini:** você pode colar `preco_revisado.py` e `exercicio.py`
completos no prompt como few-shot — a janela de contexto ampla acomoda isso
sem custo adicional.

---

## Etapa 3 — Comparação e revisão (5 min)

Para cada saída gerada, responda:

| Pergunta de revisão | Claude | OpenAI | Gemini |
|---|---|---|---|
| Identificadores em português? | | | |
| Usa @dataclass para ResultadoCupom? | | | |
| Limiares com >= (inclusivos)? | | | |
| R$200,00 → faixa "prata"? | | | |
| R$500,00 → faixa "ouro"? | | | |
| Demo inclui casos de fronteira? | | | |

**Reflexão:** qual modelo precisou de mais iterações para acertar os limiares?
A diferença entre `>` e `>=` apareceu no plano antes do código ou só no output?

---

## Fallback — sem acesso a IA

Se não tiver acesso a nenhum modelo, execute o exercício e o gabarito e compare:

```bash
python3 sessao-5/tutorial-09-engenharia-de-prompt/exercicios/exercicio.py
python3 sessao-5/tutorial-09-engenharia-de-prompt/exercicios/gabarito.py
```

Observe os casos de fronteira (`R$200,00` e `R$500,00`): a faixa muda entre os
dois arquivos. Isso é o defeito em ação. Depois leia `gabarito_revisao.md` para
ver o prompt que teria produzido o resultado correto diretamente.
