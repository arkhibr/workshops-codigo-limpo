# Gabarito — Análise e Correção do Cupom Progressivo

## A regra errada e o caso que a revela

| Elemento | No exercício (`exercicio.py/.ts`) | Correto (`gabarito.py/.ts`) |
|---|---|---|
| Comparação de faixa Ouro | `valor > FAIXA_OURO_MIN` | `valor >= FAIXA_OURO_MIN` |
| Comparação de faixa Prata | `valor > FAIXA_PRATA_MIN` | `valor >= FAIXA_PRATA_MIN` |
| Efeito em R$ 200,00 exato | Cai em "bronze" (5 %) | Entra em "prata" (10 %) |
| Efeito em R$ 500,00 exato | Cai em "prata" (10 %) | Entra em "ouro" (20 %) |

**O caso que revela o defeito:**

```
R$200,00 → exercicio: faixa=bronze, desconto=5%   ← ERRADO
R$200,00 → gabarito:  faixa=prata,  desconto=10%  ← correto

R$500,00 → exercicio: faixa=prata,  desconto=10%  ← ERRADO
R$500,00 → gabarito:  faixa=ouro,   desconto=20%  ← correto
```

A regra do negócio define faixas como "a partir de" (inclusivo), mas o código
usava comparação estrita (`>`), excluindo os valores exatos de fronteira.
O defeito não aparece em testes com valores "no meio" de cada faixa — só
nos valores-limite, que são exatamente os mais frequentes em promoções.

---

## O prompt contextualizado que deveria ter gerado o código correto

### Para Claude (Opus 4.8 / Claude Code)

O `CLAUDE.md` já está no contexto permanente ao usar Claude Code. Complemente:

```
Gere um módulo de cupom progressivo em Python seguindo o padrão do repositório
definido no CLAUDE.md. Siga as mesmas convenções de funcoes_boas.py:
  - @dataclass para entidade de resultado (ResultadoCupom)
  - Constantes nomeadas para todos os limiares e percentuais
  - ValueError para entrada inválida — sem dicionários de erro
  - Módulo plano com funções livres
  - Bloco if __name__ == "__main__": com demo de stdout

Regra de negócio OBRIGATÓRIA — detalhe crítico:
  As faixas são INCLUSIVAS nos limites (>=):
    Bronze: valor >= R$ 0,01  e valor < R$ 200,00 → 5 %
    Prata:  valor >= R$ 200,00 e valor < R$ 500,00 → 10 %
    Ouro:   valor >= R$ 500,00                     → 20 %
  R$ 200,00 exato entra em Prata. R$ 500,00 exato entra em Ouro.

Assinatura-alvo:
  def determinar_faixa(valor: float) -> tuple[str, float]
  def calcular_cupom_progressivo(valor_compra: float) -> ResultadoCupom

Inclua casos de fronteira no demo: R$199,99, R$200,00, R$499,99, R$500,00.
```

**Por que funciona:** a regra de negócio crítica (limiares inclusivos) está
explícita no prompt, com exemplos de fronteira que forçam o modelo a usar `>=`.
Sem esse detalhe, o modelo infere `>` por ser o padrão mais comum em exemplos
de faixas progressivas na internet.

---

### Para OpenAI (Codex com AGENTS.md)

```
[developer/system message]
You are a Python code generator for a Clean Code workshop (Brazilian Portuguese).
Follow conventions from AGENTS.md:
- All identifiers in Brazilian Portuguese
- @dataclass for result entities, not raw dicts
- Raise ValueError for invalid input — never return error objects
- Named constants at module top for all thresholds and rates
- Flat module with free functions, no class hierarchy
- if __name__ == "__main__": block with print demo

CRITICAL business rule: discount tiers use INCLUSIVE lower bounds (>=).
- Bronze: valor >= 0.01 and valor < 200.00 → 5%
- Prata:  valor >= 200.00 and valor < 500.00 → 10%
- Ouro:   valor >= 500.00 → 20%
R$200.00 exactly → Prata. R$500.00 exactly → Ouro. Use >= not >.

[user message]
Generate a progressive coupon module:
  determinar_faixa(valor: float) -> tuple[str, float]
  calcular_cupom_progressivo(valor_compra: float) -> ResultadoCupom

Demo must include boundary values: 199.99, 200.00, 499.99, 500.00.
```

---

### Para Gemini (Gemini CLI com GEMINI.md)

```
# system_instruction (em GEMINI.md):
Você é um gerador de código para um workshop de Clean Code em português.
Antes de gerar qualquer código, aplique as convenções do repositório:
- Identificadores em português brasileiro
- @dataclass para entidades de resultado
- ValueError para dados inválidos — nunca objetos de erro
- Constantes nomeadas para todos os limiares de negócio
- Funções planas no módulo — sem classes
- Bloco __main__ com demo de print

# prompt:
Crie o módulo cupom_progressivo.py.

REGRA DE NEGÓCIO CRÍTICA — limiares INCLUSIVOS (>=):
  Bronze: valor >= R$0,01  e valor < R$200,00 → 5%
  Prata:  valor >= R$200,00 e valor < R$500,00 → 10%
  Ouro:   valor >= R$500,00                    → 20%
R$200,00 exato → Prata (10%). R$500,00 exato → Ouro (20%).

Assinaturas obrigatórias:
  def determinar_faixa(valor: float) -> tuple[str, float]
  def calcular_cupom_progressivo(valor_compra: float) -> ResultadoCupom

Inclua estes casos de fronteira no demo:
  R$50,00, R$199,99, R$200,00, R$350,00, R$499,99, R$500,00, R$750,00
```

---

## Template de prompt da equipe

Use este template para qualquer geração de código de regra de negócio:

```
## Contexto
[Descreva o módulo, onde ele se encaixa na arquitetura, e o arquivo de
convenção do projeto (CLAUDE.md / AGENTS.md / GEMINI.md)]

## Domínio
[Liste os termos do negócio em português: nomes de entidades, campos,
operações — os mesmos que devem aparecer nos identificadores]

## Few-shot (padrão real)
[Cole um trecho de código existente do repositório como âncora de padrão.
Ex: o @dataclass de ResultadoCupom ou a assinatura de calcular_preco_final]

## Assinatura-alvo
[Declare as assinaturas exatas das funções públicas, com tipos:
  def calcular_cupom_progressivo(valor_compra: float) -> ResultadoCupom]

## Regras de negócio críticas
[Liste as regras que o modelo pode inferir errado. Seja explícito em
condições de borda, operadores (>= vs >), e comportamento nos limites.
Inclua exemplos de casos-limite e seus resultados esperados.]

## Restrições
[Sem novas dependências. Módulo plano. ValueError para erros. Bloco __main__
com demo que exercite especificamente os casos de fronteira.]

## Pedir o plano antes do código
"Antes de gerar o código, descreva em 3 linhas como você vai implementar
determinar_faixa — especialmente os operadores de comparação nos limiares."
```

---

## O que muda na aderência com o contexto de regra de negócio

| Aspecto | Prompt sem detalhe de regra | Prompt com regra explícita |
|---|---|---|
| Operador de comparação | `>` (padrão de exemplos na internet) | `>=` (regra do negócio) |
| Casos de fronteira no demo | Valores "redondos" no meio da faixa | Valores exatos de fronteira |
| Detecção do defeito | Só com caso-limite no teste | Imediata — demo já inclui |
| Confiança na saída | Alta (código polido sem aviso) | Alta com verificação |

**Conclusão:** o modelo não erra por desatenção — ele infere a regra mais
provável. Se o prompt não deixa claro que os limiares são inclusivos, o modelo
usa `>` porque é o padrão estatisticamente mais comum. A regra de negócio
crítica precisa estar no prompt, não apenas na cabeça do desenvolvedor.
