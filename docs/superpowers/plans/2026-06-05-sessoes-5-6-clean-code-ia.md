# Sessões 5 e 6 — Clean Code e Uso Consciente de IA · Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Criar o Tema 3 do workshop (8 tutoriais sobre clean code com uso consciente de IA, em Python + TypeScript) distribuídos em duas sessões de 2h (Sessão 5 e Sessão 6) e estender os artefatos existentes (`README.md` principal e `guia-de-adocao.md`).

**Architecture:** Material didático autocontido. Cada tutorial tem `README.md` (teoria), `exemplos/` com a tripla **prompt → código gerado pela IA (com falhas) → versão revisada**, e `exercicios/` com versão estática + um `roteiro-ia.md` hands-on. Os tutoriais 11 e 12 são âncoras; o 12 usa o molde "código a revisar *é* o exercício" (como o tutorial 05). Verificação por execução via stdout — sem framework de testes.

**Tech Stack:** Python 3.8+ (sem dependências externas), TypeScript via `npx ts-node`. Markdown para teoria/roteiros/gabaritos.

---

## Convenções obrigatórias (aplicam a todas as tarefas)

- **Identificadores em português** (linguagem de domínio do negócio).
- **Arquivos `*_gerado.*` e `codigo_gerado_por_ia.*` são intencionalmente falhos** — não "corrigir" os anti-padrões.
- **Autocontido:** nenhum import entre arquivos do repo; cada arquivo executável tem um bloco `if __name__ == "__main__":` (Python) ou chamada no fim (TS) que imprime uma demonstração no stdout.
- Cada arquivo executável começa com um **cabeçalho-comentário** indicando propósito e como rodar.
- READMEs seguem as seções: Contexto e Motivação → Conceito Central → Exercício → Checklist → Referências, iniciando com uma linha `> Referência:`.
- Commits no padrão `<type>: <mensagem>` terminando com a linha `Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>`.

### Comandos de verificação (reutilizados em todas as tarefas)

```bash
# Python — deve rodar sem erro e imprimir a demonstração
python3 <arquivo.py>

# TypeScript — deve rodar sem erro e imprimir a demonstração
npx ts-node <arquivo.ts>
```

Para os arquivos `*_gerado.*` / `codigo_gerado_por_ia.*` (intencionalmente falhos): devem **executar sem crashar** (a falha é de design/qualidade, não de sintaxe), salvo quando o objetivo didático for um erro de runtime — nesse caso o cabeçalho do arquivo avisa "este arquivo falha em runtime de propósito" e a verificação espera o erro específico.

---

## Domínios por tutorial (escolhidos para não repetir os das Sessões 1–2)

| Tutorial | Sessão | Domínio do cenário |
|---|---|---|
| 08 | 5 | Agendamento de consultas em clínica |
| 09 | 5 | Cálculo de preço com regras de desconto |
| 10 | 5 | Importação de arquivo CSV de clientes |
| 11 (âncora S5) | 5 | Processamento de devoluções/estornos |
| 12 (âncora tema) | 6 | Integração com gateway de pagamento |
| 13 | 6 | Endpoint de consulta de cliente por parâmetro |
| 14 | 6 | Cálculo de frete com faixas de peso |
| 15 | 6 | Relatório de vendas que cresceu com contribuições de IA |

---

## Padrão de tarefa de tutorial "tripla" (08, 09, 10, 11, 13, 14, 15)

Cada um destes tutoriais tem a mesma estrutura de arquivos e os mesmos passos. Os passos abaixo são o **molde**; cada Task instancia o molde com o domínio, as falhas plantadas e a referência específicos.

Estrutura de arquivos (substituir `NN`, `<slug>` e `<tema>`):
```
sessao-<S>/tutorial-NN-<slug>/
├── README.md
├── exemplos/
│   ├── prompt.md
│   ├── <tema>_gerado.py
│   ├── <tema>_revisado.py
│   ├── <tema>_gerado.ts
│   └── <tema>_revisado.ts
└── exercicios/
    ├── roteiro-ia.md
    ├── exercicio.py
    ├── exercicio.ts
    ├── gabarito.py
    ├── gabarito.ts
    └── gabarito_revisao.md
```

Passos do molde:
1. **README.md** — seções padrão; linha `> Referência:` específica; Conceito Central com fragmentos antes/depois; Exercício aponta para `exercicios/` (estático + `roteiro-ia.md`); Checklist de 5–6 itens em forma de pergunta; Referências.
2. **exemplos/prompt.md** — prompt fraco vs prompt forte lado a lado, com comentário curto sobre o que muda na saída.
3. **exemplos/`<tema>_gerado.py`** — saída plausível de IA a partir do prompt fraco, com as falhas plantadas da Task. Cabeçalho avisa que é saída típica de IA para revisar. Roda e imprime uma demonstração.
4. **exemplos/`<tema>_revisado.py`** — versão revisada/refatorada (falhas corrigidas). Roda imprimindo o mesmo cenário, agora correto.
5. **exemplos/`<tema>_gerado.ts` e `<tema>_revisado.ts`** — equivalentes TS, mesmos problemas/soluções mapeados 1:1. Rodam via `ts-node`.
6. **exercicios/exercicio.py e .ts** — um prompt fraco + a saída de IA correspondente (variação do domínio) com 4–5 problemas para o participante criticar e refatorar. Cabeçalho com instruções: "(1) reescreva o prompt; (2) refatore o código abaixo; (3) liste os problemas". Roda imprimindo o estado atual.
7. **exercicios/gabarito.py e .ts** — versão refatorada do exercício. Roda imprimindo o resultado correto.
8. **exercicios/gabarito_revisao.md** — lista comentada dos problemas do `exercicio.*` e o prompt forte sugerido.
9. **exercicios/roteiro-ia.md** — roteiro hands-on numerado: participante (1) abre seu assistente; (2) cola o prompt forte; (3) gera o trecho; (4) aplica o checklist do README na saída da própria IA; (5) anota critérios atendidos/violados. Aviso de que o `gabarito` é fallback sem IA.
10. **Verificar execução** — rodar os 8 comandos (`python3` e `npx ts-node` para gerado, revisado, exercicio, gabarito). Expected: cada um roda sem erro e imprime sua demonstração.
11. **Commit** — `git add sessao-<S>/tutorial-NN-<slug>` + mensagem `feat: ...` com a linha Co-Authored-By.

---

## Task 1: Tutorial 08 — Clean Code no Contexto Real com IA

**Slug:** `tutorial-08-clean-code-com-ia` · **Sessão:** 5 · **Tema (arquivos):** `agendamento` · **Domínio:** agendamento de consultas em clínica.

**Files:**
- Create: `sessao-5/tutorial-08-clean-code-com-ia/README.md`
- Create: `sessao-5/tutorial-08-clean-code-com-ia/exemplos/prompt.md`
- Create: `sessao-5/tutorial-08-clean-code-com-ia/exemplos/agendamento_gerado.py`
- Create: `sessao-5/tutorial-08-clean-code-com-ia/exemplos/agendamento_revisado.py`
- Create: `sessao-5/tutorial-08-clean-code-com-ia/exemplos/agendamento_gerado.ts`
- Create: `sessao-5/tutorial-08-clean-code-com-ia/exemplos/agendamento_revisado.ts`
- Create: `sessao-5/tutorial-08-clean-code-com-ia/exercicios/roteiro-ia.md`
- Create: `sessao-5/tutorial-08-clean-code-com-ia/exercicios/exercicio.py`
- Create: `sessao-5/tutorial-08-clean-code-com-ia/exercicios/exercicio.ts`
- Create: `sessao-5/tutorial-08-clean-code-com-ia/exercicios/gabarito.py`
- Create: `sessao-5/tutorial-08-clean-code-com-ia/exercicios/gabarito.ts`
- Create: `sessao-5/tutorial-08-clean-code-com-ia/exercicios/gabarito_revisao.md`

Seguir o **padrão de tarefa de tutorial "tripla"** com estas especializações:

- [ ] **Step 1: README.md** — Referência: `> Referência: *Clean Code*, Cap. 2–3 aplicados a código assistido por IA`.
  - **Contexto e Motivação:** a IA produz código na velocidade de um júnior incansável; o desenvolvedor passa a ser o sênior que revisa. Os princípios das Sessões 1–2 (nomes, funções, comentários) continuam sendo o critério de qualidade.
  - **Conceito Central:** o prompt é uma especificação informal; "prompt vago → código genérico e frágil" (fragmento); mesmo um bom prompt gera código que precisa ser lido criticamente.
  - **Checklist:** defini o domínio no prompt? pedi responsabilidade única? revisei nomes? validei comportamento? li o código inteiro? (5–6 itens).
- [ ] **Step 2: exemplos/prompt.md** — objetivo "função que agenda uma consulta": prompt fraco ("faz uma função de agendar consulta") vs prompt forte (domínio, restrições, formato de retorno, tratamento de horário ocupado, expectativa de clean code).
- [ ] **Step 3: exemplos/agendamento_gerado.py** — falhas plantadas: nome genérico (`def processar(d):`), parâmetros soltos em vez de objeto, mistura de idioma (`schedule_consulta`), sem validação de horário ocupado, número mágico (duração 30). Roda imprimindo um agendamento de exemplo.
- [ ] **Step 4: exemplos/agendamento_revisado.py** — `@dataclass Consulta`, `agendar_consulta(...)` com responsabilidade única, nomes em português, constante `DURACAO_PADRAO_MIN`, validação de conflito de horário extraída. Roda imprimindo o mesmo cenário correto.
- [ ] **Step 5: exemplos/agendamento_gerado.ts e agendamento_revisado.ts** — `interface Consulta`, funções tipadas; mesmos problemas/soluções.
- [ ] **Step 6: exercicios/exercicio.py e .ts** — módulo de "lista de espera" da clínica: saída de IA com 4–5 problemas de nomes/coesão/idioma. Roda imprimindo o estado atual.
- [ ] **Step 7: exercicios/gabarito.py e .ts** — versão refatorada. Roda.
- [ ] **Step 8: exercicios/gabarito_revisao.md** — problemas do exercício + prompt forte sugerido.
- [ ] **Step 9: exercicios/roteiro-ia.md** — hands-on conforme molde, usando o prompt forte de lista de espera.
- [ ] **Step 10: Verificar execução**
```bash
python3 sessao-5/tutorial-08-clean-code-com-ia/exemplos/agendamento_gerado.py
python3 sessao-5/tutorial-08-clean-code-com-ia/exemplos/agendamento_revisado.py
python3 sessao-5/tutorial-08-clean-code-com-ia/exercicios/exercicio.py
python3 sessao-5/tutorial-08-clean-code-com-ia/exercicios/gabarito.py
npx ts-node sessao-5/tutorial-08-clean-code-com-ia/exemplos/agendamento_gerado.ts
npx ts-node sessao-5/tutorial-08-clean-code-com-ia/exemplos/agendamento_revisado.ts
npx ts-node sessao-5/tutorial-08-clean-code-com-ia/exercicios/exercicio.ts
npx ts-node sessao-5/tutorial-08-clean-code-com-ia/exercicios/gabarito.ts
```
Expected: cada comando roda sem erro e imprime sua demonstração.
- [ ] **Step 11: Commit**
```bash
git add sessao-5/tutorial-08-clean-code-com-ia
git commit -m "feat: adiciona tutorial 08 - clean code no contexto real com IA

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

## Task 2: Tutorial 09 — Engenharia de Prompt para Código Limpo

**Slug:** `tutorial-09-engenharia-de-prompt` · **Sessão:** 5 · **Tema (arquivos):** `preco` · **Domínio:** cálculo de preço com regras de desconto.

**Files:**
- Create: `sessao-5/tutorial-09-engenharia-de-prompt/README.md`
- Create: `sessao-5/tutorial-09-engenharia-de-prompt/exemplos/prompt.md`
- Create: `sessao-5/tutorial-09-engenharia-de-prompt/exemplos/preco_gerado.py`
- Create: `sessao-5/tutorial-09-engenharia-de-prompt/exemplos/preco_revisado.py`
- Create: `sessao-5/tutorial-09-engenharia-de-prompt/exemplos/preco_gerado.ts`
- Create: `sessao-5/tutorial-09-engenharia-de-prompt/exemplos/preco_revisado.ts`
- Create: `sessao-5/tutorial-09-engenharia-de-prompt/exercicios/roteiro-ia.md`
- Create: `sessao-5/tutorial-09-engenharia-de-prompt/exercicios/exercicio.py`
- Create: `sessao-5/tutorial-09-engenharia-de-prompt/exercicios/exercicio.ts`
- Create: `sessao-5/tutorial-09-engenharia-de-prompt/exercicios/gabarito.py`
- Create: `sessao-5/tutorial-09-engenharia-de-prompt/exercicios/gabarito.ts`
- Create: `sessao-5/tutorial-09-engenharia-de-prompt/exercicios/gabarito_revisao.md`

Seguir o **padrão de tarefa de tutorial "tripla"** com estas especializações:

- [ ] **Step 1: README.md** — Referência: `> Referência: *Clean Code*, Cap. 2–3; engenharia de contexto em prompts de código`.
  - **Conceito Central — prompt patterns:** dar **contexto** (arquitetura, padrões existentes), **linguagem de domínio**, **restrições explícitas** (sem novas dependências, responsabilidade única), **exemplos do padrão desejado** (few-shot), **formato de saída esperado**; iterar o prompt. Fragmento mostrando o mesmo pedido com e sem contexto.
  - **Checklist:** dei contexto do projeto? listei restrições? dei um exemplo do padrão? defini o formato de saída? iterei em vez de aceitar a 1ª resposta? (5–6 itens).
- [ ] **Step 2: exemplos/prompt.md** — objetivo "função que calcula o preço final com descontos": prompt sem contexto vs prompt estruturado (com regras de desconto do domínio, restrição de não usar libs externas, exemplo do padrão de retorno).
- [ ] **Step 3: exemplos/preco_gerado.py** — saída do prompt sem contexto: ignora convenções, nomes genéricos (`calc`, `x`, `y`), regra de desconto hardcoded sem nome, mistura percentual e valor fixo sem clareza, sem tipos de retorno claros. Roda imprimindo um cálculo.
- [ ] **Step 4: exemplos/preco_revisado.py** — saída aderente ao prompt estruturado: `@dataclass ItemPedido`, constantes nomeadas para faixas de desconto, função `calcular_preco_final` coesa. Roda imprimindo o mesmo cálculo correto. **Nota didática:** ainda revisável — comentar 1 ponto que mesmo a saída boa exigiu ajuste humano.
- [ ] **Step 5: exemplos/preco_gerado.ts e preco_revisado.ts** — equivalentes TS.
- [ ] **Step 6: exercicios/exercicio.py e .ts** — módulo de "cupom de desconto progressivo": prompt fraco + saída que ignora o padrão do projeto, para o participante reescrever o prompt e refatorar. Roda.
- [ ] **Step 7: exercicios/gabarito.py e .ts** — versão aderente refatorada. Roda.
- [ ] **Step 8: exercicios/gabarito_revisao.md** — problemas + prompt estruturado sugerido + um "template de prompt da equipe" reutilizável.
- [ ] **Step 9: exercicios/roteiro-ia.md** — hands-on: participante monta um template de prompt reutilizável e o aplica para gerar a função de cupom, comparando com a saída do prompt fraco.
- [ ] **Step 10: Verificar execução** — os 8 comandos do padrão para os arquivos da Task 2 (`preco_gerado`, `preco_revisado`, `exercicio`, `gabarito`, em `.py` e `.ts`). Expected: rodam sem erro e imprimem as demonstrações.
- [ ] **Step 11: Commit**
```bash
git add sessao-5/tutorial-09-engenharia-de-prompt
git commit -m "feat: adiciona tutorial 09 - engenharia de prompt para codigo limpo

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

## Task 3: Tutorial 10 — Refatoração Assistida: Coesão e Legibilidade

**Slug:** `tutorial-10-refatoracao-assistida` · **Sessão:** 5 · **Tema (arquivos):** `importacao` · **Domínio:** importação de arquivo CSV de clientes.

**Files:**
- Create: `sessao-5/tutorial-10-refatoracao-assistida/README.md`
- Create: `sessao-5/tutorial-10-refatoracao-assistida/exemplos/prompt.md`
- Create: `sessao-5/tutorial-10-refatoracao-assistida/exemplos/importacao_gerado.py`
- Create: `sessao-5/tutorial-10-refatoracao-assistida/exemplos/importacao_revisado.py`
- Create: `sessao-5/tutorial-10-refatoracao-assistida/exemplos/importacao_gerado.ts`
- Create: `sessao-5/tutorial-10-refatoracao-assistida/exemplos/importacao_revisado.ts`
- Create: `sessao-5/tutorial-10-refatoracao-assistida/exercicios/roteiro-ia.md`
- Create: `sessao-5/tutorial-10-refatoracao-assistida/exercicios/exercicio.py`
- Create: `sessao-5/tutorial-10-refatoracao-assistida/exercicios/exercicio.ts`
- Create: `sessao-5/tutorial-10-refatoracao-assistida/exercicios/gabarito.py`
- Create: `sessao-5/tutorial-10-refatoracao-assistida/exercicios/gabarito.ts`
- Create: `sessao-5/tutorial-10-refatoracao-assistida/exercicios/gabarito_revisao.md`

Seguir o **padrão de tarefa de tutorial "tripla"** com estas especializações:

- [ ] **Step 1: README.md** — Referência: `> Referência: *Clean Code*, Cap. 3 (Funções)`.
  - **Conceito Central:** refatorar com IA em **passos pequenos e verificáveis** (extrair função, renomear, melhorar legibilidade) preservando comportamento; verificar a saída entre cada passo; coesão (função que lê + valida + grava → dividir). Fragmentos antes/depois.
  - **Checklist:** pedi um passo por vez? rodei o arquivo após cada passo? o comportamento foi preservado? cada função tem uma responsabilidade? (5–6 itens).
- [ ] **Step 2: exemplos/prompt.md** — prompt de refatoração dirigido em passos ("1. extraia a leitura; 2. extraia a validação; 3. extraia a conversão") vs prompt aberto ("melhora esse código"). Comentário sobre por que o dirigido é mais seguro.
- [ ] **Step 3: exemplos/importacao_gerado.py** — função `importar(arquivo)` que faz tudo (lê CSV em memória, valida, converte, acumula em lista), monolítica, nomes fracos. Roda imprimindo uma importação. (Sem CSV externo: usar uma string CSV embutida no `__main__`.)
- [ ] **Step 4: exemplos/importacao_revisado.py** — funções coesas (`ler_linhas`, `validar_cliente`, `converter_cliente`, `importar_clientes`). Roda imprimindo a mesma importação.
- [ ] **Step 5: exemplos/importacao_gerado.ts e importacao_revisado.ts** — equivalentes TS (string CSV embutida; sem leitura de arquivo real).
- [ ] **Step 6: exercicios/exercicio.py e .ts** — função de IA que importa um catálogo de produtos fazendo tudo junto, para refatorar em passos. Roda.
- [ ] **Step 7: exercicios/gabarito.py e .ts** — versão refatorada coesa. Roda.
- [ ] **Step 8: exercicios/gabarito_revisao.md** — problemas de coesão + a sequência de passos de refatoração sugerida.
- [ ] **Step 9: exercicios/roteiro-ia.md** — hands-on: participante pede à IA a refatoração passo a passo e roda o arquivo após cada passo para confirmar que o comportamento foi preservado.
- [ ] **Step 10: Verificar execução** — os 8 comandos do padrão para os arquivos da Task 3. Expected: rodam sem erro.
- [ ] **Step 11: Commit**
```bash
git add sessao-5/tutorial-10-refatoracao-assistida
git commit -m "feat: adiciona tutorial 10 - refatoracao assistida com IA

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

## Task 4: Tutorial 11 — Tratamento de Erros com IA ⭐ (âncora da Sessão 5)

**Slug:** `tutorial-11-tratamento-de-erros` · **Sessão:** 5 · **Tema (arquivos):** `estorno` · **Domínio:** processamento de devoluções/estornos.

**Files:**
- Create: `sessao-5/tutorial-11-tratamento-de-erros/README.md`
- Create: `sessao-5/tutorial-11-tratamento-de-erros/exemplos/prompt.md`
- Create: `sessao-5/tutorial-11-tratamento-de-erros/exemplos/estorno_gerado.py`
- Create: `sessao-5/tutorial-11-tratamento-de-erros/exemplos/estorno_revisado.py`
- Create: `sessao-5/tutorial-11-tratamento-de-erros/exemplos/estorno_gerado.ts`
- Create: `sessao-5/tutorial-11-tratamento-de-erros/exemplos/estorno_revisado.ts`
- Create: `sessao-5/tutorial-11-tratamento-de-erros/exercicios/roteiro-ia.md`
- Create: `sessao-5/tutorial-11-tratamento-de-erros/exercicios/exercicio.py`
- Create: `sessao-5/tutorial-11-tratamento-de-erros/exercicios/exercicio.ts`
- Create: `sessao-5/tutorial-11-tratamento-de-erros/exercicios/gabarito.py`
- Create: `sessao-5/tutorial-11-tratamento-de-erros/exercicios/gabarito.ts`
- Create: `sessao-5/tutorial-11-tratamento-de-erros/exercicios/gabarito_revisao.md`

Seguir o **padrão de tarefa de tutorial "tripla"** com estas especializações:

- [ ] **Step 1: README.md** — Referência: `> Referência: *Clean Code*, Cap. 7 (Error Handling)`.
  - **Contexto e Motivação:** este é o exercício âncora da Sessão 5. A IA frequentemente **engole erros** — é um vício recorrente que passa despercebido porque o caminho feliz funciona.
  - **Conceito Central:** anti-padrões (`except Exception: pass`, `catch {}` vazio, retorno de `None`/`null` mascarando falha); tratamento explícito (exceções específicas, mensagens úteis); "falha visível > falha silenciosa". Fragmentos antes/depois.
  - **Checklist:** há `except`/`catch` largo? algum erro é silenciado? as exceções são específicas? a mensagem ajuda a depurar? falhas externas são propagadas? (5–6 itens).
- [ ] **Step 2: exemplos/prompt.md** — prompt que pede tratamento de erro explícito ("levante exceções específicas; não silencie falhas") vs prompt que não menciona erros. Comentário sobre o efeito.
- [ ] **Step 3: exemplos/estorno_gerado.py** — função `processar_estorno(...)` com `try/except Exception: pass` engolindo erros e retornando `None` em falha; caminho feliz funciona, mas um estorno inválido passa silenciosamente. Cabeçalho avisa "note o tratamento de erro silencioso". Roda imprimindo um estorno OK e um inválido (que hoje some).
- [ ] **Step 4: exemplos/estorno_revisado.py** — exceções específicas (`EstornoInvalidoError`, `ValorEstornoExcedidoError`), erros propagados/coletados explicitamente. Roda imprimindo estorno bem-sucedido e o relatório de falhas tratadas.
- [ ] **Step 5: exemplos/estorno_gerado.ts e estorno_revisado.ts** — `catch {}` vazio na versão gerada; exceções/erros tipados na revisada.
- [ ] **Step 6: exercicios/exercicio.py e .ts** — função de IA que processa cancelamento de assinatura com validação + cálculo + persistência juntas e erro silenciado, para refatorar (coesão + erros explícitos). Roda imprimindo o estado atual.
- [ ] **Step 7: exercicios/gabarito.py e .ts** — versão com erros tratados e funções coesas. Roda.
- [ ] **Step 8: exercicios/gabarito_revisao.md** — cada ponto de erro silenciado + como tornar explícito.
- [ ] **Step 9: exercicios/roteiro-ia.md** — hands-on: participante pede à IA para tornar o tratamento de erro explícito, roda o arquivo provocando uma falha e confirma que agora ela aparece (em vez de sumir).
- [ ] **Step 10: Verificar execução** — os 8 comandos do padrão para os arquivos da Task 4. Os `*_gerado.*` devem rodar imprimindo o caso silenciado sem crashar. Expected: rodam sem erro.
- [ ] **Step 11: Commit**
```bash
git add sessao-5/tutorial-11-tratamento-de-erros
git commit -m "feat: adiciona tutorial 11 - tratamento de erros com IA (ancora da sessao 5)

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

## Task 5: Tutorial 12 — Revisão Crítica de Código Gerado por IA ⭐ (âncora do tema)

**Slug:** `tutorial-12-revisao-critica-ia` · **Sessão:** 6 · **Domínio:** integração com gateway de pagamento.

Estrutura âncora (o código a revisar *é* o exercício, como o tutorial 05):

**Files:**
- Create: `sessao-6/tutorial-12-revisao-critica-ia/README.md`
- Create: `sessao-6/tutorial-12-revisao-critica-ia/prompt_original.md`
- Create: `sessao-6/tutorial-12-revisao-critica-ia/codigo_gerado_por_ia.py`
- Create: `sessao-6/tutorial-12-revisao-critica-ia/codigo_gerado_por_ia.ts`
- Create: `sessao-6/tutorial-12-revisao-critica-ia/checklist_revisao_ia.md`
- Create: `sessao-6/tutorial-12-revisao-critica-ia/exercicios/roteiro-ia.md`
- Create: `sessao-6/tutorial-12-revisao-critica-ia/gabarito_review.md`
- Create: `sessao-6/tutorial-12-revisao-critica-ia/gabarito_review_ts.md`

- [ ] **Step 1: README.md** — Referência: `> Tutorial âncora do tema — acumula as Sessões 1–2 e os tutoriais 08–11 aplicados a código de IA`.
  - **Contexto e Motivação:** âncora do tema (como o 05 na Sessão 2). Código de IA é confiante e plausível — por isso exige revisão crítica.
  - **Conceito Central — modos de falha** (cada um com 1 fragmento curto): (1) API/método alucinado; (2) lógica plausível-mas-errada (off-by-one, condição invertida); (3) segurança (segredo hardcoded, concatenação de SQL/string) — apontar que o tutorial 13 aprofunda; (4) edge cases faltando (valor zero, lista vazia, timeout); (5) over-engineering; (6) confiança enganosa (comentário que mente sobre o código).
  - **Exercício:** revisar `codigo_gerado_por_ia.*` usando `checklist_revisao_ia.md`.
- [ ] **Step 2: prompt_original.md** — o prompt razoável (mas sem restrições de segurança/edge cases) que "gerou" o módulo de gateway de pagamento.
- [ ] **Step 3: codigo_gerado_por_ia.py** — módulo realista (`cobrar`, `estornar`, `consultar_status`) com **6+ problemas plantados, um de cada modo de falha**:
  - chave de API hardcoded;
  - montagem de URL/query por concatenação de string (injeção);
  - condição de aprovação invertida ou off-by-one no parcelamento;
  - chamada a método inexistente de uma lib fictícia simulada (alucinação), **isolada num branch não exercitado pela demo**, com comentário marcando;
  - sem tratamento de valor zero/negativo;
  - comentário que afirma "valida o CPF" mas não valida.
  Cabeçalho: "Código gerado por IA — contém problemas para revisar. Não corrigir aqui." Roda imprimindo uma cobrança (caminho feliz funciona; defeitos nos caminhos não-felizes/segurança).
- [ ] **Step 4: codigo_gerado_por_ia.ts** — equivalente TS com os mesmos 6+ problemas mapeados 1:1.
- [ ] **Step 5: checklist_revisao_ia.md** — checklist reutilizável (independente deste exercício) por categoria: Correção, Segurança, Edge cases, Legibilidade/Coesão, Dependências, "A IA entendeu o pedido?". Itens em forma de pergunta acionável.
- [ ] **Step 6: gabarito_review.md** — lista comentada de **todos** os problemas do `.py`, com `arquivo:linha`, categoria do checklist, por que é problema e como corrigir.
- [ ] **Step 7: gabarito_review_ts.md** — o mesmo para a versão TS.
- [ ] **Step 8: exercicios/roteiro-ia.md** — hands-on que fecha o loop "gerar → revisar": participante (1) pede à própria IA um trecho similar (ex.: integração com gateway de boleto); (2) aplica o `checklist_revisao_ia.md` na saída dele; (3) registra quantos itens violou. Fallback: revisar o `codigo_gerado_por_ia.*` deste tutorial.
- [ ] **Step 9: Verificar execução**
```bash
python3 sessao-6/tutorial-12-revisao-critica-ia/codigo_gerado_por_ia.py
npx ts-node sessao-6/tutorial-12-revisao-critica-ia/codigo_gerado_por_ia.ts
```
Expected: ambos rodam o caminho feliz sem crashar e imprimem a cobrança de exemplo. Conferir manualmente que cada problema do gabarito existe de fato no código (conferência cruzada gabarito ↔ código).
- [ ] **Step 10: Commit**
```bash
git add sessao-6/tutorial-12-revisao-critica-ia
git commit -m "feat: adiciona tutorial 12 - revisao critica de codigo gerado por IA (ancora do tema)

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

## Task 6: Tutorial 13 — Segurança em Código Gerado por IA

**Slug:** `tutorial-13-seguranca-codigo-ia` · **Sessão:** 6 · **Tema (arquivos):** `consulta` · **Domínio:** endpoint de consulta de cliente por parâmetro.

**Files:**
- Create: `sessao-6/tutorial-13-seguranca-codigo-ia/README.md`
- Create: `sessao-6/tutorial-13-seguranca-codigo-ia/exemplos/prompt.md`
- Create: `sessao-6/tutorial-13-seguranca-codigo-ia/exemplos/consulta_gerado.py`
- Create: `sessao-6/tutorial-13-seguranca-codigo-ia/exemplos/consulta_revisado.py`
- Create: `sessao-6/tutorial-13-seguranca-codigo-ia/exemplos/consulta_gerado.ts`
- Create: `sessao-6/tutorial-13-seguranca-codigo-ia/exemplos/consulta_revisado.ts`
- Create: `sessao-6/tutorial-13-seguranca-codigo-ia/exercicios/roteiro-ia.md`
- Create: `sessao-6/tutorial-13-seguranca-codigo-ia/exercicios/exercicio.py`
- Create: `sessao-6/tutorial-13-seguranca-codigo-ia/exercicios/exercicio.ts`
- Create: `sessao-6/tutorial-13-seguranca-codigo-ia/exercicios/gabarito.py`
- Create: `sessao-6/tutorial-13-seguranca-codigo-ia/exercicios/gabarito.ts`
- Create: `sessao-6/tutorial-13-seguranca-codigo-ia/exercicios/gabarito_revisao.md`

Seguir o **padrão de tarefa de tutorial "tripla"** com estas especializações:

- [ ] **Step 1: README.md** — Referência: `> Referência: modos de falha de segurança em código de IA; complementa o tutorial 12`.
  - **Conceito Central:** as brechas que a IA mais produz — **segredos hardcoded**, **injeção** (SQL/comando/string), **falta de validação de entrada externa**, dependências vulneráveis, permissões amplas demais. Como pedir e revisar com segurança em mente. Fragmentos antes/depois para cada categoria principal.
  - **Checklist:** há segredos no código? consultas são parametrizadas? a entrada externa é validada? as permissões são mínimas? as dependências são confiáveis? (5–6 itens).
- [ ] **Step 2: exemplos/prompt.md** — prompt que inclui requisitos de segurança ("não use segredos hardcoded; parametrize consultas; valide a entrada") vs prompt funcional puro. Comentário sobre o efeito.
- [ ] **Step 3: exemplos/consulta_gerado.py** — endpoint simulado `consultar_cliente(parametro)` com: query montada por concatenação de string (injeção simulada — usando um "banco" em dict/lista para rodar sem dependências), credencial hardcoded, sem validação do parâmetro. Cabeçalho avisa. Roda imprimindo uma consulta e demonstrando, em comentário, como uma entrada maliciosa quebraria a concatenação.
- [ ] **Step 4: exemplos/consulta_revisado.py** — segredo lido de "config" (constante/variável separada simulando env), consulta parametrizada (função que recebe valor e filtra com segurança em vez de concatenar), entrada validada. Roda imprimindo a mesma consulta segura.
- [ ] **Step 5: exemplos/consulta_gerado.ts e consulta_revisado.ts** — equivalentes TS.
- [ ] **Step 6: exercicios/exercicio.py e .ts** — função de IA que monta um filtro de busca de pedidos concatenando entrada do usuário + chave hardcoded, para o participante endurecer. Roda.
- [ ] **Step 7: exercicios/gabarito.py e .ts** — versão segura. Roda.
- [ ] **Step 8: exercicios/gabarito_revisao.md** — cada brecha + correção + checklist de segurança aplicado.
- [ ] **Step 9: exercicios/roteiro-ia.md** — hands-on: participante aplica o checklist de segurança na saída da própria IA para um endpoint similar.
- [ ] **Step 10: Verificar execução** — os 8 comandos do padrão para os arquivos da Task 6. Expected: rodam sem erro (a "injeção" é demonstrada via dados em memória, sem crashar).
- [ ] **Step 11: Commit**
```bash
git add sessao-6/tutorial-13-seguranca-codigo-ia
git commit -m "feat: adiciona tutorial 13 - seguranca em codigo gerado por IA

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

## Task 7: Tutorial 14 — Testes como Guard-Rails para Mudanças Assistidas

**Slug:** `tutorial-14-testes-guard-rails` · **Sessão:** 6 · **Tema (arquivos):** `frete` · **Domínio:** cálculo de frete com faixas de peso.

**Convenção de "testes":** sem framework. Os testes são funções `verificar_*()` que comparam o resultado com o esperado e imprimem `OK: <caso>` ou `FALHOU: <caso> (esperado X, obtido Y)`, coerentes com a verificação por stdout do repo. Um arquivo "de testes" roda todas as `verificar_*` no `__main__`.

**Files:**
- Create: `sessao-6/tutorial-14-testes-guard-rails/README.md`
- Create: `sessao-6/tutorial-14-testes-guard-rails/exemplos/prompt.md`
- Create: `sessao-6/tutorial-14-testes-guard-rails/exemplos/frete_gerado.py`
- Create: `sessao-6/tutorial-14-testes-guard-rails/exemplos/frete_revisado.py`
- Create: `sessao-6/tutorial-14-testes-guard-rails/exemplos/frete_gerado.ts`
- Create: `sessao-6/tutorial-14-testes-guard-rails/exemplos/frete_revisado.ts`
- Create: `sessao-6/tutorial-14-testes-guard-rails/exercicios/roteiro-ia.md`
- Create: `sessao-6/tutorial-14-testes-guard-rails/exercicios/exercicio.py`
- Create: `sessao-6/tutorial-14-testes-guard-rails/exercicios/exercicio.ts`
- Create: `sessao-6/tutorial-14-testes-guard-rails/exercicios/gabarito.py`
- Create: `sessao-6/tutorial-14-testes-guard-rails/exercicios/gabarito.ts`
- Create: `sessao-6/tutorial-14-testes-guard-rails/exercicios/gabarito_revisao.md`

Seguir o **padrão de tarefa de tutorial "tripla"** com estas especializações:

- [ ] **Step 1: README.md** — Referência: `> Referência: Feathers (testes de caracterização) + *Clean Code*, Cap. 9 (Testes)`.
  - **Conceito Central:** testes como rede de segurança antes/depois de mudanças assistidas; **testes de caracterização** para código sem testes antes de deixar a IA mexer; **TDD assistido** (IA escreve o teste a partir do comportamento esperado, depois a implementação); o risco de a IA escrever testes que apenas confirmam o bug existente. Mostrar a convenção `verificar_*`.
  - **Checklist:** havia testes antes da mudança? caracterizei o comportamento atual? os testes pegam regressão? a IA testou o comportamento certo (não o bug)? rodei antes e depois? (5–6 itens).
- [ ] **Step 2: exemplos/prompt.md** — prompt que pede "primeiro escreva testes de caracterização do comportamento atual, depois faça a mudança" vs prompt que pede só a mudança. Comentário sobre o risco do segundo.
- [ ] **Step 3: exemplos/frete_gerado.py** — `calcular_frete(peso, distancia)` com faixas de peso; uma mudança assistida (nova faixa) introduz uma **regressão silenciosa** numa faixa antiga, sem testes que peguem. Inclui `verificar_*` insuficientes (só cobrem o caminho feliz). Roda imprimindo cálculos e o resultado das verificações (que passam, mas não cobrem a regressão).
- [ ] **Step 4: exemplos/frete_revisado.py** — mesmo cálculo protegido por testes de caracterização que cobrem todas as faixas + casos de borda (peso zero, limite de faixa); a regressão é detectada (uma `verificar_*` falha) e então corrigida. Roda imprimindo `OK` em todas após a correção.
- [ ] **Step 5: exemplos/frete_gerado.ts e frete_revisado.ts** — equivalentes TS (mesma convenção `verificar*`).
- [ ] **Step 6: exercicios/exercicio.py e .ts** — `calcular_desconto_fidelidade` com faixas e sem testes; participante escreve as caracterizações antes de pedir uma mudança à IA. Roda.
- [ ] **Step 7: exercicios/gabarito.py e .ts** — caracterizações completas + a mudança protegida. Roda imprimindo todas as verificações.
- [ ] **Step 8: exercicios/gabarito_revisao.md** — quais casos caracterizar, por que o caminho feliz não basta, e a regressão que os testes pegam.
- [ ] **Step 9: exercicios/roteiro-ia.md** — hands-on: participante (1) pede à IA testes de caracterização do comportamento atual; (2) roda-os; (3) pede a mudança; (4) re-roda e confirma que nenhum quebrou (ou conserta se quebrou).
- [ ] **Step 10: Verificar execução** — os 8 comandos do padrão para os arquivos da Task 7. Expected: cada arquivo imprime suas verificações; os `gabarito`/`revisado` imprimem todas `OK`.
- [ ] **Step 11: Commit**
```bash
git add sessao-6/tutorial-14-testes-guard-rails
git commit -m "feat: adiciona tutorial 14 - testes como guard-rails para mudancas assistidas

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

## Task 8: Tutorial 15 — Manutenibilidade e Trabalho com Agentes ao Longo do Tempo

**Slug:** `tutorial-15-manutenibilidade-agentes` · **Sessão:** 6 · **Tema (arquivos):** `relatorio` · **Domínio:** relatório de vendas que cresceu com contribuições de IA.

**Files:**
- Create: `sessao-6/tutorial-15-manutenibilidade-agentes/README.md`
- Create: `sessao-6/tutorial-15-manutenibilidade-agentes/exemplos/prompt.md`
- Create: `sessao-6/tutorial-15-manutenibilidade-agentes/exemplos/relatorio_gerado.py`
- Create: `sessao-6/tutorial-15-manutenibilidade-agentes/exemplos/relatorio_revisado.py`
- Create: `sessao-6/tutorial-15-manutenibilidade-agentes/exemplos/relatorio_gerado.ts`
- Create: `sessao-6/tutorial-15-manutenibilidade-agentes/exemplos/relatorio_revisado.ts`
- Create: `sessao-6/tutorial-15-manutenibilidade-agentes/exercicios/roteiro-ia.md`
- Create: `sessao-6/tutorial-15-manutenibilidade-agentes/exercicios/exercicio.py`
- Create: `sessao-6/tutorial-15-manutenibilidade-agentes/exercicios/exercicio.ts`
- Create: `sessao-6/tutorial-15-manutenibilidade-agentes/exercicios/gabarito.py`
- Create: `sessao-6/tutorial-15-manutenibilidade-agentes/exercicios/gabarito.ts`
- Create: `sessao-6/tutorial-15-manutenibilidade-agentes/exercicios/gabarito_revisao.md`

Seguir o **padrão de tarefa de tutorial "tripla"** com estas especializações:

- [ ] **Step 1: README.md** — Referência: `> Referência: *Clean Code*, Cap. 1 e 17; Regra do Escoteiro (Sessão 2)`.
  - **Conceito Central:** evitar a entropia das contribuições de IA — consistência com padrões existentes, **revisar o *diff*** (não só a saída isolada), documentar o *porquê*, evitar inchaço de dependências, Regra do Escoteiro com IA. **Trabalho com agentes:** quando a IA edita múltiplos arquivos de uma vez, revisar o diff e ter guard-rails (testes) passa a ser inegociável.
  - **Checklist:** segue o padrão existente? revisei o diff inteiro? alguma dependência nova é justificada? documentei o porquê? deixei mais limpo do que achei? (5–6 itens).
- [ ] **Step 2: exemplos/prompt.md** — prompt que dá contexto de manutenibilidade ("siga o padrão deste módulo; não adicione dependências; mantenha o estilo de nomes") vs prompt sem contexto. Comentário sobre o efeito no diff.
- [ ] **Step 3: exemplos/relatorio_gerado.py** — módulo de relatório de vendas que "cresceu" com contribuições de IA inconsistentes: duas funções somando quase igual de formas diferentes (duplicação), mistura de estilos de nome, uma dependência desnecessária reimplementável com a stdlib, formatação divergente. Cabeçalho explica o cenário de deriva. Roda imprimindo um relatório. (A "dependência desnecessária" deve ser simulada por uma função local com nome de lib, para o arquivo rodar sem instalar nada.)
- [ ] **Step 4: exemplos/relatorio_revisado.py** — duplicação eliminada (função única de cálculo reutilizada), estilo consistente, dependência removida, formatação unificada. Roda imprimindo o mesmo relatório.
- [ ] **Step 5: exemplos/relatorio_gerado.ts e relatorio_revisado.ts** — equivalentes TS.
- [ ] **Step 6: exercicios/exercicio.py e .ts** — módulo de dashboard com 3–4 sinais de deriva por IA (duplicação, estilo divergente, dependência supérflua) para consolidar. Roda.
- [ ] **Step 7: exercicios/gabarito.py e .ts** — versão consolidada. Roda.
- [ ] **Step 8: exercicios/gabarito_revisao.md** — cada sinal de deriva + como foi consolidado.
- [ ] **Step 9: exercicios/roteiro-ia.md** — hands-on: participante pede uma feature nova *dando o contexto do padrão existente*, revisa o diff procurando deriva (duplicação? dependência? estilo?), e compara com pedir a mesma feature sem contexto.
- [ ] **Step 10: Verificar execução** — os 8 comandos do padrão para os arquivos da Task 8. Expected: rodam sem erro.
- [ ] **Step 11: Commit**
```bash
git add sessao-6/tutorial-15-manutenibilidade-agentes
git commit -m "feat: adiciona tutorial 15 - manutenibilidade e trabalho com agentes

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

## Task 9: Estender o README.md principal

**Files:**
- Modify: `README.md`

- [ ] **Step 1: Atualizar título/descrição do workshop**

A linha de abertura (atualmente "Workshop de 4 horas dividido em duas sessões...") passa a refletir três temas. Substituir por algo como:
```markdown
Workshop baseado em **Clean Code** de Robert C. Martin e **Working Effectively with Legacy Code** de Michael Feathers. Organizado em temas; o terceiro tema (Sessões 5 e 6) cobre clean code e uso consciente de IA.
```
Manter as linhas de Público e Linguagem principal; acrescentar que as Sessões 5–6 cobrem apenas Python e TypeScript.

- [ ] **Step 2: Adicionar nota de reserva e as agendas das Sessões 5 e 6**

Após a tabela de agenda da "Sessão 2", inserir:
```markdown
### Sessões 3 e 4 — *reservadas para tema futuro*

### Sessão 5 — Gerando e Refatorando Código com IA · 2 horas

| # | Tutorial | Teoria | Prática | Total |
|---|---|---|---|---|
| 08 | Clean Code no Contexto Real com IA | 15 min | 15 min | 30 min |
| 09 | Engenharia de Prompt para Código Limpo | 15 min | 15 min | 30 min |
| 10 | Refatoração Assistida: Coesão e Legibilidade | 15 min | 15 min | 30 min |
| 11 | Tratamento de Erros com IA ⭐ | 10 min | 10 min | 20 min |
| — | **Pulmão** | | | **10 min** |
| | **Total** | | | **120 min** |

### Sessão 6 — Revisando e Sustentando Código de IA · 2 horas

| # | Tutorial | Teoria | Prática | Total |
|---|---|---|---|---|
| 12 | Revisão Crítica de Código Gerado por IA ⭐ | 20 min | 20 min | 40 min |
| 13 | Segurança em Código Gerado por IA | 12 min | 13 min | 25 min |
| 14 | Testes como Guard-Rails para Mudanças Assistidas | 15 min | 15 min | 30 min |
| 15 | Manutenibilidade e Trabalho com Agentes | 12 min | 13 min | 25 min |
| | **Total** | | | **120 min** |
```

- [ ] **Step 3: Adicionar as tabelas de conceitos das Sessões 5 e 6**

Após a tabela de conceitos da "Sessão 2", adicionar:
```markdown
## Sessão 5 — Gerando e Refatorando Código com IA (2 horas)

| # | Tutorial | Conceito central | Referência |
|---|---|---|---|
| 08 | [Clean Code no Contexto Real com IA](sessao-5/tutorial-08-clean-code-com-ia/) | Prompt como especificação; revisar a saída da IA com os critérios das Sessões 1–2 | *Clean Code*, Cap. 2–3 |
| 09 | [Engenharia de Prompt para Código Limpo](sessao-5/tutorial-09-engenharia-de-prompt/) | Prompt patterns: contexto, domínio, restrições, exemplos, formato de saída | *Clean Code*, Cap. 2–3 |
| 10 | [Refatoração Assistida: Coesão e Legibilidade](sessao-5/tutorial-10-refatoracao-assistida/) | Refatorar com IA em passos verificáveis; coesão preservando comportamento | *Clean Code*, Cap. 3 |
| 11 | [Tratamento de Erros com IA ⭐](sessao-5/tutorial-11-tratamento-de-erros/) | O vício de engolir exceções; tratamento explícito | *Clean Code*, Cap. 7 |

## Sessão 6 — Revisando e Sustentando Código de IA (2 horas)

| # | Tutorial | Conceito central | Referência |
|---|---|---|---|
| 12 | [Revisão Crítica de Código Gerado por IA ⭐](sessao-6/tutorial-12-revisao-critica-ia/) | Modos de falha de código de IA; checklist de revisão reutilizável | — |
| 13 | [Segurança em Código Gerado por IA](sessao-6/tutorial-13-seguranca-codigo-ia/) | Segredos, injeção, validação de entrada externa | — |
| 14 | [Testes como Guard-Rails](sessao-6/tutorial-14-testes-guard-rails/) | Testes de caracterização e TDD assistido como rede de segurança | Feathers + *Clean Code*, Cap. 9 |
| 15 | [Manutenibilidade e Trabalho com Agentes](sessao-6/tutorial-15-manutenibilidade-agentes/) | Evitar entropia; revisar o diff; dependências; Regra do Escoteiro | *Clean Code*, Cap. 1, 17 |
```

- [ ] **Step 4: Atualizar "Estrutura de cada tutorial"**

Adicionar nota de que os tutoriais das Sessões 5 e 6 cobrem Python + TypeScript e usam a tripla `prompt.md` → `*_gerado.*` → `*_revisado.*` com um `roteiro-ia.md` hands-on em `exercicios/`. Descrever a estrutura distinta do tutorial 12 (código gerado + `checklist_revisao_ia.md` + gabaritos de review), análoga à do tutorial 05.

- [ ] **Step 5: Atualizar "Como rodar os exemplos"**

Acrescentar nota: as Sessões 5 e 6 rodam apenas com Python e TypeScript (sem PHP/TLPP). Mostrar um exemplo de comando para cada (`python3 sessao-5/...` e `npx ts-node sessao-6/...`).

- [ ] **Step 6: Estender o "Inventário completo de arquivos"**

Adicionar seções de inventário para os tutoriais 08–15 (no mesmo formato de tabela das Sessões 1–2), uma subseção por tutorial, descrevendo cada arquivo: para os tutoriais "tripla", as linhas `exemplos/prompt.md`, `*_gerado.*`, `*_revisado.*`, `exercicios/roteiro-ia.md`, `exercicios/exercicio.*`, `exercicios/gabarito.*`, `exercicios/gabarito_revisao.md`; para o 12, as linhas `prompt_original.md`, `codigo_gerado_por_ia.*`, `checklist_revisao_ia.md`, `exercicios/roteiro-ia.md`, `gabarito_review.md`, `gabarito_review_ts.md`.

- [ ] **Step 7: Verificar**

```bash
ls sessao-5/tutorial-08-clean-code-com-ia sessao-5/tutorial-09-engenharia-de-prompt sessao-5/tutorial-10-refatoracao-assistida sessao-5/tutorial-11-tratamento-de-erros
ls sessao-6/tutorial-12-revisao-critica-ia sessao-6/tutorial-13-seguranca-codigo-ia sessao-6/tutorial-14-testes-guard-rails sessao-6/tutorial-15-manutenibilidade-agentes
```
Expected: os oito diretórios listados sem erro (confirma que os links relativos novos apontam para diretórios existentes).

- [ ] **Step 8: Commit**

```bash
git add README.md
git commit -m "docs: adiciona sessoes 5 e 6 a agenda, tutoriais e inventario do README

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

## Task 10: Estender o guia-de-adocao.md

**Files:**
- Modify: `guia-de-adocao.md`

- [ ] **Step 1: Inserir as seções dos tutoriais 08–15**

Inserir **antes** da seção `## Meu Plano de Adoção` (atualmente a última), seguindo o estilo workbook já estabelecido: cada seção tem a linha `> Material de referência:`, 3–4 perguntas com contexto curto antes de cada uma, e o fechamento `**Minha decisão para este tutorial:**`.

`## Tutorial 08 — Clean Code no Contexto Real com IA` (ref: `sessao-5/tutorial-08-clean-code-com-ia/README.md`)
- O que sempre incluir num prompt para código (domínio, restrições, padrão)?
- O que revisar sempre antes de aceitar uma saída de IA?
- Quando *não* usar IA para um trecho?
- Pergunta-âncora: **qual será a política de uso de IA da sua equipe?**

`## Tutorial 09 — Engenharia de Prompt para Código Limpo` (ref: `sessao-5/tutorial-09-engenharia-de-prompt/README.md`)
- Qual será o "template de prompt" padrão da sua equipe?
- Como você dá à IA o contexto dos padrões já existentes no projeto?
- Quando vale a pena iterar o prompt em vez de corrigir a saída na mão?
- Sua decisão para este tutorial.

`## Tutorial 10 — Refatoração Assistida: Coesão e Legibilidade` (ref: `sessao-5/tutorial-10-refatoracao-assistida/README.md`)
- Refatorar em passos pequenos vs de uma vez — qual sua regra ao usar IA?
- Como você vai verificar que o comportamento foi preservado após uma refatoração assistida?
- Qual o tamanho máximo de mudança que você aceita revisar de uma vez?
- Sua decisão para este tutorial.

`## Tutorial 11 — Tratamento de Erros com IA` (ref: `sessao-5/tutorial-11-tratamento-de-erros/README.md`)
- O que você fará ao ver `except Exception`/`catch {}` numa saída de IA?
- Como garantir que falhas externas não sejam silenciadas?
- Que exceções específicas seu domínio precisa ter?
- Sua decisão para este tutorial.

`## Tutorial 12 — Revisão Crítica de Código Gerado por IA` (ref: `sessao-6/tutorial-12-revisao-critica-ia/README.md`)
- Qual será seu checklist mínimo de revisão de código de IA?
- Como confirmar que uma API/método sugerido pela IA realmente existe?
- Como você trata "confiança enganosa" (comentário que não bate com o código)?
- Sua decisão para este tutorial.

`## Tutorial 13 — Segurança em Código Gerado por IA` (ref: `sessao-6/tutorial-13-seguranca-codigo-ia/README.md`)
- Como tratar segredos em código sugerido por IA?
- Como garantir consultas parametrizadas e entrada validada?
- Qual seu critério para aceitar uma dependência nova sugerida pela IA?
- Sua decisão para este tutorial.

`## Tutorial 14 — Testes como Guard-Rails` (ref: `sessao-6/tutorial-14-testes-guard-rails/README.md`)
- Antes de deixar a IA mexer em código sem testes, o que você faz?
- Como evitar que a IA escreva testes que só confirmam o bug?
- Qual seu ritual de "rodar antes e depois" da mudança assistida?
- Sua decisão para este tutorial.

`## Tutorial 15 — Manutenibilidade e Trabalho com Agentes` (ref: `sessao-6/tutorial-15-manutenibilidade-agentes/README.md`)
- Como garantir que a IA siga os padrões já existentes no seu código?
- Vai revisar o diff inteiro ou só a saída? Qual seu compromisso?
- Como evitar inchaço de dependências introduzido por IA?
- Sua decisão para este tutorial.

- [ ] **Step 2: Estender a tabela "Meu Plano de Adoção"**

Adicionar as linhas:
```markdown
| 08 — Clean Code com IA | |
| 09 — Engenharia de Prompt | |
| 10 — Refatoração Assistida | |
| 11 — Tratamento de Erros com IA | |
| 12 — Revisão Crítica de IA | |
| 13 — Segurança com IA | |
| 14 — Testes Guard-Rails | |
| 15 — Manutenibilidade com IA | |
```

- [ ] **Step 3: Verificar**

```bash
ls sessao-5/tutorial-08-clean-code-com-ia/README.md sessao-5/tutorial-09-engenharia-de-prompt/README.md sessao-5/tutorial-10-refatoracao-assistida/README.md sessao-5/tutorial-11-tratamento-de-erros/README.md
ls sessao-6/tutorial-12-revisao-critica-ia/README.md sessao-6/tutorial-13-seguranca-codigo-ia/README.md sessao-6/tutorial-14-testes-guard-rails/README.md sessao-6/tutorial-15-manutenibilidade-agentes/README.md
```
Expected: os oito READMEs listados sem erro.

- [ ] **Step 4: Commit**

```bash
git add guia-de-adocao.md
git commit -m "docs: estende guia de adocao com tutoriais das sessoes 5 e 6 (uso consciente de IA)

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

## Self-Review (preenchido pelo autor do plano)

**Spec coverage:**
- Objetivo / 4h em duas sessões (5 e 6) → Tasks 1–8 distribuídas em `sessao-5/` e `sessao-6/`. ✓
- 8 tutoriais (08–15) → uma Task por tutorial. ✓
- Frentes originais (princípios, refatoração, revisão crítica, manutenibilidade) → Tasks 1, 3, 5, 8. ✓
- Frentes novas (prompt patterns, erros, segurança, testes) → Tasks 2, 4, 6, 7. ✓
- Âncoras (11 na S5, 12 no tema) → Tasks 4 e 5 marcadas ⭐. ✓
- Molde abordagem A (prompt → gerado → revisado) → padrão de tarefa "tripla". ✓
- Trilha hands-on com IA → `roteiro-ia.md` em cada tutorial. ✓
- Python + TS, sem PHP/TLPP → todos os pares de arquivos. ✓
- Reserva das Sessões 3 e 4 → Task 9 Step 2. ✓
- Extensões README + guia → Tasks 9 e 10. ✓
- Convenção de testes sem framework (`verificar_*`) → Task 7 nota explícita. ✓
- Convenções do repo (PT, autocontido, falhos intencionais, stdout) → seção de convenções. ✓

**Placeholder scan:** o plano descreve conteúdo por arquivo (cenário, conceitos, falhas plantadas, verificação) em vez de transcrever cada um dos ~92 arquivos — adaptação necessária para deliverable de material didático. O padrão de tarefa "tripla" é definido uma vez e referenciado pelas Tasks (DRY), com as especializações concretas listadas em cada uma. Não há TODOs/TBDs pendentes.

**Type/consistência de nomes:** slugs de diretório e prefixos de arquivo (`agendamento`, `preco`, `importacao`, `estorno`, `consulta`, `frete`, `relatorio`; `codigo_gerado_por_ia` no 12) consistentes entre as Tasks de criação (1–8) e as Tasks de extensão (9–10) que os referenciam. Numeração das âncoras (11, 12) consistente entre spec, agendas e tabelas de conceito.
