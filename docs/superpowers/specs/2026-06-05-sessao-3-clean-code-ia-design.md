# Spec — Sessão 3: Clean Code e Uso Consciente de IA

**Data:** 2026-06-05
**Status:** Aprovado para implementação

---

## 1. Objetivo

Criar a **Sessão 3** do workshop de Clean Code, com o tema **"Clean Code e Uso Consciente de IA"**. A sessão eleva a qualidade do código produzido, incluindo o código gerado ou assistido por IA, no formato de **sessões de refatoração assistida**.

**Resultados esperados:**
- Guia de clean code adaptado à equipe (extensão do `guia-de-adocao.md`).
- Maior confiança da equipe em revisar e evoluir código produzido com IA.

**Frentes do tema (uma por tutorial):**
1. Princípios de clean code aplicados ao contexto real com IA.
2. Funções coesas, legibilidade e tratamento de erros (refatoração assistida).
3. Revisão crítica de código gerado por IA.
4. Boas práticas para manter manutenibilidade ao longo do tempo.

---

## 2. Decisões de design

| Decisão | Escolha |
|---|---|
| Formato | Molde adaptado para IA — mantém README de teoria + prática, mas o conteúdo prático gira em torno de prompts, código gerado e revisão crítica. |
| Nº de tutoriais | 4 (tutoriais 08–11), sessão de ~2h espelhando sessões 1 e 2. |
| Linguagens | Python (base) + TypeScript. Sem PHP/TLPP nesta sessão. |
| Tratamento da IA | Foco em assistentes de código modernos (chat + edição inline + agentes), com prompts reais, **sem amarrar a um produto específico**. |
| Representação do fluxo de IA | Abordagem A — tripla visível: **prompt → saída da IA (com falhas) → versão revisada/refatorada**. Tudo autocontido. |
| Trilha hands-on | Cada tutorial inclui um `roteiro-ia.md` em que o participante usa o **próprio assistente de IA** para reproduzir a prática ensinada. O `exercicio`/`gabarito` estáticos permanecem como referência e fallback. |
| Extensões | Sempre estender, nunca substituir: atualizar `README.md` principal e `guia-de-adocao.md`. |

---

## 3. Estrutura de diretórios

Nova pasta `sessao-3/` com quatro tutoriais.

### Agenda (espelha o ritmo de ~2h das sessões 1 e 2)

| # | Tutorial | Teoria | Prática | Total |
|---|---|---|---|---|
| 08 | Clean Code no Contexto Real com IA | 15 | 15 | 30 min |
| 09 | Refatoração Assistida: Funções Coesas, Legibilidade e Erros | 15 | 15 | 30 min |
| 10 | Revisão Crítica de Código Gerado por IA ⭐ (âncora) | 15 | 15 | 30 min |
| 11 | Manutenibilidade ao Longo do Tempo com IA | 10 | 10 | 20 min |
| — | Pulmão | | | 10 min |
| | **Total** | | | **120 min** |

O **tutorial 10 é a âncora** da sessão (como o tutorial 05 foi na sessão 2): revisar criticamente um módulo realista gerado por IA, acumulando os conceitos das sessões anteriores.

### Layout dos tutoriais 08, 09 e 11 (molde adaptado, abordagem A)

```
tutorial-08-clean-code-com-ia/
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

### Layout do tutorial 10 (âncora — o código a revisar *é* o exercício, como o 05)

```
tutorial-10-revisao-critica-ia/
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

### Tutorial 08 — Clean Code no Contexto Real com IA
- **Conceito:** os princípios das sessões 1–2 continuam valendo para a saída da IA; o desenvolvedor é o sênior que revisa um júnior veloz; engenharia de contexto no prompt (restrições, linguagem de domínio, exemplos, expectativas explícitas de clean code); "prompt vago → código genérico e frágil".
- **Exemplo (`prompt.md` + `_gerado` + `_revisado`):** prompt fraco produz código genérico com nomes ruins e sem coesão; prompt forte produz código melhor — mas que ainda exige revisão.
- **Exercício estático:** melhorar um prompt fraco e refatorar a saída resultante.
- **Roteiro hands-on:** o participante escreve um prompt forte no próprio assistente e compara a saída com os critérios das sessões 1–2.

### Tutorial 09 — Refatoração Assistida: Funções Coesas, Legibilidade e Erros
- **Conceito:** usar IA para extrair funções, melhorar legibilidade e robustecer tratamento de erros — em passos pequenos e verificáveis; vício comum da IA de engolir exceções (`except` largo, falha silenciosa, retorno de `None` mascarando erro); verificar que o comportamento foi preservado.
- **Exemplo:** função gerada pela IA fazendo coisas demais e com erro mal tratado → versão coesa e com erros tratados de forma explícita.
- **Exercício estático:** pegar uma saída de IA e refatorar para coesão + tratamento de erros.
- **Roteiro hands-on:** pedir à IA uma refatoração passo a passo e validar cada passo.

### Tutorial 10 — Revisão Crítica de Código Gerado por IA ⭐ (âncora)
- **Conceito:** modos de falha de código de IA — APIs/métodos alucinados, lógica plausível-mas-errada, brechas de segurança (injeção, segredos hardcoded), edge cases faltando, padrões desatualizados, over-engineering, confiança enganosa.
- **Entregável-chave:** `checklist_revisao_ia.md` — checklist reutilizável para revisar código de IA.
- **Estrutura âncora:** `codigo_gerado_por_ia.{py,ts}` é um módulo realista com problemas sutis; `gabarito_review.md` / `gabarito_review_ts.md` listam os problemas comentados.
- **Roteiro hands-on:** o participante gera um trecho com a própria IA e aplica o checklist na saída dela, fechando o loop "gerar → revisar criticamente".

### Tutorial 11 — Manutenibilidade ao Longo do Tempo com IA
- **Conceito:** evitar a entropia das contribuições de IA — consistência com padrões existentes, testes como guard-rails antes/depois de mudanças, revisar o *diff* (não só a saída), documentar o *porquê* das decisões, evitar inchaço de dependências, Regra do Escoteiro com IA.
- **Exemplo:** módulo derivando por contribuições inconsistentes de IA → integração disciplinada.
- **Exercício estático + roteiro hands-on** no mesmo padrão dos demais.

---

## 5. Extensões (sempre estender, nunca substituir)

### `README.md` principal
- Adicionar a Sessão 3 na tabela de **Agenda**.
- Adicionar a seção **Sessão 3** na lista de tutoriais com conceito central e referência.
- Adicionar a Sessão 3 ao **Inventário completo de arquivos**.
- Notar na seção "Como rodar" que a Sessão 3 cobre apenas Python e TypeScript.

### `guia-de-adocao.md`
- Acrescentar 4 seções novas (Tutorial 08–11) com perguntas de aplicação no estilo workbook já estabelecido (curtas, com contexto antes de cada pergunta, terminando em "Minha decisão para este tutorial").
- Incluir uma pergunta-âncora sobre a **política de uso de IA da equipe** (quando usar, o que sempre revisar antes de aceitar).
- Adicionar as linhas dos tutoriais 08–11 à tabela final "Meu Plano de Adoção".

---

## 6. Convenções a respeitar

- **Linguagem de domínio em português** nos identificadores (padrão intencional do repo).
- **Arquivos `*_gerado.*` e `codigo_gerado_por_ia.*` são intencionalmente falhos** — demonstram saída típica de IA. Não "corrigir".
- **Autocontido:** nenhum arquivo importa de outro arquivo do repositório; verificação via `print`/stdout.
- Rodar com `python3 <arquivo>` e `npx ts-node <arquivo>`.
- Commits no padrão `<type>: <mensagem>` (`feat`, `docs`, etc.).

---

## 7. Fora de escopo

- PHP e ADVPL/TLPP nesta sessão.
- Roteiros que exijam ferramenta de IA específica ou execução de IA ao vivo como pré-requisito (a trilha hands-on é recomendada, mas o conteúdo estático garante autossuficiência).
- Integração com CI ou automação de testes além do que os exemplos demonstram via stdout.
