# Spec — Sessões 5 e 6: Clean Code e Uso Consciente de IA

**Data:** 2026-06-05
**Status:** Aprovado para implementação

---

## 1. Objetivo

Criar o **Tema 3** do workshop de Clean Code — **"Clean Code e Uso Consciente de IA"** — com **4 horas** de duração, divididas em **duas sessões de 2 horas** (**Sessão 5** e **Sessão 6**). O tema eleva a qualidade do código produzido com auxílio de IA, no formato de **sessões de geração, refatoração, revisão e sustentação de código assistido**.

**Resultados esperados:**
- Guia de clean code adaptado à equipe para uso de IA (extensão do `guia-de-adocao.md`).
- Maior confiança da equipe em gerar, revisar e evoluir código produzido com IA.
- Uma **política de uso de IA** própria da equipe, construída ao longo dos tutoriais.

**Numeração:** as Sessões 3 e 4 ficam **reservadas para um tema intermediário futuro**. Este tema ocupa, desde já, as Sessões 5 e 6 — mantendo a numeração contínua de tutoriais (08–15) após o tutorial 07 da Sessão 2.

---

## 2. Decisões de design

| Decisão | Escolha |
|---|---|
| Duração | 4 horas — duas sessões de ~2h (Sessão 5 e Sessão 6). |
| Numeração das sessões | 5 e 6 (3 e 4 reservadas para tema intermediário futuro). |
| Nº de tutoriais | 8 (tutoriais 08–15), 4 por sessão, espelhando o ritmo das Sessões 1 e 2. |
| Linguagens | Python (base) + TypeScript. Sem PHP/TLPP neste tema. |
| Tratamento da IA | Foco em assistentes de código modernos (chat + edição inline + agentes), com prompts reais, **sem amarrar a um produto específico**. |
| Representação do fluxo de IA | Abordagem A — tripla visível: **prompt → saída da IA (com falhas) → versão revisada/refatorada**. Tudo autocontido. |
| Trilha hands-on | Cada tutorial inclui um `roteiro-ia.md` em que o participante usa o **próprio assistente de IA** para reproduzir a prática. O `exercicio`/`gabarito` estáticos permanecem como referência e fallback. |
| Âncoras | Cada sessão tem um tutorial âncora ⭐: **11 (Tratamento de Erros)** na Sessão 5 e **12 (Revisão Crítica)** na Sessão 6 — sendo o 12 a âncora do tema inteiro. |
| Extensões | Sempre estender, nunca substituir: atualizar `README.md` principal e `guia-de-adocao.md`. |

---

## 3. Estrutura de diretórios

Duas pastas novas: `sessao-5/` e `sessao-6/`, com quatro tutoriais cada.

### Agenda — Sessão 5: Gerando e Refatorando Código com IA (~2h)

| # | Tutorial | Teoria | Prática | Total |
|---|---|---|---|---|
| 08 | Clean Code no Contexto Real com IA | 15 | 15 | 30 min |
| 09 | Engenharia de Prompt para Código Limpo | 15 | 15 | 30 min |
| 10 | Refatoração Assistida: Coesão e Legibilidade | 15 | 15 | 30 min |
| 11 | Tratamento de Erros com IA ⭐ (âncora da sessão) | 10 | 10 | 20 min |
| — | Pulmão | | | 10 min |
| | **Total** | | | **120 min** |

### Agenda — Sessão 6: Revisando e Sustentando Código de IA (~2h)

| # | Tutorial | Teoria | Prática | Total |
|---|---|---|---|---|
| 12 | Revisão Crítica de Código Gerado por IA ⭐ (âncora do tema) | 20 | 20 | 40 min |
| 13 | Segurança em Código Gerado por IA | 12 | 13 | 25 min |
| 14 | Testes como Guard-Rails para Mudanças Assistidas | 15 | 15 | 30 min |
| 15 | Manutenibilidade e Trabalho com Agentes | 12 | 13 | 25 min |
| — | Pulmão | | | — |
| | **Total** | | | **120 min** |

O **tutorial 12 é a âncora do tema** (como o tutorial 05 foi na Sessão 2): revisar criticamente um módulo realista gerado por IA, acumulando os conceitos de todos os tutoriais anteriores. O **tutorial 11** é a âncora prática da Sessão 5: refatorar uma saída de IA que mascara erros.

### Layout dos tutoriais de geração/refatoração (08, 09, 10, 11, 13, 14, 15 — molde adaptado, abordagem A)

```
tutorial-NN-<tema>/
├── README.md                       # teoria
├── exemplos/
│   ├── prompt.md                   # prompt fraco vs prompt forte (lado a lado)
│   ├── <tema>_gerado.py            # saída típica da IA — plausível mas com falhas
│   ├── <tema>_revisado.py          # versão revisada/refatorada por humano
│   ├── <tema>_gerado.ts
│   └── <tema>_revisado.ts
└── exercicios/
    ├── roteiro-ia.md               # hands-on: reproduza a prática usando seu assistente de IA
    ├── exercicio.py / .ts          # versão estática — prompt + saída da IA para criticar e refatorar
    ├── gabarito.py / .ts           # solução refatorada de referência
    └── gabarito_revisao.md         # a crítica escrita (problemas encontrados)
```

### Layout do tutorial 12 (âncora — o código a revisar *é* o exercício, como o 05)

```
tutorial-12-revisao-critica-ia/
├── README.md
├── prompt_original.md              # o prompt que gerou o código
├── codigo_gerado_por_ia.py         # módulo realista com problemas sutis
├── codigo_gerado_por_ia.ts
├── checklist_revisao_ia.md         # checklist reutilizável para revisar código de IA
├── exercicios/
│   └── roteiro-ia.md               # hands-on: gere um trecho com sua IA e aplique o checklist na saída
├── gabarito_review.md              # lista comentada dos problemas (Python)
└── gabarito_review_ts.md
```

### Padrão das seções de cada `README.md`

Espelha os tutoriais existentes:
1. **Contexto e Motivação**
2. **Conceito Central** (com fragmentos de código intercalados)
3. **Exercício** (referência aos arquivos de `exercicios/`, incluindo a trilha hands-on)
4. **Checklist / Resumo**
5. **Referências**

Cada README inicia com uma linha `> Referência:` apontando para o capítulo de Clean Code aplicável e/ou material complementar sobre IA.

---

## 4. Conteúdo por tutorial

### Sessão 5 — Gerando e Refatorando Código com IA

#### Tutorial 08 — Clean Code no Contexto Real com IA
- **Conceito:** os princípios das Sessões 1–2 continuam valendo para a saída da IA; o desenvolvedor é o sênior que revisa um júnior veloz; por que "prompt vago → código genérico e frágil"; o prompt não substitui a revisão.
- **Domínio do cenário:** agendamento de consultas em clínica.
- **Tripla:** prompt fraco → código genérico (nomes ruins, sem coesão) → versão revisada.
- **Hands-on:** o participante escreve um prompt forte no próprio assistente e compara a saída com os critérios das Sessões 1–2.

#### Tutorial 09 — Engenharia de Prompt para Código Limpo
- **Conceito:** prompt como especificação. Prompt patterns: dar **contexto** (arquitetura, padrões existentes), **linguagem de domínio**, **restrições explícitas** (sem novas dependências, responsabilidade única), **exemplos do padrão desejado** (few-shot), **formato de saída esperado**. Iterar o prompt em vez de aceitar a primeira resposta.
- **Domínio do cenário:** cálculo de preço com regras de desconto.
- **Tripla:** prompt sem contexto → código que ignora as convenções do projeto → mesmo pedido com prompt estruturado → saída aderente (ainda revisável).
- **Hands-on:** o participante monta um "template de prompt" reutilizável da equipe e o aplica.

#### Tutorial 10 — Refatoração Assistida: Coesão e Legibilidade
- **Conceito:** usar IA para extrair funções, renomear e melhorar legibilidade — em passos pequenos e verificáveis, preservando comportamento. Verificar a saída entre cada passo.
- **Domínio do cenário:** importação de arquivo CSV de clientes.
- **Tripla:** função gerada pela IA fazendo coisas demais → refatoração coesa em passos.
- **Hands-on:** pedir à IA uma refatoração passo a passo e validar cada passo rodando o arquivo.

#### Tutorial 11 — Tratamento de Erros com IA ⭐ (âncora da Sessão 5)
- **Conceito:** o vício comum da IA de **engolir exceções** (`except Exception: pass`, `catch {}` vazio, retorno de `None`/`null` mascarando falha). Tratamento explícito: exceções específicas, mensagens úteis, não silenciar falhas. Falha visível é melhor que falha silenciosa.
- **Domínio do cenário:** processamento de devoluções/estornos.
- **Tripla:** saída de IA que silencia erros → versão com erros tratados explicitamente.
- **Hands-on:** participante pede à IA para tornar o tratamento de erro explícito e verifica que o comportamento foi preservado.

### Sessão 6 — Revisando e Sustentando Código de IA

#### Tutorial 12 — Revisão Crítica de Código Gerado por IA ⭐ (âncora do tema)
- **Conceito — modos de falha de código de IA** (cada um com 1 fragmento curto):
  1. API/método alucinado (chamada a função que não existe na lib).
  2. Lógica plausível-mas-errada (off-by-one, condição invertida).
  3. Segurança (introduzida aqui, aprofundada no 13): segredo hardcoded, concatenação de SQL/strings.
  4. Edge cases faltando (valor zero, lista vazia, timeout).
  5. Over-engineering (abstração desnecessária).
  6. Confiança enganosa (comentário afirma algo que o código não faz).
- **Domínio do cenário:** integração com gateway de pagamento.
- **Entregável-chave:** `checklist_revisao_ia.md` — checklist reutilizável para revisar código de IA.
- **Estrutura âncora:** `codigo_gerado_por_ia.{py,ts}` é um módulo realista com 6+ problemas plantados; `gabarito_review.md` / `gabarito_review_ts.md` listam os problemas comentados.
- **Hands-on:** o participante gera um trecho com a própria IA e aplica o checklist na saída dela, fechando o loop "gerar → revisar criticamente".

#### Tutorial 13 — Segurança em Código Gerado por IA
- **Conceito:** os modos de falha de segurança que a IA produz com mais frequência — **segredos hardcoded**, **injeção** (SQL/comando/string), **falta de validação de entrada externa**, dependências com vulnerabilidades, permissões amplas demais. Como pedir e revisar com segurança em mente.
- **Domínio do cenário:** endpoint de consulta de cliente por parâmetro.
- **Tripla:** saída de IA com brechas → versão com segredos em config, query parametrizada e entrada validada.
- **Hands-on:** participante aplica um "checklist de segurança" na saída da própria IA.

#### Tutorial 14 — Testes como Guard-Rails para Mudanças Assistidas
- **Conceito:** testes como rede de segurança antes/depois de mudanças assistidas por IA; testes de caracterização para código sem testes antes de deixar a IA mexer; TDD assistido (a IA escreve o teste a partir do comportamento esperado, depois a implementação); o risco de a IA escrever testes que apenas confirmam o bug.
- **Domínio do cenário:** cálculo de frete com faixas de peso.
- **Tripla:** mudança assistida sem testes (regressão silenciosa) → mesma mudança protegida por testes de caracterização + casos novos.
- **Hands-on:** participante pede à IA testes de caracterização, roda-os, então pede a mudança e re-roda.
- **Nota:** verificação por execução via stdout (sem framework de testes) — os "testes" são funções `verificar_*` que imprimem `OK`/`FALHOU`, coerentes com a convenção do repo.

#### Tutorial 15 — Manutenibilidade e Trabalho com Agentes ao Longo do Tempo
- **Conceito:** evitar a entropia das contribuições de IA — consistência com padrões existentes, **revisar o *diff*** (não só a saída isolada), documentar o *porquê*, evitar inchaço de dependências, Regra do Escoteiro com IA. **Trabalho com agentes:** quando a IA edita múltiplos arquivos de uma vez, a revisão do diff e os guard-rails (testes) passam a ser inegociáveis.
- **Domínio do cenário:** relatório de vendas que cresceu com contribuições de IA inconsistentes.
- **Tripla:** módulo derivando por contribuições inconsistentes → integração disciplinada e consolidada.
- **Hands-on:** participante pede uma feature *dando o contexto do padrão existente*, depois revisa o diff procurando deriva; compara com pedir sem contexto.

---

## 5. Extensões (sempre estender, nunca substituir)

### `README.md` principal
- Atualizar o subtítulo/descrição do workshop (deixa de ser "4 horas / duas sessões"): agora abrange três temas e até a Sessão 6.
- Adicionar as Sessões 5 e 6 na seção **Agenda** (duas tabelas novas).
- Adicionar as seções **Sessão 5** e **Sessão 6** na lista de tutoriais com conceito central e referência.
- Adicionar as Sessões 5 e 6 ao **Inventário completo de arquivos**.
- Notar na seção "Como rodar" que as Sessões 5 e 6 cobrem apenas Python e TypeScript.
- Notar que as Sessões 3 e 4 estão reservadas para tema futuro (placeholder curto na agenda).

### `guia-de-adocao.md`
- Acrescentar 8 seções novas (Tutoriais 08–15) com perguntas de aplicação no estilo workbook já estabelecido (curtas, com contexto antes de cada pergunta, terminando em "Minha decisão para este tutorial").
- Incluir uma pergunta-âncora sobre a **política de uso de IA da equipe** (quando usar, o que sempre revisar antes de aceitar).
- Adicionar as linhas dos tutoriais 08–15 à tabela final "Meu Plano de Adoção".

---

## 6. Convenções a respeitar

- **Linguagem de domínio em português** nos identificadores (padrão intencional do repo).
- **Arquivos `*_gerado.*` e `codigo_gerado_por_ia.*` são intencionalmente falhos** — demonstram saída típica de IA. Não "corrigir".
- **Autocontido:** nenhum arquivo importa de outro arquivo do repositório; verificação via `print`/stdout.
- Rodar com `python3 <arquivo>` e `npx ts-node <arquivo>`.
- Commits no padrão `<type>: <mensagem>` (`feat`, `docs`, etc.).

---

## 7. Fora de escopo

- PHP e ADVPL/TLPP neste tema.
- Roteiros que exijam ferramenta de IA específica ou execução de IA ao vivo como pré-requisito (a trilha hands-on é recomendada, mas o conteúdo estático garante autossuficiência).
- Integração com CI ou frameworks de teste além do que os exemplos demonstram via stdout.
- Conteúdo das Sessões 3 e 4 (tema intermediário futuro) — apenas reservar a numeração.
