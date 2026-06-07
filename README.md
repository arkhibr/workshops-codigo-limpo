# Workshop: Fundamentos de Qualidade e Padronização de Código

Workshop organizado em temas, baseado em **Clean Code** de Robert C. Martin e **Working Effectively with Legacy Code** de Michael Feathers.

- **Tema 1 (Sessões 1–2):** Fundamentos de Clean Code — 4 horas
- **Tema 2 (Sessões 3–4):** Design Patterns e Idiom Patterns Aplicados — 4 horas
- **Tema 3 (Sessões 5–6):** Clean Code e uso consciente de IA — 4 horas

**Público:** Times mistos (Júnior + Pleno + Sênior).
**Linguagem principal:** Python. Sessões 1–2 incluem equivalentes em **PHP**, **TypeScript** e **ADVPL/TLPP**. Sessões 5–6 cobrem apenas **Python** e **TypeScript**.

---

## Agenda

### Sessão 1 — Os Fundamentos da Escrita Limpa · 2 horas

| # | Tutorial | Teoria | Prática | Total |
|---|---|---|---|---|
| 01 | Nomes Significativos | 15 min | 15 min | 30 min |
| 02 | Funções | 15 min | 15 min | 30 min |
| 03 | Comentários | 15 min | 15 min | 30 min |
| 04 | Formatação | 10 min | 10 min | 20 min |
| — | **Pulmão** | | | **10 min** |
| | **Total** | **55 min** | **55 min** | **120 min** |

### Sessão 2 — Trabalhando com Código em Escala · 2 horas

| # | Tutorial | Teoria | Prática | Total |
|---|---|---|---|---|
| 05 | Code Review Simulado ⭐ | 15 min | 15 min | 30 min |
| 06 | Dívida Técnica | 20 min | 20 min | 40 min |
| 07 | Gestão de Código Legado | 20 min | 20 min | 40 min |
| — | **Pulmão** | | | **10 min** |
| | **Total** | **55 min** | **55 min** | **120 min** |

### Sessão 3 — Design Patterns: Princípios e Estrutura · 2 horas

| # | Tutorial | Teoria | Prática | Total |
|---|---|---|---|---|
| 16 | SOLID na Prática | 15 min | 15 min | 30 min |
| 17 | Padrões de Criação | 15 min | 15 min | 30 min |
| 18 | Padrões Estruturais | 15 min | 15 min | 30 min |
| 19 | Anti-patterns Clássicos | 10 min | 10 min | 20 min |
| — | **Pulmão** | | | **10 min** |
| | **Total** | **55 min** | **55 min** | **120 min** |

### Sessão 4 — Design Patterns: Comportamento e Idioms · 2 horas

| # | Tutorial | Teoria | Prática | Total |
|---|---|---|---|---|
| 20 | Strategy e Template Method | 15 min | 15 min | 30 min |
| 21 | Observer e Command ⭐ | 15 min | 15 min | 30 min |
| 22 | Idiom Patterns por Linguagem | 15 min | 15 min | 30 min |
| 23 | Code Review Orientado a Padrões ⭐ | 10 min | 10 min | 20 min |
| — | **Pulmão** | | | **10 min** |
| | **Total** | **55 min** | **55 min** | **120 min** |

### Sessão 5 — Gerando Código com IA: Dirigir e Revisar · 2 horas

| # | Tutorial | Teoria | Prática | Total |
|---|---|---|---|---|
| 08 | O novo fluxo: dirigir e revisar | 15 min | 15 min | 30 min |
| 09 | Engenharia de contexto e prompt para gerar código | 15 min | 15 min | 30 min |
| 10 | Spec-first: do requisito ao código verificável | 15 min | 15 min | 30 min |
| 11 | Geração multi-arquivo com agentes ⭐ | 10 min | 10 min | 20 min |
| — | **Pulmão** | | | **10 min** |
| | **Total** | | | **120 min** |

### Sessão 6 — Revisando e Sustentando Código de IA · 2 horas

| # | Tutorial | Teoria | Prática | Total |
|---|---|---|---|---|
| 12 | Revisão crítica de código gerado por IA ⭐ | 20 min | 20 min | 40 min |
| 13 | Refatoração assistida avançada | 12 min | 13 min | 25 min |
| 14 | Segurança em código gerado (2026) | 15 min | 15 min | 30 min |
| 15 | Testes como guard-rails e manutenibilidade | 12 min | 13 min | 25 min |
| | **Total** | | | **120 min** |

---

## Sessão 1 — Os Fundamentos da Escrita Limpa (2 horas)

| # | Tutorial | Conceito central | Referência |
|---|---|---|---|
| 01 | [Nomes Significativos](sessao-1/tutorial-01-nomes/) | Nomes que revelam intenção, sem desinformação, sem notação húngara | *Clean Code*, Cap. 2 |
| 02 | [Funções](sessao-1/tutorial-02-funcoes/) | SRP, flag boolean, efeitos colaterais ocultos, CQS, lista longa de parâmetros | *Clean Code*, Cap. 3 |
| 03 | [Comentários](sessao-1/tutorial-03-comentarios/) | Comentar o *porquê*, não o *o quê*; código comentado; TODOs rastreáveis | *Clean Code*, Cap. 4 |
| 04 | [Formatação](sessao-1/tutorial-04-formatacao/) | Stepdown Rule, Newspaper Metaphor, formatadores automáticos | *Clean Code*, Cap. 5 |

## Sessão 2 — Trabalhando com Código em Escala (2 horas)

| # | Tutorial | Conceito central | Referência |
|---|---|---|---|
| 05 | [Code Review Simulado ⭐](sessao-2/tutorial-05-code-review/) | Exercício âncora: revisar código real acumulando todos os tópicos anteriores | — |
| 06 | [Dívida Técnica](sessao-2/tutorial-06-divida-tecnica/) | Quadrante de Fowler, Teoria da Janela Quebrada, Regra do Escoteiro, code smells | *Clean Code*, Cap. 17 |
| 07 | [Gestão de Código Legado](sessao-2/tutorial-07-codigo-legado/) | Testes de caracterização, Seam Model, Strangler Fig Pattern | Feathers + *Clean Code*, Cap. 1 |

## Sessão 3 — Princípios e Padrões de Estrutura (2 horas)

| # | Tutorial | Conceito central | Referência |
|---|---|---|---|
| 16 | [SOLID na Prática](sessao-3/tutorial-08-solid/) | SRP, OCP, LSP, ISP, DIP com código real | SOLID papers — Robert C. Martin |
| 17 | [Padrões de Criação](sessao-3/tutorial-09-criacao/) | Factory Method e Builder | *Design Patterns* (GoF), Cap. 3 |
| 18 | [Padrões Estruturais](sessao-3/tutorial-10-estrutural/) | Adapter para código legado + Facade | *Design Patterns* (GoF), Cap. 4 |
| 19 | [Anti-patterns Clássicos](sessao-3/tutorial-11-antipatterns/) | God Object, Magic Strings, Feature Envy, Copy-Paste | *Clean Code*, Cap. 17 |

## Sessão 4 — Padrões Comportamentais e Idioms (2 horas)

| # | Tutorial | Conceito central | Referência |
|---|---|---|---|
| 20 | [Strategy e Template Method](sessao-4/tutorial-12-strategy-template/) | Substituir if/elif por polimorfismo; esqueleto fixo com variação | *Design Patterns* (GoF), Cap. 5 |
| 21 | [Observer e Command ⭐](sessao-4/tutorial-13-observer-command/) | Desacoplamento de eventos; operações reversíveis | *Design Patterns* (GoF), Cap. 5 |
| 22 | [Idiom Patterns por Linguagem](sessao-4/tutorial-14-idioms/) | Python, TypeScript, PHP 8.1+, ADVPL/TLPP | PEP 557, TS Handbook, PHP 8.1 |
| 23 | [Code Review Orientado a Padrões ⭐](sessao-4/tutorial-15-code-review-padroes/) | Âncora: revisão integrando T16–T22; catálogo da equipe | — |

## Sessão 5 — Gerando Código com IA: Dirigir e Revisar (2 horas)

| # | Tutorial | Conceito central | Referência |
|---|---|---|---|
| 08 | [O novo fluxo: dirigir e revisar](sessao-5/tutorial-16-novo-fluxo-ia/) | O dev dirige o modelo e revisa em altitude; CLAUDE.md/AGENTS.md/GEMINI.md como contexto | *Clean Code*, Cap. 1–2 |
| 09 | [Engenharia de contexto e prompt para gerar código](sessao-5/tutorial-17-engenharia-de-prompt/) | Toolkit robusto: contexto, few-shot, assinatura-alvo, restrições, plano-antes-do-código | Engenharia de contexto |
| 10 | [Spec-first: do requisito ao código verificável](sessao-5/tutorial-18-spec-first/) | Requisito → spec → código; testes como contrato no pedido | Spec-first / plan-first |
| 11 | [Geração multi-arquivo com agentes ⭐](sessao-5/tutorial-19-multiarquivo-agentes/) | Dirigir mudança multi-arquivo; revisar o diff em altitude | Diffs multi-arquivo com agentes |

## Sessão 6 — Revisando e Sustentando Código de IA (2 horas)

| # | Tutorial | Conceito central | Referência |
|---|---|---|---|
| 12 | [Revisão crítica de código gerado por IA ⭐](sessao-6/tutorial-20-revisao-critica-ia/) | Modos de falha sutis em código polido de fronteira; checklist de revisão reutilizável | Âncora do tema |
| 13 | [Refatoração assistida avançada](sessao-6/tutorial-21-refatoracao-avancada/) | Migração de API/padrão preservando comportamento; verificação de equivalência | Feathers + *Clean Code*, Cap. 9 |
| 14 | [Segurança em código gerado (2026)](sessao-6/tutorial-22-seguranca-ia/) | Brechas sutis (ORDER BY interpolado, regex bypass) em código que parece seguro | Complementa T12 |
| 15 | [Testes como guard-rails e manutenibilidade](sessao-6/tutorial-23-testes-manutenibilidade/) | Caracterização antes de deixar o agente mudar; testes que confirmam o bug; revisar o diff | Feathers + *Clean Code*, Cap. 9; Regra do Escoteiro |

---

## Estrutura de cada tutorial

```
tutorial-0N-<tema>/
├── README.md                  # teoria completa + fragmentos de código (leia primeiro)
├── exemplos/
│   ├── <tema>_ruins.py        # código problemático — Python
│   ├── <tema>_bons.py         # versão corrigida — Python
│   ├── equivalente.php        # mesmos problemas/soluções em PHP
│   ├── equivalente.ts         # mesmos problemas/soluções em TypeScript
│   └── equivalente.tlpp       # mesmos problemas/soluções em ADVPL/TLPP
└── exercicios/
    ├── exercicio.py           # desafio — Python
    ├── gabarito.py            # solução — Python
    ├── exercicio.php          # desafio — PHP
    ├── gabarito.php           # solução — PHP
    ├── exercicio.ts           # desafio — TypeScript
    ├── gabarito.ts            # solução — TypeScript
    ├── exercicio.tlpp         # desafio — ADVPL/TLPP
    └── gabarito.tlpp          # solução — ADVPL/TLPP
```

O Tutorial 05 tem estrutura diferente (não há `exemplos/` — o código para revisar *é* o exercício):

```
tutorial-05-code-review/
├── README.md
├── codigo_para_revisar.py
├── codigo_para_revisar.php
├── codigo_para_revisar.ts
├── codigo_para_revisar.tlpp
├── gabarito_review.md         # gabarito Python
├── gabarito_review_php.md
├── gabarito_review_ts.md
└── gabarito_review_tlpp.md
```

**Tutoriais das Sessões 5–6** cobrem apenas **Python** e **TypeScript** (sem PHP e ADVPL/TLPP). Os prompts cobrem a tríade de provedores Claude/OpenAI/Gemini (`prompt.md`/`roteiro-ia.md`). Os arquivos `*_gerado.*` são código polido com defeito sutil intencional; os `*_revisado.*` aplicam os critérios das Sessões 1–2.

```
tutorial-0N-<tema>/           # Sessões 5–6 (padrão)
├── README.md
├── exemplos/
│   ├── prompt.md              # prompt usado para gerar o código (tríade Claude/OpenAI/Gemini)
│   ├── <tema>_gerado.py       # saída da IA — Python (código polido com defeito sutil)
│   ├── <tema>_gerado.ts       # saída da IA — TypeScript
│   ├── <tema>_revisado.py     # versão revisada com critérios de Clean Code — Python
│   └── <tema>_revisado.ts     # versão revisada — TypeScript
└── exercicios/
    ├── roteiro-ia.md          # roteiro hands-on com a IA
    ├── exercicio.py           # desafio — Python
    ├── exercicio.ts           # desafio — TypeScript
    ├── gabarito.py            # solução — Python
    ├── gabarito.ts            # solução — TypeScript
    └── gabarito_revisao.md    # notas de revisão do gabarito
```

O Tutorial 19 tem estrutura estendida com subpastas separando gerado e revisado, mais diff comentado:

```
tutorial-19-multiarquivo-agentes/
├── README.md
├── exemplos/
│   ├── prompt.md              # prompt de mudança multi-arquivo
│   ├── diff-comentado.md      # diff anotado com critérios de revisão em altitude
│   ├── gerado/                # saída bruta do agente
│   │   ├── carrinho.py / .ts
│   │   └── precificacao.py / .ts
│   └── revisado/              # versão revisada
│       ├── carrinho.py / .ts
│       └── precificacao.py / .ts
└── exercicios/
    ├── roteiro-ia.md
    ├── exercicio_carrinho.py / .ts
    ├── exercicio_precificacao.py / .ts
    ├── gabarito_carrinho.py / .ts
    ├── gabarito_precificacao.py / .ts
    └── gabarito_revisao.md
```

O Tutorial 20 tem estrutura análoga ao Tutorial 05 (o código gerado por IA *é* o exercício) e é o exercício âncora do tema:

```
tutorial-20-revisao-critica-ia/
├── README.md
├── prompt_original.md         # prompt que originou o código
├── codigo_gerado_por_ia.py    # código a revisar — Python
├── codigo_gerado_por_ia.ts    # código a revisar — TypeScript
├── checklist_revisao_ia.md    # checklist de revisão reutilizável
├── gabarito_review.md         # gabarito Python
├── gabarito_review_ts.md      # gabarito TypeScript
└── exercicios/
    └── roteiro-ia.md          # roteiro hands-on
```

---

## Como rodar os exemplos e exercícios

### Python
```bash
# Requisito: Python 3.8+. Sem dependências externas.
python3 sessao-1/tutorial-01-nomes/exemplos/nomes_ruins.py
python3 sessao-1/tutorial-01-nomes/exemplos/nomes_bons.py
python3 sessao-1/tutorial-01-nomes/exercicios/exercicio.py
python3 sessao-1/tutorial-01-nomes/exercicios/gabarito.py
```

### PHP
```bash
# Requisito: PHP 8.1+
php sessao-1/tutorial-01-nomes/exercicios/exercicio.php
php sessao-1/tutorial-01-nomes/exercicios/gabarito.php
```

### TypeScript
```bash
# Requisito: Node.js 18+ e ts-node
npm install -g ts-node typescript
npx ts-node sessao-1/tutorial-01-nomes/exercicios/exercicio.ts
npx ts-node sessao-1/tutorial-01-nomes/exercicios/gabarito.ts
```

### ADVPL/TLPP
```
Compile no IDE Totvs (SmartClient/TDS) ou copie o conteúdo do .tlpp
para um fonte existente no seu projeto ADVPL.
Ponto de entrada: a User Function ou Procedure indicada no topo de cada arquivo.
```

> **Sessões 5–6:** apenas Python e TypeScript (sem PHP e ADVPL/TLPP).

```bash
# Python — Sessões 5–6
python3 sessao-5/tutorial-16-novo-fluxo-ia/exemplos/catalogo_revisado.py

# TypeScript — Sessões 5–6
npx ts-node sessao-6/tutorial-20-revisao-critica-ia/codigo_gerado_por_ia.ts
```

---

## Inventário completo de arquivos

### Sessão 1 — Tutorial 01: Nomes Significativos

| Arquivo | Descrição |
|---|---|
| `exemplos/nomes_ruins.py` | 6 problemas: intenção obscura, desinformação, distinções sem sentido, nomes impronunciáveis, notação húngara, mistura de idiomas |
| `exemplos/nomes_bons.py` | 6 soluções equivalentes |
| `exemplos/equivalente.php` | Mesmos problemas/soluções em PHP |
| `exemplos/equivalente.ts` | Mesmos problemas/soluções em TypeScript |
| `exemplos/equivalente.tlpp` | Mesmos problemas/soluções em ADVPL/TLPP |
| `exercicios/exercicio.*` | Código de e-commerce com nomes obscuros para refatorar (4 linguagens) |
| `exercicios/gabarito.*` | Versão refatorada com nomes que revelam intenção (4 linguagens) |

### Sessão 1 — Tutorial 02: Funções

| Arquivo | Descrição |
|---|---|
| `exemplos/funcoes_ruins.py` | 5 problemas: SRP, flag boolean, efeito colateral oculto, muitos parâmetros, violação de CQS |
| `exemplos/funcoes_boas.py` | 5 soluções com dataclass e CQS aplicado |
| `exemplos/equivalente.php` | Mesmos problemas/soluções em PHP |
| `exemplos/equivalente.ts` | Mesmos problemas/soluções em TypeScript |
| `exemplos/equivalente.tlpp` | Mesmos problemas/soluções em ADVPL/TLPP |
| `exercicios/exercicio.*` | Sistema de relatórios com funções que violam SRP e CQS (4 linguagens) |
| `exercicios/gabarito.*` | Versão refatorada com funções de responsabilidade única (4 linguagens) |

### Sessão 1 — Tutorial 03: Comentários

| Arquivo | Descrição |
|---|---|
| `exemplos/comentarios_ruins.py` | Comentários redundantes, enganosos, código comentado e TODOs sem contexto |
| `exemplos/comentarios_bons.py` | Comentários que explicam o *porquê*, TODOs rastreáveis, código auto-documentado |
| `exemplos/equivalente.php` | Mesmos problemas/soluções em PHP |
| `exemplos/equivalente.ts` | Mesmos problemas/soluções em TypeScript |
| `exemplos/equivalente.tlpp` | Mesmos problemas/soluções em ADVPL/TLPP |
| `exercicios/exercicio.*` | Módulo de cálculo fiscal com comentários problemáticos (4 linguagens) |
| `exercicios/gabarito.*` | Versão com comentários limpos e código auto-explicativo (4 linguagens) |

### Sessão 1 — Tutorial 04: Formatação

| Arquivo | Descrição |
|---|---|
| `exemplos/formatacao_ruim.py` | Violações de Stepdown Rule, Newspaper Metaphor, espaçamento inconsistente |
| `exemplos/formatacao_boa.py` | Código aplicando as regras de formatação do Clean Code |
| `exemplos/equivalente.php` | Mesmos problemas/soluções em PHP |
| `exemplos/equivalente.ts` | Mesmos problemas/soluções em TypeScript |
| `exemplos/equivalente.tlpp` | Mesmos problemas/soluções em ADVPL/TLPP |
| `exercicios/exercicio.*` | Módulo de gestão de estoque com formatação caótica (4 linguagens) |
| `exercicios/gabarito.*` | Versão formatada com Stepdown Rule e agrupamento lógico (4 linguagens) |

### Sessão 2 — Tutorial 05: Code Review Simulado ⭐

| Arquivo | Descrição |
|---|---|
| `codigo_para_revisar.py` | Módulo de processamento de pedidos com múltiplos problemas acumulados |
| `codigo_para_revisar.php` | Equivalente em PHP |
| `codigo_para_revisar.ts` | Equivalente em TypeScript |
| `codigo_para_revisar.tlpp` | Equivalente em ADVPL/TLPP |
| `gabarito_review.md` | Lista comentada de todos os problemas encontrados — Python |
| `gabarito_review_php.md` | Lista comentada de problemas — PHP |
| `gabarito_review_ts.md` | Lista comentada de problemas — TypeScript |
| `gabarito_review_tlpp.md` | Lista comentada de problemas — ADVPL/TLPP |

### Sessão 2 — Tutorial 06: Dívida Técnica

| Arquivo | Descrição |
|---|---|
| `exemplos/divida_antes.py` | Módulo de autenticação com magic numbers, nomes obscuros, função gigante e duplicação |
| `exemplos/divida_depois.py` | Versão refatorada com constantes nomeadas e funções de responsabilidade única |
| `exemplos/equivalente.php` | Mesmos problemas/soluções em PHP |
| `exemplos/equivalente.ts` | Mesmos problemas/soluções em TypeScript |
| `exemplos/equivalente.tlpp` | Mesmos problemas/soluções em ADVPL/TLPP |
| `exercicios/exercicio.*` | Sistema de precificação com dívidas técnicas identificadas (4 linguagens) |
| `exercicios/gabarito.*` | Versão com dívidas eliminadas e checklist de qualidade (4 linguagens) |

### Sessão 2 — Tutorial 07: Gestão de Código Legado

| Arquivo | Descrição |
|---|---|
| `exemplos/legado_antes.py` | Módulo legado de cálculo de comissões: sem testes, global state, lógica duplicada |
| `exemplos/legado_depois.py` | Versão refatorada via Seam Model e testes de caracterização |
| `exemplos/equivalente.php` | Mesmos problemas/soluções em PHP |
| `exemplos/equivalente.ts` | Mesmos problemas/soluções em TypeScript |
| `exemplos/equivalente.tlpp` | Mesmos problemas/soluções em ADVPL/TLPP |
| `exercicios/exercicio.*` | Módulo de comissões em produção desde 2020 para caracterizar e refatorar (4 linguagens) |
| `exercicios/gabarito.*` | Testes de caracterização + refatoração completa com classes de responsabilidade única (4 linguagens) |

### Sessão 5 — Tutorial 16: O novo fluxo: dirigir e revisar

| Arquivo | Descrição |
|---|---|
| `exemplos/prompt.md` | Prompt que demonstra o dev no papel de dirigente: contexto + instrução + restrições |
| `exemplos/catalogo_gerado.py` | Saída da IA com defeito sutil — Python |
| `exemplos/catalogo_gerado.ts` | Saída da IA — TypeScript |
| `exemplos/catalogo_revisado.py` | Versão revisada em altitude com critérios de Clean Code — Python |
| `exemplos/catalogo_revisado.ts` | Versão revisada — TypeScript |
| `exercicios/roteiro-ia.md` | Roteiro hands-on com a IA |
| `exercicios/exercicio.py` | Desafio — Python |
| `exercicios/exercicio.ts` | Desafio — TypeScript |
| `exercicios/gabarito.py` | Solução — Python |
| `exercicios/gabarito.ts` | Solução — TypeScript |
| `exercicios/gabarito_revisao.md` | Notas de revisão do gabarito |

### Sessão 5 — Tutorial 17: Engenharia de contexto e prompt para gerar código

| Arquivo | Descrição |
|---|---|
| `exemplos/prompt.md` | Prompt com toolkit completo: contexto, few-shot, assinatura-alvo, restrições, plano-antes-do-código |
| `exemplos/preco_gerado.py` | Saída da IA — Python |
| `exemplos/preco_gerado.ts` | Saída da IA — TypeScript |
| `exemplos/preco_revisado.py` | Versão revisada — Python |
| `exemplos/preco_revisado.ts` | Versão revisada — TypeScript |
| `exercicios/roteiro-ia.md` | Roteiro hands-on com a IA |
| `exercicios/exercicio.py` | Desafio — Python |
| `exercicios/exercicio.ts` | Desafio — TypeScript |
| `exercicios/gabarito.py` | Solução — Python |
| `exercicios/gabarito.ts` | Solução — TypeScript |
| `exercicios/gabarito_revisao.md` | Notas de revisão do gabarito |

### Sessão 5 — Tutorial 18: Spec-first: do requisito ao código verificável

| Arquivo | Descrição |
|---|---|
| `exemplos/spec.md` | Spec estruturada: requisitos → contratos → casos de teste como critério de aceitação |
| `exemplos/prompt.md` | Prompt spec-first com testes como parte do pedido |
| `exemplos/reserva_gerado.py` | Saída da IA gerada a partir da spec — Python |
| `exemplos/reserva_gerado.ts` | Saída da IA — TypeScript |
| `exemplos/reserva_revisado.py` | Versão verificada contra a spec — Python |
| `exemplos/reserva_revisado.ts` | Versão revisada — TypeScript |
| `exercicios/roteiro-ia.md` | Roteiro hands-on com a IA |
| `exercicios/exercicio.py` | Desafio — Python |
| `exercicios/exercicio.ts` | Desafio — TypeScript |
| `exercicios/gabarito.py` | Solução — Python |
| `exercicios/gabarito.ts` | Solução — TypeScript |
| `exercicios/gabarito_revisao.md` | Notas de revisão do gabarito |

### Sessão 5 — Tutorial 19: Geração multi-arquivo com agentes ⭐

| Arquivo | Descrição |
|---|---|
| `exemplos/prompt.md` | Prompt de mudança multi-arquivo dirigida ao agente |
| `exemplos/diff-comentado.md` | Diff anotado com critérios de revisão em altitude |
| `exemplos/gerado/carrinho.py` | Saída do agente — módulo carrinho, Python |
| `exemplos/gerado/carrinho.ts` | Saída do agente — módulo carrinho, TypeScript |
| `exemplos/gerado/precificacao.py` | Saída do agente — módulo precificação, Python |
| `exemplos/gerado/precificacao.ts` | Saída do agente — módulo precificação, TypeScript |
| `exemplos/revisado/carrinho.py` | Versão revisada — módulo carrinho, Python |
| `exemplos/revisado/carrinho.ts` | Versão revisada — módulo carrinho, TypeScript |
| `exemplos/revisado/precificacao.py` | Versão revisada — módulo precificação, Python |
| `exemplos/revisado/precificacao.ts` | Versão revisada — módulo precificação, TypeScript |
| `exercicios/roteiro-ia.md` | Roteiro hands-on com a IA |
| `exercicios/exercicio_carrinho.py` | Desafio carrinho — Python |
| `exercicios/exercicio_carrinho.ts` | Desafio carrinho — TypeScript |
| `exercicios/exercicio_precificacao.py` | Desafio precificação — Python |
| `exercicios/exercicio_precificacao.ts` | Desafio precificação — TypeScript |
| `exercicios/gabarito_carrinho.py` | Solução carrinho — Python |
| `exercicios/gabarito_carrinho.ts` | Solução carrinho — TypeScript |
| `exercicios/gabarito_precificacao.py` | Solução precificação — Python |
| `exercicios/gabarito_precificacao.ts` | Solução precificação — TypeScript |
| `exercicios/gabarito_revisao.md` | Notas de revisão do gabarito |

### Sessão 6 — Tutorial 20: Revisão crítica de código gerado por IA ⭐

| Arquivo | Descrição |
|---|---|
| `prompt_original.md` | Prompt que originou o código gerado |
| `codigo_gerado_por_ia.py` | Código polido com modos de falha sutis a revisar — Python |
| `codigo_gerado_por_ia.ts` | Código polido a revisar — TypeScript |
| `checklist_revisao_ia.md` | Checklist de revisão reutilizável para código de fronteira |
| `exercicios/roteiro-ia.md` | Roteiro hands-on de revisão crítica |
| `gabarito_review.md` | Lista comentada de problemas encontrados — Python |
| `gabarito_review_ts.md` | Lista comentada de problemas encontrados — TypeScript |

### Sessão 6 — Tutorial 21: Refatoração assistida avançada

| Arquivo | Descrição |
|---|---|
| `exemplos/prompt.md` | Prompt de migração de API/padrão com instruções de equivalência comportamental |
| `exemplos/comissao_gerado.py` | Código antes da migração assistida — Python |
| `exemplos/comissao_gerado.ts` | Código antes da migração — TypeScript |
| `exemplos/comissao_revisado.py` | Versão migrada com equivalência verificada — Python |
| `exemplos/comissao_revisado.ts` | Versão migrada — TypeScript |
| `exercicios/roteiro-ia.md` | Roteiro hands-on com a IA |
| `exercicios/exercicio.py` | Desafio — Python |
| `exercicios/exercicio.ts` | Desafio — TypeScript |
| `exercicios/gabarito.py` | Solução — Python |
| `exercicios/gabarito.ts` | Solução — TypeScript |
| `exercicios/gabarito_revisao.md` | Notas de revisão do gabarito |

### Sessão 6 — Tutorial 22: Segurança em código gerado (2026)

| Arquivo | Descrição |
|---|---|
| `exemplos/prompt.md` | Prompt de consulta a dados externos — parece seguro, tem brecha sutil |
| `exemplos/busca_gerado.py` | Saída da IA com ORDER BY interpolado e regex bypass — Python |
| `exemplos/busca_gerado.ts` | Saída da IA — TypeScript |
| `exemplos/busca_revisado.py` | Versão com proteções explícitas e validação de entrada — Python |
| `exemplos/busca_revisado.ts` | Versão revisada — TypeScript |
| `exercicios/roteiro-ia.md` | Roteiro hands-on com a IA |
| `exercicios/exercicio.py` | Desafio — Python |
| `exercicios/exercicio.ts` | Desafio — TypeScript |
| `exercicios/gabarito.py` | Solução — Python |
| `exercicios/gabarito.ts` | Solução — TypeScript |
| `exercicios/gabarito_revisao.md` | Notas de revisão do gabarito |

### Sessão 6 — Tutorial 23: Testes como guard-rails e manutenibilidade

| Arquivo | Descrição |
|---|---|
| `exemplos/prompt.md` | Prompt de cálculo de frete com instrução de caracterização antes de modificar |
| `exemplos/frete_gerado.py` | Saída da IA sem testes — Python |
| `exemplos/frete_gerado.ts` | Saída da IA — TypeScript |
| `exemplos/frete_revisado.py` | Versão com testes de caracterização, testes que confirmam o bug e Regra do Escoteiro — Python |
| `exemplos/frete_revisado.ts` | Versão revisada — TypeScript |
| `exercicios/roteiro-ia.md` | Roteiro hands-on com a IA |
| `exercicios/exercicio.py` | Desafio — Python |
| `exercicios/exercicio.ts` | Desafio — TypeScript |
| `exercicios/gabarito.py` | Solução — Python |
| `exercicios/gabarito.ts` | Solução — TypeScript |
| `exercicios/gabarito_revisao.md` | Notas de revisão do gabarito |

---

## Referências

- MARTIN, Robert C. *Clean Code: A Handbook of Agile Software Craftsmanship*. Prentice Hall, 2008.
- FEATHERS, Michael. *Working Effectively with Legacy Code*. Prentice Hall, 2004.
- FOWLER, Martin. *Refactoring: Improving the Design of Existing Code*. Addison-Wesley, 2018.
