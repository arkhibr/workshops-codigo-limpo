# Roteiro Hands-On — Spec-first na Geração de Código

**Duração estimada:** 25 minutos  
**Objetivo:** escrever uma spec estruturada para o módulo de cancelamento de reserva,
gerar código a partir dela nos três modelos de fronteira e comparar como cada um
trata a exigência implícita de antecedência mínima.

---

## Preparação (5 min)

Antes de abrir qualquer modelo, leia:

- `sessao-5/tutorial-18-spec-first/exemplos/spec.md` — spec completa do módulo de
  reservas; use como modelo de estrutura para a sua spec de cancelamento
- `sessao-5/tutorial-18-spec-first/exercicios/exercicio.py` — o módulo com a
  exigência implícita perdida
- `sessao-5/tutorial-18-spec-first/exemplos/reserva_revisado.py` — módulo gerado
  a partir de spec completa (referência de qualidade)

Execute o exercício para ver o defeito em ação:

```bash
python3 sessao-5/tutorial-18-spec-first/exercicios/exercicio.py
```

Observe: cancelamentos com 30 minutos de antecedência são aceitos sem aviso.

---

## Etapa 1 — Escrever a spec antes de gerar (8 min)

Use a estrutura de `spec.md` como modelo. Preencha cada seção para o módulo
de cancelamento de reserva:

```
## Objetivo
[Operação de cancelamento com antecedência mínima de 2 horas]

## Regra de antecedência mínima (exigência implícita crítica)
[Descreva a fórmula: antecedencia = reserva.inicio - agora
 Se antecedencia < 2h → ???Error]

## Exemplos de contrato (entrada → saída esperada)
  cancelar(id=1, agora=11:00) onde inicio=14:00  → ???  (3h antes)
  cancelar(id=2, agora=13:00) onde inicio=15:00  → ???  (exatamente 2h — fronteira)
  cancelar(id=3, agora=14:01) onde inicio=16:00  → ???  (1h59 antes)
  cancelar(id=4, agora=17:00) onde inicio=17:00  → ???  (no horário)

## Assinatura-alvo
  def cancelar_reserva(id_reserva: int, agora: datetime) -> Reserva

## Restrições
  [Constante nomeada para o prazo; exceção de domínio com mensagem descritiva]

## Pedir o plano antes do código
  "Antes de gerar o código, descreva: fórmula de antecedência, operador de
   comparação (<, <=) e o que acontece com exatamente 2h."
```

**Pergunta crítica:** o cancelamento com exatamente 2 horas de antecedência
deve ser aceito ou rejeitado? A resposta define se você usa `<` ou `<=`.
Fixe isso no contrato antes de gerar.

---

## Etapa 2 — Gerar e comparar nos três modelos (12 min)

### Claude (Opus 4.8 / Claude Code)

O `CLAUDE.md` já está no contexto ao usar Claude Code. Envie a spec que você
escreveu na Etapa 1 com a instrução de plano antes do código:

```
Leia a spec abaixo e, antes de gerar qualquer código:
  1. Descreva a fórmula de antecedência em uma linha.
  2. Explique qual operador (< ou <=) implementa "pelo menos 2 horas".
  3. Confirme o comportamento para cada um dos 4 casos do contrato.

Depois, gere o módulo de cancelamento seguindo o padrão do repositório
(CLAUDE.md): @dataclass, exceções de domínio, constantes nomeadas,
módulo plano, bloco __main__ com todos os 4 casos do contrato.

[cole sua spec aqui]
```

**Vantagem:** Claude é forte em decompor a estratégia antes de implementar.
O contexto de 1M tokens inclui `reserva_revisado.py` e `spec.md` — o modelo
pode ver o padrão real do projeto sem que você precise colá-lo.

**Verifique:** se o modelo descrever `antecedencia <= 2h` no plano, corrija
antes de receber o código. A spec deve ter o caso de fronteira (2h exatas → OK)
para que o modelo saiba que `<` é o operador correto.

---

### OpenAI (Codex com AGENTS.md)

Crie ou edite `AGENTS.md` na raiz com as convenções do projeto. Estruture
o contexto de convenção na mensagem de sistema:

```
[developer/system message]
You are a Python code generator for a Clean Code workshop (Brazilian Portuguese).
Follow conventions from AGENTS.md:
- All identifiers in Brazilian Portuguese
- @dataclass for entities; named constants; custom domain exceptions
- Flat module with free functions; __main__ demo

[user message]
Before generating code, answer in 3 sentences:
  1. Formula to compute cancellation lead time.
  2. Operator for "at least 2 hours in advance" (<, <=, >, >=).
  3. Is cancellation exactly 2 hours before the start accepted?

[cole sua spec aqui com a regra e os casos de contrato]

Generate: cancelar_reserva(id_reserva: int, agora: datetime) -> Reserva
Demo must include all 4 contract cases.
```

**Diferença relevante:** pedir que o modelo responda as 3 perguntas antes do
código força a explicitação do operador. Se a resposta incluir `<=`, você
corrige no prompt antes de receber o código.

---

### Gemini (Gemini CLI com GEMINI.md)

Configure `GEMINI.md` na raiz com as convenções. Use a janela de contexto
ampla para colar `exercicio.py` e `reserva_revisado.py` completos como few-shot:

```
# system_instruction (em GEMINI.md):
Você é um gerador de código para um workshop de Clean Code em português.
Siga as convenções: identificadores em PT, @dataclass, constantes nomeadas,
exceções de domínio, módulo plano, bloco __main__.

# prompt (cole exercicio.py e reserva_revisado.py como few-shot antes deste bloco):
Antes de gerar o código, responda:
  1. Fórmula de antecedência para cancelamento.
  2. Operador que implementa "pelo menos 2h": < ou <=?
  3. Cancelamento exatamente 2h antes: aceito ou rejeitado?

[cole sua spec aqui]

Gere o módulo cancelar_reserva respeitando a spec e os casos de contrato.
```

**Vantagem:** colar `exercicio.py` mostra o defeito como contraste,
e `reserva_revisado.py` mostra o padrão correto de estrutura. O Gemini
usa esses exemplos para inferir a qualidade esperada.

---

## Etapa 3 — Comparação e revisão (5 min)

Para cada saída gerada, responda:

| Pergunta de revisão | Claude | OpenAI | Gemini |
|---|---|---|---|
| Identificadores em português? | | | |
| Constante nomeada para o prazo? | | | |
| Usa `<` (não `<=`) para antecedência? | | | |
| 2h exatas → aceita (não rejeita)? | | | |
| 1h59min → CancelamentoForaDoPrazoError? | | | |
| Demo inclui todos os 4 casos? | | | |

**Reflexão:** qual modelo precisou de mais iterações para acertar o operador?
A diferença entre `<` e `<=` apareceu no plano antes do código ou só na saída?

---

## Fallback — sem acesso a IA

Se não tiver acesso a nenhum modelo, execute o exercício e o gabarito e compare:

```bash
python3 sessao-5/tutorial-18-spec-first/exercicios/exercicio.py
python3 sessao-5/tutorial-18-spec-first/exercicios/gabarito.py
```

Observe a diferença nos casos de cancelamento tardio: o exercício aceita tudo,
o gabarito rejeita com `CancelamentoForaDoPrazoError`. Depois leia
`gabarito_revisao.md` para ver a spec e o prompt que teriam produzido
o resultado correto diretamente.
