# Roteiro Hands-On — Geração multi-arquivo com agentes

**Duração estimada:** 30 minutos  
**Objetivo:** dirigir uma mudança multi-arquivo (adicionar frete ao pedido) nos
três modelos de fronteira, receber o diff e revisar em altitude para detectar
a inconsistência cross-file antes de aceitar a mudança.

---

## Preparação (5 min)

Antes de abrir qualquer modelo, leia:

- `sessao-5/tutorial-11-multiarquivo-agentes/exemplos/diff-comentado.md` —
  o diff da mudança de cupom com a inconsistência anotada (referência de padrão)
- `sessao-5/tutorial-11-multiarquivo-agentes/exercicios/exercicio_carrinho.py` —
  o módulo com o chamador não atualizado
- `sessao-5/tutorial-11-multiarquivo-agentes/exercicios/exercicio_precificacao.py` —
  o módulo com a assinatura nova

Execute os dois para ver que ambos rodam sem erro:

```bash
python3 sessao-5/tutorial-11-multiarquivo-agentes/exercicios/exercicio_precificacao.py
python3 sessao-5/tutorial-11-multiarquivo-agentes/exercicios/exercicio_carrinho.py
```

Observe: o total no exercício_carrinho não inclui frete — mas o arquivo roda sem erro.

---

## Etapa 1 — Identificar a inconsistência manualmente (5 min)

Antes de usar qualquer modelo, tente identificar a inconsistência lendo os dois
arquivos de exercício juntos, como se você fosse revisor do diff:

1. Qual é a nova assinatura de `calcular_total_pedido` em `exercicio_precificacao.py`?
2. Como `fechar_pedido` em `exercicio_carrinho.py` chama essa função?
3. O argumento `regiao` está sendo passado? O frete aparece no total?

**Checklist de revisão em altitude:**

- [ ] A assinatura mudou em `precificacao` — onde ela é chamada em `carrinho`?
- [ ] Todos os chamadores foram atualizados para a nova assinatura?
- [ ] Um campo novo (`regiao`) foi adicionado ao `Pedido` — ele chega até o cálculo?
- [ ] O total retornado reflete os novos dados (frete) ou apenas o valor antigo?

Compare com `gabarito_revisao.md` para confirmar sua análise.

---

## Etapa 2 — Dirigir a correção nos três modelos (15 min)

Agora use cada modelo para corrigir a inconsistência. O objetivo é praticar
como dirigir e verificar uma mudança cross-file, não apenas pedí-la.

### Claude (Opus 4.8 / Claude Code)

```
Leia os dois arquivos abaixo e identifique a inconsistência cross-file:

  exercicio_carrinho.py — fechar_pedido chama calcular_total_pedido
  exercicio_precificacao.py — assinatura atual de calcular_total_pedido

Antes de corrigir qualquer código:
  1. Qual é a assinatura atual de calcular_total_pedido?
  2. Como fechar_pedido chama essa função hoje?
  3. Qual argumento está faltando?

Depois, aplique SOMENTE a correção em fechar_pedido — sem refatorações adicionais.
Mostre o diff da mudança.
```

**O que verificar no diff:**
- A correção toca apenas `fechar_pedido` — nenhuma outra função foi alterada?
- `calcular_total_pedido` é chamada com `(pedido.itens, pedido.regiao)` — dois argumentos?
- O dict de retorno inclui `subtotal`, `frete` e `total` separadamente?

**Instrução de parada se o modelo propuser mais do que uma linha:**

```
Pare. A mudança necessária é só em fechar_pedido, uma linha.
Não refatore nada além disso. Mostre apenas o trecho corrigido.
```

---

### OpenAI (Codex — agent mode)

```
[developer/system message]
You are a Python code agent for a Clean Code workshop (Brazilian Portuguese).
All identifiers in Portuguese. Minimal changes — fix only what's asked.

[user message]
Review the two files below and identify the cross-file inconsistency:
  exercicio_precificacao.py — current signature of calcular_total_pedido
  exercicio_carrinho.py — how fechar_pedido calls that function

Answer these questions before making any edits:
  1. Current signature of calcular_total_pedido (full line).
  2. How fechar_pedido calls it today (exact line).
  3. What argument is missing.

Then apply ONLY the fix to fechar_pedido. Do not refactor anything else.
Output the corrected function and a one-line diff.
```

**Diferença relevante:** pedir que o Codex responda as 3 perguntas antes de editar
força a explicitação da inconsistência. Se o modelo não souber responder a pergunta 2
corretamente, corrija antes de pedir o código.

**Verificação pós-edição:**

```
Run the corrected exercicio_carrinho.py and confirm that the total for the
"nordeste" order includes R$ 29.90 frete (expected total: R$ 219.60).
```

---

### Gemini (Gemini CLI)

```
# system_instruction (em GEMINI.md):
Você é um agente de código para um workshop de Clean Code em português.
Mudanças mínimas — corrija apenas o que foi pedido. Não refatore.

# prompt (cole os dois arquivos de exercício completos antes deste bloco):
Revise os dois arquivos e identifique a inconsistência cross-file.

Antes de qualquer edição, responda:
  1. Assinatura atual de calcular_total_pedido (linha completa).
  2. Como fechar_pedido chama essa função hoje (linha exata).
  3. Qual argumento está faltando.

Depois, corrija APENAS fechar_pedido. Nenhuma outra função. Mostre o diff.
```

**Vantagem:** colar os dois arquivos completos garante que o Gemini veja a
inconsistência sem depender de indexação. A janela de contexto ampla permite
colar ambos sem compressão.

**O que verificar no diff gerado:**
- O diff é minimal — toca apenas `fechar_pedido`?
- `calcular_total_pedido` recebe `(pedido.itens, pedido.regiao)` na chamada corrigida?
- O modelo não adicionou código não solicitado (ex.: nova função de validação)?

---

## Etapa 3 — Comparação e revisão (5 min)

Execute a versão corrigida de cada modelo e compare com o gabarito:

```bash
python3 sessao-5/tutorial-11-multiarquivo-agentes/exercicios/gabarito_carrinho.py
```

Para cada saída gerada pelos modelos, responda:

| Pergunta de revisão | Claude | OpenAI | Gemini |
|---|---|---|---|
| O modelo identificou a inconsistência antes de editar? | | | |
| A correção tocou apenas `fechar_pedido`? | | | |
| O total inclui frete (R$ 219.60 para nordeste)? | | | |
| O diff é minimal — sem refatorações não solicitadas? | | | |
| O modelo pediu confirmação antes de editar? | | | |

**Reflexão:** qual modelo ficou mais "ansioso" para editar sem responder as perguntas?
Qual precisou de mais iterações para gerar um diff minimal?

---

## Fallback — sem acesso a IA

Se não tiver acesso a nenhum modelo, identifique a inconsistência lendo os arquivos
de exercício e aplique a correção manualmente. Compare com o gabarito:

```bash
python3 sessao-5/tutorial-11-multiarquivo-agentes/exercicios/exercicio_carrinho.py
python3 sessao-5/tutorial-11-multiarquivo-agentes/exercicios/gabarito_carrinho.py
```

A diferença nos totais (R$ 189.70 vs. R$ 219.60) é o frete nordeste (R$ 29.90)
que estava definido no pedido mas nunca chegava ao cálculo.

Leia `gabarito_revisao.md` para ver a análise completa e o diff correto.
