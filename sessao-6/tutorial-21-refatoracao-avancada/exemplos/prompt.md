# Prompt — Refatoração assistida: if/elif para tabela de faixas

Este arquivo demonstra **como dirigir uma refatoração maior com IA** — migrar
um if/elif em escada para uma tabela de faixas — em **passos verificáveis**,
preservando o comportamento exato do original, inclusive nos limites.

**Objetivo:** refatorar `calcular_comissao` (if/elif por faixa de valor) para
uma tabela de faixas, sem alterar o comportamento — especialmente nos limites
exatos de cada faixa (ex.: valor == 10.000).

---

## O código a refatorar

```python
def calcular_comissao_original(venda: Venda) -> float:
    valor = venda.valor
    if valor >= 50_000:
        return valor * 0.10
    elif valor >= 20_000:
        return valor * 0.08
    elif valor >= 10_000:
        return valor * 0.06
    elif valor >= 5_000:
        return valor * 0.04
    else:
        return valor * 0.02
```

**Comportamento a preservar:**
- `valor = 10.000` → faixa de 6% (`>= 10.000`)
- `valor = 9.999` → faixa de 4% (`< 10.000`)
- O operador `>=` é o contrato exato de cada limite.

---

## Claude (Claude Code / Opus 4.8)

Claude Code mantém o arquivo em contexto permanente via `CLAUDE.md`.
Dirija a refatoração em passos explícitos e peça o diff antes de aceitar:

```
Refatore calcular_comissao_original para usar uma tabela de faixas em vez
do if/elif em escada. Siga o padrão do repositório definido no CLAUDE.md.

Faça em passos:
  Passo 1 — Descreva a estrutura da tabela que vai criar (NamedTuple ou
            dataclass) e o operador de comparação que vai usar em cada faixa.
            Explique especificamente o que acontece quando valor == 10.000.
  Passo 2 — Mostre o diff da refatoração (apenas o que muda).
  Passo 3 — Adicione uma função verificar_equivalencia que compare a versão
            refatorada contra a original para os seguintes casos:
              interior das faixas: 1.000, 7.500, 15.000, 35.000, 80.000
              limites exatos:      5.000, 10.000, 20.000, 50.000
              um abaixo dos limites: 4.999, 9.999, 19.999, 49.999

CONTRATO DE LIMITE (crítico):
  valor >= 10.000 → 6%   (não 4%)
  valor = 9.999  → 4%
  O operador da tabela deve preservar >= para cada limite inferior.
```

**Por que funciona:** pedir o passo 1 (estratégia + operador) antes do código
força o modelo a declarar explicitamente `>=`. Se ele disser `>`, você corrige
antes de ver o código. O passo 3 (verificação com bordas) fecha o contrato.

---

## OpenAI (Codex com AGENTS.md)

Configure `AGENTS.md` com as convenções do projeto. Estruture em dois turnos:

```
[developer/system message — vai em AGENTS.md]
You are a Python refactoring assistant for a Clean Code workshop (Brazilian Portuguese).
Conventions: PT identifiers, NamedTuple for value objects, named constants,
flat module, if __name__ == "__main__" demo with stdout.

[turno 1 — estratégia]
Before refactoring, answer these questions:
  1. What data structure will you use for the commission tiers table?
  2. What comparison operator (>, >=, <, <=) will you use to check
     if a sale value qualifies for a tier?
  3. What is the result for valor=10000 in the original code?
     What will it be in your refactored version? Are they the same?

[turno 2 — implementação + verificação]
Now refactor calcular_comissao_original into calcular_comissao_refatorada
using a TABELA_COMISSAO list. Then implement verificar_equivalencia that
tests all cases below and prints "OK: <caso>" or "FALHOU: <caso> (esperado X, obtido Y)":

  Interior: valor in [1000, 7500, 15000, 35000, 80000]
  Exact limits: valor in [5000, 10000, 20000, 50000]  ← boundary cases
  Just below:   valor in [4999, 9999, 19999, 49999]

CONTRACT: valor=10000 must yield 6% (same as original >= 10000 branch).
```

**Diferença relevante:** dividir em dois turnos (estratégia / implementação)
garante que o operador seja declarado e confirmado antes de aparecer no código.
Se o modelo responder `>` no turno 1, você corrige sem ver uma linha de código.

---

## Gemini (Gemini CLI com GEMINI.md)

Configure `GEMINI.md` com as convenções. Cole o código original completo como
contexto e use a janela ampla para incluir um few-shot da estrutura esperada:

```
# system_instruction (em GEMINI.md):
Você é um assistente de refatoração Python para um workshop de Clean Code em
português. Convenções: identificadores em PT, NamedTuple para objetos de valor,
constantes nomeadas, módulo plano, bloco __main__ com print.

# prompt:
Antes de refatorar, responda:
  1. Qual operador vai usar na comparação de faixa: > ou >=?
  2. O que acontece com valor=10.000 no original? E na versão refatorada?
     Os resultados são idênticos?

Depois, refatore o código abaixo seguindo o padrão:

  ORIGINAL (não alterar):
  [cole calcular_comissao_original aqui]

  ALVO (estrutura esperada — few-shot):
  class FaixaComissao(NamedTuple):
      limite_inferior: float
      percentual:      float

  TABELA_COMISSAO: list[FaixaComissao] = [
      FaixaComissao(50_000, 0.10),
      ...
  ]

  def calcular_comissao_refatorada(venda: Venda) -> float:
      for faixa in TABELA_COMISSAO:
          if venda.valor >= faixa.limite_inferior:   # <- operador CRÍTICO
              return venda.valor * faixa.percentual
      ...

CONTRATO DE VERIFICAÇÃO (inclua verificar_equivalencia com estes casos):
  Interior: 1.000, 7.500, 15.000, 35.000, 80.000
  Limites exatos: 5.000, 10.000, 20.000, 50.000
  Logo abaixo: 4.999, 9.999, 19.999, 49.999
  Para cada caso: "OK: <caso>" ou "FALHOU: <caso> (esperado X, obtido Y)"
```

**Vantagem:** colar a estrutura `FaixaComissao` com o operador `>=` já
visível força o modelo a imitá-la. O few-shot ancora o padrão de forma mais
concreta do que qualquer descrição textual do operador correto.

---

## O que muda na preservação de comportamento

| Aspecto | Sem passos verificáveis | Com passos e bordas explícitas |
|---|---|---|
| Operador de comparação | Pode ser `>` (regressão silenciosa) | `>=` declarado no passo 1 |
| Caso valor==10.000 | Passa para faixa de 4% | Preserva faixa de 6% |
| Verificação de equivalência | Só interior das faixas — passa | Interior + bordas — detecta |
| Detecção da regressão | Em produção (pagamento errado) | Na verificação, antes de integrar |
| Número de iterações | 2–3 (descoberta + correção) | 1 (correto após passo 1) |

**Conclusão:** uma refatoração de if/elif para tabela parece trivial. O operador
de comparação é o único ponto crítico — e é exatamente onde a IA erra por padrão
(usa `>` porque é o mais comum em exemplos de busca em tabelas). Declarar a
estratégia antes do código e verificar as bordas depois são os dois controles
que tornam a refatoração segura.
