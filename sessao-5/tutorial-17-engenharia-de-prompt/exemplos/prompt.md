# Prompt — Gerar função de cálculo de preço com descontos

Este arquivo demonstra **o mesmo objetivo de geração** expresso de dois modos —
pobre e ricamente contextualizado — para os três modelos de fronteira.

**Objetivo:** gerar uma função que calcula o preço final de um item aplicando
descontos de volume e de categoria, seguindo a regra: *vale o MAIOR desconto*.

---

## Sem contexto de regra de negócio (o problema)

```
Crie uma função Python que calcula o preço final de um item com desconto.
O item tem preço unitário, quantidade, e categoria. Aplique desconto de
volume para pedidos grandes e desconto especial para a categoria "premium".
Use boas práticas.
```

**Saída típica:** código limpo, tipado, com `@dataclass` e constantes nomeadas —
mas que **acumula** os dois descontos de forma multiplicativa:

```python
fator_volume    = 1.0 - desconto_volume
fator_categoria = 1.0 - desconto_categoria
return subtotal * fator_volume * fator_categoria  # ← acumula os dois
```

O código parece correto. Casos de desconto único saem certos. Só o caso
premium+volume alto revela o problema: o desconto fica maior do que qualquer
um dos dois individualmente. É o que está em `preco_gerado.py`.

---

## Com contexto de regra de negócio (a solução)

### Claude (Opus 4.8 / Claude Code)

O `CLAUDE.md` já está no contexto permanente ao usar Claude Code. Complemente
o prompt com a regra crítica e um few-shot do padrão real:

```
Gere um módulo de cálculo de preço com descontos em Python, seguindo o padrão
do repositório definido no CLAUDE.md. Use as mesmas convenções de preco_revisado.py
(sessão 5) e funcoes_boas.py (sessão 1):

1. @dataclass ItemPedido com campos: produto_id, categoria, preco_unit, quantidade.
2. Constantes nomeadas para todos os limiares e percentuais de desconto.
3. Funções separadas: calcular_desconto_volume, calcular_desconto_categoria,
   calcular_preco_final — uma responsabilidade cada.
4. ValueError para entradas inválidas. Módulo plano sem camadas de serviço.
5. Bloco if __name__ == "__main__": com demo de stdout.

REGRA DE NEGÓCIO CRÍTICA — detalhe que não pode ser inferido:
  Vale APENAS o MAIOR desconto disponível — os descontos NÃO se acumulam.
  Se o item for premium (15%) e tiver volume alto (10%), aplica 15% — não 23,5%.
  Implemente como: melhor_desconto = max(desconto_volume, desconto_categoria)

Assinatura-alvo:
  def calcular_preco_final(item: ItemPedido) -> float

Inclua no demo um item premium com volume alto para confirmar que o desconto
acumulado NÃO acontece.
```

**Por que funciona:** a regra de negócio crítica está explícita, com a
implementação sugerida (`max()`). O modelo vê o padrão real do repo via
contexto de 1M tokens. A combinação elimina a ambiguidade que levou ao
defeito em `preco_gerado.py`.

---

### OpenAI (Codex com AGENTS.md)

O Codex usa `AGENTS.md` como arquivo de instrução permanente. Estruture
o contexto de convenção na mensagem de sistema (`developer`) e a regra
crítica no prompt:

```
[developer/system message — vai em AGENTS.md ou como system instruction]
You are a Python code generator for a Clean Code workshop (Brazilian Portuguese).
Follow the project conventions:
- All identifiers in Brazilian Portuguese (produto, preco, categoria, desconto)
- @dataclass for entities — never raw dicts
- Raise ValueError for invalid inputs — never return error objects
- Named constants at module top for all thresholds and rates
- Flat module with free functions, no Repository/Service class layers
- if __name__ == "__main__": block with full print demo

[user message]
Before writing code, state in one sentence what operator/function you will use
to combine discount_volume and discount_category in calcular_preco_final.

Then generate the pricing module with:
  @dataclass ItemPedido: produto_id, categoria, preco_unit, quantidade
  def calcular_desconto_volume(quantidade: int) -> float
  def calcular_desconto_categoria(categoria: str) -> float
  def calcular_preco_final(item: ItemPedido) -> float

CRITICAL business rule: only the LARGEST discount applies — discounts do NOT
accumulate. For a premium item (15%) with high volume (10%), apply 15%.
Use: melhor_desconto = max(desconto_volume, desconto_categoria)

Demo must include a premium item with 60 units to confirm no compounding.
```

**Diferença relevante:** pedir ao modelo que declare a estratégia de
combinação *antes* do código força a explicitação do operador. Se o modelo
disser "multiplico os dois fatores", você corrige antes de receber o código.

---

### Gemini (Gemini CLI com GEMINI.md)

Configure `GEMINI.md` com as convenções do projeto. Use a janela de contexto
ampla para colar exemplos reais completos:

```
# system_instruction (em GEMINI.md):
Você é um gerador de código para um workshop de Clean Code em português.
Siga estas convenções antes de gerar qualquer código:
- Identificadores em português (produto, preco, categoria, desconto)
- @dataclass para entidades — nunca dicts crus
- ValueError para dados inválidos — nunca objetos de resultado
- Constantes nomeadas para todos os limiares e percentuais
- Funções planas no módulo — sem camadas Repository/Service
- Bloco __main__ com demo de print

# prompt (cole preco_revisado.py inteiro como few-shot antes deste bloco):
Antes de gerar o código, explique em uma frase como combinar
desconto_volume e desconto_categoria em calcular_preco_final.

Crie o módulo de preço com:
  @dataclass ItemPedido: produto_id, categoria, preco_unit, quantidade
  def calcular_desconto_volume(quantidade: int) -> float
  def calcular_desconto_categoria(categoria: str) -> float
  def calcular_preco_final(item: ItemPedido) -> float

REGRA OBRIGATÓRIA: vale apenas o MAIOR desconto — não acumule.
  melhor_desconto = max(desconto_volume, desconto_categoria)
  item premium (15%) + volume alto (10%) → aplica 15%, não 23,5%.

Demo com item "premium", 60 unidades — imprima o preço esperado e o calculado.
```

**Vantagem:** colar `preco_revisado.py` completo como few-shot ancora o padrão
de forma mais concreta do que qualquer descrição textual. O Gemini vê o código
real do projeto e infere o padrão de constantes, estrutura de funções e demo.

---

## O que muda na aderência

| Aspecto | Sem contexto de regra | Com regra explícita no prompt |
|---|---|---|
| Combinação de descontos | Multiplicativa (acumula) | `max()` — maior vence |
| Caso premium+volume alto | Desconto incorreto (exagerado) | Desconto correto (15%) |
| Detecção do defeito | Só com caso de fronteira no teste | Imediata — regra declarada |
| Número de iterações para acertar | 2–3 (descoberta + correção) | 1 (correto de primeira) |

**Conclusão:** ambos os prompts produzem código polido e idiomático. A diferença
está na regra de negócio — o modelo não pode inferi-la do contexto técnico.
Sem "vale o maior", ele infere "acumule os dois" porque é o padrão mais comum
em exemplos de desconto na internet. O prompt contextualizado não apenas dá
a regra: também pede que o modelo a declare antes de codificá-la.
