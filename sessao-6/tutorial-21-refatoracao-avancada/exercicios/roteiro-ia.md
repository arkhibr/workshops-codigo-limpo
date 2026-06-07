# Roteiro — Refatoração assistida com verificação de equivalência

Este roteiro orienta a execução hands-on do Tutorial 13 nos três modelos de
fronteira. O exercício central é refatorar `calcular_bonus_original` (if/elif
por faixa de atingimento) para uma tabela de faixas, verificando equivalência
com bordas a cada passo.

---

## Objetivo

Refatorar `calcular_bonus_original` de `exercicio.py` (ou `.ts`) para uma
tabela de faixas, **sem alterar o comportamento nos limites exatos**
(80%, 100%, 120%), usando verificação de equivalência para confirmar.

---

## Sequência de passos (independente do modelo)

```
Passo 1 — Declara a estratégia e o operador de comparação
Passo 2 — Gera a refatoração (tabela + função refatorada)
Passo 3 — Gera verificar_equivalencia com bordas
Passo 4 — Roda a verificação — deve revelar qualquer regressão
Passo 5 — Corrige se necessário; roda de novo até passar tudo
```

A verificação do Passo 4 deve incluir obrigatoriamente:
- Interior de cada faixa
- Limites exatos: atingimento in [0.80, 1.00, 1.20]
- Logo abaixo: atingimento in [0.799, 0.999, 1.199]

---

## Claude (Claude Code / Opus 4.8)

```
Vou refatorar calcular_bonus_original em exercicio.py para usar uma tabela de
faixas. Quero fazer em passos para garantir equivalência.

Passo 1 — Antes de gerar qualquer código, responda:
  a) Qual operador vai usar na comparação: > ou >=?
  b) O que acontece com atingimento=1.00 no original?
     O que acontecerá na versão refatorada? São idênticos?

Passo 2 — Gere a tabela TABELA_BONUS e a função calcular_bonus_refatorado.
  Mostre apenas o diff em relação ao original.

Passo 3 — Gere verificar_equivalencia que imprima "OK: <caso>" ou
  "FALHOU: <caso> (esperado X, obtido Y)" para:
    Interior: atingimento in [0.60, 0.90, 1.10, 1.30]
    Limites exatos: atingimento in [0.80, 1.00, 1.20]
    Logo abaixo: atingimento in [0.799, 0.999, 1.199]

CONTRATO CRÍTICO: atingimento=1.00 deve retornar 20% (mesmo que o original
>= 1.00). Atingimento=0.999 deve retornar 10%.
```

**Dica:** se no Passo 1 o modelo responder `>`, corrija antes de prosseguir.
A resposta correta é `>=`, porque o original usa `>= 0.80`, `>= 1.00`, `>= 1.20`.

---

## OpenAI (Codex com AGENTS.md)

```
[developer/system message — em AGENTS.md]
You are a Python refactoring assistant for a Clean Code workshop (Brazilian PT).
Conventions: PT identifiers, NamedTuple, named constants, flat module, __main__ demo.

[turno 1 — estratégia]
Before refactoring calcular_bonus_original, answer:
  1. Comparison operator for tier lookup: > or >=?
  2. Result for atingimento=1.00 in original? Same in refactored? Why?
  3. Result for atingimento=0.999 in original? Same in refactored?

[turno 2 — implementação + verificação]
Now generate the refactoring and verificar_equivalencia for:
  Interior: [0.60, 0.90, 1.10, 1.30]
  Exact limits: [0.80, 1.00, 1.20]   ← boundary cases
  Just below: [0.799, 0.999, 1.199]
Print "OK: <caso>" or "FALHOU: <caso> (esperado X, obtido Y)" for each.

CRITICAL: atingimento=1.00 → 20% (must match original >= 1.00 branch).
```

---

## Gemini (Gemini CLI com GEMINI.md)

```
# system_instruction (em GEMINI.md):
Assistente de refatoração Python para workshop de Clean Code em português.
Convenções: identificadores em PT, NamedTuple, constantes nomeadas, módulo plano.

# prompt:
Antes de refatorar, responda:
  1. Operador de comparação na tabela: > ou >=?
  2. atingimento=1.00 no original retorna quantos %? E na versão refatorada?
  3. atingimento=0.999 no original retorna quantos %? E na versão refatorada?

Depois refatore para tabela de faixas. Gere verificar_equivalencia com:
  Interior: [0.60, 0.90, 1.10, 1.30]
  Limites exatos: [0.80, 1.00, 1.20]
  Logo abaixo: [0.799, 0.999, 1.199]

CONTRATO: atingimento=1.00 → 20% (igual ao original). atingimento=0.999 → 10%.
```

---

## Nota sobre modelos locais / sem acesso à internet

Se estiver usando um modelo local (Ollama, LM Studio, etc.) ou sem acesso
a Claude/Codex/Gemini, aplique a sequência manualmente:

1. Escreva a tabela de faixas com `NamedTuple` ou `dataclass`.
2. Use `>=` em cada comparação (mesma semântica do `if/elif` original).
3. Implemente `verificar_equivalencia` com os casos listados acima.
4. Execute: `python3 exercicio.py` — se houver FALHOU, corrija o operador.
5. Compare com `gabarito.py` para confirmar a solução.

---

## Critério de aceitação

A refatoração está correta quando `verificar_equivalencia` imprime apenas
linhas `OK:` para todos os casos — interior, limites exatos e abaixo dos limites.
Qualquer `FALHOU:` indica que o operador de comparação ou a estrutura da tabela
não preserva o comportamento original.
