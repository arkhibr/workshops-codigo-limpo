# Roteiro Hands-On — Segurança em Código Gerado por IA

Este roteiro aplica o checklist do Tutorial 14 ao output real de três modelos
de fronteira. O objetivo é praticar a revisão de segurança com o olhar do
revisor, não do autor: procurar o que está **ausente**, não o que está presente.

---

## Contexto

Você vai pedir o mesmo endpoint para Claude, OpenAI e Gemini usando os prompts
de `exemplos/prompt.md`. Para cada output recebido, aplique o checklist abaixo
antes de aceitar o código.

O código gerado normalmente será polido: tipado, com docstring, sem variáveis
de letra única. O defeito, se existir, estará em **uma linha de montagem de query**
— não nos nomes nem na estrutura.

---

## Passo 1 — Gerar o endpoint (versão sem requisito de segurança)

Use o prompt "sem requisitos de segurança" de `exemplos/prompt.md` nos três modelos.
Salve cada output em um arquivo separado.

**Perguntas para registrar antes de revisar:**
- O código parece correto à primeira vista?
- Onde está a cláusula `ORDER BY` ou `LIKE`?
- Ela usa parâmetro posicional (`?`) ou interpolação de string?

---

## Passo 2 — Aplicar o checklist por modelo

Para cada output gerado, responda as seis perguntas do checklist:

### Claude (Claude Code / Opus 4.8)

| Pergunta do checklist | Resposta para o output recebido |
|---|---|
| 1. Toda parte da query é parametrizada? | |
| 2. A ordenação usa allow-list? | |
| 3. A validação tem bypass? | |
| 4. Algum segredo está inline? | |
| 5. LIKE monta o `%` com parâmetro ou concatenação? | |
| 6. A dependência nova foi justificada? | |

**Brecha encontrada (se houver):**

**Linha exata do defeito:**

---

### OpenAI (Codex / GPT-4o)

| Pergunta do checklist | Resposta para o output recebido |
|---|---|
| 1. Toda parte da query é parametrizada? | |
| 2. A ordenação usa allow-list? | |
| 3. A validação tem bypass? | |
| 4. Algum segredo está inline? | |
| 5. LIKE monta o `%` com parâmetro ou concatenação? | |
| 6. A dependência nova foi justificada? | |

**Brecha encontrada (se houver):**

**Linha exata do defeito:**

---

### Gemini (Gemini CLI / Gemini 2.5)

| Pergunta do checklist | Resposta para o output recebido |
|---|---|
| 1. Toda parte da query é parametrizada? | |
| 2. A ordenação usa allow-list? | |
| 3. A validação tem bypass? | |
| 4. Algum segredo está inline? | |
| 5. LIKE monta o `%` com parâmetro ou concatenação? | |
| 6. A dependência nova foi justificada? | |

**Brecha encontrada (se houver):**

**Linha exata do defeito:**

---

## Passo 3 — Gerar o endpoint (versão com requisito de segurança)

Repita com o prompt "com requisitos de segurança" de `exemplos/prompt.md`.
Aplique o mesmo checklist ao novo output.

**Perguntas de comparação:**
- O modelo incorporou o allow-list para ORDER BY?
- O LIKE usa parâmetro posicional agora?
- O número de iterações para chegar ao código seguro foi diferente entre os modelos?

---

## Passo 4 — Comparar e registrar

Para cada modelo, registre:

| Modelo | Defeito no prompt sem segurança | Correto no prompt com segurança | Iterações necessárias |
|---|---|---|---|
| Claude Opus 4.8 | | | |
| OpenAI Codex | | | |
| Gemini 2.5 | | | |

---

## Nota de fallback

Se você não tiver acesso a um dos modelos no momento do exercício:

- **Sem Claude Code:** use o output de `exemplos/busca_gerado.py` como substituto
  para o output gerado. Ele reproduz o padrão de defeito mais comum.

- **Sem OpenAI Codex:** peça ao modelo disponível usando o prompt do formato
  OpenAI de `exemplos/prompt.md`. O resultado será diferente, mas o checklist
  se aplica da mesma forma.

- **Sem Gemini CLI:** cole `exemplos/busca_revisado.py` como few-shot em qualquer
  modelo disponível e observe se o padrão de allow-list é reproduzido.

O checklist de seis perguntas funciona independentemente do modelo — o objetivo
é o hábito de revisar **toda** a construção da query, não apenas o WHERE.
