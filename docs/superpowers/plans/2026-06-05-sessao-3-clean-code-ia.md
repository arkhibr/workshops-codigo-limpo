# Sessão 3 — Clean Code e Uso Consciente de IA · Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Criar a Sessão 3 do workshop (4 tutoriais sobre clean code com uso consciente de IA, em Python + TypeScript) e estender os artefatos existentes (`README.md` principal e `guia-de-adocao.md`).

**Architecture:** Material didático autocontido. Cada tutorial tem `README.md` (teoria), `exemplos/` com a tripla **prompt → código gerado pela IA (com falhas) → versão revisada**, e `exercicios/` com versão estática + um `roteiro-ia.md` hands-on. O tutorial 10 é a âncora (o código a revisar *é* o exercício, como o tutorial 05). Verificação por execução via stdout — sem framework de testes.

**Tech Stack:** Python 3.8+ (sem dependências externas), TypeScript via `npx ts-node`. Markdown para teoria/roteiros/gabaritos.

---

## Convenções obrigatórias (aplicam a todas as tarefas)

- **Identificadores em português** (linguagem de domínio do negócio).
- **Arquivos `*_gerado.*` e `codigo_gerado_por_ia.*` são intencionalmente falhos** — não "corrigir" os anti-padrões.
- **Autocontido:** nenhum import entre arquivos do repo; cada arquivo executável tem um bloco `if __name__ == "__main__":` (Python) ou chamada no fim (TS) que imprime uma demonstração no stdout.
- Cada arquivo executável começa com um **cabeçalho-comentário** indicando propósito e como rodar.
- READMEs seguem as seções: Contexto e Motivação → Conceito Central → Exercício → Checklist → Referências.
- Commits no padrão `<type>: <mensagem>` terminando com a linha `Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>`.

### Comandos de verificação (reutilizados em todas as tarefas)

```bash
# Python — deve rodar sem erro e imprimir a demonstração
python3 <arquivo.py>

# TypeScript — deve rodar sem erro e imprimir a demonstração
npx ts-node <arquivo.ts>
```

Para os arquivos `*_gerado.*` (intencionalmente falhos): eles devem **executar sem crashar** (a falha é de design/qualidade, não de sintaxe), salvo quando o objetivo didático for justamente um erro de runtime — nesse caso o cabeçalho do arquivo avisa "este arquivo falha em runtime de propósito" e a verificação espera o erro específico.

---

## Domínios por tutorial (escolhidos para não repetir os das sessões 1–2)

| Tutorial | Domínio do cenário |
|---|---|
| 08 | Agendamento de consultas em clínica |
| 09 | Importação de arquivo CSV de clientes |
| 10 (âncora) | Integração com gateway de pagamento |
| 11 | Geração de relatório de vendas que cresceu com contribuições de IA |

---

## Task 1: Tutorial 08 — Clean Code no Contexto Real com IA

**Files:**
- Create: `sessao-3/tutorial-08-clean-code-com-ia/README.md`
- Create: `sessao-3/tutorial-08-clean-code-com-ia/exemplos/prompt.md`
- Create: `sessao-3/tutorial-08-clean-code-com-ia/exemplos/agendamento_gerado.py`
- Create: `sessao-3/tutorial-08-clean-code-com-ia/exemplos/agendamento_revisado.py`
- Create: `sessao-3/tutorial-08-clean-code-com-ia/exemplos/agendamento_gerado.ts`
- Create: `sessao-3/tutorial-08-clean-code-com-ia/exemplos/agendamento_revisado.ts`
- Create: `sessao-3/tutorial-08-clean-code-com-ia/exercicios/roteiro-ia.md`
- Create: `sessao-3/tutorial-08-clean-code-com-ia/exercicios/exercicio.py`
- Create: `sessao-3/tutorial-08-clean-code-com-ia/exercicios/exercicio.ts`
- Create: `sessao-3/tutorial-08-clean-code-com-ia/exercicios/gabarito.py`
- Create: `sessao-3/tutorial-08-clean-code-com-ia/exercicios/gabarito.ts`
- Create: `sessao-3/tutorial-08-clean-code-com-ia/exercicios/gabarito_revisao.md`

- [ ] **Step 1: README.md**

Conteúdo (seções padrão). Linha de referência: `> Referência: *Clean Code*, Cap. 2–3 aplicados a código assistido por IA`.
- **Contexto e Motivação:** a IA produz código na velocidade de um júnior incansável; o desenvolvedor passa a ser o sênior que revisa. Os princípios das sessões 1–2 (nomes, funções, comentários) continuam sendo o critério de qualidade — agora aplicados à saída da IA.
- **Conceito Central:**
  - Engenharia de contexto no prompt: restrições explícitas, linguagem de domínio, exemplos do padrão desejado, expectativas de clean code ("funções com responsabilidade única", "nomes em português do domínio").
  - "Prompt vago → código genérico e frágil." Mostrar com fragmentos.
  - O prompt não substitui a revisão: mesmo um bom prompt gera código que precisa ser lido criticamente.
- **Exercício:** apontar para `exercicios/` (estático + `roteiro-ia.md`).
- **Checklist:** 5–6 itens (defini o domínio no prompt? pedi responsabilidade única? revisei nomes? validei comportamento? …).
- **Referências:** Clean Code caps. 2–3.

- [ ] **Step 2: exemplos/prompt.md**

Dois prompts lado a lado para o mesmo objetivo ("função que agenda uma consulta"):
- **Prompt fraco:** uma linha vaga ("faz uma função de agendar consulta").
- **Prompt forte:** com domínio, restrições, formato de retorno, expectativa de clean code e tratamento de horários ocupados.
- Comentário curto explicando o que muda na saída de cada um.

- [ ] **Step 3: exemplos/agendamento_gerado.py**

Saída plausível de IA a partir do **prompt fraco**, com falhas características: nome genérico (`def processar(d):`), parâmetros soltos em vez de objeto, mistura idioma (`def schedule_consulta`), sem validação de horário ocupado, número mágico (duração 30). Cabeçalho avisa que é saída típica de IA para revisar. Deve rodar e imprimir um agendamento de exemplo.

- [ ] **Step 4: exemplos/agendamento_revisado.py**

Versão revisada: `@dataclass Consulta`, função `agendar_consulta(...)` com responsabilidade única, nomes em português, constante `DURACAO_PADRAO_MIN`, validação de conflito de horário extraída. Roda e imprime o mesmo cenário, agora correto.

- [ ] **Step 5: exemplos/agendamento_gerado.ts e agendamento_revisado.ts**

Equivalentes em TypeScript (mesmos problemas/soluções). `interface Consulta`, funções tipadas. Rodam via `ts-node`.

- [ ] **Step 6: exercicios/exercicio.py e .ts**

Um prompt fraco + a saída de IA correspondente (módulo de "lista de espera" da clínica) com 4–5 problemas de nomes/coesão/idioma para o participante criticar e refatorar. Cabeçalho com instruções: "(1) reescreva o prompt; (2) refatore o código abaixo; (3) liste os problemas". Roda imprimindo o estado atual.

- [ ] **Step 7: exercicios/gabarito.py e .ts**

Versão refatorada do exercício. Roda imprimindo o resultado correto.

- [ ] **Step 8: exercicios/gabarito_revisao.md**

Lista comentada dos problemas do `exercicio.*` e o prompt forte sugerido.

- [ ] **Step 9: exercicios/roteiro-ia.md**

Roteiro hands-on (passos numerados): o participante (1) abre seu assistente; (2) cola o prompt forte sugerido; (3) gera a função de lista de espera; (4) aplica o checklist do README na saída da própria IA; (5) anota quais critérios a saída atendeu/violou. Inclui aviso de que o `gabarito` serve de fallback sem IA.

- [ ] **Step 10: Verificar execução**

```bash
python3 sessao-3/tutorial-08-clean-code-com-ia/exemplos/agendamento_gerado.py
python3 sessao-3/tutorial-08-clean-code-com-ia/exemplos/agendamento_revisado.py
python3 sessao-3/tutorial-08-clean-code-com-ia/exercicios/exercicio.py
python3 sessao-3/tutorial-08-clean-code-com-ia/exercicios/gabarito.py
npx ts-node sessao-3/tutorial-08-clean-code-com-ia/exemplos/agendamento_gerado.ts
npx ts-node sessao-3/tutorial-08-clean-code-com-ia/exemplos/agendamento_revisado.ts
npx ts-node sessao-3/tutorial-08-clean-code-com-ia/exercicios/exercicio.ts
npx ts-node sessao-3/tutorial-08-clean-code-com-ia/exercicios/gabarito.ts
```
Expected: cada comando roda sem erro e imprime sua demonstração.

- [ ] **Step 11: Commit**

```bash
git add sessao-3/tutorial-08-clean-code-com-ia
git commit -m "feat: adiciona tutorial 08 - clean code no contexto real com IA

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

## Task 2: Tutorial 09 — Refatoração Assistida: Funções Coesas, Legibilidade e Erros

**Files:**
- Create: `sessao-3/tutorial-09-refatoracao-assistida/README.md`
- Create: `sessao-3/tutorial-09-refatoracao-assistida/exemplos/prompt.md`
- Create: `sessao-3/tutorial-09-refatoracao-assistida/exemplos/importacao_gerado.py`
- Create: `sessao-3/tutorial-09-refatoracao-assistida/exemplos/importacao_revisado.py`
- Create: `sessao-3/tutorial-09-refatoracao-assistida/exemplos/importacao_gerado.ts`
- Create: `sessao-3/tutorial-09-refatoracao-assistida/exemplos/importacao_revisado.ts`
- Create: `sessao-3/tutorial-09-refatoracao-assistida/exercicios/roteiro-ia.md`
- Create: `sessao-3/tutorial-09-refatoracao-assistida/exercicios/exercicio.py`
- Create: `sessao-3/tutorial-09-refatoracao-assistida/exercicios/exercicio.ts`
- Create: `sessao-3/tutorial-09-refatoracao-assistida/exercicios/gabarito.py`
- Create: `sessao-3/tutorial-09-refatoracao-assistida/exercicios/gabarito.ts`
- Create: `sessao-3/tutorial-09-refatoracao-assistida/exercicios/gabarito_revisao.md`

- [ ] **Step 1: README.md**

Referência: `> Referência: *Clean Code*, Cap. 3 e 7 (Error Handling)`.
- **Contexto e Motivação:** a IA é ótima para refatorar — extrair função, renomear, melhorar legibilidade — *quando dirigida em passos pequenos e verificáveis*. O risco: a IA frequentemente engole erros (`except` largo, `catch {}` vazio, retorno de `None`/`null` mascarando falha).
- **Conceito Central:**
  - Refatoração em passos pequenos com verificação a cada passo (o comportamento deve ser preservado).
  - Tratamento de erros explícito: exceções específicas, mensagens úteis, não silenciar falhas. Fragmentos antes/depois.
  - Coesão: função que lê + valida + grava → dividir.
- **Exercício / Checklist / Referências** no padrão.

- [ ] **Step 2: exemplos/prompt.md**

Prompt de refatoração bem dirigido ("refatore esta função em passos: 1. extraia a validação; 2. trate erros de parsing explicitamente; ...") vs um prompt aberto ("melhora esse código"). Comentário sobre por que o dirigido é mais seguro.

- [ ] **Step 3: exemplos/importacao_gerado.py**

Saída de IA: função `importar(arquivo)` que faz tudo (lê CSV, valida, converte, grava em lista), com `try/except Exception: pass` engolindo erros e retornando `None` em falha. Cabeçalho avisa "saída típica de IA — note o tratamento de erro silencioso". Roda imprimindo uma importação (inclusive um caso de erro que hoje passa silenciosamente).

- [ ] **Step 4: exemplos/importacao_revisado.py**

Versão refatorada: funções coesas (`ler_linhas`, `validar_cliente`, `converter_cliente`, `importar_clientes`), exceções específicas (`ClienteInvalidoError`), erros propagados/coletados explicitamente em vez de silenciados. Roda imprimindo importação bem-sucedida e relatório de linhas inválidas.

- [ ] **Step 5: exemplos/importacao_gerado.ts e importacao_revisado.ts**

Equivalentes TS: `catch {}` vazio na versão gerada; `Result`/exceções tipadas e funções coesas na revisada.

- [ ] **Step 6: exercicios/exercicio.py e .ts**

Função de IA que processa devoluções/estornos fazendo validação + cálculo + persistência juntas, com erro silenciado. Cabeçalho: refatorar para coesão + tratamento de erro explícito, em passos. Roda imprimindo o estado atual.

- [ ] **Step 7: exercicios/gabarito.py e .ts**

Versão refatorada coesa e com erros tratados. Roda.

- [ ] **Step 8: exercicios/gabarito_revisao.md**

Lista dos problemas (coesão + cada ponto de erro silenciado) e a sequência de passos de refatoração sugerida.

- [ ] **Step 9: exercicios/roteiro-ia.md**

Hands-on: participante pede à IA, em passos, para (1) extrair a validação; (2) tornar o tratamento de erro explícito; (3) verificar que o comportamento foi preservado rodando o arquivo após cada passo. Enfatiza verificar a saída entre passos.

- [ ] **Step 10: Verificar execução** — mesmos 8 comandos do padrão, apontando para os arquivos da Task 2. Expected: rodam sem erro e imprimem as demonstrações.

- [ ] **Step 11: Commit**

```bash
git add sessao-3/tutorial-09-refatoracao-assistida
git commit -m "feat: adiciona tutorial 09 - refatoracao assistida com IA

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

## Task 3: Tutorial 10 — Revisão Crítica de Código Gerado por IA ⭐ (âncora)

**Files:**
- Create: `sessao-3/tutorial-10-revisao-critica-ia/README.md`
- Create: `sessao-3/tutorial-10-revisao-critica-ia/prompt_original.md`
- Create: `sessao-3/tutorial-10-revisao-critica-ia/codigo_gerado_por_ia.py`
- Create: `sessao-3/tutorial-10-revisao-critica-ia/codigo_gerado_por_ia.ts`
- Create: `sessao-3/tutorial-10-revisao-critica-ia/checklist_revisao_ia.md`
- Create: `sessao-3/tutorial-10-revisao-critica-ia/exercicios/roteiro-ia.md`
- Create: `sessao-3/tutorial-10-revisao-critica-ia/gabarito_review.md`
- Create: `sessao-3/tutorial-10-revisao-critica-ia/gabarito_review_ts.md`

- [ ] **Step 1: README.md**

Referência: `> Tutorial âncora — acumula sessões 1–2 aplicadas a código de IA`.
- **Contexto e Motivação:** este é o exercício âncora da sessão 3 (como o 05 foi na sessão 2). Código de IA é confiante e plausível — e é exatamente por isso que exige revisão crítica.
- **Conceito Central — modos de falha de código de IA** (cada um com 1 fragmento curto):
  1. API/método alucinado (chamada a função que não existe na lib).
  2. Lógica plausível-mas-errada (off-by-one, condição invertida).
  3. Segurança: segredo hardcoded, concatenação de SQL/strings, falta de validação de entrada externa.
  4. Edge cases faltando (valor zero, lista vazia, timeout).
  5. Over-engineering (abstração desnecessária).
  6. Confiança enganosa (comentário afirma algo que o código não faz).
- **Exercício:** revisar `codigo_gerado_por_ia.*` usando `checklist_revisao_ia.md`.
- **Checklist / Referências.**

- [ ] **Step 2: prompt_original.md**

O prompt que "gerou" o módulo de integração com gateway de pagamento — realista, razoável, mas sem restrições de segurança/edge cases (mostrando como um prompt OK ainda produz código a revisar).

- [ ] **Step 3: codigo_gerado_por_ia.py**

Módulo realista de integração de pagamento (`cobrar`, `estornar`, `consultar_status`) com **6+ problemas plantados**, um de cada modo de falha do README:
- chave de API hardcoded;
- montagem de URL/query por concatenação de string (injeção);
- condição de aprovação invertida ou off-by-one no parcelamento;
- chamada a um método inexistente de uma lib fictícia simulada (alucinação) — isolada de modo que o arquivo ainda **rode** (ex.: dentro de um branch não exercitado pela demo, com comentário marcando);
- sem tratamento de valor zero/negativo;
- comentário que afirma "valida o CPF" mas não valida.
Cabeçalho: "Código gerado por IA — contém problemas para revisar. Não corrigir aqui." Roda imprimindo uma cobrança de exemplo (caminho feliz funciona; os defeitos estão nos caminhos não-felizes/segurança).

- [ ] **Step 4: codigo_gerado_por_ia.ts**

Equivalente TS com os mesmos 6+ problemas mapeados 1:1.

- [ ] **Step 5: checklist_revisao_ia.md**

Checklist reutilizável (independente deste exercício) para revisar qualquer código de IA, organizado por categoria: Correção, Segurança, Edge cases, Legibilidade/Coesão, Dependências, "A IA entendeu o pedido?". Itens acionáveis em forma de pergunta.

- [ ] **Step 6: gabarito_review.md**

Lista comentada de **todos** os problemas plantados no `codigo_gerado_por_ia.py`, com `arquivo:linha`, categoria do checklist, por que é problema e como corrigir.

- [ ] **Step 7: gabarito_review_ts.md**

O mesmo para a versão TypeScript.

- [ ] **Step 8: exercicios/roteiro-ia.md**

Hands-on que fecha o loop "gerar → revisar": participante (1) pede à própria IA um trecho similar (ex.: integração com gateway de boleto); (2) aplica o `checklist_revisao_ia.md` na saída da IA dele; (3) registra quantos itens do checklist a saída violou. Fallback: revisar o `codigo_gerado_por_ia.*` deste tutorial.

- [ ] **Step 9: Verificar execução**

```bash
python3 sessao-3/tutorial-10-revisao-critica-ia/codigo_gerado_por_ia.py
npx ts-node sessao-3/tutorial-10-revisao-critica-ia/codigo_gerado_por_ia.ts
```
Expected: ambos rodam o caminho feliz sem crashar e imprimem a cobrança de exemplo. Confirmar manualmente que cada problema listado no gabarito existe de fato no código (conferência cruzada gabarito ↔ código).

- [ ] **Step 10: Commit**

```bash
git add sessao-3/tutorial-10-revisao-critica-ia
git commit -m "feat: adiciona tutorial 10 - revisao critica de codigo gerado por IA

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

## Task 4: Tutorial 11 — Manutenibilidade ao Longo do Tempo com IA

**Files:**
- Create: `sessao-3/tutorial-11-manutenibilidade-ia/README.md`
- Create: `sessao-3/tutorial-11-manutenibilidade-ia/exemplos/prompt.md`
- Create: `sessao-3/tutorial-11-manutenibilidade-ia/exemplos/relatorio_gerado.py`
- Create: `sessao-3/tutorial-11-manutenibilidade-ia/exemplos/relatorio_revisado.py`
- Create: `sessao-3/tutorial-11-manutenibilidade-ia/exemplos/relatorio_gerado.ts`
- Create: `sessao-3/tutorial-11-manutenibilidade-ia/exemplos/relatorio_revisado.ts`
- Create: `sessao-3/tutorial-11-manutenibilidade-ia/exercicios/roteiro-ia.md`
- Create: `sessao-3/tutorial-11-manutenibilidade-ia/exercicios/exercicio.py`
- Create: `sessao-3/tutorial-11-manutenibilidade-ia/exercicios/exercicio.ts`
- Create: `sessao-3/tutorial-11-manutenibilidade-ia/exercicios/gabarito.py`
- Create: `sessao-3/tutorial-11-manutenibilidade-ia/exercicios/gabarito.ts`
- Create: `sessao-3/tutorial-11-manutenibilidade-ia/exercicios/gabarito_revisao.md`

- [ ] **Step 1: README.md**

Referência: `> Referência: *Clean Code*, Cap. 1 e 17; Regra do Escoteiro (sessão 2)`.
- **Contexto e Motivação:** cada contribuição de IA, isoladamente plausível, pode empurrar a base para a entropia — estilos divergentes, duplicação, dependências novas. Manutenibilidade é o que sustenta a velocidade ao longo do tempo.
- **Conceito Central:**
  - Consistência com padrões existentes (a IA não conhece suas convenções a menos que você as dê).
  - Revisar o *diff*, não só a saída isolada.
  - Testes/verificação como guard-rails antes e depois de mudanças assistidas.
  - Documentar o *porquê* das decisões assistidas.
  - Evitar inchaço de dependências (a IA adiciona libs com facilidade).
  - Regra do Escoteiro aplicada a contribuições de IA.
- **Exercício / Checklist / Referências.**

- [ ] **Step 2: exemplos/prompt.md**

Prompt que dá contexto de manutenibilidade ("siga o padrão deste módulo: X; não adicione dependências; mantenha o estilo de nomes") vs prompt sem contexto. Comentário sobre o efeito no diff.

- [ ] **Step 3: exemplos/relatorio_gerado.py**

Módulo de relatório de vendas que "cresceu" com contribuições de IA inconsistentes: duas funções que fazem quase a mesma soma de forma diferente (duplicação), mistura de estilos de nome, uma dependência desnecessária reimplementável com a stdlib, formatação divergente. Cabeçalho explica o cenário de deriva. Roda imprimindo um relatório.

- [ ] **Step 4: exemplos/relatorio_revisado.py**

Versão consolidada: duplicação eliminada, estilo consistente, dependência desnecessária removida, função única de cálculo reutilizada. Roda imprimindo o mesmo relatório.

- [ ] **Step 5: exemplos/relatorio_gerado.ts e relatorio_revisado.ts**

Equivalentes TS.

- [ ] **Step 6: exercicios/exercicio.py e .ts**

Módulo de dashboard que acumulou 3–4 sinais de deriva por IA (duplicação, estilo divergente, dependência supérflua) para o participante consolidar. Roda.

- [ ] **Step 7: exercicios/gabarito.py e .ts**

Versão consolidada. Roda.

- [ ] **Step 8: exercicios/gabarito_revisao.md**

Lista dos sinais de deriva e como cada um foi consolidado.

- [ ] **Step 9: exercicios/roteiro-ia.md**

Hands-on: participante pede à IA uma feature nova no módulo *dando o contexto do padrão existente*, depois revisa o diff procurando deriva (duplicação? nova dependência? estilo?). Compara com pedir a mesma feature sem contexto.

- [ ] **Step 10: Verificar execução** — 8 comandos do padrão para os arquivos da Task 4. Expected: rodam sem erro.

- [ ] **Step 11: Commit**

```bash
git add sessao-3/tutorial-11-manutenibilidade-ia
git commit -m "feat: adiciona tutorial 11 - manutenibilidade ao longo do tempo com IA

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

## Task 5: Estender o README.md principal

**Files:**
- Modify: `README.md`

- [ ] **Step 1: Adicionar Sessão 3 à Agenda**

Após a tabela "Sessão 2 — Trabalhando com Código em Escala", inserir nova subseção de agenda:
```markdown
### Sessão 3 — Clean Code e Uso Consciente de IA · 2 horas

| # | Tutorial | Teoria | Prática | Total |
|---|---|---|---|---|
| 08 | Clean Code no Contexto Real com IA | 15 min | 15 min | 30 min |
| 09 | Refatoração Assistida ⭐ | 15 min | 15 min | 30 min |
| 10 | Revisão Crítica de Código Gerado por IA ⭐ | 15 min | 15 min | 30 min |
| 11 | Manutenibilidade ao Longo do Tempo com IA | 10 min | 10 min | 20 min |
| — | **Pulmão** | | | **10 min** |
| | **Total** | | | **120 min** |
```
(Usar a estrela ⭐ apenas no tutorial 10, que é a âncora — ajustar para não marcar o 09.)

- [ ] **Step 2: Adicionar a tabela de tutoriais da Sessão 3**

Após a tabela "Sessão 2" de conceitos centrais, adicionar:
```markdown
## Sessão 3 — Clean Code e Uso Consciente de IA (2 horas)

| # | Tutorial | Conceito central | Referência |
|---|---|---|---|
| 08 | [Clean Code no Contexto Real com IA](sessao-3/tutorial-08-clean-code-com-ia/) | Prompt como especificação; revisar a saída da IA com os critérios das sessões 1–2 | *Clean Code*, Cap. 2–3 |
| 09 | [Refatoração Assistida](sessao-3/tutorial-09-refatoracao-assistida/) | Refatorar com IA em passos verificáveis; coesão e tratamento de erros explícito | *Clean Code*, Cap. 3, 7 |
| 10 | [Revisão Crítica de Código Gerado por IA ⭐](sessao-3/tutorial-10-revisao-critica-ia/) | Modos de falha de código de IA; checklist de revisão | — |
| 11 | [Manutenibilidade ao Longo do Tempo com IA](sessao-3/tutorial-11-manutenibilidade-ia/) | Evitar entropia das contribuições de IA; consistência, diff, guard-rails | *Clean Code*, Cap. 1, 17 |
```

- [ ] **Step 3: Atualizar "Estrutura de cada tutorial"**

Adicionar nota de que os tutoriais da Sessão 3 cobrem Python + TypeScript e incluem a tripla `prompt.md` → `*_gerado.*` → `*_revisado.*` e um `roteiro-ia.md` hands-on em `exercicios/`. Descrever a estrutura distinta do tutorial 10 (código gerado + checklist + gabaritos de review).

- [ ] **Step 4: Atualizar "Como rodar os exemplos"**

Acrescentar nota: Sessão 3 roda apenas com Python e TypeScript (sem PHP/TLPP).

- [ ] **Step 5: Estender o "Inventário completo de arquivos"**

Adicionar seções de inventário para os tutoriais 08–11, descrevendo cada arquivo (no mesmo formato de tabela usado para as sessões 1–2).

- [ ] **Step 6: Verificar**

Conferir que todos os links relativos novos apontam para diretórios que existem (criados nas Tasks 1–4):
```bash
ls sessao-3/tutorial-08-clean-code-com-ia sessao-3/tutorial-09-refatoracao-assistida sessao-3/tutorial-10-revisao-critica-ia sessao-3/tutorial-11-manutenibilidade-ia
```
Expected: os quatro diretórios listados sem erro.

- [ ] **Step 7: Commit**

```bash
git add README.md
git commit -m "docs: adiciona sessao 3 a agenda, tutoriais e inventario do README

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

## Task 6: Estender o guia-de-adocao.md

**Files:**
- Modify: `guia-de-adocao.md`

- [ ] **Step 1: Inserir as seções dos tutoriais 08–11**

Inserir **antes** da seção `## Meu Plano de Adoção` (atualmente a última), seguindo o estilo workbook já estabelecido: cada seção tem a linha `> Material de referência:`, 4 perguntas com contexto antes de cada uma, e o fechamento `**Minha decisão para este tutorial:**`.

`## Tutorial 08 — Clean Code no Contexto Real com IA` (ref: `sessao-3/tutorial-08-clean-code-com-ia/README.md`)
- Pergunta sobre o que sempre incluir num prompt para código (domínio, restrições, padrão).
- Pergunta sobre o que revisar sempre antes de aceitar uma saída de IA.
- Pergunta sobre quando *não* usar IA para um trecho.
- Pergunta-âncora: **qual será a política de uso de IA da sua equipe?**

`## Tutorial 09 — Refatoração Assistida` (ref: `.../tutorial-09-refatoracao-assistida/README.md`)
- Refatorar em passos pequenos vs de uma vez — qual sua regra ao usar IA?
- Como você vai verificar que o comportamento foi preservado após uma refatoração assistida?
- O que você fará ao ver `except Exception`/`catch {}` numa saída de IA?
- Sua decisão para este tutorial.

`## Tutorial 10 — Revisão Crítica de Código Gerado por IA` (ref: `.../tutorial-10-revisao-critica-ia/README.md`)
- Qual será seu checklist mínimo de revisão de código de IA?
- Como tratar segredos/segurança em código sugerido por IA?
- Como confirmar que uma API/método sugerido pela IA realmente existe?
- Sua decisão para este tutorial.

`## Tutorial 11 — Manutenibilidade ao Longo do Tempo com IA` (ref: `.../tutorial-11-manutenibilidade-ia/README.md`)
- Como garantir que a IA siga os padrões já existentes no seu código?
- Vai revisar o diff inteiro ou só a saída? Qual seu compromisso?
- Como evitar inchaço de dependências introduzido por IA?
- Sua decisão para este tutorial.

- [ ] **Step 2: Estender a tabela "Meu Plano de Adoção"**

Adicionar as linhas:
```markdown
| 08 — Clean Code com IA | |
| 09 — Refatoração Assistida | |
| 10 — Revisão Crítica de IA | |
| 11 — Manutenibilidade com IA | |
```

- [ ] **Step 3: Verificar**

Conferir que os links de "Material de referência" apontam para READMEs existentes:
```bash
ls sessao-3/tutorial-08-clean-code-com-ia/README.md sessao-3/tutorial-09-refatoracao-assistida/README.md sessao-3/tutorial-10-revisao-critica-ia/README.md sessao-3/tutorial-11-manutenibilidade-ia/README.md
```
Expected: os quatro READMEs listados sem erro.

- [ ] **Step 4: Commit**

```bash
git add guia-de-adocao.md
git commit -m "docs: estende guia de adocao com tutoriais da sessao 3 (uso consciente de IA)

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

## Self-Review (preenchido pelo autor do plano)

**Spec coverage:**
- Objetivo/4 frentes → Tasks 1–4 (um tutorial por frente). ✓
- Molde adaptado / abordagem A (prompt → gerado → revisado) → exemplos/ de cada tutorial. ✓
- Trilha hands-on com IA → `roteiro-ia.md` em cada tutorial. ✓
- Python + TS → todos os pares de arquivos. ✓
- Foco em assistentes sem produto específico → prompts genéricos nos `prompt.md`/roteiros. ✓
- Tutorial 10 âncora com checklist → Task 3. ✓
- Extensões README + guia → Tasks 5 e 6. ✓
- Convenções do repo (PT, autocontido, falhos intencionais, stdout) → seção de convenções. ✓

**Placeholder scan:** o plano descreve conteúdo por arquivo (cenário, conceitos, falhas, verificação) em vez de transcrever cada arquivo — adaptação necessária para deliverable de material didático (~45 arquivos). Não há TODOs/TBDs pendentes.

**Type consistency:** nomes de diretórios e arquivos consistentes entre as tasks de criação (1–4) e as tasks de extensão (5–6) que os referenciam.
