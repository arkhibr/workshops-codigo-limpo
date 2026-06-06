# Workshop: Fundamentos de Qualidade e Padronização de Código

Workshop organizado em temas, baseado em **Clean Code** de Robert C. Martin e **Working Effectively with Legacy Code** de Michael Feathers.

- **Tema 1 (Sessões 1–2):** Fundamentos de Clean Code — 4 horas
- **Tema 2 (Sessões 3–4):** *reservado para tema futuro*
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
| 14 | [Testes como Guard-Rails para Mudanças Assistidas](sessao-6/tutorial-14-testes-guard-rails/) | Testes de caracterização e TDD assistido como rede de segurança | Feathers + *Clean Code*, Cap. 9 |
| 15 | [Manutenibilidade e Trabalho com Agentes](sessao-6/tutorial-15-manutenibilidade-agentes/) | Evitar entropia; revisar o diff; dependências; Regra do Escoteiro | *Clean Code*, Cap. 1, 17 |

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

**Tutoriais das Sessões 5–6** cobrem apenas **Python** e **TypeScript** (sem PHP e ADVPL/TLPP) e seguem a tripla `prompt.md` → `*_gerado.*` → `*_revisado.*`:

```
tutorial-0N-<tema>/           # Sessões 5–6
├── README.md
├── exemplos/
│   ├── prompt.md              # prompt usado para gerar o código
│   ├── <tema>_gerado.py       # saída bruta da IA — Python
│   ├── <tema>_gerado.ts       # saída bruta da IA — TypeScript
│   ├── <tema>_revisado.py     # versão revisada conforme critérios de Clean Code — Python
│   └── <tema>_revisado.ts     # versão revisada — TypeScript
└── exercicios/
    ├── roteiro-ia.md          # roteiro hands-on com a IA
    ├── exercicio.py           # desafio — Python
    ├── exercicio.ts           # desafio — TypeScript
    ├── gabarito.py            # solução — Python
    ├── gabarito.ts            # solução — TypeScript
    └── gabarito_revisao.md    # notas de revisão do gabarito
```

O Tutorial 12 tem estrutura análoga ao Tutorial 05 (o código gerado por IA *é* o exercício):

```
tutorial-12-revisao-critica-ia/
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
python3 sessao-5/tutorial-08-clean-code-com-ia/exemplos/agendamento_revisado.py

# TypeScript — Sessões 5–6
npx ts-node sessao-6/tutorial-12-revisao-critica-ia/codigo_gerado_por_ia.ts
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

### Sessão 5 — Tutorial 08: Clean Code no Contexto Real com IA

| Arquivo | Descrição |
|---|---|
| `exemplos/prompt.md` | Prompt usado para gerar o código de agendamento |
| `exemplos/agendamento_gerado.py` | Saída bruta da IA — Python |
| `exemplos/agendamento_gerado.ts` | Saída bruta da IA — TypeScript |
| `exemplos/agendamento_revisado.py` | Versão revisada com critérios de Clean Code — Python |
| `exemplos/agendamento_revisado.ts` | Versão revisada — TypeScript |
| `exercicios/roteiro-ia.md` | Roteiro hands-on com a IA |
| `exercicios/exercicio.py` | Desafio — Python |
| `exercicios/exercicio.ts` | Desafio — TypeScript |
| `exercicios/gabarito.py` | Solução — Python |
| `exercicios/gabarito.ts` | Solução — TypeScript |
| `exercicios/gabarito_revisao.md` | Notas de revisão do gabarito |

### Sessão 5 — Tutorial 09: Engenharia de Prompt para Código Limpo

| Arquivo | Descrição |
|---|---|
| `exemplos/prompt.md` | Prompt com aplicação dos patterns de engenharia de prompt |
| `exemplos/preco_gerado.py` | Saída bruta da IA — Python |
| `exemplos/preco_gerado.ts` | Saída bruta da IA — TypeScript |
| `exemplos/preco_revisado.py` | Versão revisada — Python |
| `exemplos/preco_revisado.ts` | Versão revisada — TypeScript |
| `exercicios/roteiro-ia.md` | Roteiro hands-on com a IA |
| `exercicios/exercicio.py` | Desafio — Python |
| `exercicios/exercicio.ts` | Desafio — TypeScript |
| `exercicios/gabarito.py` | Solução — Python |
| `exercicios/gabarito.ts` | Solução — TypeScript |
| `exercicios/gabarito_revisao.md` | Notas de revisão do gabarito |

### Sessão 5 — Tutorial 10: Refatoração Assistida: Coesão e Legibilidade

| Arquivo | Descrição |
|---|---|
| `exemplos/prompt.md` | Prompt de refatoração passo a passo |
| `exemplos/importacao_gerado.py` | Código antes da refatoração assistida — Python |
| `exemplos/importacao_gerado.ts` | Código antes da refatoração assistida — TypeScript |
| `exemplos/importacao_revisado.py` | Versão refatorada com coesão preservando comportamento — Python |
| `exemplos/importacao_revisado.ts` | Versão refatorada — TypeScript |
| `exercicios/roteiro-ia.md` | Roteiro hands-on com a IA |
| `exercicios/exercicio.py` | Desafio — Python |
| `exercicios/exercicio.ts` | Desafio — TypeScript |
| `exercicios/gabarito.py` | Solução — Python |
| `exercicios/gabarito.ts` | Solução — TypeScript |
| `exercicios/gabarito_revisao.md` | Notas de revisão do gabarito |

### Sessão 5 — Tutorial 11: Tratamento de Erros com IA ⭐

| Arquivo | Descrição |
|---|---|
| `exemplos/prompt.md` | Prompt focado em tratamento explícito de erros |
| `exemplos/estorno_gerado.py` | Saída da IA com tratamento de erros problemático — Python |
| `exemplos/estorno_gerado.ts` | Saída da IA — TypeScript |
| `exemplos/estorno_revisado.py` | Versão com tratamento explícito de exceções — Python |
| `exemplos/estorno_revisado.ts` | Versão revisada — TypeScript |
| `exercicios/roteiro-ia.md` | Roteiro hands-on com a IA |
| `exercicios/exercicio.py` | Desafio — Python |
| `exercicios/exercicio.ts` | Desafio — TypeScript |
| `exercicios/gabarito.py` | Solução — Python |
| `exercicios/gabarito.ts` | Solução — TypeScript |
| `exercicios/gabarito_revisao.md` | Notas de revisão do gabarito |

### Sessão 6 — Tutorial 12: Revisão Crítica de Código Gerado por IA ⭐

| Arquivo | Descrição |
|---|---|
| `prompt_original.md` | Prompt que originou o código gerado |
| `codigo_gerado_por_ia.py` | Código gerado por IA com múltiplos problemas a revisar — Python |
| `codigo_gerado_por_ia.ts` | Código gerado por IA a revisar — TypeScript |
| `checklist_revisao_ia.md` | Checklist de revisão reutilizável para código de IA |
| `exercicios/roteiro-ia.md` | Roteiro hands-on de revisão crítica |
| `gabarito_review.md` | Lista comentada de problemas encontrados — Python |
| `gabarito_review_ts.md` | Lista comentada de problemas encontrados — TypeScript |

### Sessão 6 — Tutorial 13: Segurança em Código Gerado por IA

| Arquivo | Descrição |
|---|---|
| `exemplos/prompt.md` | Prompt de consulta a dados externos sem restrições de segurança |
| `exemplos/consulta_gerado.py` | Saída da IA com vulnerabilidades de segurança — Python |
| `exemplos/consulta_gerado.ts` | Saída da IA — TypeScript |
| `exemplos/consulta_revisado.py` | Versão com validação de entrada, segredos e proteção contra injeção — Python |
| `exemplos/consulta_revisado.ts` | Versão revisada — TypeScript |
| `exercicios/roteiro-ia.md` | Roteiro hands-on com a IA |
| `exercicios/exercicio.py` | Desafio — Python |
| `exercicios/exercicio.ts` | Desafio — TypeScript |
| `exercicios/gabarito.py` | Solução — Python |
| `exercicios/gabarito.ts` | Solução — TypeScript |
| `exercicios/gabarito_revisao.md` | Notas de revisão do gabarito |

### Sessão 6 — Tutorial 14: Testes como Guard-Rails para Mudanças Assistidas

| Arquivo | Descrição |
|---|---|
| `exemplos/prompt.md` | Prompt para geração de código de cálculo de frete |
| `exemplos/frete_gerado.py` | Saída da IA sem cobertura de testes — Python |
| `exemplos/frete_gerado.ts` | Saída da IA — TypeScript |
| `exemplos/frete_revisado.py` | Versão com testes de caracterização e TDD assistido — Python |
| `exemplos/frete_revisado.ts` | Versão revisada — TypeScript |
| `exercicios/roteiro-ia.md` | Roteiro hands-on com a IA |
| `exercicios/exercicio.py` | Desafio — Python |
| `exercicios/exercicio.ts` | Desafio — TypeScript |
| `exercicios/gabarito.py` | Solução — Python |
| `exercicios/gabarito.ts` | Solução — TypeScript |
| `exercicios/gabarito_revisao.md` | Notas de revisão do gabarito |

### Sessão 6 — Tutorial 15: Manutenibilidade e Trabalho com Agentes

| Arquivo | Descrição |
|---|---|
| `exemplos/prompt.md` | Prompt de geração de relatório com múltiplos ciclos de agente |
| `exemplos/relatorio_gerado.py` | Saída da IA com problemas de manutenibilidade — Python |
| `exemplos/relatorio_gerado.ts` | Saída da IA — TypeScript |
| `exemplos/relatorio_revisado.py` | Versão com entropia controlada e Regra do Escoteiro aplicada — Python |
| `exemplos/relatorio_revisado.ts` | Versão revisada — TypeScript |
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
