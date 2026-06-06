# Gabarito — Análise: Cancelamento de Reserva sem Spec Firme

## A exigência implícita perdida

| Elemento | No exercício (`exercicio.py/.ts`) | Correto (`gabarito.py/.ts`) |
|---|---|---|
| Regra de antecedência | Ausente — cancela a qualquer momento | 2 horas mínimas antes do início |
| Cancelamento 3h antes | Aceito | Aceito |
| Cancelamento exatamente 2h antes | Aceito | Aceito (no limite, OK) |
| Cancelamento 1h59min antes | Aceito sem aviso | `CancelamentoForaDoPrazoError` |
| Cancelamento no horário da reserva | Aceito sem aviso | `CancelamentoForaDoPrazoError` |

**O caso que revela o defeito:**

```
# exercicio.py — às 14:01 para reserva às 15:00 (59min antes)
cancelar_reserva(r2.id, agora=14:01)
→ cancelada com sucesso  ← ERRADO (viola política de 2h)

# gabarito.py — mesmo caso
cancelar_reserva(r2.id, agora=14:01)
→ CancelamentoForaDoPrazoError: "faltam 0.98h para o início (mínimo: 2h)"
```

A política de antecedência mínima é uma exigência que qualquer desenvolvedor
familiarizado com sistemas de agendamento infere imediatamente — mas o modelo
não pode inferir o prazo específico (2 horas, 24 horas, 48 horas?) sem que
ele esteja explícito na spec.

---

## A spec que fixa a exigência implícita

```
## Objetivo
Operação de cancelamento de reserva de sala.

## Regra de antecedência mínima (exigência implícita crítica)
O cancelamento só é permitido com ANTECEDÊNCIA MÍNIMA DE 2 HORAS em relação
ao horário de início da reserva.

  antecedencia = reserva.inicio - agora
  Se antecedencia < 2h → CancelamentoForaDoPrazoError

Constante nomeada: ANTECEDENCIA_MINIMA_CANCELAMENTO = timedelta(hours=2)

## Exemplos de contrato (entrada→saída)
  cancelar_reserva(id=1, agora=11:00) onde inicio=14:00  → OK (3h de antecedência)
  cancelar_reserva(id=2, agora=13:00) onde inicio=15:00  → OK (exatamente 2h — no limite)
  cancelar_reserva(id=3, agora=14:01) onde inicio=16:00  → CancelamentoForaDoPrazoError
  cancelar_reserva(id=4, agora=17:00) onde inicio=17:00  → CancelamentoForaDoPrazoError
  cancelar_reserva(id=99, agora=10:00)                   → ReservaNaoEncontradaError

## Mensagem de erro obrigatória
  "Cancelamento não permitido: faltam X.Xh para o início da reserva
   (mínimo exigido: 2h)"
```

O caso de fronteira crítico é o cancelamento **exatamente com 2 horas de
antecedência**: deve ser aceito (`>=`, não `>`). Sem esse exemplo no contrato,
o modelo pode gerar `antecedencia < 2h` (correto) ou `antecedencia <= 2h`
(rejeitaria o limite, que é válido).

---

## O prompt contextualizado que deveria ter gerado o código correto

### Para Claude (Opus 4.8 / Claude Code)

```
Leia a spec abaixo e gere o módulo de cancelamento de reserva em Python,
seguindo o padrão do repositório definido no CLAUDE.md.

SPEC:

Operação: cancelar_reserva(id_reserva: int, agora: datetime) -> Reserva
Exceções: ReservaNaoEncontradaError, CancelamentoForaDoPrazoError
Constante: ANTECEDENCIA_MINIMA_CANCELAMENTO = timedelta(hours=2)

REGRA DE ANTECEDÊNCIA MÍNIMA (exigência crítica):
  antecedencia = reserva.inicio - agora
  Se antecedencia < ANTECEDENCIA_MINIMA_CANCELAMENTO → CancelamentoForaDoPrazoError
  Se antecedencia >= ANTECEDENCIA_MINIMA_CANCELAMENTO → cancelar e retornar reserva

Antes de gerar o código, descreva:
  1. A fórmula exata que vai usar para calcular antecedência.
  2. Qual operador de comparação vai usar (< vs <=) e por quê.
  3. O que acontece quando antecedencia == exatamente 2h.

Depois, gere o módulo com @dataclass Reserva, as exceções, criar_reserva,
cancelar_reserva, listar_reservas_ativas. Bloco __main__ exercitando
os 5 casos do contrato acima.

CONTRATO DE VERIFICAÇÃO:
  agora=11:00, inicio=14:00 (3h antes) → OK
  agora=13:00, inicio=15:00 (2h exatas) → OK
  agora=14:01, inicio=16:00 (1h59) → CancelamentoForaDoPrazoError
  agora=17:00, inicio=17:00 (0h) → CancelamentoForaDoPrazoError
```

**Por que funciona:** o caso `2h exatas → OK` força o modelo a usar `<` em vez
de `<=`. Sem esse caso de contrato explícito, a escolha do operador fica
ambígua — e `<=` seria igualmente plausível.

---

### Para OpenAI (Codex com AGENTS.md)

```
[developer/system message]
You are a Python code generator for a Clean Code workshop (Brazilian Portuguese).
Conventions: PT identifiers, @dataclass for entities, named constants,
ValueError/custom exceptions for errors, flat module, __main__ demo.

[user message]
Before writing code, answer:
  1. What formula computes the cancellation lead time?
  2. What operator (<, <=, >, >=) enforces "at least 2 hours in advance"?
  3. Should cancellation exactly 2 hours before the start be accepted? Why?

Then generate: cancelar_reserva(id_reserva: int, agora: datetime) -> Reserva

CRITICAL rule: cancellation requires MINIMUM 2-HOUR lead time.
  ANTECEDENCIA_MINIMA_CANCELAMENTO = timedelta(hours=2)
  antecedencia = reserva.inicio - agora
  if antecedencia < ANTECEDENCIA_MINIMA_CANCELAMENTO → CancelamentoForaDoPrazoError

Contract (the demo must reproduce all 5):
  agora=11:00, inicio=14:00 → OK
  agora=13:00, inicio=15:00 → OK  (exactly 2h — boundary)
  agora=14:01, inicio=16:00 → CancelamentoForaDoPrazoError
  agora=17:00, inicio=17:00 → CancelamentoForaDoPrazoError
  id=99 → ReservaNaoEncontradaError
```

---

### Para Gemini (Gemini CLI com GEMINI.md)

```
# system_instruction (em GEMINI.md):
Você é um gerador de código para um workshop de Clean Code em português.
Convenções: identificadores em PT, @dataclass, constantes nomeadas,
ValueError/exceções de domínio, módulo plano, bloco __main__.

# prompt:
Antes de gerar o código, responda:
  1. A fórmula para calcular antecedência de cancelamento.
  2. O operador que implementa "pelo menos 2 horas": < ou <=?
  3. Cancelamento exatamente 2h antes do início deve ser aceito?

REGRA OBRIGATÓRIA — antecedência mínima de cancelamento:
  ANTECEDENCIA_MINIMA_CANCELAMENTO = timedelta(hours=2)
  antecedencia = reserva.inicio - agora
  antecedencia < ANTECEDENCIA_MINIMA → CancelamentoForaDoPrazoError
  antecedencia >= ANTECEDENCIA_MINIMA → cancelamento aceito

CONTRATO (todos os casos devem aparecer no demo):
  agora=11:00, inicio=14:00 (3h) → OK
  agora=13:00, inicio=15:00 (2h exatas) → OK
  agora=14:01, inicio=16:00 (1h59) → CancelamentoForaDoPrazoError
  agora=17:00, inicio=17:00 (0h) → CancelamentoForaDoPrazoError

Gere o módulo completo com criar_reserva, cancelar_reserva,
listar_reservas_ativas, @dataclass Reserva, as exceções.
```

---

## O que muda na aderência com a spec estruturada

| Aspecto | Prompt sem spec | Prompt com spec e contrato |
|---|---|---|
| Regra de antecedência | Ausente | `antecedencia < timedelta(hours=2)` |
| Caso exato 2h (fronteira) | Não testado | Testado — OK esperado |
| Operador de comparação | Ambíguo (`<` ou `<=`) | Definido pelo contrato |
| Mensagem de erro | Genérica ou ausente | Formato especificado na spec |
| Detecção do defeito | Em produção | No contrato, antes do código |

**Conclusão:** o prazo de 2 horas não pode ser inferido — o modelo não sabe
se a empresa usa 1h, 2h, 24h ou 48h. Mesmo o operador (`<` vs `<=`) só
fica claro quando o contrato inclui o caso de fronteira exato. A spec é o único
lugar onde essa informação existe antes do código.
