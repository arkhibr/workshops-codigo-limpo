# Roteiro Hands-On — Testes de Caracterização como Guard-Rails

Este roteiro aplica o conceito do Tutorial 15 ao código de `exercicio.py` / `exercicio.ts`
usando os três modelos de fronteira. O objetivo é praticar o ciclo completo:
caracterizar → mudar → re-verificar — e observar o que acontece quando a suite existe
antes da mudança versus quando ela é pedida depois.

---

## Contexto

Você vai trabalhar com `calcular_desconto_fidelidade` — uma função com 4 faixas de
tempo e fronteiras em 6, 12 e 24 meses. A tarefa de negócio é adicionar uma nova faixa:
clientes com mais de 36 meses recebem 20% de desconto.

O exercício tem duas versões do mesmo fluxo:
- **Fluxo A (sem caracterização prévia):** pedir a mudança diretamente.
- **Fluxo B (com caracterização prévia):** escrever os testes primeiro, depois pedir a mudança.

Compare os resultados. Anote se o modelo introduziu alguma regressão no Fluxo A.

---

## Passo 1 — Preparar o código base

Abra `exercicio.py` (ou `exercicio.ts`). Familiarize-se com as faixas e fronteiras atuais.

**Perguntas para registrar antes de qualquer prompt:**
- Quais são os valores exatos das fronteiras entre as faixas?
- O que acontece com um cliente de exatamente 6 meses? E de 12 meses? E de 24 meses?
- A suite de verificação atual existe? Se não, quem vai detectar uma regressão?

---

## Passo 2 — Fluxo A: mudar sem caracterização (veja o que acontece)

Peça a mudança diretamente, sem pedir testes primeiro:

```
Adicione uma nova faixa de desconto: clientes com mais de 36 meses recebem
20% de desconto. Mantenha as faixas existentes sem alterar.
```

Receba o output, rode o arquivo e observe:
- O comportamento para 6, 12 e 24 meses mudou?
- O modelo testou as fronteiras antes de entregar?
- Você consegue dizer com certeza que não houve regressão?

---

## Passo 3 — Fluxo B: caracterizar primeiro, mudar depois

### Claude (Claude Code / Opus 4.8)

Use dois turnos separados na mesma sessão:

```
[turno 1 — caracterização]
Antes de modificar calcular_desconto_fidelidade, escreva verificar_faixas_completo()
cobrindo mid-band e bordas exatas de cada faixa:
  - 0, 3, 5 meses (faixa novato — borda em 6)
  - 6, 9, 11 meses (faixa iniciante — borda em 12)
  - 12, 18, 23 meses (faixa regular — borda em 24)
  - 24, 30 meses (faixa fiel — borda em 24)
  - meses negativos e valor_compra zero (devem levantar ValueError)

Rode contra o código atual e confirme que todos passam.
Aguarde minha confirmação antes de qualquer mudança.

[turno 2 — mudança]
Agora adicione a faixa veterano: clientes com mais de 36 meses recebem 20%.
Rode verificar_faixas_completo() novamente e reporte qualquer FALHOU.
Se algum falhar, corrija antes de entregar.
```

**O que observar:** o modelo rodará a suite no turno 2 com o código novo.
Se ele deslocar `<= 36` para `< 36` ou mudar a fronteira de 24, o caso
correspondente vai falhar — e o modelo vai corrigir antes de entregar.

---

### OpenAI (Codex com AGENTS.md)

Configure `AGENTS.md` com as convenções do repositório (identificadores em PT,
funções `verificar_*`, bloco `__main__`). Use três turnos:

```
[turno 1 — estratégia]
Quais são os valores exatos das fronteiras entre as faixas de
calcular_desconto_fidelidade? Por que testar apenas 9 meses e 18 meses
é insuficiente para detectar um deslocamento de fronteira em 12 meses?

[turno 2 — suite]
Escreva verificar_faixas_completo() com os casos listados abaixo.
Rode contra o código atual. Confirme que todos os casos passam.
[lista de casos: 0, 5, 6, 11, 12, 23, 24, 30, -1, valor_compra=0]

[turno 3 — mudança]
Adicione a faixa veterano (> 36 meses: 20%). Re-rode verificar_faixas_completo().
Se algum caso falhar, corrija a regressão antes de entregar.
```

**Nota de fallback:** se o Codex não estiver disponível, use o prompt dos três
turnos em qualquer modelo de fronteira disponível. O mecanismo de detecção
funciona independentemente do modelo — o que importa é a existência da suite
antes da mudança.

---

### Gemini (Gemini CLI com GEMINI.md)

Configure `GEMINI.md` com as convenções. Cole `gabarito.py` como few-shot
antes do prompt para ancorar o padrão de suite completa:

```
# system_instruction (em GEMINI.md):
Você é um gerador de código para um workshop de Clean Code em português.
Convenções: identificadores em PT, funções verificar_*(), bloco __main__,
sem framework de teste, constantes nomeadas para todos os limiares.

# prompt (cole gabarito.py inteiro como few-shot, depois este bloco):
Antes de gerar código, responda: quais são os valores de fronteira entre
as faixas de calcular_desconto_fidelidade?

Passo 1: escreva verificar_faixas_completo() cobrindo mid-band e bordas.
Rode contra o código atual. Confirme todos OK.

Passo 2: adicione a faixa veterano (> 36 meses: 20%).
Re-rode verificar_faixas_completo(). Reporte qualquer FALHOU e corrija.
```

**Vantagem do few-shot:** colar `gabarito.py` inteiro mostra ao Gemini
a estrutura exata de uma suite com bordas — incluindo os comentários
"borda inferior / borda superior / fronteira crítica". O modelo reproduz
o padrão sem precisar inferir quais valores são importantes.

---

## Passo 4 — Comparar Fluxo A e Fluxo B

Para cada modelo, registre:

| Modelo | Regressão no Fluxo A | Suite detectou no Fluxo B | Iterações até código correto |
|---|---|---|---|
| Claude Opus 4.8 | | | |
| OpenAI Codex | | | |
| Gemini 2.5 | | | |

**Perguntas de reflexão:**
- No Fluxo A, o modelo testou as fronteiras voluntariamente antes de entregar?
- No Fluxo B, a suite detectou alguma regressão que o Fluxo A não detectaria?
- O número de iterações foi diferente entre os fluxos?

---

## Nota de fallback

Se você não tiver acesso a um dos modelos durante o exercício:

- **Sem Claude Code:** use o prompt do Fluxo B em qualquer modelo disponível.
  O mecanismo de dois turnos funciona em qualquer interface de chat.

- **Sem Codex:** o turno de declaração de estratégia (turno 1) pode ser feito
  como uma pergunta separada em qualquer modelo antes de pedir a implementação.

- **Sem Gemini CLI:** cole `gabarito.py` diretamente na janela de contexto
  do modelo disponível como exemplo antes do prompt.

O checklist do README se aplica ao output de qualquer modelo — o objetivo
é o hábito de verificar as bordas, independentemente de qual ferramenta gerou o código.
