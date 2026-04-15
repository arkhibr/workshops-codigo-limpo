# Workshop: Fundamentos de Qualidade e Padronização de Código

Workshop de 4 horas dividido em duas sessões, baseado em **Clean Code** de Robert C. Martin e **Working Effectively with Legacy Code** de Michael Feathers.

**Público:** Times mistos (Júnior + Pleno + Sênior).
**Linguagem principal:** Python. Cada tutorial inclui equivalentes em **PHP**, **TypeScript** e **ADVPL/TLPP**.

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

---

## Referências

- MARTIN, Robert C. *Clean Code: A Handbook of Agile Software Craftsmanship*. Prentice Hall, 2008.
- FEATHERS, Michael. *Working Effectively with Legacy Code*. Prentice Hall, 2004.
- FOWLER, Martin. *Refactoring: Improving the Design of Existing Code*. Addison-Wesley, 2018.
